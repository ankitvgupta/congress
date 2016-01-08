import yaml
import os

ids = []
with open(os.getcwd() + "/congress-legislators/legislators-current.yaml", 'r') as stream:
    legislators = yaml.load(stream)

    for legislator in legislator:
    	new_person = {}
    	new_person["name"] = legislator["name"]
    	new_person["id"] = legislator["id"]["bioguide"]

