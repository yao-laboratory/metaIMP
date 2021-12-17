module load eggnog-mapper/2.1

echo 'starting eggnog'
mergedfile=$1
eggnog_output=$2
emapper.py -i $mergedfile -o $eggnog_output
