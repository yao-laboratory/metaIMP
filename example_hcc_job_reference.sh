#!/bin/bash
#SBATCH --job-name=hcc_reference
#SBATCH --nodes=1
#SBATCH --time=2:00:00
#SBATCH --mem=20gb
#SBATCH --output=hcc_reference.%J.out
#SBATCH --error=hcc_reference.%J.err


metaIMP_path=/work/yaolab/shared/2022_05_metaIMP/Workshop_testing/metaIMP/
#export USER_ENV_NAME=ENV_SAMPLE
#kraken_db_path=/work/HCC/BCRF/app_specific/kraken/2.0
#export KRAKEN_DATABASE=$kraken_db_path
#phylophlan_db_name=SGB.Jan19
#export PHYLOPHLAN_DATABASE=$phylophlan_db_name
#Inputs- FASTQ/FASTA paired-end files
#output_folder_reference path
output_folder_reference=$PWD/reference_output_1_another_testin

fastq1=/work/yaolab/shared/2022_05_metaIMP/Workshop_testing/metaIMP/SRR9205542_1.fastq

fastq2=/work/yaolab/shared/2022_05_metaIMP/Workshop_testing/metaIMP/SRR9205542_2.fastq


sampleID=SRR9205542




MIDAS_DB=/work/HCC/BCRF/app_specific/midas/1.3/MIDAS/midas_db_v1.2/

#number of threads to be used by metaSPADES and Instrain
threads=2



###THIS IS THE END FOR USER###
echo -e " \n "
echo "###########################################################################################################"





module purge
module load java
module load midas/1.3
module load samtools/1.9
module load fastqc/0.11
#module load singularity/3.7
module load apptainer/1.1
#MIDAS_DB=/work/HCC/BCRF/app_specific/midas/1.3/MIDAS/midas_db_v1.2/
database_folder=$MIDAS_DB

echo " "
echo "###########################################################################################################"

echo "$metaIMP_path/main_reference_processing.sh $fastq1 $fastq2 $sampleID $database_folder $output_folder_reference $threads"
$metaIMP_path/main_reference_processing.sh $fastq1 $fastq2 $sampleID $database_folder $output_folder_reference $threads
echo " "
echo "###########################################################################################################"

