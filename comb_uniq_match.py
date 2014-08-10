import string
input_file = open("tax_ranks_ssu_115.csv")
input_file2 = open("/exports/projects/msc_students_2014/ljingyun/ncbi_taxonomy/names_ranks.txt")

silva_tax_dict = {}
ncbi_tax_dict = {}

# populate the ncbi tax dict
for line in input_file2:
	line=line.rstrip("\n")
	column=line.split("\t")
	node_name = column[0]
	node_rank = column[1]
	ncbi_tax_dict[node_name] = node_rank

# populate the silva tax dict
for line in input_file:
	column=line.split("\t")
	node_name = column[1]
	node_rank = column[2]
	silva_tax_dict[node_name] = node_rank
	

def get_the_tax(name1,name2):

	# check the silva tax dict
	
	for node in tax_infor:
		rank =silva_tax_dict.get(node, 'unknown')
		if rank == name2:
			name1 = node
	
	  
	# now check the ncbi tax dict
	
	if name1 == 'unknown':
		for node in tax_infor:
                	rank = ncbi_tax_dict.get(node, 'unknown')
                	if rank == name2:
                		name1 = node
	
	return name1		 

otu_table=open('/exports/projects/msc_students_2014/ljingyun/bioblitz/RBGEBioBlitz_merged_l_u_s_c99_m2_otus_r_nx.otu_table.txt')
silvablastn=open('/exports/projects/msc_students_2014/ljingyun/bioblitz/RBGEBioBlitz_merged_l_u_s_c99_m2_otus_r_silvablastn_v3.txt')		

otu_dict = {}
for line in otu_table.readlines():
	line = line.rstrip("\n")
	column = line.split("\t")
	key=column[0]
	infor=column[1:]
	infor=string.join(infor)	
	otu_dict[key]=infor

blast_dict = {}
for line in silvablastn.readlines():
	line = line.rstrip("\n")
	column = line.split("\t")
	key=column[0]
	
	#get the species name
			
	tax_line=column[12].split(";")
	spec_infor= tax_line[-1].split(" ")
	spec_list = spec_infor[1:]
	spec_str = ''
	spec_str=' '.join(spec_list[0:])
			
	# get the tax path infor
	tax_infor=tax_line[1:]
	tax_infor.append(spec_infor[0])

	tax_class=get_the_tax('unknown','class')
			
	phylum = get_the_tax('unknown','phylum')
			
	genus = get_the_tax('unknown','genus')
			
			
	order = get_the_tax('unknown','order')
			
	family = get_the_tax('unknown','family')
			
	kingdom = get_the_tax('unknown','kingdom')
	species = spec_str
			
	e_value = column[10]
			
	id_match=column[2]
	
	output_infor = kingdom + "\t" + phylum +"\t"+tax_class+"\t"+order+"\t"+family+"\t"+genus+"\t"+species+"\t"+e_value+"\t"+id_match
	
	infor = output_infor
	blast_dict[key]=infor

for i in otu_dict:
	if blast_dict.has_key(i):
		print i+"\t"+ otu_dict[i]+"\t"+blast_dict[i]			
	else:
		print i+"\t"+otu_dict[i]+"\t"+"all unknown"
		

silvablastn.close()
otu_table.close()
