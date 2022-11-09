#!/bin/bash
#this script perfroms the following actions: 1) Assembly using MetaSPADES 2) Megahit
#
#
#
#STARTING ASSEMBLY_METHODS SCRIPT

#VARIABLES DEFINED HERE
#INPUTS ARE CALLED FROM ASSEMBLY_MAIN_SCRIPT
fastq1=$1
fastq2=$2
assembly_mode=$3
overall_output_folder=$4
t=$5
minimum_contig_len=$6


DIR="${BASH_SOURCE[0]}"
DIR="$(dirname "$DIR")"

metaspade_output=$overall_output_folder/METASPADES
if [ ! -d "$metaspade_output" ] ; then
        mkdir $metaspade_output
fi

megahit_output=$overall_output_folder/MEGAHIT
if [ ! -d "$megahit_output" ] ; then
        mkdir $megahit_output
fi



echo -n "Enter the number of method you want to use \n 1) Basic Assembly with read-correction  2) Assembly without error-correcttion  3)Basic Megahit  4) Megahit with k-mer list  "
#read OPTION

echo -n "You have choosen the following option $assembly_mode"

case $assembly_mode in

  1 | "1")
  	spades.py --meta --pe1-1 $fastq1 \
        	--pe1-2 $fastq2 \
        	-t $t \
        	-m 1000 \
        	-o $metaspade_output
	scp $metaspade_output/contigs.fasta $metaspade_output/metaspades_contigs_backup.fasta

 	echo "spades.py --meta --pe1-1 $fastq1 \
        	--pe1-2 $fastq2 \
        	-t $t \
		-m 1000 \
		-o $metaspade_output"
    ;;

  2 | "2")
	spades.py --meta --pe1-1 $fastq1 \
        	--pe1-2 $fastq2 \
        	-t $t \
		-m 1000 \
		--only-assembler \
		-o $metaspade_output
	scp $metaspade_output/contigs.fasta $metaspade_output/metaspades_contigs_backup.fasta

    	echo -n "spades.py --meta --pe1-1 $fastq1 --pe1-2 $fastq2 -t $t -m 1000 --only-assembler -o $metaspade_output"
    ;;

  3 |  "3") 
	megahit -1 $fastq1 -2 $fastq2 --min-contig-len 1000 -t $t -o $megahit_output
	scp $megahit_output/final.contigs.fa $metaspade_output/contigs.fasta
    	
    	echo -n "megahit -1 $fastq1 -2 $fastq2 --min-contig-len 1000 -t $t -o $megahit_output"

    ;;
  4 | "4")
	megahit -1 $fastq1 -2 $fastq2 --k-list 79,99,119,141 --min-contig-len 1000 -t $t -o $megahit_output
	scp $megahit_output/final.contigs.fa $metaspade_output/contigs.fasta
	
    	echo -n "megahit -1 $fastq1 -2 $fastq2 --k-list 79,99,119,141 --min-contig-len 1000 -t $t -o $megahit_output"
    ;;    

  *)
	echo -n " \n  Wrong parameters. Choose between MetaSPADES: With Read correction (Option 1), Without Read Correction (Option 2), and MEGAHIT: Without k-mers and all contig length (Option 3), With 			k-mer list [79,99,119,141], min_contig_len=1000bp (Option 4)"
    ;;
esac

