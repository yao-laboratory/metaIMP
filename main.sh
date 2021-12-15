#!/bin/bash
#SBATCH --job-name=assembly_main
#SBATCH --nodes=1
#SBATCH --time=12:00:00
#SBATCH --mem=8gb
#SBATCH --output=assembly_main.%J.out
#SBATCH --error=assembly_main%J.err


A=/work/yaolab/shared/2021_milk_2017_metagenome/MIT_DATA/sample_SRR9205533/SRR9205533_1.fastq
B=/work/yaolab/shared/2021_milk_2017_metagenome/MIT_DATA/sample_SRR9205533/SRR9205533_2.fastq

./preprocessing.sh $A $B


#C=/work/yaolab/shared/2021_milk_2017_metagenome/MIT_DATA/sample_SRR9205532/spades
#D=/work/yaolab/shared/2021_milk_2017_metagenome/ATLAS_DATA/sample_SRR7691145/midas_op

#t=8


#E=mergedfile.fna location
#F=eggnog_output_location
#G=contigs.fasta
#H=/work/yaolab/shared/2021_milk_2017_metagenome/ATLAS_DATA/sample_SRR7691145/spades_1208/smfile.sam
#./spades2checkm.sh $A $B $C $t

#./midas_consolidated.sh $D $A $B

#wait

#./eggnog.sh $G $F

#wait

#./sam2checkm.sh $H


