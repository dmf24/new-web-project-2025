import sys
import os
import csv
from os.path import join
from pprint import pprint as pp
import json
import socket


o2sites = json.loads(open('/home/dmf24/webconf2-repo/build/sites.json').read())

scriptdir = os.path.dirname(os.path.abspath(sys.argv[0]))
datadir = join(scriptdir, os.path.pardir, 'data')

surveycsv = open(join(datadir, 'o2web-surveyplus-2024.csv')).readlines()
reader=csv.reader(surveycsv)
surveydata = [row for row in reader][1:]

o2sitenames = set([site['name'] for site in o2sites])
trimnames = set([x[0] for x in surveydata])

#pp(trimnames)

not_in_survey = o2sitenames.difference(trimnames)

def host(name):
    try:
        return socket.gethostbyname(name)
    except socket.gaierror:
        return None

def checkdns(names):
    for name in names:
        yield (name, host(name))

def nodns(names):
    return [name for name, result in checkdns(names) if result is None]

def yesdns(names):
    return [name for name, result in checkdns(names) if result is not None]

#print('\n'.join(nodns(not_in_survey)))

print('\n'.join(yesdns(not_in_survey)))
