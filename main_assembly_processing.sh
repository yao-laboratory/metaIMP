#!/bin/bash
#THIS IS THE MAIN_ASSEMBLY_SCRIPT.
#STEPS INVOLVED IN THIS SCRIPT : 
#		1) PREPROCESSING: This process is executed by preprocessing.sh which takes two inputs for paire-end forward and reverse fastq files 
#		2) ASSEMBLY: This process is executed by assembly_binning.sh which has 5 inputs: A) FORWARD-END FASTQ FILE PATH
#												 B) REVERSE-END FASTQ FILE PATH
#												 C) OUTPUT PATH
#												 D) NUMBER OF THREADS
#												 E) MINIMUM CONTIG LENGTH


#DEFINING THE VARIABLES	

read1=$1
read2=$2
output_folder=$3
min_thread=$4
min_contig_length=$5
#env_var=$6

if [ ! -d "$output_folder" ] ; then
	mkdir $output_folder
fi

log_folder=$output_folder/log_folder
if [ ! -d "$log_folder" ] ; then
        mkdir $log_folder
fi

temp_folder=$output_folder/temp_folder
if [ ! -d "$temp_folder" ] ; then
        mkdir $temp_folder
fi

DIR="${BASH_SOURCE[0]}"
DIR="$(dirname "$DIR")"
echo "running main assembly process in the folder $DIR"

if [ $read1 = -h ] ; then
	echo 'Usage information: 1) read1 = Forward paired-end file (FASTQ)
	2) read2 = Reverse paired-end file (FASTQ)
	3) output_folder= Output folder path
	4) min_thread= Total number of threads
	5)min_contig_length (OPTIONAL) = filter contigs based on minimum length (ex: 1000)'
	
else
	# PRE-PROCESSING

	log_preprocessing=$log_folder/preprocessing.log
	if [ -f "$log_preprocessing" ] ; then
		echo "$log_preprocessing exists. Skip preprocessing..."
	else
		 echo "$log_preprocessing does not exist"
		 echo "starting preprocessing $(date) ..."
		 echo "./preprocessing.sh $read1 $read2 $min_thread"
	         $DIR/preprocessing.sh $read1 $read2 $min_thread
		 echo "completed pre-processing at $(date). starting assembly"

	         touch $log_preprocessing
	fi
	echo ' '
	echo '###########################################################################################################'

	echo 'moving filtered reads to output folder provided by user'

	read1_temp=$read1.filtered_1.fastq
	read2_temp=$read2.filtered_2.fastq
	
	mv $read1_temp $read2_temp $output_folder

	read1=$output_folder/$read1_temp
	read2=$ouput_folder/$read2_temp

	echo 'finished moving reads to output folder'
	echo '###########################################################################################################'
	
	# FASTQC
	echo 'starting fastqc'

	ftqc=$output_folder/FASTQC_RESULTS

	if [ ! -d "$ftqc" ] ; then
		mkdir $ftqc
	fi

	fastqc $read1
	fastqc $read2
	
	mv *.html *.zip $ftqc

	echo 'finished fastqc. check results in' $ftqc	
	
	echo '###########################################################################################################'



	# BINNING
	log_assembly_binning=$log_folder/assembly_binning.log
	if [ -f "$log_assembly_binning" ]; then
		echo "$log_assembly_binning exists. Skip assembly and binning..."
        else
		echo "$log_assembly_binning does not exist"
		echo "starting assembly binning at $(date)..."
		$DIR/assembly_binning.sh $read1 $read2 $output_folder $min_thread $min_contig_length
		echo "finished assembly binning at $(date). Check" $output_folder
		touch $log_assembly_binning
	
	fi
	echo ' '
        echo '###########################################################################################################'


	# CONTIG_ANNOTATION


	mergedfile=$output_folder/BINS/CHECKM/bins/mergedfile.fna
	annotation_results=$output_folder/EGGNOG
	
	log_assembly_contig_annotation=$log_folder/assembly_contig_annotation.log
	if [ -f "$log_assembly_contig_annotation" ] ; then
		echo "$log_assembly_contig_annotation exists. Skip annotation..."
        else
		echo "$log_assembly_contig_annotation does not exist"
		echo "starting assembly contig annotation at $(date)..."
		$DIR/assembly_contig_annotation.sh $mergedfile $annotation_results
		echo "contig annotation complete at $(date). starting snp calling using instrain"
		touch $log_assembly_contig_annotation
	fi
	echo ' '
        echo '###########################################################################################################'

	# SNP_CALLING

	bam_sorted_file=$output_folder/METASPADES/contig_mapping_sort.bam
	contig=$output_folder/METASPADES/contigs.fasta
	snp_output=$output_folder/INSTRAIN
	
	log_snp_calling=$log_folder/snp_calling.log
	if [ -f "$log_snp_calling" ] ; then
		echo "$log_snp_calling exists. Skip SNP calling..."
        else
		echo "$log_snp_calling does not exist"
		echo "starting snp calling at $(date)..."
		$DIR/assembly_snp_calling.sh $bam_sorted_file $contig $snp_output $min_thread $mergedfile
		echo "completed snp calling at $(date). starting assembly_snp_annotation"
		touch $log_snp_calling
	fi
	echo ' '
        echo '###########################################################################################################'

	# SNP_ANNOTATION
	source activate $USER_ENV_NAME
	instrain_file=$snp_output/output/INSTRAIN_SNVs.tsv
	annotation_file=$annotation_results/eggnog_results.emapper.annotations
	assembly_snp_annotation=$output_folder/ASSEMBLY_SNP_ANNOTATION
	
	
	log_snp_annotation=$log_folder/snp_annotation.log
	if [ -f "$log_snp_annotation" ] ; then
		echo "$log_snp_annotation exists. Skip snp annotation mapping..."
	else
                echo "$log_snp_annotation does not exist"
		echo "starting final mapping between snps and annotations at $(date)..."
		$DIR/assembly_snp_annotation.sh $instrain_file $annotation_file $mergedfile $assembly_snp_annotation
		echo "finishd assembly_snp_annotation at $(date)"
		touch $log_snp_annotation

	fi
	echo ' '
        echo '###########################################################################################################'

	echo "finished assembly pipeline with snp calling and annotations. SNPS and their annotations are mapped. Thank you!!!"
	source deactivate
fi

#THIS IS THE END OF MAIN_ASSEMBLY SCRIPT
#####
