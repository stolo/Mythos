#!/usr/bin/python

import yaml
from Olympus import *
oly = Olympus()
oly.load_yaml('./olympiansHR.yaml')

lu = {'children': 'child', 'description': 'description', 'domains': 'domain', 'father': 'father', 'generation': 'generation', 'mother': 'mother', 'name': 'name', 'native_name': 'native_name', 'pantheon': 'pantheon', 'sacred_animals': 'sacred_animal', 'siblings': 'sibling', 'symbols': 'symbol'}

def go():
    breakout(lu)
    
#def breakout(key, desc):
def breakout(lookups):
    glob = {}
    glub = {}
    for (old_attr, value) in lookups.iteritems():
        glob[old_attr] = [] 
        for god in oly:
            if god.has_key(old_attr):
                if hasattr(god[old_attr], 'append'):
                    for desc in god[old_attr]: 
                        if re.match('\S', desc):
                            glob[old_attr].append( (lookups[old_attr], desc.lower()) )
                            glub[(lookups[old_attr], desc.lower())] = god["name"]
                else:
                    glob[old_attr].append( (lookups[old_attr], god[old_attr].lower()) )
                    glub[(lookups[old_attr], god[old_attr].lower())] = god["name"]

    final_gobits = []
    final_glubits = []
    name_gobits = []

    #i = 0
    #for entry in set(glob["name"]):
    #    i += 1
    #    name_gobits.append( fmt_entry(entry, i) )
#
#    for attr_group in glob.keys():
#        i = 0
#        for entry in set(glob[attr_group]):
#            i += 1
#            final_gobits.append( fmt_entry(entry, i) )
#
#    for glu in glub.keys():
#        final_glubits.append( (get_god_by_name(name_gobits, glub[glu])[0], fmt_entry(glu, i)[0] ))

    fp = file("gobits.yaml", 'w')
    yaml.dump(final_gobits, fp)
    fp.close()
    fp = file("glubits.yaml", 'w')
    yaml.dump(final_glubits, fp)
    fp.close()

def get_god_by_name(gobit_list, name):
    return [g for g in gobit_list if g[1].lower() == name.lower()][0] 

def fmt_entry(entry, i):
    return ((entry[0], i), entry[1])

def rev_list_o_dicts(list_o_dicts):
    result = []
    for item in list_o_dicts:
        key = item.keys()[0]
    #    print item[key], key
        result.append({item[key]: key})
    return result

         
def item_fmt(desc, i, item):
    #return {"%s:%u"%(desc,i):item.lower().encode("utf-8").decode("utf-8")} 
    return ((desc, i), item.lower().encode("utf-8").decode("utf-8")) 

def test(file):
    fp = open(file, 'rw')
    my_yaml = yaml.load(fp)
    for item in my_yaml:
        key = item.keys()[0] 
        value = item[key].encode("utf-8")
        print key, value
        #item[key] = value
    fp.close()
    #fp = open(file, 'w')
    #yaml.dump_all(my_yaml, fp)
    #fp.close()

if __name__ == '__main__':
    go()
