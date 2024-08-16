#!/bin/bash


#Example HCC Assembly job
#metaimp path: Repository downloaded by user from Github
metaIMP_path=$HOME/metaIMP/
#Inputs- FASTQ/FASTA paired-end files
fastq1=$HOME/metaIMP/2024_Workshop/2024_Workshop_day1/data/assembly_R1.fastq
fastq2=$HOME/metaIMP/2024_Workshop/2024_Workshop_day1/data/assembly_R2.fastq
output_folder_assembly=$HOME/metaIMP/2024_Workshop/2024_Workshop_day1/assembly_output

sampleID=testassembly
threads=1

#Minimum_contig_length for filtering. THIS IS OPTIONAL
con_len=1000


##############################################################
#USER DOES NOT NEED TO CHANGE ANYTHING FROM HERE
##############################################################

#Kraken database path
kraken_db_path=/work/HCC/BCRF/app_specific/kraken/2.0
export KRAKEN_DATABASE=$kraken_db_path
#Phylophlan database path
phylophlan_db_name=SGB.Jan19
export PHYLOPHLAN_DATABASE=$phylophlan_db_name
#Eggnog database path
eggnog_db_name=/work/HCC/BCRF/app_specific/eggnog-mapper/2.1.3
export EGGNOG_DIAMOND_DATABASE=$eggnog_db_name

#modules for assembly_contig_annotation.sh:
module purge
module load megahit/1.1
module load quast/5.0
module load bowtie/2.3
module load samtools/1.9
module load metabat2/2.15
module load checkm-genome/1.1
module load fastqc/0.11
module load kraken2/2.0.8-beta
module load das_tool/1.1
module load usearch/11.0
module load phylophlan/3.0
#modules for assembly_contig_annotation.sh:
echo "loading modules for assembly_contig_annotation.sh"
module load eggnog-mapper/2.1
#modules for assembly_snp_calling.sh:
module load instrain/1.3
export PYTHONNOUSERSITE=1
PATH=/util/opt/anaconda/deployed-conda-envs/packages/instrain/envs/instrain-1.3.7/bin:$PATH

echo " "
assembly_mode=3
echo "assembly mode is $assembly_mode"
echo "###########################################################################################################"
echo "$metaIMP_path/main_assembly_processing.sh $fastq1 $fastq2 $sampleID $output_folder_assembly $threads $con_len $assembly_mode"
$metaIMP_path/main_assembly_processing_new.sh $fastq1 $fastq2 $sampleID $output_folder_assembly $threads $con_len $assembly_mode

echo " "
echo "###########################################################################################################"

