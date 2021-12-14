#!/bin/bash
#SBATCH --job-name=scpt145
#SBATCH --nodes=1
#SBATCH --time=108:00:00
#SBATCH --mem=500gb
#SBATCH --output=scpt145.%J.out
#SBATCH --error=scpt145%J.err


A=/work/yaolab/shared/2021_milk_2017_metagenome/MIT_DATA/sample_SRR9205532/SRR9205532_filtered_1.fastq
B=/work/yaolab/shared/2021_milk_2017_metagenome/MIT_DATA/sample_SRR9205532/SRR9205532_filtered_2.fastq
C=/work/yaolab/shared/2021_milk_2017_metagenome/MIT_DATA/sample_SRR9205532/spades
#D=/work/yaolab/shared/2021_milk_2017_metagenome/ATLAS_DATA/sample_SRR7691145/midas_op
t=8
#E=mergedfile.fna location
#F=eggnog_output_location
#G=contigs.fasta
#H=/work/yaolab/shared/2021_milk_2017_metagenome/ATLAS_DATA/sample_SRR7691145/spades_1208/smfile.sam
./spades2checkm.sh $A $B $C $t

#./midas_consolidated.sh $D $A $B

#wait

#./eggnog.sh $G $F

#wait

./sam2checkm.sh $H


