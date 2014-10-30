#!/usr/bin/env python

import requests
import urllib
import time
import csv
import os
from elasticsearch import Elasticsearch
import json

'''
- Remember where we are and handle exceptions
- add doc_as_upsert:true to update or create based on existence
http://www.elasticsearch.org/guide/en/elasticsearch/reference/current/docs-update.html
'''


'''
This should be a tree that looks likes this:

Organization-1
  | 
  |
   -- Repository-1
      |
       -- issue-1
       -- issue-2
       -- issue-n
   |
    -- Repository-2
      |
       -- issue-1
       -- issue-2
       -- issue-n
   |
    -- Repository-n
      |
       -- issue-1
       -- issue-2
       -- issue-n

Organization-2
  |  
  |
   -- Repository-1
      |
       -- issue-1
       -- issue-2
       -- issue-n
  |
   -- Repository-2
      |
       -- issue-1
       -- issue-2
       -- issue-n
   |
    -- Repository-n
      |
       -- issue-1
       -- issue-2
       -- issue-n

'''


# Set the token in the environment. (Is this a good idea?)
# E.g., export GH_API_TOKEN=your_token
token = os.environ.get('GH_API_TOKEN')

auth_header = 'x-oauth-basic'
api_host = 'api.github.com'
user_agent_header = 'User-Agent'
user_agent = 'Glue Mule/Haiku'

headers = {auth_header : token, user_agent_header : user_agent}


# Should use the Elastic Search Python API
es_host = 'localhost'
es_port = 9200
#esparams = urllib.urlencode({'':''})
#esconn = httplib.HTTPSConnection(es_host,es_port)



def rate_limit():
	r = requests.get('https://api.github.com/rate_limit', auth=('',token))
	print r.text



def import_all_from_one_org(org_name='cfpb'):
		print 'Fetching %s into Elasticsearch.' % (org_name)
		org_data = get_org (org_name)
		j_org = json.loads(org_data)
		print j_org
		if ( 'message' in j_org):
			if( j_org['message'] == 'Not Found' ):	
				#log 
				print 'Organization (%s) not found or is not public.' % org_name
				print 'Moving on ...'
				return
		write_org_to_es( org_name,org_data )
		add_repos_and_issues_for_org(org_name)
		#time.sleep(.05)



def import_from_csv(f='./gh_gov_orgs.csv'):
	with open(f, 'r') as _csv:
		reader = csv.reader(_csv)
		for org in reader:
			org_name = org[1]
			print org
			import_all_from_one_org(org_name)



def get_org(org):
	response = requests.get( 'https://api.github.com/orgs/' + org, \
    	                  auth=('',token), headers=headers )
	return response.text
    



def write_org_to_es(id, org):
	print '-----------------------------------------------'
	#es = Elasticsearch([{ 'host': 'localhost', 'port': '9200', 'use_ssl': False }])
	print org
	#org_data = urllib.urlencode(org)
	print '-----------------------------------------------'
	#es.create(index='gluemule', doc_type='org', id=id, body=org.encode('UTF-8'))
	r = requests.post( 'http://localhost:9200/gluemule/org/' + id , data=org.encode('UTF-8') )
	print r.text



#Refactor!
def add_repos_and_issues_for_org(org):
	#fetch from gh
	response = requests.get( 'https://api.github.com/orgs/' + org + \
							 '/repos?per_page=10000', auth=('',token), headers=headers )
	repos =json.loads(response.text)
	print org
	j = ''
	for repo in repos:
		print 'repo = %s' % repo
		_id = repo['id']
		_parent = repo['owner']['login']
		_u = 'http://localhost:9200/gluemule/repo/' + str(_id)
		print _u
		#print json.dumps(repo)
		requests.post( _u, data=json.dumps(repo) , headers=headers)
		# Recurse down into issues
		add_issues_for_repo(org=org,repo=repo['name'])
		



def add_issues_for_repo(org='foo', repo='bar'):
	#fetch from gh
	# GET /repos/:owner/:repo/issues
	u = 'https://api.github.com/repos/%s/%s/issues?per_page=10000' \
															% (org,repo)
	print u
	response = requests.get( u, auth=('',token), headers=headers )
	json_obj =json.loads(response.text)
	print len(json_obj)
	j = ''
	for obj in json_obj:
		_id = obj['id']
		obj['org'] = org
		obj['repo'] = repo
		#_parent = obj['owner']['login']
		_u = 'http://localhost:9200/gluemule/issues/%s' % (str(_id))
		print _u
		print json.dumps(obj)
		requests.post( _u, data=json.dumps(obj) , headers=headers)

# ----------------------------

rate_limit()

import_from_csv()

#import_all_from_one_org('edelegationen')


#add_repos_for_org('cfpb')

#import_from_csv()



