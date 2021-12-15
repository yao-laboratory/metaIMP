module load eggnog-mapper/2.1
module load python/3.6

echo 'starting eggnog'
mergedfile=$1
egg_op=$2
emapper.py -i $mergedfile -o $2
