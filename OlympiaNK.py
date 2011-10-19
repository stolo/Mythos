#!/usr/bin/python
import pickle 
import json
import re
import yaml
import collections

JSON_FILE = "olympians.json"
#alternate YAML files: olympians.yaml (as dumped), olympiansSTR.yaml (explicit typing str)
YAML_FILE = "olympiansHR.yaml"

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
        self.dispatch_table = {
            "count gods": self.count_gods,
            "list gods": self.list_gods,
            "gods with": self.list_gods_with_attr,
            "what are the \w+ of \w+": self.get_attr,
            "what is the \w+ of \w+": self.get_attr,
            "what is important in \w+ culture": self.rank_domains,
            "top \w+ \w+": self.rank_domains
        }

    def dispatch(self, question):
        for item in self.dispatch_table:
            if re.search(item, question):
                return self.dispatch_table[item]

    def prompt(self):
        """ start questioning """
        self.question = raw_input("Question? ")
        self.question_tokens = self.question.split(" ") 
        self.answer()

    def answer(self):
        """ generate answers to current question """
        print "----------------------"
        try:
            self.dispatch(self.question)()
        except:
            print "I dunno"
        print "----------------------"

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
                  
    def list_gods_with_attr(self):
        """ return gods that have certain attribute value """
        result = []
        key = self.question_tokens[2]
        value = self.question_tokens[3]

        try:
            if self._is_string(key):
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
            
    def rank_domains(self):
        """use anthropologist class to obtain ranked list of domains"""
        a = Anthropologist(olympus)
        n = int(self.question_tokens[1])
        if self.question_tokens[2] in ['Greek','Roman','Norse','Egyptian']:
            a.AnthroWithPanth(olympus, self.question_tokens[2])
        print "Top", str(n), "cultural attributes: ", a.top_n(n)
    

    def list_attr(self):
        """ return set of attributes on all gods """
        keys = []
        [keys.extend(god.keys()) for god in self.olympus] 
        return set(keys)

    def list_gods(self): 
        """ list gods """
        print "The Gods are: "
        for god in self.olympus:
            if self.olympus.index(god) < len(self.olympus)-1:
                print "%s," %god,
            else:
                print "%s" %god

    def count_gods(self): 
        """ count the gods in olympus """
        print "There are %d Gods" % (len(self.olympus))

    def _is_string(self, key):
        return isinstance(self.olympus[0][key], str)

    def _get_god_by_name(self, name):
        for god in self.olympus:
            if god['name'].lower() == name.lower() or god['roman_name'].lower() == name.lower():
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
        """ by default printing god returns the name """
        if self.has_key('name') == True:
            return self['name']
        else:
            return self
        
class Anthropologist(collections.Counter):
    def __init__(self,gods):
        self.gods = gods
        for god in self.gods:
            if god.has_key('domains'):
                for d in god['domains']:
                    self[(d.lower())] += 1
                    
    def AnthroWithPanth(self,gods,pantheon):
        self.clear()
        self.gods = gods
        for god in self.gods:
            if god['pantheon'] == pantheon:
                if god.has_key('domains'):
                    for d in god['domains']:
                        self[(d.lower())] += 1
  
    def top_five (self):
        return self.most_common(5)
    
    def top_n (self,n):
        return self.most_common(n)
    
    def high_freq(self,n):
        hf = collections.Counter()
        for item in self:
            if item[1] >= n:
                hf[0] = item[0]
                hf[1] = item[1]
        return hf
    
if __name__ == '__main__':
    olympus = Olympus()
#    olympus.load(JSON_FILE)
    olympus.load_yaml(YAML_FILE)
    the_oracle = TheOracle(olympus)
    while 1:
        the_oracle.prompt()
