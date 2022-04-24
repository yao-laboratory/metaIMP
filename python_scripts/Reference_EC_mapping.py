#imports
import pandas as pd 
import numpy as np
import os
import argparse

def ec_all_file(reference_snp_output_folder,output_folder):
    list_of_species=os.listdir(reference_snp_output_folder)
    for dir in list_of_species:
        if os.path.isdir(dir):
            print("dir is ::",dir)
            output_file_loc=os.path.join(output_folder,dir)
            final_step5_file_loc=os.path.join(reference_snp_output_folder,dir,(str(dir)+"_patric_midassnps.csv"))
            
            print(final_step5_file_loc)
            ec_one_file(final_step5_file_loc,output_file_loc)
            
def ec_one_file(final_step5_file_loc,output_file_loc):
    reference_mapping_file=pd.read_csv(final_step5_file_loc)
    temp_ec_table = reference_mapping_file[['ref_id','gene_id','feature.ec','coverage','count_reads']]
    temp_ec_result = temp_ec_table.groupby(['ref_id','gene_id','feature.ec','coverage','count_reads']).size()
    temp_ec_result = temp_ec_result.to_frame().reset_index()
    temp_ec_result.columns=['ref_id','gene_id','ec','coverage','reads','num_of_mutation']
    
    ref_id_list=[]
    gene_id_list=[]
    ec_list=[]
    coverage_list=[]
    reads_list=[]
    mutation_list=[]
    final_ec_table = pd.DataFrame()
    for i in temp_ec_result.index:
        ref_id=str(temp_ec_result.loc[i]['ref_id'])
        gene_id=str(temp_ec_result.loc[i]['gene_id'])
        coverage=float(temp_ec_result.loc[i]['coverage'])
        reads=int(temp_ec_result.loc[i]['reads'])
        mutation=int(temp_ec_result.loc[i]['num_of_mutation'])

        ec_number= str(temp_ec_result.loc[i]['ec'])
        ec_number_split=ec_number.split('::')

        for ec in ec_number_split:
            ec_list.append(ec)
            ref_id_list.append(ref_id)
            gene_id_list.append(gene_id)
            coverage_list.append(coverage)
            reads_list.append(reads)
            mutation_list.append(mutation)
            
    final_ec_table['ref_id']=ref_id_list
    final_ec_table['EC']=ec_list
    final_ec_table['gene_id']=gene_id_list
    final_ec_table['coverage']=coverage_list
    final_ec_table['reads']=reads_list
    final_ec_table['num_of_mutations']=mutation_list

    final_ec_table = final_ec_table.groupby(['ref_id','EC']).sum().reset_index()
    
    ec_table_name=os.path.join(output_file_loc,"table_7_ec.csv")
    print("GO TABLE NAME IS:",ec_table_name)
    final_ec_table.to_csv(str(ec_table_name), sep=",",index=None)
    
def main():
    parser = argparse.ArgumentParser(prog='step6_reference_based_ec_go', description='ec go tables')
    subparser = parser.add_subparsers(dest='subcommand',help='enter output folder path')

    ec_parser = subparser.add_parser("ec_map",help="This function creates the ec_go file")
    ec_parser.add_argument("-i", dest="input_folder", type=str, help="final output folder as output")
    ec_parser.add_argument("-o", dest="output_folder", type=str, help="final output folder")

    args = parser.parse_args()

    if args.subcommand=='ec_map':
        reference_snp_output_folder = args.input_folder
        output_folder = args.output_folder
        print(reference_snp_output_folder, output_folder)
        ec_all_file(reference_snp_output_folder,output_folder)

if __name__ == "__main__":
    main()

                           
