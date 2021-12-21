#!/bin/bash
#SBATCH --job-name=main
#SBATCH --nodes=1
#SBATCH --time=24:00:00
#SBATCH --mem=96gb
#SBATCH --output=main.%J.out
#SBATCH --error=main.%J.err


metaIMP_path=/home/yaolab/ksahu2/.ssh/metaIMP
export USER_ENV_NAME=metaimp_env


#Inputs- FASTQ/FASTA paired-end files
fastq1=/work/yaolab/shared/2021_milk_2017_metagenome/MIT_DATA/sample_SRR9205538/SRR9205538_1.fastq
fastq2=/work/yaolab/shared/2021_milk_2017_metagenome/MIT_DATA/sample_SRR9205538/SRR9205538_2.fastq

#output_folder_assembly path
output_folder_assembly=/work/yaolab/shared/2021_milk_2017_metagenome/MIT_DATA/sample_SRR9205538/assembly_output

#output_folder_reference path
output_folder_reference=/work/yaolab/shared/2021_milk_2017_metagenome/MIT_DATA/sample_SRR9205537/reference_output

#create output directory for reference pipeline
mkdir $output_folder_reference

#number of threads to be used by metaSPADES and Instrain
threads=8

#Minimum_contig_length for filtering. THIS IS OPTIONAL
con_len=1500

#user environment name
env_var=$USER_ENV_NAME


#modules for assembly_binning.sh:

echo "loading modules for assembly_binning.sh"
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

echo ' '
echo '###########################################################################################################'
echo $metaIMP_path/main_assembly_processing.sh $fastq1 $fastq2 $output_folder_assembly $threads $con_len $env_var
#/home/yaolab/ksahu2/.ssh/metaIMP
$metaIMP_path/main_assembly_processing.sh $fastq1 $fastq2 $output_folder_assembly $threads $con_len $env_var

mkdir $output_folder_assembly/temp

module purge
module load midas/1.3
module load samtools

#create output directory for reference pipeline
mkdir $output_folder_reference


echo ' '
echo '###########################################################################################################'

echo $metaIMP_path/main_reference_processing.sh $fastq1 $fastq2 $output_folder_reference $env_var
$metaIMP_path/main_reference_processing.sh $fastq1 $fastq2 $output_folder_reference $env_var

echo ' '
echo '###########################################################################################################'

mkdir $output_folder_reference/temp
