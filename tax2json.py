import tax

SIZE_MINIMUM = 50
ranks = ['kingdom', 'phylum', 'class', 'order', 'genus','species','motu', 'superkingdom', 'root']

taxid2motus = {}
for count, line in enumerate(open("filtered_tax_ncbi.txt")):
    # skip "all unknown" lines
    if len(line.split("\t")) == 11:
        (name, counts, evalue, percent_id, kingdom, phylum, phylo_class, family, order, genus, species) = line.rstrip("\n").split("\t")
        # build a dict for the row
        counts_in_sample = int(counts.split(" ")[0])
        if counts_in_sample > SIZE_MINIMUM:
            motu = {'name':name,
                    'counts':counts,
                    'evalue':evalue,
                    'size':counts_in_sample,
                    'id':percent_id,
                    'taxonomy':{
                        'kingdom':kingdom,
                        'phylum':phylum,
                        'class':phylo_class,
                        'family':family,
                        'order':order,
                        'genus':genus,
                        'species':species,
                        'motu' : name
                        }
                    }
            taxid = tax.name2taxid[species]
            current_motus = taxid2motus.get(taxid, [])
            #print(taxid2motus, current_motus)
            taxid2motus[taxid] = current_motus + [motu]
        
        
taxid2motu_count = {}
for taxid, motus in taxid2motus.items():
    for parent in tax.get_all_parents(taxid):
        taxid2motu_count[parent] = taxid2motu_count.get(parent, 0) + len(motus)
len(taxid2motu_count)

taxids_to_keep = set([t for t in taxid2motu_count.keys()] + [1])

import json
import pprint
set(tax.taxid2rank.values())
taxid2node = {}
def create_nodes(taxid, depth=0, max_depth=2):
    #print((" " * depth) + str(taxid))
    if depth > max_depth or taxid not in taxids_to_keep:
        return None
    this_node = {'taxid': taxid, 'name' : tax.taxid2name[taxid], 'rank' : tax.taxid2rank[taxid] , 'children':[]}
    if taxid in taxid2motus:       
        for motu in taxid2motus[taxid]:
            this_node['children'].append({'name' : motu['name'], 'rank':'motu', 'children':[], 'taxid':9999999, 'size':motu['size']})
    for child_taxid in tax.parent2child.get(taxid, []):
        child_nodes = create_nodes(child_taxid, depth+1, max_depth)
        if child_nodes != None:
            this_node['children'].extend(child_nodes)
        #else:
        #    this_node['size'] = 1
    taxid2node[taxid] = this_node
    return [this_node]


def trim_nodes(parent, node):
    if node['rank'] not in ranks:
        parent['children'].remove(node)
        parent['children'].extend(node['children'])
    for c in node['children']:
        trim_nodes(node, c)


json_root = {'name' : 'root', 'taxid': 1, 'rank': 'root'}
json_root['children'] = []
json_root['children'].extend(create_nodes(tax.name2taxid['Eukaryota'], max_depth=10000))
trim_nodes(json_root, json_root)

with open("out.json", "w") as outfile:
    outfile.write(json.dumps(json_root, indent=4))

