#imports
import pandas as pd 
import numpy as np
import os
import argparse


def ec_summary_map(reference_output_folder):
    path=reference_output_folder
    dir_list=next(os.walk(path))[1]

    species_list=list()
    final_species_ec_sumarry=pd.DataFrame()

    for species in dir_list:
        this_species_list=species.rsplit('_',1)
        this_species_name = this_species_list[0]
        this_species_id = this_species_list[1]


        ec_table_file=os.path.join(reference_output_folder,species,'table_7_ec_gene.csv')

        ec_file=pd.read_csv(ec_table_file)
        num_rows=ec_file.shape[0]
        ec_file['species_name']=[this_species_name]*num_rows
        ec_file['species_id']=[this_species_id]*num_rows

        final_species_ec_sumarry= final_species_ec_sumarry.append(ec_file,ignore_index = True)
    
    final_species_table=os.path.join(reference_output_folder,'ec_summary_table.csv')
    print("THIS IS THE FINAL SPECIES TABLE PATH FOR EC_SUmMARY.py \n \n ")
    print(final_species_table)
    final_species_ec_sumarry.to_csv(str(final_species_table),sep=',',index=None)




def main():
    parser = argparse.ArgumentParser(prog='ec_summary', description='ec species summary tables')
    subparser = parser.add_subparsers(dest='subcommand',help='enter reference_snp_annotation output folder path')

    ec_species_parser = subparser.add_parser("ec_species_map",help="This function creates the ec_summary file file")
    ec_species_parser.add_argument("-i", dest="output_folder", type=str, help="reference_snp_annotation output folder")

    args = parser.parse_args()

    if args.subcommand=='ec_summary':
        reference_output_folder=args.output_folder
        print(reference_output_folder)
        ec_summary_map(reference_output_folder)


if __name__ == "__main__":
    main()
