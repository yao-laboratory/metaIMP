#imports
import pandas as pd 
import numpy as np
import os
import argparse

def go_all_file(reference_snp_output_folder,output_folder):
    list_of_species=os.listdir(reference_snp_output_folder)
    for dir in list_of_species:
        input_dir = os.path.join(reference_snp_output_folder, dir)
        if os.path.isdir(input_dir):
            print("dir is ::",dir)
            output_file_loc=os.path.join(output_folder,dir)
            #final_step5_file_loc=os.path.join(reference_snp_output_folder,dir,(str(dir)+"_patric_midassnps.csv"))
            #Edited by K.Sahu 06102022
            final_step5_file_loc=os.path.join(reference_snp_output_folder,dir,(str(dir)+"_reference_coding_Table_1.csv"))

            print(final_step5_file_loc)
            go_one_file(final_step5_file_loc,output_file_loc)
            
def go_one_file(final_step5_file_loc,output_file_loc):
    reference_mapping_file=pd.read_csv(final_step5_file_loc)
    temp_go_table = reference_mapping_file[['ref_id','gene_id','feature.go','coverage','count_reads']]
    temp_go_result = temp_go_table.groupby(['ref_id','gene_id','feature.go','coverage','count_reads']).size()
    temp_go_result = temp_go_result.to_frame().reset_index()
    temp_go_result.columns=['ref_id','gene_id','go','coverage','reads','num_of_mutation']
    
    ref_id_list=[]
    gene_id_list=[]
    go_list=[]
    coverage_list=[]
    reads_list=[]
    mutation_list=[]
    final_go_table = pd.DataFrame()
    for i in temp_go_result.index:
        ref_id=str(temp_go_result.loc[i]['ref_id'])
        gene_id=str(temp_go_result.loc[i]['gene_id'])
        coverage=float(temp_go_result.loc[i]['coverage'])
        reads=int(temp_go_result.loc[i]['reads'])
        mutation=int(temp_go_result.loc[i]['num_of_mutation'])

        go_number= str(temp_go_result.loc[i]['go'])
        go_number_split=go_number.split('::')

        for go in go_number_split:
            go_list.append(go)
            ref_id_list.append(ref_id)
            gene_id_list.append(gene_id)
            coverage_list.append(coverage)
            reads_list.append(reads)
            mutation_list.append(mutation)
            
    final_go_table['ref_id']=ref_id_list
    final_go_table['GO']=go_list
    final_go_table['gene_id']=gene_id_list
    final_go_table['coverage']=coverage_list
    final_go_table['reads']=reads_list
    final_go_table['num_of_mutations']=mutation_list
    
    go_table_name_ref=os.path.join(output_file_loc,"table_8_go_ref.csv")
    print("GO TABLE NAME IS:",go_table_name_ref)
    final_go_table.to_csv(str(go_table_name_ref), sep=",",index=None)
    

    final_go_table_gene = final_go_table.groupby(['gene_id','GO']).sum().reset_index()
    
    go_table_name_gene=os.path.join(output_file_loc,"table_8_go_gene.csv")
    print("GO TABLE NAME IS:",go_table_name_gene)
    final_go_table_gene.to_csv(str(go_table_name_gene), sep=",",index=None)
    
def main():
    parser = argparse.ArgumentParser(prog='step6_reference_based_ec_go', description='ec go tables')
    subparser = parser.add_subparsers(dest='subcommand',help='enter output folder path')

    go_parser = subparser.add_parser("go_map",help="This function creates the ec_go file")
    go_parser.add_argument("-i", dest="input_folder", type=str, help="final output folder as output")
    go_parser.add_argument("-o", dest="output_folder", type=str, help="final output folder")

    args = parser.parse_args()

    if args.subcommand=='go_map':
        reference_snp_output_folder = args.input_folder
        output_folder = args.output_folder
        print(reference_snp_output_folder, output_folder)
        go_all_file(reference_snp_output_folder,output_folder)

if __name__ == "__main__":
    main()

                           
