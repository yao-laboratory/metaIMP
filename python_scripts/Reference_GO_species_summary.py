#imports
import pandas as pd 
import numpy as np
import os
import argparse


def go_summary_map(reference_output_folder):
    path=reference_output_folder
    dir_list=next(os.walk(path))[1]

    species_list=list()
    final_species_go_sumarry=pd.DataFrame()

    for species in dir_list:
        this_species_list=species.rsplit('_',1)
        this_species_name = this_species_list[0]
        this_species_id = this_species_list[1]

        go_table_file=os.path.join(reference_output_folder,species,'table_8_go_gene.csv')

        #print(ec_table_file)

        go_file=pd.read_csv(go_table_file)
        num_rows=go_file.shape[0]
        go_file['species_name']=[this_species_name]*num_rows
        go_file['species_id']=[this_species_id]*num_rows


        #ec_file["species"]=" "
        #ec_file.loc[len(ec_file)]=this_species_list



        final_species_go_sumarry= final_species_go_sumarry.append(go_file,ignore_index = True)

    final_species_table=os.path.join(reference_output_folder,'go_summary_table.csv')
    final_species_go_sumarry.to_csv(str(final_species_table),sep=',',index=None)



def main():
    parser = argparse.ArgumentParser(prog='go_summary', description='go species summary tables')
    subparser = parser.add_subparsers(dest='subcommand',help='enter reference_snp_annotation output folder path')

    go_species_parser = subparser.add_parser("go_species_map",help="This function creates the go_summary file file")
    go_species_parser.add_argument("-i", dest="output_folder", type=str, help="reference_snp_annotation output folder")

    args = parser.parse_args()

    if args.subcommand=='ec_go_summary':
        reference_output_folder=args.output_folder
        print(reference_output_folder)
        go_summary_map(reference_output_folder)


if __name__ == "__main__":
    main()
