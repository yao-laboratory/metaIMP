#this script perfroms the following actions: 1) Assembly using MetaSPADES 2) Filter for minimum contig length (optional)
#       			             3) Quality using Quast
# 					     4) SAM and BAM file creation, sorting BAM file using BOWTIE and SAMTOOLS
#					     5) BINNING using MetaBAT 6) Genome quality using CHECKM
#
#
#STARTING ASSEMBLY_BINNING SCRIPT

#VARIABLES DEFINED HERE
#INPUTS ARE CALLED FROM ASSEMBLY_MAIN_SCRIPT
fastq1=$1
fastq2=$2
output=$3
t=$4
minimum_contig_len=$5

#METASPADES
#STARTING ASSEMBLY

echo 'spades python file called for 1st sample-reverse and forward read'
spades.py --meta --pe1-1 $fastq1 \
        --pe1-2 $fastq2 \
        -t $t \
        -o $output
echo 'finshed spades'

#DEFINE CONTIGS FILE IN contigs
contigs=$output/contigs.fasta


#OPTIONAL ARGUMENT FOR USER TO FILTER CONTIG

if [ $minimum_contig_len -gt 0 ] ; then
	./bbmap/reformat.sh in=$output/contigs.fasta out=$output/contigs.fasta minlength=$minimum_contig_len
fi

#QUAST QUALITY CHECK

echo 'starting quast'
quast.py $contigs -1 $fastq1 -2  $fastq2 -o $output/quast

#INDEXED CONTIG

echo 'Creating indexed contigs'
idc=$output/indexed_contigs/
bowtie2-build $contigs $idc
echo 'indexed contigs done'

#SAM FILE CREATION

echo 'starting SAM file creation'
sam_file=$output/smfile.sam
bowtie2 --threads $t -x $idc -1 $fastq1 -2 $fastq2 --no-unal -S $sam_file
echo 'finished creating sam file'

#SAMTOBAM conversion

echo 'starting SAM to BAM conversion'
bam_file=$output/bmfile.bam
echo 'touch bam file and change permission to global. also changed permission of SAM file to global'
samtools view -F 4 -bS $sam_file > $bam_file

#BAM FILE SORTING
echo 'bam sorting'
bam_sorted_file=$output/bmfile_sort.bam
samtools sort $bam_file -o $bam_sorted_file
rm $bam_file
echo 'finished bam sort.starting binning'

#BINNING
echo 'starting BINNING modules'
echo 'starting depth file creation'
depth_file=$output/depth.txt
jgi_summarize_bam_contig_depths --outputDepth $depth_file $bam_sorted_file
echo 'finished depth file creation'
echo 'starting binning'
bins=$output/bins/bins
metabat2 -i $contigs -a $depth_file -o $bins

#CHECKM
echo 'starting checkm'
c_bins=$output/bins
checkm=$output/bins/checkm
checkm lineage_wf -t $t -x fa $c_bins $checkm
mergedfile=$output/bins/checkm/bins
find $mergedfile  -type f -name '*.faa' -exec cat {} + >$mergedfile/mergedfile.fna

#ASSEMBLY_BINNING script is complete
echo 'assembly_binning step is complete'
