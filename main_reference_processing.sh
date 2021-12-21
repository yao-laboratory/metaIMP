#main_script for reference based pipeline
#these are the inputs to reference-based pipeline

read1=$1
read2=$2
output_folder=$3
env_var=$4

if [ $read1 = -h ] ; then
	echo "Usage information: 1) read1 = Forward paired-end file (FASTQ) 2) read2 = Reverse paired-end file (FASTQ) 3) output_folder= Output folder path"
else 
	echo "starting pre-processing for reference-based pipeline"
	source activate $env_var
	log_folder=$output_folder/log_folder
	mkdir $log_folder
	
	if [ -f "$FILE" ] ; then
		echo "$FILE exists. Skipping pre-processing"
	else
		echo "$FILE does not exist."
		./preprocessing.sh $read1 $read2
		log_preprocessing=$log_folder/preprocessing.log
		touch $log_preprocessing
	fi
	echo 'finished preprocessing of paired-end input files. starting annotations now'
	echo ' '
        echo '###########################################################################################################'

	
	if [ -f "$log_reference_pipeline" ] ; then
		echo "$log_reference_pipeline exists. Skipping pre-processing"
	else
		 echo "$log_reference_pipeline  does not exist."
		 echo "starting midas species, genes, snps procedures"
		 ./ref_species_genes_snps.sh $read1 $read2 $output_folder
		 echo 'reference pipeline is ready for annotations'
		 log_reference_pipeline=$log_folder/ref_species_genes_snps.log
		 touch $log_reference_pipeline
	fi

	echo 'starting annotation using PATRIC and mapping annotations with snps'
	echo ' '
        echo '###########################################################################################################'

	

	if [ -f "$log_snp_annotation" ] ; then 
		echo "$log_snp_annotation exists. Skipping annotations"
	else
		echo "$log_snp_annotation doesnot exist. Starting SNP_annotation"
		./ref_snp_annotation.sh $output_folder/genes $output_folder/genes $output_folder/snps $output_folder
		echo 'Finished annotations and mapping snps. Reference pipeline is now complete. Thank you!!!'
		log_snp_annotation=$log_folder/snp_annotation.log
		touch $log_snp_annotation
	fi
        echo ' '
        echo '###########################################################################################################'	
	source deactivate $env_var
fi
