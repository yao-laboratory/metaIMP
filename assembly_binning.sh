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
overall_output_folder=$3
t=$4
minimum_contig_len=$5


DIR="${BASH_SOURCE[0]}"
DIR="$(dirname "$DIR")"

#METASPADES
#STARTING ASSEMBLY
output=$overall_output_folder/METASPADES
if [ ! -d "$output" ] ; then
        mkdir $output
fi


echo "spades python file called for 1st sample-reverse and forward read"
spades.py --meta --pe1-1 $fastq1 \
        --pe1-2 $fastq2 \
        -t $t \
        -o $output
echo "finshed spades"

#DEFINE CONTIGS FILE IN contigs
contigs=$output/contigs.fasta


#OPTIONAL ARGUMENT FOR USER TO FILTER CONTIG

if [ $((minimum_contig_len+0)) -gt 0 ] ; then
	mv $contigs $output/rawcontigs.fasta
	$DIR/bbmap/reformat.sh in=$output/rawcontigs.fasta out=$output/contigs.fasta minlength=$minimum_contig_len
fi

#QUAST QUALITY CHECK

echo "starting quast"
quast.py $contigs -1 $fastq1 -2  $fastq2 -o $overall_output_folder/QUAST

#INDEXED CONTIG

echo "Creating indexed contigs"
idc=$output/indexed_contigs/
mkdir $idc

bowtie2-build $contigs $idc/indexed_contigs
echo "indexed contigs done"

#SAM FILE CREATION

echo "starting SAM file creation"
sam_file=$output/contig_mapping.sam
bowtie2 --threads $t -x $idc/indexed_contigs -1 $fastq1 -2 $fastq2 --no-unal -S $sam_file
echo "finished creating sam file"

#SAMTOBAM conversion

echo "starting SAM to BAM conversion"
bam_file=$output/contig_mapping.bam
samtools view -F 4 -bS $sam_file > $bam_file

#BAM FILE SORTING
echo "bam sorting"
bam_sorted_file=$output/contig_mapping_sort.bam
samtools sort $bam_file -o $bam_sorted_file

echo "finished bam sort.starting binning"

rm $sam_file
rm $bam_file

#BINNING
echo "starting BINNING modules"
echo "starting depth file creation"
depth_file=$output/depth.txt
jgi_summarize_bam_contig_depths --outputDepth $depth_file $bam_sorted_file
echo "finished depth file creation"
echo "starting binning"
binfolder=$overall_output_folder/BINS
if [ ! -d "$binfolder" ] ; then
        mkdir $binfolder
fi


bins=$binfolder/bins

#checking for mininmum_contig_length. If user provides value, use that. Else set minimum_contig_length as 1000bp.
#to get binned and unbinned contigs
if [ $((minimum_contig_len+0)) -gt 1500 ] ; then
	metabat2 -i $contigs -a $depth_file -o $bins -m $minimum_contig_len --seed 1 --unbinned
else
	metaIMP_min_contig_len = 1500
	metabat2 -i $contigs -a $depth_file -o $bins -m $metaIMP_min_contig_len --seed 1 --unbinned

fi

#CHECKM
echo "starting checkm"
c_bins=$binfolder

checkm=$binfolder/CHECKM
if [ ! -d "$checkm" ] ; then
        mkdir $checkm
fi

checkm lineage_wf -t $t -x fa $c_bins $checkm
mergedfile=$checkm/bins
find $mergedfile  -type f -name '*.faa' -exec cat {} + >$mergedfile/mergedfile.fna

#ASSEMBLY_BINNING script is complete
echo "assembly_binning step is complete"

imusage=$(free | awk '/Mem/{printf("RAM Usage: %.2f%\n Mbits"), $3/1000000}' |  awk '{print $3}' | cut -d"." -f1)
echo "Current Memory Usage for ${BASH_SOURCE[0]} is: $imusage MBits"
