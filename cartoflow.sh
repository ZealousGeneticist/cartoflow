#! /usr/bin/bash
##Make sure to run:
#chmod u+x cartoflow.sh
##Then run at least:
#bash cartoflow.sh -i <your_chemical_file.tsv>
##Workflow Program which runs all other Programs##
##################################
#Define Input and Output Files
infile="" #-i
outfile3="faceted_inact_node_network.tsv" #-o
outfile1="interactionsCTD" #-c
outjson="" #-j
organism="" #Define Taxonomy ID -g
test="" #Omniscience function toggle for single file output -t
debug="" #Debugging toggle for verbose output -d
removeJSON="" #Toggle for deleting orginal IntAct JSON file -r
noinstall="" #Disables installation of required packages in requirements.txt -z
#This one is for genebridge, not cartogene#
outputHeader="" #Toggle for having headers in the final master list(s) -e
chugReduction="" #Toggle to enable group betweeneness centrality for genebridge, VERY SLOW -f
fileName="edge2comm.txt" #Edge to Community file suffix -a
fileName2="comm2nodes.txt" #Community to Nodes file suffix -b
CARTOGENE_ARGS=""
GENEBRIDGE_ARGS=""
###USER DEFINED FUNCTIONS###
# Iterating through the arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        -a)
            if [ -n "$2" ]; then
                GENEBRIDGE_ARGS="$GENEBRIDGE_ARGS -a $2"
                fileName="$2"
            fi
            shift 2
            ;;
        -b)
            if [ -n "$2" ]; then
                GENEBRIDGE_ARGS="$GENEBRIDGE_ARGS -b $2"
                fileName2="$2"
            fi
            shift 2
            ;;
        -c)
            if [ -n "$2" ]; then
                CARTOGENE_ARGS="$CARTOGENE_ARGS -c $2"
                GENEBRIDGE_ARGS="$GENEBRIDGE_ARGS -c $2"
                outfile1="$2"
            fi
            shift 2
            ;;
        -d)
            CARTOGENE_ARGS="$CARTOGENE_ARGS -d"
            shift
            ;;
        -e)
            GENEBRIDGE_ARGS="$GENEBRIDGE_ARGS -e"
            shift
            ;;
        -f)
            GENEBRIDGE_ARGS="$GENEBRIDGE_ARGS -f"
            shift
            ;;
        -g)
            if [ -n "$2" ]; then
                CARTOGENE_ARGS="$CARTOGENE_ARGS -g $2"
                GENEBRIDGE_ARGS="$GENEBRIDGE_ARGS -g $2"
                organism="$2"
            fi
            shift 2
            ;;
        -i)
            if [ -n "$2" ]; then
                CARTOGENE_ARGS="$CARTOGENE_ARGS -i $2"
                infile="$2"
            fi
            shift 2
            ;;
        -j)
            if [ -n "$2" ]; then
                CARTOGENE_ARGS="$CARTOGENE_ARGS -j $2"
                outjson="$2"
            fi
            shift 2
            ;;
        -o)
            if [ -n "$2" ]; then
                CARTOGENE_ARGS="$CARTOGENE_ARGS -o $2"
                outfile3="$2"
            fi
            shift 2
            ;;
        -r)
            CARTOGENE_ARGS="$CARTOGENE_ARGS -r"
            shift
            ;;
        -t)
            CARTOGENE_ARGS="$CARTOGENE_ARGS -t"
            shift
            ;;
        -z)
            CARTOGENE_ARGS="$CARTOGENE_ARGS -z"
            GENEBRIDGE_ARGS="$GENEBRIDGE_ARGS -z"
            shift
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

#repository download
rm -rf cartogene || true
rm -rf linkcomm-U || true
rm -rf genebridge || true
git clone https://github.com/ZealousGeneticist/cartogene.git
git clone https://github.com/ZealousGeneticist/linkcomm-U.git
git clone https://github.com/ZealousGeneticist/genebridge.git
echo ""
echo "If git wasn't 'found', then you may have to run this:"
echo "sudo apt install git"
echo ""
sleep 5
#
echo "Cartogene Phase..."
sleep 1
cp $infile ./cartogene
cd ./cartogene
python3 cartogene_standalone.py $CARTOGENE_ARGS
#
sleep 1
echo "LinkComm-U Phase..."
cp $outfile3 ../linkcomm-U
cd ../linkcomm-U
sleep 2
python3 python/link_clustering.py $outfile3
#Aquire actual file names
e2c=$fileName
fileName=$(find "." -type f -name "*$fileName")
fileName2=$(find "." -type f -name "*$fileName2")
outfile1+="_chemical-protein.tsv"
#fileName & fileName2 refer to linkcomm-U files 
sleep 1
echo "Genebridge Phase..."
sleep 2
cp $fileName ../genebridge
cp $fileName2 ../genebridge
cd ../cartogene
cp $outfile1 ../genebridge
cp $outfile1 ../chemicalProteinInteractions.tsv
cd ../genebridge
sleep 2
python3 genebridge.py $GENEBRIDGE_ARGS
cp -r toppfunANDgraphs ..
cp Pyvis_Graph.html ../fullNetworkGraph.html
cp commMetrics.tsv ../communityMetrics.tsv
cp nodeMetrics.tsv ..
cp $fileName ../communityEdgeList.tsv
cd ..
#conclusion message
echo "Workflow complete!"