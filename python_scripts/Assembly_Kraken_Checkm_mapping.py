"""
This program maps KRAKEN annotations to CHECKM BINS
ASSEMBLY-PROCESS
##############################################################################
"""

#imports
import pandas as pd
import os
import json

def kraken_checkm_mapping(checkm_stats, scaffold_information, step_5_mapping_result,path_of_the_directory):
    
    
    checkm_stats=pd.read_csv(checkm_stats,sep='\t',header=None)
    scaffold_information=pd.read_csv(scaffold_information,sep='\t',header=None)
    step_5_mapping_result=pd.read_csv(step_5_mapping_result)
    
    
    #renaming scaffold dataframe columns
    scaffold_information=scaffold_information.rename(columns={0: "contig", 1: "bin"})
    step_5_scaffold_mapping_df = pd.merge(scaffold_information, step_5_mapping_result, left_on='contig', right_on = 'location_x', how ='inner' )
    

    
    checkm_mapping_final_df= pd.DataFrame()
    #kraken_inter_df=pd.DataFrame()
    bins_list=list()
    stat_list=list()


    for i in checkm_stats.index:
        bins_list.append(checkm_stats.loc[i][0])
        dict_string=checkm_stats.loc[i][1]
        dict_string=dict_string.replace("\'","\"")
        a_dict=json.loads(dict_string)
        #print(a_dict)
        stat_list.append(a_dict)
    checkm_mapping_final_df=pd.DataFrame.from_records(stat_list)
    checkm_mapping_final_df['BINS']=bins_list
    #checkm_mapping dataframe is created
    #checkm_mapping_final_df[]=bins_list
    #heckm_mapping_final_df




    #stat_list
    #rough_work
    #print(checkm_stats.loc[0])
    #df['Hello']=bins_list
    #checkm_stats.loc[1][0]
    #bins_list


    #os.chdir(path_of_the_directory)

    onlyfiles = [f for f in os.listdir(path_of_the_directory) if os.path.isfile(os.path.join(path_of_the_directory, f)) and f.split(".")[-1]=='report']
    kraken_list=list()
    kraken_bin_list=list()
    for filename in onlyfiles:
        #print(filename)
        bin_id=filename.replace('.report','')
        kraken_bin_list.append(bin_id)
        df_kraken_report = pd.read_csv(os.path.join(path_of_the_directory,filename),sep='\t',header=None)
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
    kraken_inter_df['BINS']=kraken_bin_list

    checkm_mapping_final_df['Kraken_Annotation']=kraken_list
    
    binning_info_final_df = pd.merge(checkm_mapping_final_df, step_5_scaffold_mapping_df, left_on = 'BINS', right_on = 'bin',how='inner' )
    
    final_filename="Kraken_Checkm_assembly_mapping.csv"
    output_filename=os.path.join(path_of_the_directory,final_filename)
    binning_info_final_df.to_csv(output_filename, index = None)
   
#checkm_stats, scaffold_information, step_5_mapping_result,path_of_the_directory,output_filename
def main():
    parser = argparse.ArgumentParser(prog='step6_assembly_based_kraken_checkm_annotaion',description='this method executes the kraken checkm annotations')
    subparser = parser.add_subparsers(dest='subcommand',help ='Enter Kraken folder, Checkm_stats file')
    assembly_mapping_parser = subparser.add_parser("c_map",help="This function is to map bins with annotations")
    
    assembly_mapping_parser.add_argument("-c", dest="checkm_stats_file", type=str, help="checkm_stats_file eg./path/to/BINS/CHECKM/storage/bin_stats.analyze.tsv as input")
    assembly_mapping_parser.add_argument("-s", dest="scaffold_file", type=str, help="scaffold_file eg. /path/to/BINS/my_scaffolds2bin.tsv as input")
    assembly_mapping_parser.add_argument("-a", dest="assembly_mapping_file", type=str, 
                                         help="assembly_mapping_file obtained from step_5 as input eg. /path/to/ASSEMBLY_SNP_ANNOTATION/assembly_mapping_result.csv")
    assembly_mapping_parser.add_argument("-o", dest="output_file_path", type=str, help="output file path")
    
    args = parser.parse_args()
    
    if args.subcommand=='c_map':
        checkm_stats = args.checkm_stats_file
        scaffold_information = args.scaffold_file
        assembly_mapping_file = args.assembly_mapping_file
        output_filepath = args.output_file_path
        
        kraken_checkm_mapping(checkm_stats,scaffold_information,assembly_mapping_file,output_filepath)
    else:
        print("Wrong input. Check parameters")

if __name__ == "__main__":
    main()
    
    
