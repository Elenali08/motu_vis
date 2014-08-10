SIZE_MINIMUM = 200

for count, line in enumerate(open("filtered_tax_ncbi.txt")):
    
    if len(line.split("\t")) == 11:
        (name, counts, evalue, percent_id, kingdom, phylum, phylo_class, family, order, genus, species) = line.rstrip("\n").split("\t")
     
        counts_in_sample = int(counts.split(" ")[0])
	if counts_in_sample > SIZE_MINIMUM:
               print name+","+str(counts_in_sample)
	   
