#!/usr/bin/python
from OlympiaNK import Olympus, God

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

get_aztec()
