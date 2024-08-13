#!/bin/bash

##THIS IS THE UPDATED VERSION OF METAIMP_ASSEMBLY_MAPPING
##Authors: Kalyan Sahu, Qiuming Yao
##Affiliation: Integrated Digital Omics Lab (IDOL), School of Computing, University of Nebraska-Lincoln

#THIS IS THE MAIN_ASSEMBLY_SCRIPT.
#STEPS INVOLVED IN THIS SCRIPT : 
#		1) PREPROCESSING: This process is executed by preprocessing.sh which takes two inputs for paire-end forward and reverse fastq files 
#		2) ASSEMBLY: This process is executed by assembly_binning.sh which has 5 inputs: A) FORWARD-END FASTQ FILE PATH
#												 B) REVERSE-END FASTQ FILE PATH
#												 C) SAMPLEID
#												 D) OUTPUT PATH
#												 E) NUMBER OF THREADS
#												 F) MINIMUM CONTIG LENGTH

##WE HAVE NOW ADDED STEP_6 TO METAIMP
#DEFINING THE VARIABLES	

read1=$1
read2=$2
sampleID=$3
output_folder=$4
min_thread=$5
min_contig_length=$6
assembly_mode=$7
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
	3) sampleID = sample name used in renaming the fastq reads and later processing
	4) output_folder= Output folder path
	5) min_thread= Total number of threads
	6)min_contig_length (OPTIONAL) = filter contigs based on minimum length (ex: 1000)'
	
else
	# PRE-PROCESSING

	log_preprocessing=$log_folder/preprocessing.log
	if [ -f "$log_preprocessing" ] ; then
		echo "$log_preprocessing exists. Skip preprocessing..."
	else
		 echo "$log_preprocessing does not exist"
		 echo "starting preprocessing $(date) ..."
		 echo "./preprocessing.sh $read1 $read2 $sampleID $min_thread $output_folder"
		 $DIR/preprocessing.sh $read1 $read2 $sampleID $min_thread $output_folder
		 echo "completed pre-processing at $(date). starting assembly"

	         touch $log_preprocessing
	fi
	echo ' '
	echo '###########################################################################################################'
	
	read1=$output_folder/${read1##*/}.filtered_1.fastq
	read2=$output_folder/${read2##*/}.filtered_2.fastq	
	
	echo '###########################################################################################################'

	#METHODS
	log_assembly_methods=$log_folder/assembly_methods.log
	if [ -f "$log_assembly_methods" ]; then
                echo "$log_assembly_methods exists. Skip assembly and binning..."
        else
                echo "$log_assembly_methods does not exist"
                echo "starting assembly methods at $(date)..."
		$DIR/assembly_methods.sh $read1 $read2 $assembly_mode $output_folder $min_thread $min_contig_length
		touch $log_assembly_methods
	fi
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

	
	# BINNING TAXONOMY; this part is independent of the next one

	log_binning_taxonomy=$log_folder/binning_taxonomy.log

	if [ -f "$log_binning_taxonomy" ]; then
		echo "$log_binning_taxonomy exists. Skip binning taxonomy (kraken, phyophlan, DAS_TOOL)..."
        else
		echo "$log_binning_taxonomy does not exist"
		echo " starting binning taxonomy at $(date)..."
		$DIR/assembly_binning_taxonomy.sh $output_folder $min_thread
		echo "finished taxonomy binning at $(date). Results available in KRAKEN, PHYLOPHLAN and DAS_TOOL folders in" $output_folder
		touch $log_binning_taxonomy
	fi

	echo ' '
        echo '###########################################################################################################'


	# CONTIG_ANNOTATION; this part is independent


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

	# SNP_CALLING; this part is independent

	bam_sorted_file=$output_folder/METASPADES/contig_mapping_sort.bam
	contig=$output_folder/METASPADES/contigs.fasta
	snp_output=$output_folder/INSTRAIN
	scaffold2bin=$output_folder/BINS/my_scaffolds2bin.tsv
	
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
	#source activate $USER_ENV_NAME
	if [ ! -z $USER_ENV_NAME ]; then

                source activate $USER_ENV_NAME

        fi

	instrain_file=$snp_output/output/INSTRAIN_SNVs.tsv
	annotation_file=$annotation_results/eggnog_results.emapper.annotations
	assembly_snp_annotation=$output_folder/ASSEMBLY_SNP_ANNOTATION
	contigs_file=$output_folder/METASPADES/contigs.fasta
	path_to_kraken_dir=$output_folder/KRAKEN
	scaffold_info=$output_folder/BINS/my_scaffolds2bin.tsv
	checkm_stats=$output_folder/BINS/CHECKM/storage/bin_stats.analyze.tsv

	log_snp_annotation=$log_folder/snp_annotation.log
	if [ -f "$log_snp_annotation" ] ; then
		echo "$log_snp_annotation exists. Skip snp annotation mapping..."
	else
                echo "$log_snp_annotation does not exist"
		echo "starting final mapping between snps and annotations at $(date)..."
		$DIR/assembly_snp_annotation.sh $instrain_file $annotation_file $mergedfile $assembly_snp_annotation $contigs_file $path_to_kraken_dir $scaffold_info $checkm_stats
		echo "finishd assembly_snp_annotation at $(date)"
		touch $log_snp_annotation

	fi
	echo ' '
        echo '###########################################################################################################'

	echo "finished assembly pipeline with snp calling and annotations. SNPS and their annotations are mapped. Thank you!!!"
	#source deactivate
	if [ ! -z $USER_ENV_NAME ]; then

                source deactivate

        fi

	# PROTEIN_ANNOTATION

	#source activate $USER_ENV_NAME
	if [ ! -z $USER_ENV_NAME ]; then

                source activate $USER_ENV_NAME

        fi

        instrain_file=$snp_output/output/INSTRAIN_SNVs.tsv
        annotation_file=$annotation_results/eggnog_results.emapper.annotations
        assembly_snp_annotation=$output_folder/ASSEMBLY_SNP_ANNOTATION
        contigs_file=$output_folder/METASPADES/contigs.fasta
        path_to_kraken_dir=$output_folder/KRAKEN
        scaffold_info=$output_folder/BINS/my_scaffolds2bin.tsv
        checkm_stats=$output_folder/BINS/CHECKM/storage/bin_stats.analyze.tsv
	coverage_file=$output_folder/METASPADES/coverage.txt #coverage file from bbwrap added as parameter 
	log_protein_annotation=$log_folder/protein_annotation.log
        if [ -f "$log_protein_annotation" ] ; then
                echo "$log_protein_annotation exists. Skip snp annotation mapping..."
        else
                echo "$log_protein_annotation does not exist"
                echo "starting final mapping between snps and annotations at $(date)..."
                $DIR/assembly_protein_annotation.sh $instrain_file $annotation_file $mergedfile $assembly_snp_annotation $contigs_file $path_to_kraken_dir $scaffold_info $checkm_stats $coverage_file $output_folder $sampleID
                echo "finishd assembly_protein_annotation at $(date)"
                touch $log_protein_annotation
	fi
	
	echo ' '
        echo '###########################################################################################################'

        echo "MetaIMP assembly pipeline complete with protein identification and annotations. Thank you!!! CHECK $output_folder for results."
        #source deactivate
	if [ ! -z $USER_ENV_NAME ]; then

                source deactivate

        fi


fi

#THIS IS THE END OF MAIN_ASSEMBLY SCRIPT
#####
