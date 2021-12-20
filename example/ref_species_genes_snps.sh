#this script executes MIDAS modules to identify metagenome species, genes and their mutations (snps)


echo 'starting midas'

fastq1=$1
fastq2=$2
output_folder=$3

run_midas.py species $output_folder \
        -1 $fastq1 \
        -2 $fastq2\
        -d $MIDAS_DB

echo 'midas_species complete'

run_midas.py genes $output_folder \
        -1 $fastq1 \
        -2 $fastq2\
        -d $MIDAS_DB

echo 'midas_genes complete'

run_midas.py snps $output_folder \
        -1 $fastq1 \
        -2 $fastq2\
        -d $MIDAS_DB

echo 'midas_snps complete'
