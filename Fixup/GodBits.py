#!/usr/bin/python
import yaml

class BaseBits(list):
    """ Work in progress """
    def __init__(self, yaml_file="gobits.yaml"):
        self.load(yaml_file)

    def load(self, yaml_file):
        """ Load Olympus from YAML file """
        fp = open(yaml_file, 'r')
        list.__init__(self, yaml.load(fp))
        print "%s loaded..." %yaml_file
        
    def save(self, yaml_file):
        """ Saving... duh! """
        fp = open(yaml_file, 'w')
        yaml.dump_all(self, fp)

    #def get_by_type(self, my_type):
    #    return [entry for entry in self if entry[0] == my_type]

class Gobits(BaseBits):
    def __init__(self, yaml_file="gobits.yaml"):
        super(Gobits, self).__init__()
        self.load(yaml_file)

    def get_by_type(self, my_type):
        return set([entry[1] for entry in self if entry[0] == my_type])

    def list_types(self):
        return set([entry[0] for entry in self])

    def list_entries(self):
        return [entry[1] for entry in self]

    #def get_by_str(self, my_str):
    #    return [entry for entry in self if entry[1].lower() == my_str.lower()]

    #def get_by_gobit(self, my_gobit):
    #    return [entry for entry in self if entry[0] == my_gobit][0]

    #def get_by_type_entry(self, my_type, my_entry):
    #    return [entry for entry in self if entry[0] == my_type and entry[1] == my_entry]

class Glubits(BaseBits):
    def __init__(self, yaml_file="glubits.yaml"):
        super(Glubits, self).__init__()
        self.load(yaml_file)

    def get_by_gobit(self, my_gobit):
        return [entry for entry in self if entry[0] == my_gobit]

    def get_by_type(self, my_type):
        pass 

    def get_by_gobit_type(self, my_gobit, my_type):
        return [entry[1][1] for entry in self if entry[0] == my_gobit and entry[1][0] == my_type]

    #def get_by_type_gobit(self, my_type, my_gobit):
    #    return [entry for entry in self if entry[0][0] == my_type and entry[1] == my_gobit]

class Query():
    def __init__(self, gobits, glubits):
        self.gobits = gobits 
        self.glubits = glubits
        self.entries = gobits.list_entries()
        self.types = gobits.list_types()
        self.names = gobits.get_by_type("name")

    def question(self, question):
        tokens = question.split(" ") 
        num_tokens = len(tokens)
        self.chunks = []
        for i in range(0, num_tokens + 1):
            for j in range(0, num_tokens + 1):
                if i < j:
                    self.chunks.append( str.join(" ", tokens[i: j]) )

    def answer(self):
        types_mentioned = self.intersection(self.chunks, self.types)
        entries_mentioned = self.intersection(self.chunks, self.entries)
        names_mentioned = self.intersection(self.chunks, self.names)

        lnm = len(names_mentioned) 
        ltm = len(types_mentioned)
        lem = len(entries_mentioned)

        result = []
        print lnm, ltm, lem
        if lnm > 0 and ltm == 0:
            for my_name in names_mentioned:
                my_filter = lambda x: x[0][1] == my_name and x[1][0] == "description"
                result += [entry[1][1] for entry in filter(my_filter, self.glubits)]

        if lnm == 0 and ltm > 0 and lem == 0:
            for my_type in types_mentioned:
                my_filter = lambda x: x[0][0] == my_type 
                result += [entry[0][1] for entry in filter(my_filter, self.gobits)]
        
        if lem > 0:
            all_results = []
            for my_entry in entries_mentioned:
                my_filter = lambda x: x[1][1] == my_entry
                all_results.append([entry[0][1] for entry in filter(my_filter, self.glubits)])
            result = set(self.intersection_all(all_results))              

#        if lnm == 0 and ltm > 0 and lem == 0:
#            for typ in types_mentioned:
#                for item in self.gobits.get_by_type(typ):
#                    result.append( item[1] )
#
#        if lnm == 0 and ltm == 1 and lem == 1:
#            for entry in entries_mentioned:
#                for typ in types_mentioned:
#                    for item in self.gobits.get_by_type_entry(typ, entry):
#                        name_gobits = self.glubits.get_by_type_gobit("name", item[0])
#                        for ngb in name_gobits:
#                            result.append(self.gobits.get_by_gobit(ngb[0])[1]) 
#
        return "<br>".join(result)

    def intersection(self, l1, l2):
        return [x for x in l1 if x in l2]

    def intersection_all(self, list_of_lists):
        common = list_of_lists.pop()
        for my_list in list_of_lists:
            if type(my_list) == type([]):
                common = [x for x in common if x in list_of_lists]
        return common 
        
if __name__ == '__main__':
    gobits=Gobits()
    glubits=Glubits()
    query = Query(gobits, glubits)
    while 1:
        query.question()
        query.answer()
