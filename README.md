# cartoflow
A Python workflow of three programs for taking chemicals, finding the genes they interact with, and mapping the communities of genetic interactions.

# Installation Instructions
git clone https://github.com/ZealousGeneticist/cartoflow.git

chmod u+x ./cartoflow/cartoflow.sh

## User Guide
Welcome to the all-in-one workflow, cartoflow! Part of the goal of this program is to make it as simple to use as possible. As such, there are only two major things to account for before you can properly utilize this program: 
1. The most complicated part is making sure your input chemical file, which is the file where all chemicals you want analyzed for chemical gene interactions are listed, is formatted correctly. Your input chemical file will now be referred to as <your_chem_file> .
+ This entire section is repeated in the cartogene User Guide as well, but will be repeated here as well.
    + Put the chemicals you are wanting to analyze in the input text file (tutorial example (in cartogene): <bioactive.tsv>) as a MeSH® name, synonym, or accession ID (“MESH:…”), or by CAS RN. You may also limit your search to official names by using the “name:” prefix. *Make sure they are return- or |-delimited!*
        + The tutorial text file (in cartogene) <bioactive.tsv> has been given to show multiple examples for how chemicals can be written. However, if you are unsure as to if your chemical is not showing up, check the Comparative Toxicogenomic Database to make sure it is there!
2.The next part is then to put <your_chem_file> in the cartoflow folder. Easy!

------
**Once you have made and placed <your_chem_file> in the cartoflow folder, just run these two commands.**
+ *You can add additional arguments from the Advanced User Guide if you want to do something special, but this should work for most people.*

**cd cartoflow**

**bash cartoflow.sh -i <your_chem_file>**

------
Once the workflow is finished, there should be 4 other files output into the cartoflow file. Those are <nodeMetrics.tsv>, <edge2comm.txt>, <commMetrics.tsv>, and <Pyvis_Graph.html> .

+ <Pyvis_Graph.html> is the visualization of the network of chemical-gene interactions and gene-gene interactions.
+ <nodeMetrics.tsv> is a table of the nodes in the network and a number of statistics, such as the communities they are part of, about them. 
    + This can be particularly useful if you want to look more into a particular point of interest such as how many interactions a specific chemical has with genes.
+ <commMetrics.tsv> is a table of communities in the network and a number of statistics, such as the number of nodes that are in the community.
+ <edge2comm.txt> is a table of edges in the network and which community they are a part of.
    + Edges only have 1 community, unlike nodes.

### Workflow Pathing
Here is a clear visualization of the workflow as it goes between programs, which will be confirmed to you as the program proceeds. This may help if you need to figure out where an issue has occured!

Input: <your_chem_file>

->
cartogene
->
linkcomm
->
genebridge
->

Output: <your_chem_file>,<nodeMetrics.tsv>,<commMetrics.tsv>,<Pyvis_Graph.html>, <edge2comm.txt>
