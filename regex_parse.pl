import re
import sys

all_file = open(sys.argv[1]).read()
out_file = open(sys.argv[2], "wt")

count = 0


# danger! this will break if ENA XML format changes
for m in re.finditer(r'scientificName="([A-Za-z. _0123456789]+)" taxId="(\d+)".*?<sequence>(.+?)</sequence>', all_file, re.DOTALL):
	count = count + 1
	if count % 1000 == 0:
		print("done " + str(count))
	species_name = m.group(1)
	# print(species_name)
	taxid = m.group(2).rstrip("\n") 	
	sequence = m.group(3).rstrip("\t")
	if len(sequence) > 100 and not (species_name.startswith('uncultured') or species_name.startswith('unknown')):
		out_file.write(">" + taxid + sequence )
		
		
		


