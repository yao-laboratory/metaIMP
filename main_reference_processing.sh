#!/bin/bash
#SBATCH --job-name=main_reference
#SBATCH --nodes=1
#SBATCH --time=12:00:00
#SBATCH --mem=8gb
#SBATCH --output=main_reference.%J.out
#SBATCH --error=main_reference%J.err


echo 'starting pre-processing for reference-based pipeline'

A=/work/yaolab/shared/2021_milk_2017_metagenome/MIT_DATA/sample_SRR9205533/SRR9205533_1.fastq
B=/work/yaolab/shared/2021_milk_2017_metagenome/MIT_DATA/sample_SRR9205533/SRR9205533_2.fastq

./preprocessing.sh $A $B

echo 'finished preprocessing of paired-end input files. starting annotations now'

A=/work/yaolab/shared/2021_milk_2017_metagenome/MIT_DATA/sample_SRR9205533/SRR9205533_1.fastq.filtered_1.fastq
B=/work/yaolab/shared/2021_milk_2017_metagenome/MIT_DATA/sample_SRR9205533/SRR9205533_2.fastq.filtered_2.fastq
C=/work/yaolab/shared/2021_milk_2017_metagenome/MIT_DATA/sample_SRR9205533/reference_pipeline

echo 'starting midas species, genes, snps procedures'
/home/yaolab/ksahu2/.ssh/metaIMP/ref_species_genes_snps.sh $C $A $B
echo 'reference pipeline is ready for annotations'

echo 'starting annotation using PATRIC and mapping annotations with snps'

/home/yaolab/ksahu2/.ssh/metaIMP/ref_snp_annotation.sh $C $C $C $C

echo 'finished annotations and mapping snps. Thank you!!!'










