import unittest
import requests
import json

class TestMethods(unittest.TestCase):
	#def setUp(self):
		#requests.get('http://127.0.0.1:5000/setup')
	
	def test_specificget(self):
		print(requests.get('http://127.0.0.1:5000/contact'))
		self.maxDiff = 'None'
		self.assertEqual(requests.get('http://127.0.0.1:5000/contact').json(), {"took": 3, "timed_out": 'false', "_shards": {"total": 5, "successful": 5, "skipped": 0, "failed": 0}, "hits": {"total": 6, "max_score": 1.0, "hits": [{"_index": "address-book", "_type": "_doc", "_id": "5", "_score": 1.0, "_source": {"Name": "Oscar", "Phone": "7036569925", "Email": "oscar@gmail.com"}}, {"_index": "address-book", "_type": "_doc", "_id": "2", "_score": 1.0, "_source": {"Name": "Sabrina", "Phone": "5371368283", "Email": "sabrina@gmail.com"}}, {"_index": "address-book", "_type": "_doc", "_id": "4", "_score": 1.0, "_source": {"Name": "Jiay", "Phone": "2008207846", "Email": "jiay@gmail.com"}}, {"_index": "address-book", "_type": "_doc", "_id": "6", "_score": 1.0, "_source": {"Name": "Cat", "Phone": "3025409677", "Email": "cat@gmail.com"}}, {"_index": "address-book", "_type": "_doc", "_id": "1", "_score": 1.0, "_source": {"Name": "Alan", "Phone": "5647012772", "Email": "alan@gmail.com"}}, {"_index": "address-book", "_type": "_doc", "_id": "3", "_score": 1.0, "_source": {"Name": "Summer", "Phone": "5037683211", "Email": "summer@gmail.com"}}]}})

	


if __name__ == '__main__':
    unittest.main()