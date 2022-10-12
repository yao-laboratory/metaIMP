##THIS IS THE UPDATED VERSION OF METAIMP_ASSEMBLY_PROTEIN_ANNOTATION_MAPPING 
##Authors: Kalyan Sahu, Qiuming Yao
##Affiliation: Integrated Digital Omics Lab (IDOL), School of Computing, University of Nebraska-Lincoln

##UPDATE THIS
#This script runs the Assembly mapping between SNPS provided by INSTRAIN and ANNOTATIONS provided by EGGNOG
#Inputs are provided in MAIN_ASSEMBLY_PROCESSING.SH
##METAIMP_STEP_6
#THERE ARE FOUR INPUTS TO THIS SCRIPT:  1) SNPS FILE/FOLDER PATH OBTAINED FROM INSTRAIN
#                                       2) ANNOTATIONS FILE/FOLDER PATH OBTAINED FROM EGGNOG
#                                       3) MERGEDFILE PATH OBTAINED FROM CHECKM BINNING (ASSEMBLY_BINNING.SH)
#                                       4) OUTPUT FOLDER PATH
#					5) CONTIGS.FASTA FROM ASSEMBLY PROCESS


instrain=$1
eggnog=$2
mergedfile=$3
output=$4
contigs=$5
path_to_kraken_dir=$6
scaffold_info=$7
checkm_stats=$8
coverage_file=$9 #coverage file from bbwrap
main_output_folder=$10
sampleID=$11
step_5_mapping_results=$output/Table_1_assembly_mapping_result_coding.csv

if [ ! -d "$output" ] ; then
        mkdir $output
fi

DIR="${BASH_SOURCE[0]}"
DIR="$(dirname "$DIR")"



echo 'creating VCF assembly output file'
python $DIR/python_scripts/VCF_converter_assembly.py vcf_map_assembly -i $output/Table_1_assembly_mapping_result_coding.csv -o $output
echo 'VCF file created for assembly process'

echo 'starting amino acid mapping'
python $DIR/python_scripts/Assembly_AA_mapping.py aa_map -a $output/Table_1_assembly_mapping_result_coding.csv -v $output/Table_4_coding_Table_1_assembly_mapping_result_coding.vcf -c $contigs -o $output
echo 'amino acid mapping complete'

echo "mapping Kraken annotations to bins"
echo "scaffold is $scaffold_info"
python $DIR/python_scripts/Assembly_Complete_Bin_Table.py k_map -k $path_to_kraken_dir -c $scaffold_info -i $instrain -v $step_5_mapping_results -s $checkm_stats -e $coverage_file -o $output
echo "Kraken annotation-bin mapping complete"
echo "$DIR/python_scripts/Assembly_Complete_Bin_Table.py k_map -k $path_to_kraken_dir -c $scaffold_info -i $instrain -v $step_5_mapping_results -s $checkm_stats -e $coverage_file -o $output"

echo "python $DIR/python_scripts/Assembly_EC_calculation.py ec_map -i $instrain -e $eggnog -v $step_5_mapping_results -s $scaffold_info -k $path_to_kraken_dir -o $output"
echo "EC and GO tables"
python $DIR/python_scripts/Assembly_EC_calculation.py ec_map -i $instrain -e $eggnog -v $step_5_mapping_results -s $scaffold_info -k $path_to_kraken_dir -o $output
python $DIR/python_scripts/Assembly_GO_calculation.py go_map -i $instrain -e $eggnog -v $step_5_mapping_results -s $scaffold_info -k $path_to_kraken_dir -o $output
echo "EC + GO annotations ready"

echo "Bin_AA mapping py from DST and bins"
python $DIR/python_scripts/Assembly_bin_AA_mapping.py bin_aa_map -i $main_output_folder -s $sampleID
echo "python $DIR/python_scripts/Assembly_bin_AA_mapping.py bin_aa_map -i $main_output_folder -s $sampleID"
echo "Bin_AA mapping complete"
