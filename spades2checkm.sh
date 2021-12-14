#spades

echo 'spade module load started'
module load spades/3.14
echo 'spade module load complete'


fastq1=$1
fastq2=$2
output=$3
t=$4


echo 'spades python file called for 1st sample-reverse and forward read'
spades.py --meta --pe1-1 $fastq1 \
        --pe1-2 $fastq2 \
        -t 32 \
        -o $output
echo 'finshed spades'


echo 'starting quast'

echo 'loading quast module'
module load quast/5.0
echo 'quast loaded. starting quast'

quast.py $contigs -1 $fastq1 -2  $fastq2 -o $output/quast


echo 'bowtie module load started'
module load bowtie/2.3
echo 'bowtie module loaded. starting bowtie conversion'
#contigs=$4
contigs=$output/contigs.fasta
idc=$output/indexed_contigs
bowtie2-build $contigs $idc
echo 'indexed contigs done'

echo ' starting job'
module load bowtie/2.3
echo 'finished loading bowtie module'

sam_file=$output/smfile.sam

bowtie2 --threads $t -x $idc -1 $fastq1 -2 $fastq2 --no-unal -S $sam_file
echo 'finished creating sam file'


echo 'starting SAM to BAM conversion'

echo 'loading SAMtools'
module load samtools/1.9

bam_file=$output/bmfile.bam
echo 'touch bam file and change permission to global. also changed permission of SAM file to global'


samtools view -F 4 -bS $sam_file > $bam_file

echo 'bam sorting'
module load samtools/1.9
bam_sorted_file=$output/bmfile_sort.bam


samtools sort $bam_file -o $bam_sorted_file
rm $bam_file

echo 'finished bam sort.starting binning'

echo 'loading module'
module load metabat2/2.15
echo 'finished loading module'

echo 'starting depth file creation'

depth_file=$output/depth.txt


jgi_summarize_bam_contig_depths --outputDepth $depth_file $bam_sorted_file

echo 'finished depth file creation'
echo 'starting binning'

bins=$output/bins/bins

metabat2 -i $contigs -a $depth_file -o $bins

#startingcheckm

echo 'loading module'

module load checkm-genome/1.1

echo 'finished loading module'

echo 'starting checkm'
c_bins=$output/bins
checkm=$output/bins/checkm

checkm lineage_wf -t $t -x fa $c_bins $checkm

mergedfile=$output/bins/checkm/bins

find $mergedfile  -type f -name '*.faa' -exec cat {} + >mergedfile.fna


