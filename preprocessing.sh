#!/bin/bash
#this script is for pre-processing of paired-end fastq input files - forward and reverse

echo 'starting bbmap'
echo "starting metaIMP test sequence v1 at $(date)"
DIR="${BASH_SOURCE[0]}"
DIR="$(dirname "$DIR")"

input1=$1
input2=$2
sampleID=$3
num_thread=$4
output_folder=$5

file1=$input1
file2=$input2






OT1=$output_folder/${input1##*/}.filtered_1.fastq
OT2=$output_folder/${input2##*/}.filtered_2.fastq

temp1=$output_folder/${input1##*/}.temp_1.fastq
temp2=$output_folder/${input2##*/}.temp_2.fastq

echo "finshing loading files at $(date)"

bbmap_folder=$DIR/bbmap

echo "starting adapters at $(date)"

adapters=$bbmap_folder/resources/adapters.fa

echo "finishing adapters at $(date)"

echo "starting phix_adapters at $(date)"

phiX_adapters=$bbmap_folder/resources/phix174_ill.ref.fa.gz

echo "finishing phix_adapters at $(date)"


echo "rename the fastq files readid $(date)"



echo "finishing the rename procedure $(date)"

Rename_OT_1=$output_folder/${input1##*/}.renamed_1.fastq
Rename_OT_2=$output_folder/${input2##*/}.renamed_2.fastq

#prefix=${input1#*_}

$bbmap_folder/rename.sh in=$file1 in2=$file2 out=$Rename_OT_1 out2=$Rename_OT_2 prefix=$sampleID



echo "creating temp files at $(date)"

$bbmap_folder/bbduk.sh -Xmx7g in1=$Rename_OT_1 in2=$Rename_OT_2 \
	out1=$temp1\
	out2=$temp2\
	minlen=10 qtrim=rl trimq=20 ktrim=r k=21 mink=11 ref=$adapters hdist=1 threads=$num_thread tbo tpe

echo "finishing temp file creation at $(date)"
echo "starting filtered files at $(date)"

$bbmap_folder/bbduk.sh \
	in1=$temp1 \
	in2=$temp2 \
	out1=$OT1 out2=$OT2 ref=$phiXadapters hdist=1 k=21 threads=$num_thread

echo "finishing filtered files at $(date)"


# FASTQC

echo "starting fastqc at $(date)"

ftqc=$output_folder/FASTQC
if [ ! -d "$ftqc" ] ; then
	mkdir $ftqc
fi

fastqc -o $ftqc -t $num_thread  $OT1
fastqc -o $ftqc -t $num_thread  $OT2

echo "finishing fastqc at $(date)"

imusage=$(free | awk '/Mem/{printf("RAM Usage: %.2f%\n Mbits"), $3/1000000}' |  awk '{print $3}' | cut -d"." -f1)
echo "Current Memory Usage for ${BASH_SOURCE[0]} is: $imusage MBits"
