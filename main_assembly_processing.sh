#!/bin/bash
#SBATCH --job-name=assembly
#SBATCH --nodes=1
#SBATCH --time=24:00:00
#SBATCH --mem=48gb
#SBATCH --output=assembly.%J.out
#SBATCH --error=assembly%J.err


A=/work/yaolab/shared/2021_milk_2017_metagenome/MIT_DATA/sample_SRR9205533/SRR9205533_1.fastq
B=/work/yaolab/shared/2021_milk_2017_metagenome/MIT_DATA/sample_SRR9205533/SRR9205533_2.fastq


echo'starting preprocessing'

/home/yaolab/ksahu2/.ssh/metaIMP/preprocessing.sh $A $B


echo 'completed pre-processing. starting assembly'

A=/work/yaolab/shared/2021_milk_2017_metagenome/MIT_DATA/sample_SRR9205533/SRR9205533_1.fastq.filtered_1.fastq
B=/work/yaolab/shared/2021_milk_2017_metagenome/MIT_DATA/sample_SRR9205533/SRR9205533_2.fastq.filtered_2.fastq
C=/work/yaolab/shared/2021_milk_2017_metagenome/MIT_DATA/sample_SRR9205533/error_corrected_fi/no_filt_1k
t=8
D=0

/home/yaolab/ksahu2/.ssh/metaIMP/assembly_binning.sh $A $B $C $t $D

mergedfile=$C/bins/checkm/bins/mergedfile.fna
annotation_results=$C/eggnog_output

/home/yaolab/ksahu2/.ssh/metaIMP/assembly_contig_annotation.sh $mergedfile $annotation_results

echo 'contig annotation complete. starting snp calling using instrain'


bam_sorted_file=$C/bmfile_sort.bam
contig=$C/contigs.fasta
snp_output=$C/instrain_results

/home/yaolab/ksahu2/.ssh/metaIMP/assembly_snp_calling.sh $bam_sorted_file $contig $snp_output $t $mergedfile

echo 'completed snp calling. starting assembly_snp_annotation'

instrain_file=$C/instrain_results/home/yaolab/ksahu2/.ssh/metaIMP/instrain_results/instrain_SNVs.tsv
annotation_file=$C/eggnog_output/eggnog_results.emapper.annotations

echo 'starting final mapping between snps and annotations'
assembly_snp_annotation=$C/snp_annotation
/home/yaolab/ksahu2/.ssh/metaIMP/assembly_snp_annotation.sh $instrain_file $annotation_file $mergedfile $assembly_snp_annotation


echo 'finished assembly pipeline with snp calling and annotations. SNPS and their annotations are mapped. Thank you!!!'
