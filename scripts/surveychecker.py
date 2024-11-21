import sys
import os
import csv
from os.path import join
from pprint import pprint as pp
import json
import socket

repodir = '/home/dmf24/webconf2-repo'

o2sites = json.loads(open('/home/dmf24/webconf2-repo/build/sites.json').read())

scriptdir = os.path.dirname(os.path.abspath(sys.argv[0]))
datadir = join(scriptdir, os.path.pardir, 'data')

surveycsv = open(join(datadir, 'o2web-surveyplus-2024.csv'), encoding='iso-8859-1').readlines()
reader=csv.reader(surveycsv)
surveydata = [row for row in reader][1:]

o2sitesbyname = dict([(site['name'], site) for site in o2sites])
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

def isdev(site):
    for m in site.get('memberof', []):
        if 'dev' in m:
            return True
    return False

sitetypes = set()

for site in o2sites:
    for t in site.get('types', []):
        if t.strip() != '':
            sitetypes.add(t)

xtypes = dict(
    app=['celery',
         'gunicorn',
         'jupyterhub',
         'multigunicorn',
         'shellscript',
         'supervisord'],
    redirect=['redirect',
              'redirect301'],
    proxy=['proxy',
           'raw-proxy'],
    web=['nginx', 'httpd24'],
    other=['redis'])

def istype(site, apptypes):
    for apptype in apptypes:
        for t in site.get('types', []):
            if t in xtypes[apptype]:
                return True

def surveycheck():
    for name in yesdns(not_in_survey):
        site = o2sitesbyname[name]
        stypes = site.get('types', ['none'])
        if not isdev(site) and istype(site, ['app', 'web', 'proxy']):
            print(name)

header = ['name', 'primary-contact', 'primary-email', 'o2_www', 'active-traffic', 'site-type', 'recommendation','technology','site-type-2', 'note']

for row in surveydata:
    site = dict(zip(header, row))
    sitedir = join(repodir, 'registry', 'sites', site['name'])
    metadir = join(sitedir, 'metadata')
    if not os.path.isdir(metadir):
        os.mkdir(metadir)    
    #for x in ['primary-contact', 'primary-email', 'recommendation', 'o2_www']:
    for x in ['technology', 'site-type', 'site-type-2']:
        with open(join(metadir, x), 'w') as f:
            f.write(site[x])
            f.write('\n')
    with open(join(metadir, 'readme.md'), 'w') as f:
        f.write('''This directory was created in 2024 to record, in a centralized place, contact information and notes on important, visible sites.
        Note: {note}
        The 'site-type', 'site-type-2' and 'technology' values are NOT configuration values, they are merely survey assessments tracked here.
        '''.format(**site))
#    print('{name} {primary-contact} {primary-email}'.format(**site))
    

#surveycheck()
#print("%s %s" % (','.join(site.get('types', ['none'])), name))
#print('\n'.join(yesdns(not_in_survey)))
