#!/bin/bash
#SBATCH --job-name=saj_a_34
#SBATCH --nodes=1
#SBATCH --time=24:00:00
#SBATCH --mem=96gb
#SBATCH --ntasks-per-node=8
#SBATCH --output=saj_a_34.%J.out
#SBATCH --error=saj_a_34.%J.err

#SAJ:stand_alone_job_assembly

#metaimp path: Repository downloaded by user from Github
metaIMP_path=/home/yaolab/ksahu2/.ssh/metaIMP/
#create user environment
export USER_ENV_NAME=metaimp_env
#Kraken database path
kraken_db_path=/work/HCC/BCRF/app_specific/kraken/2.0
export KRAKEN_DATABASE=$kraken_db_path
#Phylophlan database path
phylophlan_db_name=SGB.Jan19
export PHYLOPHLAN_DATABASE=$phylophlan_db_name
#Eggnog database path
eggnog_db_name=/work/HCC/BCRF/app_specific/eggnog-mapper/2.1.3
export EGGNOG_DIAMOND_DATABASE=$eggnog_db_name
#export eggnog_db_name=$EGGNOG_DIAMOND_DATABASE

#Inputs- FASTQ/FASTA paired-end files
fastq1=/work/yaolab/ksahu2/sample_SRR9205534/SRR9205534_1.fastq
fastq2=/work/yaolab/ksahu2/sample_SRR9205534/SRR9205534_2.fastq
sampleID=SRR9205534
#output_folder_assembly path
output_folder_assembly=/work/yaolab/ksahu2/sample_SRR9205534/assembly_output

#number of threads to be used by metaSPADES and Instrain
threads=8

#Minimum_contig_length for filtering. THIS IS OPTIONAL
con_len=1000


##############################################################
#USER DOES NOT NEED TO CHANGE ANYTHING FROM HERE
##############################################################

export PYTHONNOUSERSITE=1

source activate $USER_ENV_NAME
echo '###########################################################################################################'
echo "$metaIMP_path/main_assembly_processing.sh $fastq1 $fastq2 $sampleID $output_folder_assembly $threads $con_len"
$metaIMP_path/main_assembly_processing.sh $fastq1 $fastq2 $sampleID $output_folder_assembly $threads $con_len

echo '###########################################################################################################'
conda deactivate
