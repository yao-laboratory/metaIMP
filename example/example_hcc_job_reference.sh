#!/bin/bash
#SBATCH --job-name=hcc_reference
#SBATCH --nodes=1
#SBATCH --time=24:00:00
#SBATCH --mem=64gb
#SBATCH --output=hcc_reference.%J.out
#SBATCH --error=hcc_reference.%J.err


metaIMP_path=/home/yaolab/ksahu2/.ssh/metaIMP
export USER_ENV_NAME=metaimp_env

#Inputs- FASTQ/FASTA paired-end files
fastq1=/work/yaolab/shared/2021_milk_2017_metagenome/MIT_DATA/sample_SRR9205542/SRR9205542_1.fastq
fastq2=/work/yaolab/shared/2021_milk_2017_metagenome/MIT_DATA/sample_SRR9205542/SRR9205542_2.fastq

#output_folder_assembly path
output_folder_assembly=/work/yaolab/shared/2021_milk_2017_metagenome/MIT_DATA/sample_SRR9205542/assembly_output

#output_folder_reference path
output_folder_reference=/work/yaolab/shared/2021_milk_2017_metagenome/MIT_DATA/sample_SRR9205542/reference_output

#number of threads to be used by metaSPADES and Instrain
threads=8

#Minimum_contig_length for filtering. THIS IS OPTIONAL
con_len=1500


#user environment name
#env_var=$USER_ENV_NAME


#modules for assembly_binning.sh:

echo "loading modules for assembly_binning.sh"
module load python/3.8
module load spades/3.14
module load quast/5.0
module load bowtie/2.3
module load samtools/1.9
module load metabat2/2.15
module load checkm-genome/1.1

#modules for assembly_contig_annotation.sh:
echo "loading modules for assembly_contig_annotation.sh"
module load eggnog-mapper/2.1

#modules for assembly_snp_calling.sh:
module load instrain/1.3
export PYTHONNOUSERSITE=1




#echo ' '
#echo '###########################################################################################################'
#echo $metaIMP_path/main_assembly_processing.sh $fastq1 $fastq2 $output_folder_assembly $threads $con_len

#$metaIMP_path/main_assembly_processing.sh $fastq1 $fastq2 $output_folder_assembly $threads $con_len

#echo ' '
#echo '###########################################################################################################'






module purge
module load java
module load midas/1.3
module load samtools
module laod fastqc/0.11
database_folder=$MIDAS_DB

echo ' '
echo '###########################################################################################################'

echo $metaIMP_path/main_reference_processing.sh $fastq1 $fastq2 $database_folder $output_folder_reference $threads
$metaIMP_path/main_reference_processing.sh $fastq1 $fastq2 $database_folder $output_folder_reference $threads

echo ' '
echo '###########################################################################################################' 

