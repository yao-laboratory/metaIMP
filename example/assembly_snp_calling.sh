#THIS SCRIPT IDENTIFIES EXISTING SNPS PRESENT IN THE CONTIGS FILE POST-ASSEMBLY.
#THESE ARE THE FOLLOWING INPUTS TO THIS SCRIPT: 1) BMS - BAM SORTED FILE. THIS FILE WAS CREATED AFTER SORTING THE BAM FILE IN ASSEMBLY_BINNING.SH
#						2) CONTIGS- CONTIGS.FASTA FILE (ASSEMBLY_BINNING.SH)
#						3) OP_FOLDER - OUTPUT FOLDER PATH
#						4) THREADS - TOTAL NUMBER OF THREADS TO USE
#						5) MERGEDFILE- MERGEDFILE.FNA CREATED POST-CHECKM (ASSEMBLY_BINNING.SH)


echo 'starting instrain'

bms=$1
contigs=$2
op_folder=$3
threads=$4
mergefile=$5

inStrain profile $bms $contigs -o $op_folder -p $threads -g $mergedfile

echo 'finished instrain. ASSEMBLY_SNP_CALLING.sh complete'