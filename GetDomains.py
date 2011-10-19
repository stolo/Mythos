#!/usr/bin/python
from OlympiaNK import Olympus, God

YAML_FILE = './olympiansHR.yaml'
olympus = Olympus()
olympus.load_yaml(YAML_FILE)

domainless = [god for god in olympus if not god.has_key('domains')]
print len(olympus)
print len(domainless)
for god in domainless: 
    print god['description']
    my_input = raw_input("domains: ")
    domains = my_input.split(',')
    god['domains'] = domains
    olympus.save_yaml(YAML_FILE)
