echo 'starting midas modules'

op_folder=$1
fastq1=$2
fastq2=$3

module purge
module load midas/1.3
module load samtools

run_midas.py species $op_folder \
        -1 $fastq1 \
        -2 $fastq2\
        -d $MIDAS_DB



echo 'midas_species complete'


run_midas.py genes $op_folder \
        -1 $fastq1 \
        -2 $fastq2\
        -d $MIDAS_DB

echo 'midas_genes complete'



run_midas.py snps $op_folder \
        -1 $fastq1 \
        -2 $fastq2\
        -d $MIDAS_DB
