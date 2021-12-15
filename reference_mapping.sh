module load python/3.6

genes_folder=$1
patric_folder=$2
snps_folder=$3
output_folder=$4

echo 'this is reference based mapping'

cd /work/yaolab/shared/2021_milk_2017_metagenome/PIPELINE_TESTING/python_scripts/

python Reference_mapping.py -add_figid -gf $genes_fodler -pf $patric_folder

echo 'finished adding fig_ids to peg_ids. now run patric.sh first to get the annotation. then last step is to map the annotation with midas by running the ref_map command'


module load singularity/3.7
patric_directory=$1
cd $patric_directory

for f in *.patric.csv:
do
        echo 'we are now processing all genes files to which 'fig_id' tag is added and these files will now run through PATRIC DATABASE'
	echo 'currently processing'$f
        singularity exec docker://unlhcc/patric p3-get-feature-data --col=1 --attr aa_length --attr aa_sequence  --attr aa_sequence_md5 --attr accession --attr alt_locus_tag \
                --attr annotation --attr classifier_round --attr classifier_score --attr date_inserted --attr date_modified --attr ec --attr end --attr feature_id --attr feature_type \
                --attr figfam_id  --attr gene --attr gene_id --attr genome_id --attr genome_name --attr go --attr location --attr na_length --attr na_sequence --attr na_sequence_md5 \
                --attr notes --attr owner  --attr p2_feature_id --attr pathway --attr patric_id --attr pgfam_id --attr plfam_id --attr product --attr property --attr protein_id \
                --attr public --attr refseq_locus_tag --attr segments --attr sequence_id --attr start --attr strand --attr subsystem --attr taxon_id \
                --attr text --attr user_read --attr user_write --attr function \
                < f.patric.csv > f.feature.csv


echo 'completed mapping PEG_IDs to PATRIC'

python Reference_mapping.py -ref_map -pf $patric_folder -sf $snps_folder -o $output_folder

echo 'completed reference_mapping. Good luck!!!'

