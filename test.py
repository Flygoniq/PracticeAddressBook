from flask import Flask
from flask import request
import json
from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch()

@app.route('/setup')
def initialization():
	es.indices.delete(index='address-book')
	return json.dumps(es.indices.create(index='address-book'))

@app.route('/contact', methods=['GET','POST'])
def nonspecific():
	if request.method == 'GET':
		return 'hi'
		#read params, access database, return results
	elif request.method == 'POST':
		return
		#post new contact

@app.route('/contact/<name>', methods=['GET','PUT','DELETE'])
def specific():
	if request.method == 'GET':
		return
		#request specific name contact
	elif request.method == 'PUT':
		return
		#check for specific name contact.  replace with JSON sent.
	elif request.method == 'DELETE':
		return
		#delet this