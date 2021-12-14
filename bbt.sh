#!/bin/bash
#SBATCH --job-name=bbt_118
#SBATCH --nodes=1
#SBATCH --time=168:00:00
#SBATCH --mem=10gb
#SBATCH --output=bbtool_118.%J.out
#SBATCH --error=bbtool_118.%J.err

module load java/12
echo 'starting bbmap'
echo 'starting metaIMP test sequence v1'

file1=/work/yaolab/shared/2021_milk_2017_metagenome/MIT_DATA/sample_SRR9205532/SRR9205532_1.fastq
file2=/work/yaolab/shared/2021_milk_2017_metagenome/MIT_DATA/sample_SRR9205532/SRR9205532_2.fastq

OT1=/work/yaolab/shared/2021_milk_2017_metagenome/MIT_DATA/sample_SRR9205532/SRR9205532_filtered_1.fastq
OT2=/work/yaolab/shared/2021_milk_2017_metagenome/MIT_DATA/sample_SRR9205532/SRR9205532_filtered_2.fastq


temp1=/work/yaolab/shared/2021_milk_2017_metagenome/MIT_DATA/sample_SRR9205532/SRR9205532_temp_1.fastq
temp2=/work/yaolab/shared/2021_milk_2017_metagenome/MIT_DATA/sample_SRR9205532/SRR9205532_temp_2.fastq
echo 'finshing loading files'


echo 'starting adapters'

adapters=/home/yaolab/shared/bbtools/bbmap/resources/adapters.fa


echo 'finishing adapters'

echo 'starting phix_adapters'

phiX_adapters=/home/yaolab/shared/bbtools/bbmap/resources/phix174_ill.ref.fa.gz


echo 'finishing phix_adapters'


echo 'creating temp files'

/home/yaolab/shared/bbtools/bbmap/bbduk.sh -Xmx7g in1=$file1 in2=$file2 \
	out1=$temp1\
	out2=$temp2\
	minlen=10 qtrim=rl trimq=20 ktrim=r k=21 mink=11 ref=$adapters hdist=1 tbo tpe



echo 'finishing temp file creation'


echo 'starting filtered files'

/home/yaolab/shared/bbtools/bbmap/bbduk.sh \
	in1=$temp1 \
	in2=$temp2 \
	out1=$OT1 out2=$OT2 ref=$phiXadapters hdist=1 k=21 threads=8

echo 'finishing filtered files'
