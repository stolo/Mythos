#!/usr/bin/python
from OlympiaNK import Olympus, God
import sys

YAML_FILE = './olympiansHR.yaml'
olympus = Olympus()
olympus.load_yaml(YAML_FILE)

def get_greek():
    page = open("./GreekGods.data", 'r')
    for line in page.readlines():
        greek_name = line.split("||")[0].decode('utf-8')
        name = line.split("||")[1].decode('utf-8')
        description = line.split("||")[2].decode('utf-8')
        pantheon = "Greek"
        g = God( { 'name' : name,
                   'greek_name' : greek_name,
                   'description': description,
                   'pantheon' : pantheon })
        olympus.append(g)
        olympus.save_yaml(YAML_FILE)

def get_egyptian():
    page = open("./EgyptianGods.data", 'r')
    for line in page.readlines():
        name = line.split("|")[0].decode('utf-8')
        description = line.split("|")[1].decode('utf-8')
        pantheon = "Egyptian"
        g = God( { 'name' : name,
                   'description': description,
                   'pantheon' : pantheon })
        olympus.append(g)
        olympus.save_yaml(YAML_FILE)

def get_aztec():
    page = open("./AztecGods.data", 'r')
    for line in page.readlines():
        name = line.split("|")[0].decode('utf-8')
        description = line.split("|")[1].decode('utf-8')
        pantheon = "Aztec"
        g = God( { 'name' : name,
                   'description': description,
                   'pantheon' : pantheon })
        olympus.append(g)
        olympus.save_yaml(YAML_FILE)

def get_chinese():
    page = open("./NewChineseGods.data1", 'r')
    for line in page.readlines():
        name = line.split("|")[0].decode('utf-8')
        description = line.split("|")[1].decode('utf-8')
        domains = []
        if len(line.split("|")) > 2:
            domains_text = line.split("|")[2].decode('utf-8')
            domains = domains_text.split(",")
        pantheon = "Chinese"
        g = God( { 
                   'name' : name,
                   'description': description,
                   'pantheon' : pantheon,
                   'domains' : domains 
                 }
               )
        olympus.append(g)
        print name, description, pantheon, domains
    olympus.save_yaml(YAML_FILE)

def get_gods():
    page = open(sys.argv[1], 'r')
    for line in page.readlines():
        name = line.split(" | ")[0].decode('utf-8')
        description = line.split(" | ")[1].decode('utf-8')
        pantheon = sys.argv[2]
        g = God( { 'name' : name,
                   'description': description,
                   'pantheon' : pantheon })
        olympus.append(g)
        print name
        #print name, description, pantheon
    olympus.save_yaml(YAML_FILE)

get_chinese()
