# cartoflow
A Python workflow of three programs for taking chemicals, finding the genes they interact with, performing gene enrichment and mapping the communities of genetic interactions.

# Installation Instructions
git clone https://github.com/ZealousGeneticist/cartoflow.git

chmod u+x ./cartoflow/cartoflow.sh

## User Guide
Welcome to the all-in-one workflow, cartoflow! Part of the goal of this program is to make it as simple to use as possible. As such, there are only two major things to account for before you can properly utilize this program: 
1. The most complicated part is making sure your input chemical file, which is the file where all chemicals you want analyzed for chemical gene interactions are listed, is formatted correctly. Your input chemical file will now be referred to as <your_chem_file> .
+ This entire section is repeated in the cartogene User Guide as well, but will be repeated here as well.
    + Put the chemicals you are wanting to analyze in the input text file (tutorial example (in cartogene): <bioactive.tsv>) as a MeSH® name, synonym, or accession ID (“MESH:…”), or by CAS RN. You may also limit your search to official names by using the “name:” prefix. *Make sure they are return- or |-delimited!*
        + The tutorial text file (in cartogene) <bioactive.tsv> has been given to show multiple examples for how chemicals can be written. However, if you are unsure as to if your chemical is not showing up, check the Comparative Toxicogenomic Database to make sure it is there!

2. The next part is then to put <your_chem_file> in the cartoflow folder. Easy!

------

**Once you have made and placed <your_chem_file> in the cartoflow folder, just run these two commands.**
+ *You can add additional arguments from the Advanced User Guide if you want to do something special, but this should work for most people.*

**cd cartoflow**

**bash cartoflow.sh -i <your_chem_file>**

***If you are using a machine like a supercomputer where you do not have permissions to install packages to the python folder which are needed for this program, make sure to run this command after MANUALLY installing the required packages. A fix for this so you don't need to manually do that is coming soon for the less permissioned among your machines.***

**bash cartoflow.sh -i <your_chem_file> -z**

------

#### Quick Guide on Networks
    Nodes: Think of nodes as individual points or entities. In a biological network, nodes could be genes or chemicals or proteins or all of the above.

    Edges: Edges represent connections or relationships between nodes. In a biological network, an edge could represent an interaction between genes or proteins or chemicals or any of the above.

    Networks: Networks are a collection of nodes and edges. When you have multiple chemicals/proteins/genes connected through interactions, you have a biological network.

    Communities: Communities are groups of nodes that are more densely connected to each other than to nodes outside the group. In a biological network, a community could be a group of proteins who interact more with each other (say, to make an enzyme) than with proteins outside the group.
So, nodes are individual data points, edges are connections between them, networks are the overall structure, and communities are tightly-knit groups within that structure.

------

Once the workflow is finished, there should be 6 other files output into the cartoflow file and a folder containing potentially many files. Those are <nodeMetrics.tsv>, <communityEdgeList.tsv>, <communityMetrics.tsv>, <chemicalProteinInteractions.tsv>, <diseaseOutfile.tsv>, and <fullNetworkGraph.html> . The folder is called toppfunANDgraphs and contains two types of files: <community#GeneEnrichment.csv> and <community#Subgraph.html> .

+ <fullNetworkGraph.html> is the visualization of the entire network of chemical-protein interactions and gene-gene (protein-protein) interactions.
+ <nodeMetrics.tsv> is a table of the nodes in the network and a number of statistics, such as the communities they are part of, about them. 
    + This can be particularly useful if you want to look more into a particular point of interest such as how many interactions a specific chemical has with genes.
+ <communityMetrics.tsv> is a table of communities in the network and a number of statistics, such as the number of nodes that are in the community.
+ <communityEdgeList.tsv> is a table of edges in the network and which community they are a part of.
    + Edges only have 1 community, unlike nodes.
+<diseaseOutfile.tsv> (optional if you run chem_gene_disease) is a unique TSV showing gene-disease associations merged with your chemical-gene data. By default: chem_gene_disease_test.tsv.
+ toppfunANDgraphs contains the information for individual communities. Communities matter because it breaks down the complexity of the network into even more closely associated parts. The two files that make up this information are:
    + <community#GeneEnrichment.csv> are the gene enrichments from ToppFun of the genes that make up community #, where # is the community number. *Statistically significant* insights can be found here, and it is presorted by the type of association (example: disease) and then how significant it is while accounting for the chance of false positives (qValueFDR_BH).
    + <community#Subgraph.html> are graphs just like <fullNetworkGraph.htm> EXCEPT they only contain nodes that are part of community #, where # is the community number. This is extremely helpful, more so than even the full network graph, because you get a less clutter look while keeping things that show whether they are a protein or a chemical, or part of multiple other communities for each node.

### Workflow Pathing
Here is a clear visualization of the workflow as it goes between programs, which will be confirmed to you as the program proceeds. This may help if you need to figure out where an issue has occured!

Input: <your_chem_file>

->
DisGeNet (optional, requires API key)
->
cartogene
->
linkcomm
->
genebridge
->

Output: <your_chem_file>,<chemicalProteinInteractions.tsv>, <nodeMetrics.tsv>,<communityMetrics.tsv>,<fullNetworkGraph.html>, <communityEdgeList.tsv>, <diseaseOutfile> (if chem_gene_disease is run)
toppfunANDgraphs CONTAINS <community#GeneEnrichment.csv>,<community#Subgraph.html>


### Advanced User Guide
Here are the optional commands that can be utilized for cartoflow. All can be combined as needed; only the -i/--input argument is strictly required: 
+ **Input File**
    + "-i", "--input"
    + **ONLY REQUIRED ARGUMENT**
    + *Description*: This is the one required argument for the program which feeds the chemical list from the file into the script. This is the full name of the file.
        + As stated above; put the chemicals you want to analyze in the input text file (tutorial example: <bioactive.tsv>) as a MeSH® name, synonym, or accession ID (“MESH:…”), or by CAS RN. You may also limit your search to official names by using the “name:” prefix.
+ **Edge List File Name**
    +"-o", "--output"
    + *Description*: This is the final name of your edge list file. No alterations are made to this final name, so you may label it as any file type you wish (.tsv is suggested). By default, the name is set to <faceted_inact_node_network.tsv>
+ **CTD Chemical-Gene Interaction Table File Name**
    +"-c", "--ctd"
    + *Description*: This is the name for the intermediate Comparative Toxicogenomics Database (CTD) chemical-gene interaction table file. You can put in a name like -i or -o , however this final file name will have the suffix '_chemical-protein.tsv' added to it and the suffix "_cgd.tsv" added for the file in the DisGeNet step. By default, the name is `interactionsCTD`, which makes the final product <interactionsCTD_chemical-protein.tsv>
+ **IntAct Intermediate Data File Name**
    + "-j", "--json"
    + *Description*: This is the name for the intermediate IntAct gene-gene interaction JSON data file *prefix*. When any files are being made they have a file number for order like this: `_#_PPI.json` (unless running --test True). By default, the name is `faceted_intact_results`, which means the final name(s) is/are <faceted_intact_results_#_PPI.json>
        + *This file is extremely large for the JSON data type and can make most viewers stall significantly or even crash. If you wish to view it anyways, check the --removejson documentation below.* 
+ **NCBI Organism Taxonomy Number**
    + "-g", "--organism"
    + *Integer value*
    + *Description*: This integer value is the ID for the organism you wish to search by. By default, it uses the one for humans (`9606`).
+ **Omniscience Specific Single-Data-File Tester**
    + "-t", "--test"
    + *Bool value*
    + *Description*: This bool value is used to output only one IntAct JSON to test computing problems on weaker hardware. By default, it is `False` and doesn't affect anything.
+ **Debug**
    + "-d", "--debug"
    + *Bool value*
    + *Description*: This bool value is used to activate debug mode. This is primary used by the developers to figure out why some code is messing up and where in the script. It is by default `False` and off.
+ **Remove Intermediate IntAct Data JSON**
    + "-r", "--removejson"
    + *Bool value*
    + *Description*: This bool value is used to turn on or off the cleanup() process in the script which removes the chunky IntAct JSON, as normally the JSON is to large for any convient use on the user's end after it has been used by the program. It is **by default** `True` and **turned on.**
+ **Edge List Header Toggle**
    + "-e", "--header"
    + *Bool value*
    + *Description*: This bool value is used as a way to control whether you wish for the final output file to have headers for the edge list or to only have the columns be data. It is **by default** `False` and as such **keeps no headers**.


## New Options for Disease Data (chem_gene_disease)

These flags apply if you wish to run the optional chem_gene_disease step before CartoGene.

    If you do not provide an API key (-k), cartoflow will skip the disease association step.

    Disease Output File
        -m, --diseaseOutfile
        Description: The optional name for the disease-association TSV produced by the chem_gene_disease script. By default, this is chem_gene_disease_test.tsv. This file combines your chemical-gene interactions with disease annotations from DisGeNet.

    DisGeNet API Key
        -k
        Description: Required if you want to run the DisGeNet queries for gene-disease associations. If omitted, cartoflow will skip the disease enrichment step.

    Auto-Run DisGeNet
        -y or -n
        Description: If -y, runs chem_gene_disease automatically. If -n, bypasses DisGeNet calls entirely.

Extra:
*There should be maxium number of ~4000 chemicals that can be utilized as stated by the CTD Batch Query API.*