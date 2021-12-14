#!/bin/bash
#SBATCH --job-name=pat61439
#SBATCH --nodes=1
#SBATCH --time=48:00:00
#SBATCH --mem=96gb
#SBATCH --output=pat61439.%J.out
#SBATCH --error=pat61439%J.err




module load singularity/3.7

cd /work/yaolab/shared/2021_milk_2017_metagenome/uni_geneva_data/SRR12506343/midas_op/patric_testing


singularity exec docker://unlhcc/patric p3-get-feature-data --col=1 --attr aa_length --attr aa_sequence  --attr aa_sequence_md5 --attr accession --attr alt_locus_tag \
        --attr annotation --attr classifier_round --attr classifier_score --attr date_inserted --attr date_modified --attr ec --attr end --attr feature_id --attr feature_type \
        --attr figfam_id  --attr gene --attr gene_id --attr genome_id --attr genome_name --attr go --attr location --attr na_length --attr na_sequence --attr na_sequence_md5 \
        --attr notes --attr owner  --attr p2_feature_id --attr pathway --attr patric_id --attr pgfam_id --attr plfam_id --attr product --attr property --attr protein_id \
        --attr public --attr refseq_locus_tag --attr segments --attr sequence_id --attr start --attr strand --attr subsystem --attr taxon_id \
        --attr text --attr user_read --attr user_write --attr function \
        < Lachnospiraceae_bacterium_patric_op_61439.csv > Lachnospiraceae_bacterium_patric_op_final__61439.csv
