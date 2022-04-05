##THIS IS THE UPDATED VERSION OF METAIMP_ASSEMBLY_MAPPING 
##Authors: Kalyan Sahu, Qiuming Yao
##Affiliation: Integrated Digital Omics Lab (IDOL), School of Computing, University of Nebraska-Lincoln


#imports
import pandas as pd 
import numpy as np
import os


def assembly_go_calculation(eggnog_file, scaffold_file, step_5_mapping_result, path_of_the_directory, instrain_snvs, output):
    eggnong_file=pd.read_csv(eggnog_file, sep ='\t', skiprows =  2, header =2, skipfooter= 3, engine='python')
    scaffold_file=pd.read_csv(scaffold_information,sep='\t',header=None)
    step_5_mapping_result=pd.read_csv(step_5_mapping_result)
    instrain_snvs=pd.read_csv(instrain_snvs,sep='\t')
    path_of_the_directory= (path_of_the_directory)
    
    final_go_table = pd.DataFrame()
    checkm_mapping_final_df= pd.DataFrame()


    protein_id_list= list()
    contig_list_eggnog_for_go = list()
    go_number_split_list=list()

    #scaffold_info renamed
    scaffold_information=scaffold_information.rename(columns={0: "contig", 1: "bin"})
    
    #getting species information from kraken
    os.chdir(path_of_the_directory)

    onlyfiles = [f for f in os.listdir(path_of_the_directory) if os.path.isfile(os.path.join(path_of_the_directory, f)) and f.split(".")[-1]=='report']
    kraken_list=list()
    kraken_bin_list=list()
    for filename in onlyfiles:
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
    kraken_inter_df['bin']=kraken_bin_list
    for i in eggnog_df.index:    

        go_number= str(eggnog_df.loc[i]['GOs'])
        go_number_split=go_number.rsplit(',')
        go_number_split_list=go_number_split_list+go_number_split  
        protein_id=str(eggnog_df.loc[i]['#query'])
        contig_id=protein_id.rsplit('_',1)[0]


        for i in range(0, len(go_number_split)):
            contig_list_eggnog_for_go.append(contig_id)
            protein_id_list.append(protein_id)
            
            
    final_go_table['contig']=contig_list_eggnog_for_go
    final_go_table['GO']=go_number_split_list
    final_go_table['protein_id']=protein_id_list
    final_go_table['GO'].replace('-', np.nan, inplace=True)
    final_go_table.dropna(subset=['GO'], inplace=True)
    
    bin_contig_info_df = pd.merge(final_go_table,scaffold_information,how='left',on='contig')
    bin_species_info_df = pd.merge(bin_contig_info_df, kraken_inter_df,how='left', on ='bin')
    
    step_5_mutataion=step_5_mapping_result.groupby(['#query']).size()
    step_5_mutataion_df=step_5_mutataion.to_frame().reset_index()
    step_5_mutataion_df.columns=['protein_id','total_mutation_in_metaIMP']
    
    final_go_table_assembly= pd.merge(bin_species_info_df,step_5_mutataion_df,how='left',on='protein_id')
    final_go_table_assembly['total_mutation_in_metaIMP'] = final_go_table_assembly['total_mutation_in_metaIMP'].fillna(int(0))
    final_go_table_assembly = final_go_table_assembly.astype({"total_mutation_in_metaIMP": int})
    
    coverage_list=list()

    for i in final_go_table_assembly.index:
        contig_id=final_go_table_assembly.loc[i]['contig']
        coverage=contig_id.rsplit('_')
        coverage_list.append(float(coverage[-1]))

    final_go_table_assembly['cov']=coverage_list 
    final_go_table=os.path.join(output,'Assembly_GO_table.csv')
    final_go_table_assembly.to_csv(output,index=None)
    
def main():
    parser = argparse.ArgumentParser(prog='step6_assembly_based',description='this method creates GO table')
    subparser = parser.add_subparsers(dest='subcommand',help ='enter the eggnog, instrain file names, kraken_annotation and scaffold file')
    
    assembly_go_parser=subparser.add_parser("go_map",help="This function is to map GO number with annotations")
    
    #assembly_mapping_parser.add_argument("-i", dest="instrain_file", type=str, help="instrain file eg./path/to/instrain_SNVs.tsv as input")
    
    assembly_go_parser.add_argument("-i", dest="instrain_file", type=str, help="instrain file eg./path/to/instrain_SNVs.tsv as input")
    
    assembly_go_parser.add_argument("-e", dest="eggnog_file", type=str, help="eggnog file eg./path/to/instrain_SNVs.tsv as input")
    
    assembly_go_parser.add_argument("-v", dest="step_5_mapping_result", type=str, 
                                         help="step_5_mapping_result obtained from metaIMP as input eg. /path/to/assembly_mapping.csv")
    
    assembly_go_parser.add_argument("-s", dest="scaffold_file", type=str, help=" eg. /path/to/my_scaffolds2bin.tsv as input")
    assembly_go_parser.add_argument("-k", dest="path_of_the_directory", type=str, help='path to kraken results')
    assembly_go_parser.add_argument("-o", dest="output", type=str, help="output file path")
    
    args = parser.parse_args()
    
    if args.subcommand=='go_map':
        eggnog_file=args.eggnog_file
        scaffold_file=args.scaffold_file
        step_5_mapping_result=args.step_5_mapping_result
        path_of_the_directory=args.path_of_the_directory
        instrain_snvs=args.instrain_file
        output=args.output
        
    else:
        print("Wrong input. Check parameters")
        
if __name__ == "__main__": 
    main()    
