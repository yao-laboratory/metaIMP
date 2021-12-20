#this script is for pre-processing of paired-end fastq input files - forward and reverse

echo 'starting bbmap'
echo 'starting metaIMP test sequence v1'

input1=$1
input2=$2

file1=$input1
file2=$input2

OT1=$input1.filtered_1.fastq
OT2=$input2.filtered_2.fastq

temp1=$input1.temp_1.fastq
temp2=$input2.temp_2.fastq

echo 'finshing loading files'

bbmap_folder=./bbmap

echo 'starting adapters'

adapters=$bbmap_folder/resources/adapters.fa

echo 'finishing adapters'

echo 'starting phix_adapters'

phiX_adapters=$bbmap_folder/resources/phix174_ill.ref.fa.gz

echo 'finishing phix_adapters'

echo 'creating temp files'

$bbmap_folder/bbduk.sh -Xmx7g in1=$file1 in2=$file2 \
	out1=$temp1\
	out2=$temp2\
	minlen=10 qtrim=rl trimq=20 ktrim=r k=21 mink=11 ref=$adapters hdist=1 tbo tpe

echo 'finishing temp file creation'
echo 'starting filtered files'

$bbmap_folder/bbduk.sh \
	in1=$temp1 \
	in2=$temp2 \
	out1=$OT1 out2=$OT2 ref=$phiXadapters hdist=1 k=21 threads=8

echo 'finishing filtered files'