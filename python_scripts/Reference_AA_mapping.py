"""
This program maps mutations in nucleotide sequence to mutations in corresponding amino acid sequence

#REFERENCE-PROCESS
##############################################################################
"""

#imports
import pandas as pd
import math
import Bio
#import skbio
import os
import argparse

from Bio import SeqIO
from Bio.SeqIO import parse
#from skbio import DNA

#functions for calculation
def complement(base):
	""" Complement nucleotide """
	d = {'A':'T', 'T':'A', 'G':'C', 'C':'G'}
	if base in d: return d[base]
	else: return base

def rev_comp(seq):
	""" Reverse complement sequence """
	return(''.join([complement(base) for base in list(seq[::-1])]))


def translate(codon):
    codon=codon.upper()
    codontable = {
    'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',
    'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
    'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',
    'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',
    'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
    'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
    'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',
    'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
    'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
    'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
    'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
    'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
    'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
    'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
    'TAC':'Y', 'TAT':'Y', 'TAA':'*', 'TAG':'*',
    'TGC':'C', 'TGT':'C', 'TGA':'*', 'TGG':'W',
    }
    if codon in codontable:
        return codontable[str(codon)]
    elif codon.find('N')!=-1:
        possible_na=['A','T','C','G']
        possible_aa=''
        for na in possible_na:
            possible_codon=codon.replace("N",na)
            current_aa=codontable[str(possible_codon)]
            if possible_aa=='':
                possible_aa=current_aa
            if possible_aa==current_aa:
                continue
            else:
                return '-'
        return possible_aa
    else:
        return '-'

'''
def translate(codon):
	""" Translate individual codon """
	codontable = {
	'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',
	'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
	'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',
	'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',
	'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
	'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
	'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',
	'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
	'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
	'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
	'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
	'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
	'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
	'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
	'TAC':'Y', 'TAT':'Y', 'TAA':'*', 'TAG':'*',
	'TGC':'C', 'TGT':'C', 'TGA':'*', 'TGG':'W',
	}
	return codontable[str(codon)]

'''
def translate_gene(gene_seq):
    protein_seq=""
    number_of_condons=math.floor(len(gene_seq)/3)
    for i in range(0,number_of_condons):
        condon_seq=gene_seq[3*i:3*i+3]
        aa = translate(condon_seq)
        protein_seq=protein_seq+aa
    return protein_seq

#calcuate mutation position in amino acid
def calculate_mutation_aa(ref_na, alt_na, mutation_na_pos, gene_na):
    #in this code, all positions are one-based
    #mutation_na_pos=5
    #ref_na='A'
    #alt_na='G'
    ref_aa=''
    alt_aa=''
    #print(ref_na)
    #print(alt_na)
    #print(mutation_na_pos)
    #print(gene_na)
    
   
    #if alt_na.find(',')>0:
    #    alt_na_split=alt_na.split(',')
    #    print('this is the split alt_na',alt_na_split[0],alt_na_split[1])
       # print(alt_na_split[1])
   

    '''
    if alt_na.find(",")>0:
        alt_na_first=alt_na[0]
        alt_na_second=alt_na[2]
        print(alt_na_first)
        print(alt_na_second)

    '''

    codon_num=math.ceil(mutation_na_pos/3)
    na_start=3*codon_num-2
    na_end=na_start+2
    ref_codon = gene_na[na_start-1:na_end]

    if gene_na[mutation_na_pos-1]==ref_na:
        new_gene=gene_na[0:mutation_na_pos-1]+alt_na+gene_na[mutation_na_pos:]
        alt_codon = new_gene[na_start-1:na_end]
        ref_aa=translate(ref_codon)
        alt_aa=translate(alt_codon)
    #return ref_aa, alt_aa,codon_num
    
    if len(ref_codon) < 3:
        print(ref_codon)
        print(gene_na)
        print(alt_codon)
    
    return ref_aa, alt_aa, codon_num
    

def amino_acid_all_files(reference_snp_annotation_folder, output_path):
    path=reference_snp_annotation_folder
    dir_list=next(os.walk(path))[1]
    #print(path)
    #print(output_path)
    print(" HI THIS IS PRINTING FOR NEW FUNCTION \n ")
    print(" &&&&********************************&&&&&&&&&&&&&&*************&&&&&&&&&&&& \n ")
    

    for species in dir_list:
        #folder_name=dir_list[species]
        folder_name=species
        
        print("FOLDER NAME IS HERE \n")
        print(folder_name)

        abs_folder_name=os.path.join(output_path,folder_name)

        
        reference_mapping_result=os.path.join(abs_folder_name,folder_name+"_patric_midassnps.csv")
        print("***********************")
        print("\n \n \n")
        print("THIS IS REFERENCE MAPPING RESULT FILE:", reference_mapping_result)
        paired_vcf_file_path=os.path.join(abs_folder_name,folder_name+"_patric_midassnps.vcf")
        amino_acid_mapping(reference_mapping_result,paired_vcf_file_path,abs_folder_name)
        

        print("THIS IS THE ABSOLUTE FOLDER PATH \n")
        print(abs_folder_name)
        print("THIS IS THE NEW AMINO ACID MAPPING CODE")
        #filename=os.path.join

        #print("THIS SPECIES IS IS DONE:"+ species)
        
        '''
        split_filename=filename.split('.')
        if split_filename[1]=='csv':
            if split_filename[0].find("_patric_midassnps")>0:
                species_id = split_filename[0].replace("_patric_midassnps","")
                #print(species_id)
                reference_mapping_result=os.path.join(reference_snp_annotation_folder,species_id+"_patric_midassnps.csv")
                vcf_file_name=split_filename[0]+".vcf"
                paired_vcf_file_path=os.path.join(reference_snp_annotation_folder,vcf_file_name)
                #print(paired_vcf_file_path)
                amino_acid_mapping(reference_mapping_result,paired_vcf_file_path,output_path)
        '''



def amino_acid_all_files_old(reference_snp_annotation_folder, output_path):
    #print(reference_snp_annotation_folder)
    #print(output_path)
    snp_annotation_files_list=os.listdir(reference_snp_annotation_folder)
    
    for i in range (0, len(snp_annotation_files_list)):
        #filename=str(snp_annotation_files_list[i])
        #print(filename)
        #split_filename=filename.split_filename('.')
        #split_filename=string.split_filename('.')
        #print(filename)
        filename=snp_annotation_files_list[i]
        #split_filename=string.split_filename('.')
        split_filename=filename.split('.')
        if split_filename[1]=='csv':
            if split_filename[0].find("_patric_midassnps")>0:
                species_id = split_filename[0].replace("_patric_midassnps","")
                print(species_id)
                reference_mapping_result=os.path.join(reference_snp_annotation_folder,species_id+"_patric_midassnps.csv")
                vcf_file_name=split_filename[0]+".vcf"
                paired_vcf_file_path=os.path.join(reference_snp_annotation_folder,vcf_file_name)
                print(paired_vcf_file_path)
                amino_acid_mapping(reference_mapping_result,paired_vcf_file_path,output_path)
        
        



def amino_acid_mapping(reference_final_result, vcf, aa_final_output):
    #get reference_mapping_final_results
    reference_mapping_result=pd.read_csv(reference_final_result)
    #print("REFERNCE_MAPPING_RESULT FILENAME:"+reference_mapping_result)
    vcf_file=pd.read_csv(vcf, sep='\t', skiprows=17)#,comment="##")
    reference_merged_df=pd.merge(reference_mapping_result,vcf_file,on='MetaIMP_ID')
    aa_df=pd.DataFrame([])
    
    reference_id_list=list()
    strand_list= list()
    ec_number_list= list()
    go_number_list=list()
    description_list=list()
    genome_name_list=list()
    alt_aa_list = list()
    #alt_aa_list_second= list()
    ref_aa_list = list()
    alt_na_list=list()
    ref_na_list=list()
    na_sequence_list=list()
    aa_sequence_list=list()
    metaimp_id_list=list()
    protein_mutation_pos_list=list()
    gene_mutation_pos_list=list()
    

    for i in reference_merged_df.index:
        na_seq_patric=reference_merged_df.loc[i]['feature.na_sequence'].upper()
        protein_seq_converted=translate_gene(na_seq_patric)
        #aa_seq_patric=reference_merged_df.loc[i]['feature.aa_sequence'].upper()

        #all positions from MIDAS and Patric are 1-based
        start_pos=int(reference_merged_df.loc[i]['feature.start'])
        end_pos=int(reference_merged_df.loc[i]['feature.end'])
        mutation_na_pos=int(reference_merged_df.loc[i]['ref_pos'])
        ref_na_letter=reference_merged_df.loc[i]['REF']
        alt_na_letter_string=reference_merged_df.loc[i]['ALT'] #can be 'A', or two letters 'A,T'
        reference_id=reference_merged_df.loc[i]['ref_id']
        strand= reference_merged_df.loc[i]['feature.strand']
        ec_number= reference_merged_df.loc[i]['feature.ec']
        go_number=reference_merged_df.loc[i]['feature.go']
        description=reference_merged_df.loc[i]['feature.product']
        genome_name=reference_merged_df.loc[i]['feature.genome_name']
        metaimp_id = reference_merged_df.loc[i]['MetaIMP_ID']
 

        
    
    
        alt_na_split_list=alt_na_letter_string.split(',')
        for alt_na_letter in alt_na_split_list:
            # print('this is the split alt_na',alt_na_split[0],alt_na_split[1])
            if reference_merged_df.loc[i]['feature.strand']=='+':
                #protein_seq_converted=translate_gene(na_seq_patric)
                mutation_pos=mutation_na_pos-start_pos
                mutation_pos=mutation_pos+1
                ref_aa,alt_aa,mutated_protein_pos=calculate_mutation_aa(ref_na_letter, alt_na_letter, mutation_pos, na_seq_patric)
                #ref_aa,alt_aa_second=calculate_mutation_aa(ref_na_letter, alt_na_letter, mutation_pos, na_seq_patric)
                alt_aa_list.append(alt_aa)
                ref_aa_list.append(ref_aa)
                protein_mutation_pos_list.append(mutated_protein_pos)
                alt_na_list.append(alt_na_letter)
                ref_na_list.append(ref_na_letter)
                gene_mutation_pos_list.append(mutation_pos)
            
            elif reference_merged_df.loc[i]['feature.strand']=='-':
                #new_na_rev_seq=rev_comp(na_seq_patric)#MIDAS provides the reverse complement sequence
                #protein_seq_converted=translate_gene(new_na_rev_seq)

                mutation_pos=end_pos-mutation_na_pos
                mutation_pos=mutation_pos+1

                ref_na_letter_rev=rev_comp(ref_na_letter)
                alt_na_letter_rev=rev_comp(alt_na_letter)
                ref_aa,alt_aa,mutated_protein_pos=calculate_mutation_aa(ref_na_letter_rev, alt_na_letter_rev, mutation_pos, na_seq_patric)
                alt_aa_list.append(alt_aa)
                ref_aa_list.append(ref_aa)
                protein_mutation_pos_list.append(mutated_protein_pos)
                alt_na_list.append(alt_na_letter)
                ref_na_list.append(ref_na_letter)
                gene_mutation_pos_list.append(mutation_pos)

         
            #print(len(protein_seq_converted))
            if protein_seq_converted[-1]!='*'  or protein_seq_converted.count('*')>1:
                aa_sequence_list.append('')
            else:
                aa_sequence_list.append(protein_seq_converted)

            reference_id_list.append(reference_id)
            strand_list.append(strand)
            ec_number_list.append(ec_number)
            go_number_list.append(go_number)
            description_list.append(description)
            genome_name_list.append(genome_name)
            na_sequence_list.append(na_seq_patric)
            #aa_sequence_list.append(protein_seq_converted)
            metaimp_id_list.append(metaimp_id)

    #please make this aa_df dataframe as output
    
    

    aa_df['Ref_ID']=reference_id_list
    aa_df['Genome_Name']=genome_name_list
    aa_df['Description']=description_list
    aa_df['EC']=ec_number_list
    aa_df['GO']=go_number_list
    aa_df['Gene_seq']=na_sequence_list
    aa_df['Protein_seq']=aa_sequence_list
    aa_df['ALT_AA']=alt_aa_list
    aa_df['REF_AA']=ref_aa_list
    aa_df['MetaIMP_ID']=metaimp_id_list
    aa_df['Protein Mutation Position (1-based)']=protein_mutation_pos_list    
    aa_df['Gene Mutation Position (1-based)']=gene_mutation_pos_list
    aa_df['ALT_NA']=alt_na_list
    aa_df['REF_NA']=ref_na_list
        

    final_reference_AA = os.path.join(aa_final_output,'AA_mapping.csv')
    aa_df.to_csv(final_reference_AA,index=None)        

def main():
    
    parser = argparse.ArgumentParser(prog='step6_reference_based',description='this method executes the reference based amino acid mapping')
    subparser = parser.add_subparsers(dest='subcommand',help ='enter the outputfilepath')
    
    aa_file_parser = subparser.add_parser("aa_map_reference", help = "This function outputs reference based results with their corresponding AA mutations")
    aa_file_parser.add_argument("-i",dest="reference_mapping_files_folder", type=str, help= 'reference based input folder containing all csv files eg./path/to/REFERENCE_SNP_ANNOTATION')
    aa_file_parser.add_argument("-o",dest="aa_file_path", type=str, help= 'output file destination eg./path/to/OUTPUT_FOLDER')
    
    args = parser.parse_args()
    if args.subcommand=='aa_map_reference':
        reference_files=args.reference_mapping_files_folder
        output_files=args.aa_file_path
        print(reference_files,output_files)
        amino_acid_all_files(reference_files, output_files)
    else:
        print("Wrong input. Check parameters")
    
if __name__ == "__main__":
        main()
