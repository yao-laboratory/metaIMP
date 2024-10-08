#this script does the following: 1) DAS_TOOL for binning quality
#       			 2) Kraken tools for  binning taxonomy
#   				 3) Phylophlan for binning annotation
			

#DEFINING VARIALBES



overall_output_folder=$1
thread=$2

#DIR="${BASH_SOURCE[0]}"
#DIR="$(dirname "$DIR")"


#DAS_TOOL

echo "starting DAS_TOOL at $(date)"
bins=$overall_output_folder/BINS
scaffold_file=$bins/my_scaffolds2bin.tsv
contigs_file=$overall_output_folder/METASPADES/contigs.fasta
dastool_output=$overall_output_folder/DAS_TOOL/


if [ ! -d "$dastool_output" ] ; then
        mkdir $dastool_output
fi
dastool_output_base=$dastool_output/das_tool_output

#new if-else for version compatability
if command -v Fasta_to_Contig2Bin.sh; then
	Fasta_to_Contig2Bin.sh -e fa -i $bins > $scaffold_file
else
	Fasta_to_Scaffolds2Bin.sh -e fa -i $bins > $scaffold_file
fi


echo " Fasta_to_Scaffolds2Bin.sh -e fa -i $bins > $scaffold_file  " 
DAS_Tool -i $scaffold_file -c $contigs_file --score_threshold 0 -o $dastool_output_base

echo "********************** \n \n \n **************** \n \n \n  "
echo " THIS IS DAS TOOL PRINT statment:" 
echo " \n \n "
echo " DAS_Tool -i $scaffold_file -c $contigs_file --score_threshold 0 -o $dastool_output_base " 
echo "finishing DAS_TOOL at $(date)"


#KRAKEN
#look for total number of fasta files, not the total count in that folder

echo "starting KRAKEN at $(date)"

bins_count=$(ls -la $bins/bins.*.fa | wc -l)

kraken_output=$overall_output_folder/KRAKEN


if [ ! -d "$kraken_output" ] ; then
	mkdir $kraken_output
fi

for i in $(seq $bins_count); do
	outputfile=$kraken_output/bins.$i.kraken
	reportfile=$kraken_output/bins.$i.report
	inputfile=$bins/bins.$i.fa

	#echo $outputfile
	#echo $reportfile
	#echo $inputfile
	kraken2 --db $KRAKEN_DATABASE --use-names --threads $thread --output $outputfile --report $reportfile $inputfile
done

echo "finished kraken at $(date)"



#PHYLOPHLAN
echo "starting PHYLOPHLAN at $(date)"

phylophlan_output=$overall_output_folder/PHYLOPHLAN/

if [ ! -d "$phylophlan_output" ] ; then
        mkdir $phylophlan_output
fi


phylophlan_assign_sgbs -i $bins -d $PHYLOPHLAN_DATABASE -e .fa -o $phylophlan_output/phylophlan

#phylophlan_metagenomic -i $bins -d $PHYLOPHLAN_DATABASE -e .fa -o $phylophlan_output/phylophlan

echo "finishing PHYLOPHLAN at $(date)"


imusage=$(free | awk '/Mem/{printf("RAM Usage: %.2f%\n Mbits"), $3/1000000}' |  awk '{print $3}' | cut -d"." -f1)
echo "Current Memory Usage for ${BASH_SOURCE[0]} is: $imusage MBits"







