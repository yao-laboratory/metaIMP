#main_script for reference based pipeline
#these are the inputs to reference-based pipeline

read1=$1
read2=$2
sampleID=$3
database_folder=$4
output_folder=$5
min_thread=$6
midas_tax_db=$7

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
echo "running main reference based analysis process in the folder $DIR at $(date)"

if [ $read1 = -h ] ; then
	echo "Usage information: 1) read1 = Forward paired-end file (FASTQ) 2) read2 = Reverse paired-end file (FASTQ) 3) output_folder= Output folder path"
else 
	echo "starting pre-processing for reference-based pipeline at $(date)"
	
	
	
	
	
	log_preprocessing=$log_folder/preprocessing.log
	if [ -f "$log_preprocessing" ] ; then
		echo "$log_preprocessing exists. Skipping pre-processing"
	else
		echo "$log_preprocessing does not exist. Startin pre-processing at $(date)"
		echo "./preprocessing.sh $read1 $read2 $sampleID $min_thread $output_folder"
		$DIR/preprocessing.sh $read1 $read2 $sampleID $min_thread $output_folder
		touch $log_preprocessing
	fi
	echo "finished preprocessing of paired-end input files $(date). starting annotations now"
	echo ' '
        echo '###########################################################################################################'
        
	
	
        read1=$output_folder/${read1##*/}.filtered_1.fastq
        read2=$output_folder/${read2##*/}.filtered_2.fastq

	
	echo '###########################################################################################################'
		
	echo '###########################################################################################################'

        echo '###########################################################################################################'



	log_reference_pipeline=$log_folder/ref_species_genes_snps.log
	if [ -f "$log_reference_pipeline" ] ; then
		echo "$log_reference_pipeline exists. Skipping MIDAS annotation procedures..."
	else
		 echo "$log_reference_pipeline  does not exist."
		 echo "starting midas species, genes, snps procedures at $(date)..."
		 $DIR/ref_species_genes_snps.sh $read1 $read2 $min_thread $database_folder $output_folder
		 echo "reference pipeline is ready for annotations at $(date)"
		 touch $log_reference_pipeline
	fi

	echo 'starting annotation using PATRIC and mapping annotations with snps'
	echo ' '
        echo '###########################################################################################################'

	source activate $USER_ENV_NAME
	log_snp_annotation=$log_folder/snp_annotation.log
	if [ -f "$log_snp_annotation" ] ; then 
		echo "$log_snp_annotation exists. Skipping annotations"
	else
		echo "$log_snp_annotation does not exist. Starting SNP_annotation at $(date)"
		$DIR/ref_snp_annotation.sh $output_folder/MIDAS/genes/output $output_folder/MIDAS/genes/output $output_folder/MIDAS/snps/output $output_folder/REFERENCE_SNP_ANNOTATION
		echo "Finished annotations and mapping snps at $(date)."
		touch $log_snp_annotation
	fi
        echo ' '
        echo '###########################################################################################################'	
	source deactivate
	
	
	source activate $USER_ENV_NAME
        log_protein_annotation=$log_folder/protein_annotation.log
	
	if [ -f "$log_protein_annotation" ] ; then
                echo "$log_protein_annotation exists. Skipping annotations @ $(date) "
        else
                echo "$log_protein_annotation does not exist. Starting SNP_annotation at $(date)"
		$DIR/ref_protein_annotation.sh $output_folder/MIDAS/genes/output $output_folder/MIDAS/genes/output $output_folder/MIDAS/snps/output $output_folder/
		echo "Finished protein_annotaion at $(date)."
		touch $log_protein_annotation
	fi

	log_protein_annotation_post=$log_folder/protein_annotation_post.log

	if [ -f "$log_protein_annotation_post" ] ; then
		echo "$log_protein_annotation_post exists. No log creation @ $(date)"
	else
		echo "$log_protein_annotation_post does not exists. Log creation @ $(date)"
		echo "#### PROTEIN_ANNOTATION_LOG CREATED AT #### $(date)."
		touch $log_protein_annotation
	fi
		

	


	echo ' '
	echo '###########################################################################################################'
	source deactivate
fi
