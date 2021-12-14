module load instrain/1.3
#module load python/3.6
#module load biopython/py27/1.74
export PYTHONNOUSERSITE=1

bms=$1
contigs=$2
op_folder=$3
threads=$4
mergefile=$5

inStrain profile $bms $contigs -o $op_folder -p $threads -g $mergedfile
