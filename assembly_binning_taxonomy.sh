#this script does the following: 1) DAS_TOOL for binning quality
#       			 2) Kraken tools for  binning taxonomy
#   				 3) Phylophlan for binning annotation
			

#DEFINING VARIALBES


overall_output_folder=$1
thread=$2

DIR="${BASH_SOURCE[0]}"
DIR="$(dirname "$DIR")"


#DAS_TOOL


bins=$overall_output_folder/BINS
scaffold_file=$bins/my_scaffolds2bin.tsv
contigs_file=$overall_output_folder/METASPADES/contigs.fasta
dastool_output=$overall_output_folder/DAS_TOOL

Fasta_to_Scaffolds2Bin.sh -e $bins/fa > $scaffold_file


DAS_Tool -i $scaffold_file -c $contigs_file -o $dastool_output


#KRAKEN

bins_count=ls $bins | wc -l
kraken_output=$overall_output_folder/KRAKEN


if [ ! -d "$kraken_output" ] ; then
	mkdir $kraken_output
fi

for i in $(seq $count); do
	outputfile="$bins/bin."$i".kraken"
	reportfile="$bins/bin."$i".report"
	inputfile= "$bins/bins."$i".fa"

	kraken --db $KRAKEN_DB --use-names --threads $thread --output $outputfile --report $reportfile $inputfile
done

echo 'finished kraken'

#PHYLOPHLAN

phylophlan_output=$overall_output_folder/PHYLOPHLAN

if [ ! -d "$phylophlan_output" ] ; then
        mkdir $phylophlan_output
fi


phylophlan_metagenomic -i $bins -d SGB.Jan19 -e .fa -o $phylophlan_output'

echo 'finished phylophlan'










