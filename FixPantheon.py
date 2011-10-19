#!/usr/bin/python
from OlympiaNK import Olympus, God

YAML_FILE = './olympiansHR.yaml'
olympus = Olympus()
olympus.load_yaml(YAML_FILE)

pantheonless = [god for god in olympus if not god.has_key('pantheon')]
for god in pantheonless: 
    print god['name']
    my_input = raw_input("pantheon: ")
    god['pantheon'] = my_input 
    olympus.save_yaml(YAML_FILE)

