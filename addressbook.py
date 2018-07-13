from flask import Flask
from flask import request
import json
import requests
from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch()

currentid = 7

@app.route('/setup')
def initialization():
	if es.indices.exists(index='address-book'):
		es.indices.delete(index='address-book')
	es.indices.create(index='address-book')
	populate()
	currentid = 7
	return ''

@app.route('/contact', methods=['GET','POST'])
def nonspecific():
	if request.method == 'GET':
		pageSize = request.args.get('pageSize', default = 10, type = int)
		pageNumber = request.args.get('page', default = 1, type = int)
		query = request.args.get('query', default = '', type = str)
		results = getList(pageSize, pageNumber, query)
		return json.dumps(results)
		#read params, access database, return results
	elif request.method == 'POST':
		if not isContactValid(request.json):
			return''
		name = request.json["Name"]
		list = es.search(index='address-book', doc_type='_doc', body={"query": {"query_string" : { "query" : name }}})
		if list['hits']['total'] == 0:
			print('There are no hits!')
			global currentid
			es.create(index='address-book', doc_type='_doc', id=currentid, body=request.json)
			currentid += 1
			return 'Successfully added'
		else:
			print('already exists')
			return 'An entry already exists under that name'
		#post new contact

@app.route('/contact/<name>', methods=['GET','PUT','DELETE'])
def specific(name):
	list = es.search(index='address-book', doc_type='_doc', body={"query": {"query_string" : { "query" : name }}})
	if list['hits']['total'] == 0:
		return 'There is no such contact'
	if request.method == 'GET':
		return json.dumps(list['hits']['hits'][0]['_source'])
	elif request.method == 'PUT':
		return json.dumps(es.index(index='address-book', doc_type='_doc', id=list['hits']['hits'][0]['_id'], body=request.json))
	elif request.method == 'DELETE':
		return json.dumps(es.delete(index='address-book', doc_type='_doc', id=list['hits']['hits'][0]['_id']))

#@app.route('/test')
#def test():
	#requests.post('http://127.0.0.1:5000/contact', headers={'Content-Type': 'application/json'}, data=json.dumps({"Name":"Feli","Phone":"3025409677","Email":"feli@gmail.com"}))
	#requests.put('http://127.0.0.1:5000/contact/Feline', headers={'Content-Type': 'application/json'}, data=json.dumps({"Name":"Feli","Phone":"3025409677","Email":"felicitas@gmail.com"}))
	#requests.put('http://127.0.0.1:5000/contact/Feli', headers={'Content-Type': 'application/json'}, data=json.dumps({"Name":"Feli","Phone":"3025409677","Email":"felicitas@gmail.com"}))
	#requests.delete('http://127.0.0.1:5000/contact/Feli')
	#return ''

#fill index with some premade people
def populate():
	es.create(index='address-book', doc_type='_doc', id=1, body={"Name":"Alan","Phone":"5647012772","Email":"alan@gmail.com"})
	es.create(index='address-book', doc_type='_doc', id=2, body={"Name":"Sabrina","Phone":"5371368283","Email":"sabrina@gmail.com"})
	es.create(index='address-book', doc_type='_doc', id=3, body={"Name":"Summer","Phone":"5037683211","Email":"summer@gmail.com"})
	es.create(index='address-book', doc_type='_doc', id=4, body={"Name":"Jiay","Phone":"2008207846","Email":"jiay@gmail.com"})
	es.create(index='address-book', doc_type='_doc', id=5, body={"Name":"Oscar","Phone":"7036569925","Email":"oscar@gmail.com"})
	es.create(index='address-book', doc_type='_doc', id=6, body={"Name":"Cat","Phone":"3025409677","Email":"cat@gmail.com"})
	return ''

#make a list of results with the pageSize and number requested, based on the query.  Default no query returns all.
def getList(pageSize, pageNumber, query):
	start = pageSize * (pageNumber - 1)
	querybuilder = {"query": {"match_all": {}}}
	if query != '':
		querybuilder = {"query": {"query_string" : { "query" : query }}}
	return es.search(index='address-book', doc_type='_doc', from_=start, size=pageSize, body=querybuilder)

def isContactValid(contact):
	return len(contact["Phone"]) == 10 #example, but would include other checks such as regex to ensure all numbers, 
	