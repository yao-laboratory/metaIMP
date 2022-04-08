##THIS IS THE UPDATED VERSION OF METAIMP_ASSEMBLY_MAPPING ( Step-5 )
##Authors: Kalyan Sahu, Qiuming Yao
##Affiliation: Integrated Digital Omics Lab (IDOL), School of Computing, University of Nebraska-Lincoln

#imports
import pandas as pd
import os
import json
import functools
from functools import reduce
import argparse
pd.options.mode.chained_assignment = None  # default='warn'

def checkm_mapping(path_of_the_directory, instrain_snvs, step_5_mapping_result, checkm_stats, scaffold_information, output):
    path_of_the_directory= (path_of_the_directory)
    #this path saves the kraken_report folder to loop through all Kraken files
    
    instrain_snvs=pd.read_csv(instrain_snvs,sep='\t')
    step_5_mapping_result=pd.read_csv(step_5_mapping_result)
    checkm_stats=pd.read_csv(checkm_stats,sep='\t',header=None)
    scaffold_information=pd.read_csv(scaffold_information,sep='\t',header=None)
    scaffold_information=scaffold_information.rename(columns={0: "contig", 1: "bin"})
    
    groups_instrain=instrain_snvs.groupby('scaffold').size()
    groups_instrain_df=groups_instrain.to_frame().reset_index()
    groups_instrain_df.columns=['scaffold','total_mutation_count_instrain']
    
    groups_step_5_mapping_result=step_5_mapping_result.groupby(['scaffold']).size()
    group_step_5_mapping_result=groups_step_5_mapping_result.to_frame().reset_index()
    group_step_5_mapping_result.columns=['scaffold','total_mutation_count_step5']
      
    #checkm_stats
    checkm_mapping_final_df= pd.DataFrame()
    bins_list=list()
    stat_list=list()

    #instrain_snvs
    groups_instrain=instrain_snvs.groupby('scaffold').size()
    groups_instrain_df=groups_instrain.to_frame().reset_index()
    groups_instrain_df.columns=['scaffold','total_mutation_count_by_instrain']

    #scaffold_info
    scaffold_information=scaffold_information.rename(columns={0: "contig", 1: "bin"})
    groups_step_5_mapping_result=step_5_mapping_result.groupby(['scaffold']).size()
    group_step_5_mapping_result=groups_step_5_mapping_result.to_frame().reset_index()
    group_step_5_mapping_result.columns=['scaffold','total_mutation_count_by_metaIMP']


    #merge scaffold_info and instrain_snvs dataframes
    instrain_snvs_comparison_df=pd.merge(groups_instrain_df,group_step_5_mapping_result,on = 'scaffold')
    bin_scaffold_info=pd.merge(instrain_snvs_comparison_df,scaffold_information,left_on='scaffold', right_on='contig',copy=False)

    #groupby bin for scaffold info
    new_bin_scaffold_info_grouped=bin_scaffold_info.groupby(['bin']).sum()

    #creating checkm_final dataframe
    for i in checkm_stats.index:
        bins_list.append(checkm_stats.loc[i][0])
        dict_string=checkm_stats.loc[i][1]
        dict_string=dict_string.replace("\'","\"")
        a_dict=json.loads(dict_string)
        stat_list.append(a_dict)
    checkm_mapping_final_df=pd.DataFrame.from_records(stat_list)
    checkm_mapping_final_df['bin']=bins_list


    os.chdir(path_of_the_directory)

    onlyfiles = [f for f in os.listdir(path_of_the_directory) if os.path.isfile(os.path.join(path_of_the_directory, f)) and f.split(".")[-1]=='report']
    kraken_list=list()
    kraken_bin_list=list()
    for filename in onlyfiles:
        #print("filename is"+str(filename))
        bin_id=filename.replace('.report','')
        #print("bin_id is"+str(bin_id))
        #print("path of dir is :"+str(path_of_the_directory))
        kraken_bin_list.append(bin_id)
        #take kraken_report_fullpath with filename
        kraken_report_file_fullpath=os.path.join(path_of_the_directory,filename)
        
        #check if kraken_file is empty
        if os.path.getsize(kraken_report_file_fullpath) > 0:
            df_kraken_report = pd.read_csv(kraken_report_file_fullpath),sep='\t',header=None)
            df_kraken_report.columns=['a','b','c','Notion','e','Description']

            new_annotation_list=list()
            for i in df_kraken_report.index:
                species_id=df_kraken_report.loc[i]['e']
                species_name=df_kraken_report.loc[i]['Description'].strip()
                new_annotation=(species_id, species_name)
                new_annotation_list.append(new_annotation)
            df_kraken_report['New_annotation']=new_annotation_list

            df_kraken_report=df_kraken_report.loc[df_kraken_report['a']>=80]
            kraken_dict=df_kraken_report.set_index('Notion')['New_annotation'].to_dict()
            kraken_list.append(kraken_dict)

    kraken_inter_df=pd.DataFrame.from_records(kraken_list)
    kraken_inter_df['bin']=kraken_bin_list

    final_merge_dfs= [kraken_inter_df, checkm_mapping_final_df, bin_scaffold_info]
    df_kraken_checkm_annotation = reduce(lambda left,right: pd.merge(left,right,on='bin'), final_merge_dfs)
    
    output=os.path.join(output, 'Table_6_Assembly_protein_information.csv')
    df_kraken_checkm_annotation.to_csv(output, index= None)
    
def main():
    parser = argparse.ArgumentParser(prog='META_IMP_assembly_based',description='this method executes Kraken annotation mapping with CHECKM-Prodigal protein inforamtion')
    subparser = parser.add_subparsers(dest='subcommand',help ='Enter the following files: 1) Scaffold_information 2) Instrain_SNVS 3) Assemnly_based_mapping_result 4) Checkm_stats')
    
    kraken_assembly_mapping_parser = subparser.add_parser("k_map",help="This function is to map snps with annotations")
    kraken_assembly_mapping_parser.add_argument("-k", dest="path_of_the_directory", type=str, help='path to kraken results')
    kraken_assembly_mapping_parser.add_argument("-c", dest="scaffold_information", type=str, help="eggnog file eg. /path/to/my_scaffolds2bin.tsv as input")
    kraken_assembly_mapping_parser.add_argument("-i", dest="instrain_snvs", type=str, help="instrain file eg./path/to/instrain_SNVs.tsv as input")
    kraken_assembly_mapping_parser.add_argument("-v", dest="step_5_mapping_result", type=str, 
                                         help="step_5_mapping_result obtained from metaIMP as input eg. /path/to/assembly_mapping.csv")
    kraken_assembly_mapping_parser.add_argument("-s", dest="checkm_stats", type=str, help='checkm stats file eg. /path/to/BINS/CHECKM/storage/bin_stats.analyze.tsv')
    kraken_assembly_mapping_parser.add_argument("-o", dest="output", type=str, help="output file path")
    
    args = parser.parse_args()
    
    if args.subcommand=='k_map':
        path_of_the_directory=args.path_of_the_directory  #kraken_dir
        instrain_snvs=args.instrain_snvs
        step_5_mapping_result=args.step_5_mapping_result
        checkm_stats=args.checkm_stats
        scaffold_information=args.scaffold_information
        output=args.output
        checkm_mapping(path_of_the_directory, instrain_snvs, step_5_mapping_result, checkm_stats, scaffold_information, output)
        
    else:
        print("Wrong input. Check parameters")

if __name__ == "__main__":
    main()
    
    
    
    
    
    

    
    
    
    
