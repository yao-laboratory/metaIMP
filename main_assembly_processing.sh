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


if [[ read1 = -h]]
then 
	echo 'Usage information: 1) read1 = Forward paired-end file (FASTQ) 2) read2 = Reverse paired-end file (FASTQ) 3) output_folder= Output folder path 4) min_thread= Total number of threads 5)min_contig_length (OPTIONAL) = filter contigs based on minimum length (ex: 1000)'

else
	# PRE-PROCESSING
	log_folder=$output_folder/log_folder
	mkdir $log_folder
	log_preprocessing=$log_folder/preprocessing.log
	if [[ -f "$log_preprocessing"]]
	then 
		echo "$log_preprocessing exists"
	else 
		echo "$log_preprocessing does not exist"
		echo "starting preprocessing"
		./preprocessing.sh $read1 $read2
		echo "completed pre-processing. starting assembly"
		touch $log_preprocessing
	fi
	
	# BINNING
	log_assembly_binning=$log_folder/assembly_binning.log
	if [[ -f "$log_assembly_binning"]]
	then
                echo "$log_assembly_binning exists"
        else
                echo "$log_assembly_binning does not exist"
                echo "starting assembly binning"
		./assembly_binning.sh $read1 $read2 $output_folder $min_thread $min_contig_length
		echo "finished assembly binning. Check" $output_folder
		touch $log_assembly_binning
	fi


	# CONTIG_ANNOTATION


	mergedfile=$output_folder/bins/checkm/bins/mergedfile.fna
	annotation_results=$output_folder/eggnog_output
	log_assembly_contig_annotation=$log_folder/assembly_contig_annotation.log

	if [[ -f "$log_assembly_contig_annotation"]]
        then
                echo "$log_assembly_contig_annotation exists"
        else
                echo "$log_assembly_contig_annotation does not exist"
                echo "starting assembly contig annotation"
		./assembly_contig_annotation.sh $mergedfile $annotation_results
		echo 'contig annotation complete. starting snp calling using instrain'
		touch $log_assembly_contig_annotation
	fi
	

	# SNP_CALLING

	bam_sorted_file=$output_folder/bmfile_sort.bam
	contig=$output_folder/contigs.fasta
	snp_output=$output_folder/instrain_results
	log_snp_calling=$log_folder/snp_calling.log

	if [[ -f "$log_snp_calling"]]
	then
                echo "$log_snp_calling exists"
        else
                echo "$log_snp_calling does not exist"
                echo "starting snp calling"
		./assembly_snp_calling.sh $bam_sorted_file $contig $snp_output $min_thread $mergedfile
		echo 'completed snp calling. starting assembly_snp_annotation'
		touch $log_snp_calling
	fi
	

	# SNP_ANNOTATION

	instrain_file=$output_folder/instrain_results/instrain_SNVs.tsv
	annotation_file=$output_folder/eggnog_output/eggnog_results.emapper.annotations
	log_snp_annotation=$log_folder/snp_annotation.log
	assembly_snp_annotation=$output_folder/snp_annotation
	
	if [[ ! -d $assembly_snp_annotation]]
	then 
		mkdir $assembly_snp_annotation
	else
		continue
	fi

	if [[ -f "$log_snp_annotation"]]
	then
		echo "$log_snp_annotation exists"
	else
                echo "$log_snp_annotation does not exist"
                echo 'starting final mapping between snps and annotations'
		./assembly_snp_annotation.sh $instrain_file $annotation_file $mergedfile $assembly_snp_annotation
		echo "finishd assembly_snp_annotation"
		touch $log_snp_annotations

	fi

echo 'finished assembly pipeline with snp calling and annotations. SNPS and their annotations are mapped. Thank you!!!'
fi

#THIS IS THE END OF MAIN_ASSEMBLY SCRIPT
#####
