#!/usr/bin/env python

import httplib
import urllib
import time
import csv
import os
import elasticsearch

# Set the token in the environment. (Is this a good idea?)
# E.g., export GH_API_TOKEN=your_token
token = os.env.get('GH_API_TOKEN')

auth_header = 'x-oauth-basic'
api_host = 'api.github.com'
user_agent_header = 'User-Agent'
user_agent = 'Glue Mule/Haiku'

params = urllib.urlencode({'foo':'bar'})
headers = {auth_header : token, user_agent_header : user_agent}

conn = httplib.HTTPSConnection(api_host,443)


def read_csv(f='./gh_gov_orgs.csv'):
	with open(f, 'r') as _csv:
		reader = csv.reader(_csv)
		for row in reader:
			_org = row[1]
			print get_org (org)
			write_to_es( org )
			time.sleep(.05)



def get_org(org):
    _resource = "/orgs/" + org 
    print _resource
    conn.request("GET", _resource, None, headers)
    response = conn.getresponse()
    json = response.read()
    return json





# Should use the Elastic Search Python API
es_host = 'localhost'
es_port = 9200
esparams = urllib.urlencode({'':''})
esconn = httplib.HTTPSConnection(es_host,es_port)


def write_to_es():
	_resource = 'gluemule/org/'
	pass
# ----------------------------

read_csv()

conn.close()

#get_org('cfpb')


