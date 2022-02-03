#!/bin/bash
#SBATCH --job-name=saj_r_34
#SBATCH --nodes=1
#SBATCH --time=24:00:00
#SBATCH --mem=64gb
#SBATCH --output=saj_r_34.%J.out
#SBATCH --error=saj_r_34.%J.err

#SAJ_R: stand_alone_job_reference
#metaimp path: Repository downloaded by user from Github
metaIMP_path=/home/yaolab/ksahu2/.ssh/metaIMP/
export USER_ENV_NAME=metaimp_env

#Inputs- FASTQ/FASTA paired-end files
fastq1=/work/yaolab/ksahu2/sample_SRR9205534/SRR9205534_1.fastq
fastq2=/work/yaolab/ksahu2/sample_SRR9205534/SRR9205534_2.fastq

#output_folder_reference path
output_folder_reference=/work/yaolab/ksahu2/sample_SRR9205534/reference_output

#number of threads 
threads=8

#MIDAS database path
database_folder=/work/HCC/BCRF/app_specific/midas/1.3/MIDAS/midas_db_v1.2/

##############################################################
#USER DOES NOT NEED TO CHANGE ANYTHING FROM HERE
##############################################################

module purge

source activate $USER_ENV_NAME
echo ' '
echo '###########################################################################################################'

echo "$metaIMP_path/main_reference_processing.sh $fastq1 $fastq2 $database_folder $output_folder_reference $threads"
$metaIMP_path/main_reference_processing.sh $fastq1 $fastq2 $database_folder $output_folder_reference $threads

echo ' '
echo '###########################################################################################################' 
conda deactivate
