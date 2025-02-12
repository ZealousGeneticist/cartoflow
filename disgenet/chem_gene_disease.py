### Pull chemical gene interactions from the CTD and print them into a tsv file
### Necessary libraries
import subprocess, sys, os
import requests
import pandas as pd
import requests, json, time
import csv
import re
import argparse

### User input and output files + API key for DisGeNet
# infile = '/home/smoorsh/ondemand/data/NKH/APIwork/Practice_Chem.csv'
# geneOutfile = '/home/smoorsh/ondemand/data/NKH/APIwork/chemicalProtein.tsv'
# diseaseFile = '/home/smoorsh/ondemand/data/NKH/APIwork/DiseaseOntology/HumanDiseaseOntology-2024-08-29/DOreports/allXREFinDO.tsv'
# diseaseOutfile = 'chem_gene_disease_test.tsv'
# API_KEY = 'b9ef2818-162b-4297-a0f3-92a3de81dd2e'
#### Command line: python chem_gene_disease.pi infile geneOutfile diseaseFile diseaseOutfile API_KEY ####

### Send API request to the CTD
inputType= 'chem'
actionTypes= 'ANY'

### User defined functions
### CTD
def cgixns(infile, geneOutfile, inputType='chem', actionTypes='ANY'):
    with open(infile, 'r') as lines:
        inTerms = lines.read()
    #CTD URL Batch Querry with input
    url = 'http://ctdbase.org/tools/batchQuery.go?report=cgixns&format=tsv&inputTerms='
    get = requests.get(url+inTerms+'&'+'inputType='+inputType+'&'+'actionTypes='+actionTypes)
    ### Place results into tsv file
    with open(geneOutfile, 'wb') as q:
        q.write(get.content)

### Switch DO identifiers from DisGeNet from starting with "DO_" to "DOID:", 
def process_disease_ids(a_dict):
    input_dict = {}
    
    for gene_id, disease_ids in a_dict.items():
        # Remove all non-DOids from each gene, replace 'DO_' with 'DOID:'
        DO_ids = [re.sub(r'^DO_', 'DOID:', id) for id in disease_ids if id.startswith('DO_')]
        
        # Add all DO ids to the new dictionary
        if DO_ids:
            input_dict[gene_id] = DO_ids
    
    return input_dict

### parser arguments for command line
def inputData():
    parser = argparse.ArgumentParser(description='Process chemical, gene, and disease data files')
    
    parser.add_argument("-i", 'infile', required=True, 
                        help='Path to the input CSV file')
    parser.add_argument("-c", 'geneOutfile', required=False, 
                        default="interactionsCTD.tsv", 
                        help='Path to the output TSV file for chemical-protein data')
    parser.add_argument("-p", 'diseaseFile', required=False,
                        default="allXREFinDO.tsv", 
                        help='Path to the disease ontology TSV file')
    parser.add_argument("-m", 'diseaseOutfile', required=False, 
                        default='chem_gene_disease_test.tsv', 
                        help='Path to the output TSV file for chemical-gene-disease data')
    parser.add_argument("-k", 'API_KEY', required=True, 
                        help='API key for data access')

    args = parser.parse_args()

    # Now you can use the arguments in your code
    infile = args.infile
    geneOutfile = args.geneOutfile
    diseaseFile = args.diseaseFile
    diseaseOutfile = args.diseaseOutfile
    API_KEY = args.API_KEY

    # Your existing code here, using these variables
    print(f"Input file: {infile}")
    print(f"Gene output file: {geneOutfile}")
    print(f"Disease file: {diseaseFile}")
    print(f"Disease output file: {diseaseOutfile}")
    print(f"API Key: {API_KEY}")
    
    return infile, geneOutfile, diseaseFile, diseaseOutfile, API_KEY

### main program ###

infile, geneOutfile, diseaseFile, diseaseOutfile, API_KEY = inputData()
cgixns(infile, geneOutfile, actionTypes='ANY')

### Pull chemical gene interactions from the CTD and print them into a tsv file
df = pd.read_csv(geneOutfile, sep='\t', dtype="string")

# Identify human genes by moving them into a data frame
human_df = df[df['OrganismID'] == '9606']

### remove duplicates from the data frame
df_unique = human_df.drop_duplicates(subset='GeneID')

### Create a data frame with just the NCBI Gene IDs for DisGeNet
df_ncbiID = df_unique[['GeneID']]

### Use DisGeNet to find diseases associated with the above genes

## Place ncbiIDs into a list for DisGeNet to iterate through
list_ncbiID = df_ncbiID.values.tolist()

params = {}

# Initialize an empty dictionary to store the results
DGN_dict = {}

#Create empty list for removing duplicates
output_data = []

for i in list_ncbiID:
    params["gene_ncbi_id"] = i
    params["page_number"] = "0"
    
    # Create a dictionary with the HTTP headers of your API call 
    HTTPheadersDict = {}
    # Set the 'Authorization' HTTP header equal to API_KEY (your API key) 
    HTTPheadersDict['Authorization'] = API_KEY
    # Set the 'accept' HTTP header to specify the response format: 'application/json' 
    HTTPheadersDict['accept'] = 'application/json'

    # Query the gda summary endpoint 
    response = requests.get("https://api.disgenet.com/api/v1/gda/summary",\
                            params=params, headers=HTTPheadersDict, verify=True)

    # If the status code of response is 429, it means you have reached one of your query limits 
    # You can retrieve the time you need to wait until doing a new query in the response headers
    if not response.ok:
        if response.status_code == 429:
            while response.ok is False:
                print("You have reached a query limit for your user. Please wait {} seconds until next query".format(\
                response.headers['x-rate-limit-retry-after-seconds']))
                time.sleep(int(response.headers['x-rate-limit-retry-after-seconds']))
                print("Your rate limit is now restored")

                # Repeat your query
                response = requests.get("https://api.disgenet.com/api/v1/gda/summary",\
                                        params=params, headers=HTTPheadersDict, verify=False)
                if response.ok is True:
                    break
                else:
                    continue

    # Parse response content in JSON format since we set 'accept:application/json' as HTTP header 
    response_parsed = json.loads(response.text)
    print('STATUS: {}'.format(response_parsed["status"]))
    print('TOTAL NUMBER OF RESULTS: {}'.format(response_parsed["paging"]["totalElements"]))
    print('NUMBER OF RESULTS RETRIEVED BY CURRENT CALL (PAGE NUMBER {}): {}'.format(\
          response_parsed["paging"]["currentPageNumber"], response_parsed["paging"]["totalElementsInPage"]))
    
    # Iterate through the payload to extract gene_ncbi_id and diseaseVocabularies
    for entry in response_parsed['payload']:
        gene_ncbi_id = entry['geneNcbiID']
        disease_vocabularies = entry['diseaseVocabularies']

        # Check if the gene_ncbi_id already exists in the dictionary
        if gene_ncbi_id in DGN_dict:
            # Append the new disease vocabularies to the existing list
            DGN_dict[gene_ncbi_id].extend(disease_vocabularies)
        else:
            # Create a new list for the gene_ncbi_id
            DGN_dict[gene_ncbi_id] = disease_vocabularies
    
    
    # Iterate through the payload to extract gene_ncbi_id and diseaseVocabularies
    for entry in response_parsed['payload']:
        gene_ncbi_id = entry['geneNcbiID']
        disease_name = entry['diseaseName']

        # Check if the gene_ncbi_id already exists in the dictionary
        if gene_ncbi_id in DGN_dict:
            # Append the new disease name to the existing list
            DGN_dict[gene_ncbi_id].append(disease_name)
        else:
            # Create a new list for the gene_ncbi_id
            DGN_dict[gene_ncbi_id] = disease_name

for gene_id, disease_ids in DGN_dict.items():
    # Remove duplicates by converting the list to a set and back to a list
    unique_disease_ids = list(set(disease_ids))
    
    # Append each unique disease ID with the corresponding gene ID to the output data
    for disease_id in unique_disease_ids:
        output_data.append((gene_id, disease_id))


#### Take just the Disease Ontology results and search for them in the Disease Ontology allXREF file

# Use function on DGN_dict
input_dict = process_disease_ids(DGN_dict)

## Parse through each DO file, and pull out the disease name and ID for matching DOIDs ##

with open(diseaseFile, 'r') as keyList:
    key = keyList.readlines()
    key_cleaned = [s.strip() for s in key]
    
key_dict = {} # create dictionary of disease ontology IDs and names for reference
for entry in key_cleaned[1:]:
    parts = entry.split('\t') # split entry by tab
    
    # Extract the disease ID, name, and reference
    disease_id = parts[0].strip('"')  # Remove quotes
    disease_name = parts[1].strip('"')  # Remove quotes
    reference = parts[2].strip('"')  # Remove quotes
    
    # If the disease ID is not in the dictionary, initialize it
    if disease_id not in key_dict:
        key_dict[disease_id] = disease_name

# #print(key_dict)
result_dict = {}
output_ids = []


# Iterate through the values in the first dictionary
for gene_id, disease_ids in input_dict.items():
    for disease_id in disease_ids:
        # Perform operations with gene_id and disease_id
        if disease_id in key_dict:
            if gene_id not in result_dict:
                result_dict[gene_id] = {}
            result_dict[gene_id][disease_id] = key_dict[disease_id]

            
## Put matching disease names into a separate file with the gene they interact with and CTD results ##

# Convert the dictionary to a dataframe
DO_df = pd.DataFrame([(gene_id, disease_id, disease_name) 
                                for gene_id, diseases in result_dict.items() 
                                for disease_id, disease_name in diseases.items()],
                               columns=['GeneID', 'DiseaseID', 'DiseaseName'])
DO_df['GeneID'] = DO_df['GeneID'].astype(str) ## convert to string

# make one data frame of both the disease ontology data and the CTD data
merged_df = pd.merge(human_df, DO_df, on='GeneID', how='inner')

# Make columns with appropriate titles for output
final_df = merged_df[['ChemicalName', 'GeneSymbol', 'GeneID', 'DiseaseID', 'DiseaseName']]

# Write to TSV file
final_df.to_csv(diseaseOutfile, sep='\t', index=False)