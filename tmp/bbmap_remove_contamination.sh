#This script is used to remove any contamination in metagenome fastq files.



#Download reference human genome "GRCh38_latest_genomic.fna.gz" from https://www.ncbi.nlm.nih.gov/genome/guide/human/
reference_file=/work/yaolab/shared/2023_Nebraska_Lake/GRCh38_latest_genomic.fna.gz
#define pathways for fastq files and clean version files
fastq1=./sample_SRR9205534/SRR9205534_1.fastq
fastq2=./sample_SRR9205534/SRR9205534_2.fastq
clean1=./R1-clean-test-v02.fastq.gz
clean2=./R2-clean-test-v02.fastq.gz

#define metaIMP path

metaIMP_bbmap_path=/home/yaolab/ksahu2/.ssh/metaIMP/bbmap/

$metaIMP_bbmap_path/bbmap.sh minid=0.9 maxindel=3 bandwidthratio=0.16 bandwidth=12 quickmatch fast minhits=2 \
    ref=$reference_file qtrim=r trimq=10 untrim usemodulo \
    printunmappedcount kfilter=25 maxsites=1 k=14 bloom in1=$fastq1 \
    in2=$fastq2  outu1=$clean1 outu2=$clean2
