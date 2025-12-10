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

o2dbs_fname = join(datadir, 'databases-sites-users.csv')
o2dbs_csv = open(o2dbs_fname).readlines()
o2dbs_reader = csv.reader(o2dbs_csv)
o2dbdata = [row for row in o2dbs_reader]



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

def finddbs(site):
    results = []
    for row in o2dbdata:
        if site == row[2]:
            results.append(row[:2])
    return results

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

def writemetafields():
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
            The 'site-type', 'site-type-2' and 'technology' values are NOT configuration values, they are merely survey assessments tracked here.\n'''.format(**site))

def getalldbs():
    results = []
    for row in surveydata:
        site = dict(zip(header, row))
        sitedir = join(repodir, 'registry', 'sites', site['name'])
        metadir = join(sitedir, 'metadata')
        dbs = finddbs(site['name'])
        print(site['name'], ','.join([':'.join(db) for db in dbs]))

def surveyq(field, values, negate=False):
    results = []
    for row in surveydata:
        site = dict(zip(header, row))
        if (site[field] in values) ^ negate:
            results.append((site[field], site['name']))
    return sorted(results)

def fieldchecker(site, field, values):
    for value in values:
        if value in site[field]:
            return True
    return False

def surveyqi(field, values, negate=False):
    results = set([])
    for row in surveydata:
        site = dict(zip(header, row))
        if fieldchecker(site, field, values) ^ negate:
            results.add((site[field], site['name']))
    return sorted(list(results))

def showstuff(txt, field, values, negate=False):
    lst = surveyqi(field, values, negate=negate)
    print()
    print("%s:" % txt, len(lst))
    for x in lst:
        print("%s %s" % x)

def dotech():
    Apache_based = ['PHP', 'HTML', 'Raw HTTP', 'CGI']
    Complex = ['Complex', 'Posit Connect']
    Webapp = ['Gunicorn', 'Ruby on Rails', 'Discourse (Ruby)']

    showstuff("Complex sites", 'technology', Complex)
    showstuff('Apache-based', 'technology', ['PHP', 'HTML', 'Raw HTTP', 'CGI'])
    showstuff('Web Applications', 'technology', Webapp)
    showstuff('Cryosparc', 'technology', ['CryoSparc'])
    showstuff('Tomcat', 'technology', ['Tomcat'])
    showstuff('Remainder', 'technology', ['Tomcat', 'CryoSparc'] + Webapp + Complex + Apache_based, negate=True)

def dositetype1():
    sitetypes1 = ['Research connected',
                  'Brochure Site',
                  'Library',
                  'DevOps Infrastructure',
                  'Business Workflow',
                  'Data sharing only']
    for st in sitetypes1:
        showstuff(st, 'site-type', [st])
    showstuff('Remainder', 'site-type', sitetypes1, negate=True)


def dositetype2():
    sitetypes2 = ['Specialized Tool',
                  'HPC',
                  'Lab Site',
                  'Posit Connect',
                  'Forum Site',
                  'Library Site',
                  'File and Data',
                  'Static Site',
                  'Project site',
                  'Business Workflow',
                  'Education Site',
                  'Professional Site',
                  '?']
    for st in sitetypes2:
        showstuff(st, 'site-type-2', [st])
    showstuff('Remainder', 'site-type-2', sitetypes2, negate=True)

if __name__ == '__main__':
    #pp(surveydata)
    if '1' in sys.argv:
        dositetype1()
        print(' : ')
    if '2' in sys.argv:
        dositetype2()
        print(' : ')
    if 'tech' in sys.argv:
        dotech()
        print(' : ')

    #getalldbs()
    #showstuff('blank', 'technology', [''])
