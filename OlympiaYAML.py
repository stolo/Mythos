#!/usr/bin/python
import pickle 
import json
import re
import yaml

JSON_FILE = "./olympians.json"
#alternate YAML files: olympians.yaml (as dumped), olympiansSTR.yaml (explicit typing str)
YAML_FILE = "./olympiansHR.yaml"

class Olympus(list):
    """ Olympus holds a list of God objects """
    def save(self, json_file):
        """ Save Olympus as list of dictionaries into specified json file """
        fp = open(json_file, 'w')
        json.dump(self, fp)

    def load(self, json_file):
        """ Load Olympus from json file """
        fp = open(json_file, 'r')
        self.__init__(json.load(fp, object_hook=self._custom_decode))

    def load_yaml(self, yaml_file):
        """ Load Olympus from YAML file """
        print "Loading file: " + yaml_file
        fp = open(yaml_file, 'r')
        self.__init__(yaml.load_all(fp))
        print str(len(self)) + " God(s) loaded."

    def get_all_attr(self):
        self.all_attr = []
        [self.all_attr.extend(god.keys()) for god in self] 
        self.all_attr = set(self.all_attr)
        #for attr in self.all_attr:
        #    print attr
        #    print "loaded"

    def get_all_val(self):
        self.all_val = []
        for god in self:
            for val in god.values():
                if self._is_string(val):
                    self.all_val.append(val)
                else:
                    for item in val:
                        self.all_val.append(item)
        #self.all_val = set(self.all_val)

    def _is_string(self, val):
       return isinstance(val, str)
        
    def save_yaml(self, yaml_file):
        fp = open(yaml_file, 'w')
        yaml.dump_all(self, fp)

    def append(self, item):
        """ Override list append method to add God to Olympus list """
        list.append(self, God(item))

    def __getitem__(self, key):
        """ Override __getitem__ to cast item as God object """
        return God(list.__getitem__(self,key))

    def _custom_decode(self, god):
        """ Custom decode method to cast objects loaded from json file to God objects """
        god = God(god)
        print "loading god: %s" %god
        return god

class TheOracle():
    def __init__(self, olympus):
        """ initialize with current olympus god list """
        self.olympus = olympus 

        #for god in self.olympus:
        #    print god 
        #for attr in self.olympus.all_attr:
        #    print attr
        #for val in self.olympus.all_val:
        #    print val 

        self.dispatch_table = {
            "count gods": self.count_gods,
            "describe \w+": self.describe_god,
            "list gods": self.list_gods,
            "list attributes": self.list_attr,
            "list attr": self.list_attr,
            "gods with": self.list_gods_with_attr,
            "what are the \w+ of \w+": self.get_attr,
            "who are the \w+ of \w+": self.get_attr,
            "what is the \w+ of \w+": self.get_attr,
            "who is the \w+ of \w+": self.get_attr,
            "help": self.hlp
        }

    def dispatch(self, question):
        for item in self.dispatch_table:
            if re.search(item, question):
                return self.dispatch_table[item]

    def prompt(self):
        """ start questioning """
        self.question = raw_input("> ")
        self.question_tokens = self.question.split(" ") 

        for token in self.question_tokens:
            try:
                god_index = self.olympus.index(God(token))
                attr_index = self.olympus.all_attr.index(token)
                val_index = self.olympus.all_val.index(token)

                self.gods_mentioned = []
                self.attr_mentioned = []
                self.val_mentioned = []

                if god_index > -1:
                    self.gods_mentioned.append(self.olympus(god_index))
                if attr_index > -1:
                    self.attr_mentioned.append(token)
                if val_index > -1:
                    self.val_mentioned.append(token)
            except:
                next

        #for god in self.olympus:
        #    print god 

        self.answer()

    def answer(self):
        """ generate answers to current question """
        print #"----------------------"
        try:
            self.dispatch(self.question)()
        #except:
        #    try:
        #        print "my" 
        #        len_gods = len(self.gods_mentioned)
        #        len_attr = len(self.attr_mentioned)
        #        len_val = len(self.val_mentioned)
        #        print len_gods
        #        print "test"
        #        if len_gods > 0 and len_attr == 0 and len_val == 0:
        #            for god in self.gods_mentioned():
        #                self.dispatch("describe %s") % god
        except:
            print "I dunno"
        print #"----------------------"

    def hlp(self):
        for r in self.dispatch_table.keys():
            print r

    def describe_god(self):
        god_name = self.question_tokens[1]
        print self._get_god_by_name(god_name)['description']

    def get_attr(self):
        """ Return attribute for a given god """
        result = []
        god_name = self.question_tokens[5]
        god_attr = self.question_tokens[3]
        god =  self._get_god_by_name(god_name)
    
        try:
            if self._is_string(god_attr):
                print god[god_attr]
            else:
                for item in god[god_attr]:
                    if god[god_attr].index(item) < len(god[god_attr])-1:
                        print "%s," %item,
                    else:
                        print "%s" % item
        except:
            print "problem looking up %s for %s" %(god_attr, god_name)
                  
    def get_print_list(self, my_func):
        def print_list(): 
            print my_func()
            my_list = my_func()
            for item in my_list:
                print item 
        return print_list
         
    def list_gods_with_attr(self):
        """ return gods that have certain attribute value """
        result = []
        key = self.question_tokens[2]
        value = self.question_tokens[3]

        try:
            if self._is_string(self, key):
                result = [god for god in self.olympus if god[key] == value]
            else:
                for god in self.olympus:
                    for attr in god[key]:
                        if attr.lower() == value.lower():
                            result.append(god)
            for god in result:
                if result.index(god) < len(result) -1:
                    print "%s," %god,
                else:
                    print "%s" %god
        except:
            print "problem checking for %s in %s " % (value, key)

    def list_attr(self):
        """ return set of attributes on all gods """
        print "The known attributes of the Olympian gods are : "
        keys = []
        [keys.extend(god.keys()) for god in self.olympus] 
        keys = set(keys)
        for attr in keys:
            print attr,
        print

    def list_gods(self): 
        """ list gods """
        print "The Greek Gods of Olympus are: "
        for god in self.olympus:
            if self.olympus.index(god) < len(self.olympus)-1:
                print "%s," %god,
            else:
                print "%s" %god

    def count_gods(self): 
        """ count the gods in olympus """
        print "There are %d Olympian Gods" % (len(self.olympus))

    def _is_string(self, key):
       return isinstance(self.olympus[0][key], str)

    def _get_god_by_name(self, name):
        for god in self.olympus:
            if god['greek_name'].lower() == name.lower() or god['roman_name'].lower() == name.lower():
                return god

class God(dict):
    def __init__(self, god_attr=None):
        """ initialize god with dictionary, allow any key value pairs, no schema """
        for k in god_attr.keys():
            self[k] = god_attr[k]

    def save(self, olympus):
        """ save god into olympus """
        olympus.append(self) 
        olympus.save()

    def __str__(self):
        """ by default printing god returns the greek_name """
        if self.has_key('greek_name') == True:
            return self['greek_name']
        else:
            return self

if __name__ == '__main__':
    olympus = Olympus()
#    olympus.load(JSON_FILE)
    olympus.load_yaml(YAML_FILE)
    olympus.get_all_attr()
    olympus.get_all_val()
    the_oracle = TheOracle(olympus)
    while 1:
        the_oracle.prompt()
