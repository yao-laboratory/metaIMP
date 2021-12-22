#this script executes MIDAS modules to identify metagenome species, genes and their mutations (snps)


echo 'starting midas'

fastq1=$1
fastq2=$2
num_thread=$3
database_folder=$4
overall_output_folder=$5

output_folder=$overall_output_folder/MIDAS

run_midas.py species $output_folder \
        -1 $fastq1 \
        -2 $fastq2 \
	-t $num_thread \
        -d $database_folder

echo 'midas_species complete'

run_midas.py genes $output_folder \
        -1 $fastq1 \
        -2 $fastq2 \
	-t $num_thread \
        -d $database_folder

echo 'midas_genes complete'

run_midas.py snps $output_folder \
        -1 $fastq1 \
        -2 $fastq2 \
	-t $num_thread \
        -d $database_folder

echo 'midas_snps complete'
