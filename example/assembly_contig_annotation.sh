#This script is used for functional annotation of large sets of sequence
#Only two user inputs are required: 1) mergedfile.fna obtained after CHECKM binning from assembly_binning.sh 
#				    2) Eggnog output folder path

echo 'starting eggnog'

mergedfile=$1
eggnog_output=$2
emapper.py -i $mergedfile -o $eggnog_output

echo 'Assembly_contig annotation is complete. Check' $eggnog_output 
