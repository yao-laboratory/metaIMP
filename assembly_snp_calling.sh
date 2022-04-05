#THIS SCRIPT IDENTIFIES EXISTING SNPS PRESENT IN THE CONTIGS FILE POST-ASSEMBLY.
#THESE ARE THE FOLLOWING INPUTS TO THIS SCRIPT: 1) BMS - BAM SORTED FILE. THIS FILE WAS CREATED AFTER SORTING THE BAM FILE IN ASSEMBLY_BINNING.SH
#						2) CONTIGS- CONTIGS.FASTA FILE (ASSEMBLY_BINNING.SH)
#						3) OP_FOLDER - OUTPUT FOLDER PATH
#						4) THREADS - TOTAL NUMBER OF THREADS TO USE
#						5) MERGEDFILE- MERGEDFILE.FNA CREATED POST-CHECKM (ASSEMBLY_BINNING.SH)


echo 'starting instrain...'

bms=$1
contigs=$2
op_folder=$3
threads=$4
mergedfile=$5
scaffold2bin=$6

echo "inStrain profile $bms $contigs -o $op_folder -p $threads -g $mergedfile"

inStrain profile $bms $contigs -o $op_folder -p $threads -g $mergedfile -s $scaffold2bin

echo 'finished instrain. ASSEMBLY_SNP_CALLING.sh complete'

imusage=$(free | awk '/Mem/{printf("RAM Usage: %.2f%\n Mbits"), $3/1000000}' |  awk '{print $3}' | cut -d"." -f1)
echo "Current Memory Usage for ${BASH_SOURCE[0]} is: $imusage MBits"
