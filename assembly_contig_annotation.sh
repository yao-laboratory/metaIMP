#This script is used for functional annotation of large sets of sequence
#Only two user inputs are required: 1) mergedfile.fna obtained after CHECKM binning from assembly_binning.sh 
#				    2) Eggnog output folder path

echo 'starting eggnog'

mergedfile=$1
eggnog_output_folder=$2

if [ ! -d "$eggnog_output_folder" ] ; then
        mkdir $eggnog_output_folder
fi
eggnog_output=$eggnog_output_folder/eggnog_results
emapper.py -i $mergedfile -o $eggnog_output

echo 'Assembly_contig annotation is complete. Check' $eggnog_output 

imusage=$(free | awk '/Mem/{printf("RAM Usage: %.2f%\n Mbits"), $3/1000000}' |  awk '{print $3}' | cut -d"." -f1)
echo "Current Memory Usage for ${BASH_SOURCE[0]} is: $imusage MBits"
