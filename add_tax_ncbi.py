import tax
import string


# fix for amoebas
tax.taxid2rank[554915] = 'phylum' #Amoebozoa
tax.taxid2rank[33634] = 'kingdom' #Stramenopiles
tax.taxid2rank[33630] = 'kingdom' #Alveolata

tax.taxid2rank[1137986] = 'phylum' #Mortierellomycotina
tax.taxid2rank[193537] = 'kingdom' #Centroheliozoa
tax.taxid2rank[136419] = 'class' #Cercozoa 
tax.taxid2rank[543769] = 'kingdom' #Rhizaria

tax.taxid2rank[555392] = 'order' #Dactylopodida
tax.taxid2rank[1485085] = 'class' #Flabellinia 
tax.taxid2rank[555280] = 'phylum' #Discosea
tax.taxid2rank[554915] = 'kingdom' #Amoebozoa

tax.taxid2rank[33634] = 'kingdom' #Stramenopiles
tax.taxid2rank[4762] = 'class' #Oomycetes
tax.taxid2rank[33154] = 'kingdom' #Opisthokonta 
tax.taxid2rank[2763] = 'phylum'#Rhodophyta
tax.taxid2rank[554296] = 'kingdom' # Apusozoa 


otu_table=open('/exports/projects/msc_students_2014/ljingyun/bioblitz/RBGEBioBlitz_merged_l_u_s_c99_m2_otus_r_nx.otu_table.txt')
marker_blast=open('all_filtered_markerblast.txt')	


# populate the otu table
otu_dict = {}
for line in otu_table.readlines():
	line = line.rstrip("\n")
	column = line.split("\t")
	key=column[0]
	infor=column[1:]
	infor=string.join(infor)	
	otu_dict[key]=infor

# dict for taxid
blast_dict = {}

# dict for e_value and percentage of identical match
blast_dict2 = {}

for line in marker_blast.readlines():
	line = line.rstrip("\n")
	column = line.split("\t")
	key=column[0]
	infor=column[1]
	infor2=column[10]+"\t"+column[2]
		
	blast_dict[key]=infor
	blast_dict2[key]=infor2

for i in otu_dict:
	if blast_dict.has_key(i):
		
		tax_child_list = tax.get_children_recursive(int(blast_dict[i]))
		tax_parent_list = tax.get_all_parents(int(blast_dict[i])) 
		
		parents_list = [tax.taxid2names(x) for x in tax_parent_list]	
		children_list = [tax.taxid2names(x) for x in tax_child_list]
		
		parents_list.extend(children_list)	
			
		path_output=[]
		tax_path_infor=["kingdom","phylum","class","order","family","genus","species"]
		for path_name in tax_path_infor:
			
			path_name_list = "unknown"
			for x in parents_list:
				taxid_x = tax.name_taxid(x)
				
				if tax.taxid2rank.has_key(taxid_x):
					rank=tax.taxid2rank[taxid_x]		
				
				if rank==path_name:
					path_name_list = tax.taxid2names(taxid_x)
				continue	
			path_output.append(path_name_list)
			continue	
						
		print i+"\t"+ otu_dict[i]+"\t"+blast_dict2[i]+"\t"+string.join(path_output,"\t")
		
		#print i+"\t"+ otu_dict[i]+"\t"+string.join(parents_list)		
					
	else:
		print i+"\t"+otu_dict[i]+"\t"+"all unknown"
		

marker_blast.close()
otu_table.close()
