import Bio
import os
import argparse
import pandas as pd 
import gzip 

from Bio import SeqIO
from os import listdir
from os.path import isfile, join

#function to add the term 'figid|' to peg_id in genes/output folder.
def adding_figid(genes_path,patric_path):
    genes_path = (genes_path)
    
    os.chdir(genes_path)
    
    onlyfiles = [f for f in listdir(genes_path) if isfile(join(genes_path, f)) and f.split(".")[-1]=='gz']
    
    for i in range (0, len(onlyfiles)):
        #print(i,onlyfiles[i])
        filefullpath=join(genes_path, onlyfiles[i])
        df_peg_id = pd.read_csv(filefullpath,compression ='gzip',sep='\t')
        df_peg_id['gene_id'] = 'fig|' + df_peg_id['gene_id'].astype(str)
        realfilename = onlyfiles[i].replace(".genes.gz","")
        df_peg_id.to_csv(join(patric_path, realfilename + '.patric.csv'), index = None, sep = '\t')
            
            
#after adding fig_id, we call patric using the new file obtained from here. Once PATRIC is complete, we map the results to
#corresponding to the MIDAS_snps
#The filename will change from "Akkermansia_muciniphila_55290.patric.csv" to "Akkermansia_muciniphila_55290.feature.csv"
 
def reference_mapping(patric_path, midas_snps_path, output_path): #for looping
    

    
    patric_list = os.listdir(patric_path)
    species_list=list()
    for filename in patric_list:
        if filename.endswith(".feature.csv"):
            filename_without_extension = filename.replace(".feature.csv", "")
            species_list.append(filename_without_extension)
            
    for species in species_list:
        patric_filename = species+".feature.csv"
        snp_filename = species + ".snps.gz"
        
        patric_fullpath = join(patric_path, patric_filename)
        snp_fullpath = join(midas_snps_path, snp_filename)
    
        if os.path.exists(patric_fullpath)==False and os.path.exists(snp_fullpath)==False:
            continue
            
        print(species)
        output_fullpath_filename = join(output_path, species+"_patric_midassnps.csv")
        reference_mapping_for_one_data(patric_fullpath, snp_fullpath, output_fullpath_filename)


def reference_mapping_for_one_data(patric_fullpath_filename,midas_snp_fullpath_filename, output_fullpath_filename):
    patric_op = pd.read_csv(patric_fullpath_filename, sep="\t")
    midas_snps = pd.read_csv(midas_snp_fullpath_filename, sep="\t",compression ='gzip')

    if patric_op.shape[0] !=0:
        print(patric_fullpath_filename," is not empty, we continue processing")
        patric_op.rename(columns={'feature.accession':'ref_id'},inplace='True')
        mut_count= midas_snps[['count_a','count_c','count_g','count_t']].max(axis=1)
        count_equals = mut_count.eq(midas_snps['depth'])
        midas_snps['count_equals']= count_equals

        mutations = midas_snps['count_equals'].values == 0
        mutation_list = midas_snps[mutations]

        mutation_list=mutation_list.sort_values(by='ref_id', ascending=True)

        df_reference_final = pd.DataFrame([])
        patric_op_sub=pd.DataFrame([])

        pre_ref_id=""

        count=0
        for j in mutation_list.index:
            if count%100==0:
                print(count)
            count=count+1

            current_ref_id=mutation_list.loc[j]['ref_id']
            mutation_pos=mutation_list.loc[j]['ref_pos']
            a=mutation_list.loc[[j], :]


            if current_ref_id!=pre_ref_id:
                patric_op_sub=patric_op.loc[patric_op['ref_id']==current_ref_id]
                pre_ref_id=current_ref_id

            for i in patric_op_sub.index:
                start_pos=patric_op.loc[i]['feature.start']
                end_pos=patric_op.loc[i]['feature.end']
                if mutation_pos>=start_pos and mutation_pos<=end_pos:
                    b=patric_op.loc[[i], :]
                    newrow=pd.merge(a,b,on='ref_id',how='inner')
                    df_reference_final =pd.concat([df_reference_final,newrow],axis=0,ignore_index=True)
        #df_reference_final.to_csv(output_fullpath_filename, sep=",",index=None)
        #print('FINISH!!!!')

        metaimp_id_list = list()
        for i in df_reference_final.index:
            metaimp_id="MetaIMP_"+str(i+1)
            metaimp_id_list.append(metaimp_id)
            df_reference_final['MetaIMP_ID']=metaimp_id_list
        df_reference_final.to_csv(output_fullpath_filename, sep=",",index=None)
        print('FINISH!!!!')

    else:
        print(patric_fullpath,"this patric file is empty. skipping this file")






def reference_mapping_for_one_data_old(patric_fullpath_filename,midas_snp_fullpath_filename, output_fullpath_filename):
    patric_op = pd.read_csv(patric_fullpath_filename, sep="\t")
    midas_snps = pd.read_csv(midas_snp_fullpath_filename, sep="\t",compression ='gzip')
    if patric_op.shape[0] != 0:
        print(patric_fullpath_filename," is not empty, we continue processing")

        range_beginning = list()
        range_end = list()

        for i in range (0, len(patric_op['feature.location'])):
            range_beginning.append(patric_op['feature.location'][i].split('..')[0])
            range_end.append(patric_op['feature.location'][i].split('..')[1])

        #starting and ending position extracted

        patric_op['range_start'] = pd.Series(range_beginning)
        patric_op['range_end'] = pd.Series(range_end)


        mut_count= midas_snps[['count_a','count_c','count_g','count_t']].max(axis=1)
        count_equals = mut_count.eq(midas_snps['depth'])
        midas_snps['count_equals']= count_equals



        mutations = midas_snps['count_equals'].values == 0
        mutation_list = midas_snps[mutations]

        #mutation count calculated
        print("finished mutation count in midas_snps")


        patric_op['range_start'] = patric_op['range_start'].str.replace("(",' ',regex=True)
        patric_op['range_start'] = patric_op['range_start'].str.replace('complement',' ',regex=True)
        patric_op['range_start'] = patric_op['range_start'].str.replace(")",' ',regex=True)
        patric_op['range_end'] = patric_op['range_end'].str.replace(')',' ',regex=True)


        print("finished seperating range start and end positions")

        s = pd.Series(patric_op['feature.location'])
        comp_val = s.str.find('complement')
        patric_op['complement'] = comp_val


        #complement value is calculated

        node_length_start = patric_op[['range_start']].to_numpy()
        node_length_end = patric_op[['range_end']].to_numpy()
        patric_r_id = midas_snps[['ref_id']].to_numpy()

        r_pos=mutation_list[['ref_pos']].to_numpy()
        r_id = mutation_list[['ref_id']].to_numpy()
        r_pos_id = mutation_list[['ref_pos','ref_id']].to_numpy()

        #created final dataframe
        df_assembly_final = pd.DataFrame([],columns=mutation_list.columns.tolist()+patric_op.columns.tolist())

        map_complete = 'False'
        for i in range(0, len(patric_op.range_start)):
            if i%100==0:
                print(i)
            for j in range(0,len(mutation_list.ref_pos)):
                if r_id[j]== patric_r_id[i]:
                    if r_pos[j]>=node_length_start[i].astype(int) and r_pos[j]<=node_length_end[i].astype(int) :


                        #df_assembly_result=pd.concat([df_assembly_result,mutation_list.iloc[j:j+1]],ignore_index=True)

                        #df2=pd.concat([df2,patric_op.iloc[i:i+1]],ignore_index=True)
                        #newrow=pd.concat([mutation_list.iloc[j:j+1],patric_op.iloc[i:i+1]],axis=1)
                        a=mutation_list.iloc[j:j+1].reset_index(drop=True)
                        b=patric_op.iloc[i:i+1].reset_index(drop=True)
                        newrow=pd.concat([a,b],axis=1)
                        df_assembly_final =pd.concat([df_assembly_final,newrow],axis=0,ignore_index=True)

                    else:
                        map_complete = 'False'

        df_assembly_final.to_csv(output_fullpath_filename, sep=",",index=None)
        print('FINISH!!!!')

    else:
        print(patric_fullpath,"this patric file is empty. skipping this file")


def main():
    parser = argparse.ArgumentParser(prog='step5_reference_based', description='mapping snp from reference based method to annotation')
    subparser = parser.add_subparsers(dest='subcommand',help='select from two subcommands: add_figid, ref_map')

    add_figid_parser = subparser.add_parser("add_figid",help="This function is to add figid to the patric file")
    add_figid_parser.add_argument("-gf", dest="genes_folder", type=str, help="gene folder from midas as input")
    add_figid_parser.add_argument("-pf", dest="patric_folder",type=str, help="patric folder as output folder")


    ref_map_parser= subparser.add_parser("ref_map",help="This function is to map snp to annotations")
    ref_map_parser.add_argument("-pf", dest="patric_folder",type=str, help="patric folder as input folder")
    ref_map_parser.add_argument("-sf", dest="midas_snp_folder",type=str, help="midas snp folder as input folder")
    ref_map_parser.add_argument("-o", dest="output_csv_file_path",type=str, help="final output folder name for csv files ")


        #command_line="add_figid -gf /somefolder/ -pf /someoutputfolder/".split()

        #command_line="ref_map -pf /somefolder/ -sf /midasfolder/ -o filename.csv".split()

        #command_line = "-h".split()
        #command_line = "-h".split()
        #command_line = "ref_map -h".split()
        #print(command_line)
        #args = parser.parse_args(command_line)
    args = parser.parse_args()


    if args.subcommand=='add_figid':
        genes_path = args.genes_folder
        patric_path = args.patric_folder
        print(genes_path, patric_path)
        adding_figid(genes_path,patric_path)

    elif args.subcommand=='ref_map':
        patric_path = args.patric_folder
        midas = args.midas_snp_folder
        reference_ppln = args. output_csv_file_path
        print(patric_path, midas, reference_ppln)
        reference_mapping(patric_path,midas,reference_ppln)

if __name__ == "__main__":
        main()
