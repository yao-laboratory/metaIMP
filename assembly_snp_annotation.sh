#This script runs the Assembly mapping between SNPS provided by INSTRAIN and ANNOTATIONS provided by EGGNOG
#Inputs are provided in MAIN_ASSEMBLY_PROCESSING.SH
#THERE ARE FOUR INPUTS TO THIS SCRIPT:  1) SNPS FILE/FOLDER PATH OBTAINED FROM INSTRAIN
#					2) ANNOTATIONS FILE/FOLDER PATH OBTAINED FROM EGGNOG
#					3) MERGEDFILE PATH OBTAINED FROM CHECKM BINNING (ASSEMBLY_BINNING.SH)
#					4) OUTPUT FOLDER PATH

instrain=$1
eggnog=$2
mergedfile=$3
output=$4
contigs=$5
path_to_kraken_dir=$6
scaffold_info=$7
checkm_stats=$8
if [ ! -d "$output" ] ; then
        mkdir $output
fi

DIR="${BASH_SOURCE[0]}"
DIR="$(dirname "$DIR")"

echo 'starting assembly mapping'
#cd ./python_scripts/
python $DIR/python_scripts/Assembly_mapping.py a_map -i $instrain -e $eggnog -m $mergedfile -o $output

echo 'assembly mapping complete'

imusage=$(free | awk '/Mem/{printf("RAM Usage: %.2f%\n Mbits"), $3/1000000}' |  awk '{print $3}' | cut -d"." -f1)
echo "Current Memory Usage for ${BASH_SOURCE[0]} is: $imusage MBits"

echo 'creating VCF assembly output file'
python $DIR/python_scripts/VCF_converter_assembly.py vcf_map_assembly -i $output/assembly_mapping_result.csv -o $output
echo 'VCF file created for assembly process'

echo 'starting amino acid mapping'
python $DIR/python_scripts/Assembly_AA_mapping.py aa_map -a $output/assembly_mapping_result.csv -v $output/assembly_mapping_result.vcf  -c $contigs -o $output
echo 'amino acid mapping complete'

echo "mapping Kraken annotations to bins"
echo "scaffold is $scaffold_info"
python $DIR/python_scripts/Assembly_Kraken_Checkm_mapping.py c_map -c $checkm_stats -s $scaffold_info -a $output/assembly_bin_table.csv -o $path_to_kraken_dir
echo "Kraken annotation-bin mapping complete"





