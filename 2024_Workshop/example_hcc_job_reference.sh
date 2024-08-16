#!/bin/bash


metaIMP_path=$HOME/metaIMP/
output_folder_reference=$HOME/metaIMP/2024_Workshop/2024_Workshop_day1/reference_output

fastq1=$HOME/metaIMP/2024_Workshop/2024_Workshop_day1/data/reference_R1.fastq

fastq2=$HOME/metaIMP/2024_Workshop/2024_Workshop_day1/data/reference_R2.fastq


sampleID=testreferencesample

#number of threads to be used by metaSPADES and Instrain
threads=1

##############################################################
#USER DOES NOT NEED TO CHANGE ANYTHING FROM HERE
##############################################################


MIDAS_DB=/work/HCC/BCRF/app_specific/midas/1.3/MIDAS/midas_db_v1.2/



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

