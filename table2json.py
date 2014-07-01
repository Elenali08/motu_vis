# usage: python table2json filtered_tax_file.txt output.json

import json
import sys
import itertools

motus = []
for count, line in enumerate(open(sys.argv[1])):
    # skip "all unknown" lines
    if len(line.split("\t")) == 11:
        (name, counts, evalue, percent_id, kingdom, phylum, phylo_class, family, order, genus, species) = line.rstrip("\n").split("\t")
        # build a dict for the row
        motu = {'name':name,
                'counts':counts,
                'evalue':evalue,
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
        motus.append(motu)


#count total number of nodes
node_count = len(set([t for t in itertools.chain.from_iterable([m['taxonomy'].values() for m in motus]) if t != 'unknown']))



# this is our heirarchy of ranks
ranks = ['kingdom', 'phylum', 'class', 'order', 'genus','species','motu']


processed_nodes = 0
# recursive function to construct nodes (dicts)
def build_node_with_size(rank_index, name):
    global processed_nodes
    processed_nodes += 1
   # sys.stdout.write(str(processed_nodes) + " / " + str(node_count))
    sys.stdout.write("\r" + name + " : " + str(processed_nodes) )
    # as soon as we encounter an unknown rank, stop descending the ranks
    if name == 'unknown':
        return None
    rank = ranks[rank_index]
    this_node = {}
    this_node['name'] = name
    # add up the sample1 counts of all motus for this rank
    size = sum([int(m['counts'].split(" ")[0]) for m in motus if m['taxonomy'][rank] == name])
    # only include nodes with at least 100 reads in sample1
    if size > 100:
        this_node['size'] = size
        # if we are at the lowest rank, stop and return
        if rank_index == len(ranks) - 1:
            return this_node
        # otherwise go down to the next rank and recurse
        else:
            child_rank = ranks[rank_index + 1]
            this_node['children'] = []
            for child in set([m['taxonomy'][child_rank] for m in motus if m['taxonomy'][rank] == name]):
                child_node = build_node_with_size(rank_index + 1, child)
                if child_node != None:
                    this_node['children'].append(child_node)
            return(this_node)
    else:
       return None



# create the dict that will eventually be turned in to JSON
json_root = {}
json_root['name'] = 'root'
json_root['children'] = []

# add each kingdom to the dict except the unknown stuff
for kingdom in set([m['taxonomy']['kingdom'] for m in motus]):
    print("\nprocessing " + kingdom)
    kingdom_node = build_node_with_size(0, kingdom)
    if kingdom_node != None:
        json_root['children'].append(kingdom_node)

with open(sys.argv[2], "w") as outfile:
    outfile.write(json.dumps(json_root, indent=4))
    print("\n")

