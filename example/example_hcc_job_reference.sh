#!/bin/bash
#SBATCH --job-name=hcc_reference
#SBATCH --nodes=1
#SBATCH --time=24:00:00
#SBATCH --mem=64gb
#SBATCH --output=hcc_reference.%J.out
#SBATCH --error=hcc_reference.%J.err


metaIMP_path=/home/yaolab/ksahu2/.ssh/metaIMP
export USER_ENV_NAME=metaimp_env
#kraken_db_path=/work/HCC/BCRF/app_specific/kraken/2.0
#export KRAKEN_DATABASE=$kraken_db_path
#phylophlan_db_name=SGB.Jan19
#export PHYLOPHLAN_DATABASE=$phylophlan_db_name

#Inputs- FASTQ/FASTA paired-end files
fastq1=/work/yaolab/shared/2021_milk_2017_metagenome/MIT_DATA/sample_SRR9205542/SRR9205542_1.fastq
fastq2=/work/yaolab/shared/2021_milk_2017_metagenome/MIT_DATA/sample_SRR9205542/SRR9205542_2.fastq
sampleID=SRR9205542
#output_folder_reference path
output_folder_reference=/work/yaolab/shared/2021_milk_2017_metagenome/MIT_DATA/sample_SRR9205542/reference_output

#number of threads to be used by metaSPADES and Instrain
threads=8

echo " "
echo "###########################################################################################################"





module purge
module load java
module load midas/1.3
module laod fastqc/0.11
database_folder=$MIDAS_DB

echo " "
echo "###########################################################################################################"

echo "$metaIMP_path/main_reference_processing.sh $fastq1 $fastq2 $sampleID $database_folder $output_folder_reference $threads"
$metaIMP_path/main_reference_processing.sh $fastq1 $fastq2 $sampleID $database_folder $output_folder_reference $threads

echo " "
echo "###########################################################################################################"

