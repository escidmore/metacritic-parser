#!/usr/bin/python3
from json import dumps
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from flask import Flask, abort, make_response, Response, jsonify

#Changing host here will specify a different IP address to listen on
#Setting it to 0.0.0.0 will make it listen on all available IP addresses
#Make sure this value is in "quotes"
host = "127.0.0.1"
#Defines the port number that the application will listen on.
port = 5000

class scores:
	"""A list of titles and scores parsed from a metacritic page.  A set of scores has the following attributes:
	
	* url: the URL that the scores were pulled from
	* scores: a list of dictionaries, with each dictionary containing:
			title: the name of the game
			score: the metacritic score of the game
		
	The following methods are exposed:
	
	
	* json_all_scores(): returns a json dump of all titles & scores retrieved from url
	* json_score(title): returns a json dump of the title & score specified as title.  Returns None if not valid
	* get_products_and_scores(): returns a list of dictionaries containing the titles and scores. 
	NOTE: self.scores is populated with get_products_and_scores(), so that method usually won't be called directly
	"""		
	
	url=""
	scores=[]
	def __init__(self, url):
		"""Return a scores object with url set to *url* and scores set by the parser"""
		self.url = url
		self.scores = self.get_products_and_scores()
	
	def _fetch_url(self,useragent="Mozilla/5.0",referrer="None"):
		"""Opens self.url and returns all data read from it.  
		Optionally allows defining useragent and referrer (in case we decide to expand this later), 
		but assumes default values that metacritic doesn't reject"""
		
		req = Request(self.url)
		req.add_header('User-Agent', useragent)
		req.add_header('Referrer', referrer)
		response = urlopen(req)
		return(response.read())	
	
	def get_products_and_scores(self):
		"""Parses HTML contents for the data we're interested in, 
		then returns a list of dictionaries containing the results"""
		
		html_contents=self._fetch_url()
		products_and_scores=[]
		soup = BeautifulSoup(html_contents, 'html.parser')
		products_html = soup.find_all("li",{"class": "has_small_image"})
		for product_html in products_html:
			product_title_header = product_html.find("h3",{"class": "product_title"})
			product_title = product_title_header.get_text()
			product_score_span = product_html.find("span",{"class": "metascore_w"})
			product_score = product_score_span.get_text()
			products_and_scores.append({"title": product_title, "score": product_score})
		return(products_and_scores)
	
	def json_all_scores(self):
		"""Processes self.scores and returns all of them in the json format that we want"""
		
		return(dumps(self.scores, indent=4, separators=(',', ': '), sort_keys=False))
	
	def json_score(self, title):
		"""When given a specific title, will return the title and its score in json format.
		If the title it's given is not valid, it returns None"""
		
		for product in self.scores:
				if product['title'] == title:
					return(dumps(product, indent=4, separators=(',', ': '), sort_keys=False))
		return None
 

app = Flask(__name__)

@app.route('/games', methods=['GET'])
def get_all_ps3_scores():
	"""returns json scores for all playstation 3 games"""
	score_set = scores("http://www.metacritic.com/game/playstation-3")
	return(Response(score_set.json_all_scores(),mimetype='application/json'))

@app.route('/games/<path:title>', methods=['GET'])
def get_title_ps3_scores(title):
	"""returns json scores for one ps3 game, or an error if invalid"""
	score_set = scores("http://www.metacritic.com/game/playstation-3")
	this_score=score_set.json_score(title)
	if this_score != None:
		return(Response(this_score,mimetype='application/json'))
	else:
		abort(404)

@app.route('/PS4games', methods=['GET'])
def get_all_ps4_scores():
	"""returns json scores for all playstation 3 games"""
	score_set = scores("http://www.metacritic.com/game/playstation-4")
	return(Response(score_set.json_all_scores(),mimetype='application/json'))
		
@app.route('/PS4games/<path:title>', methods=['GET'])
def get_title_ps4_scores(title):
	"""returns json scores for one ps4 game, or an error if invalid"""
	score_set = scores("http://www.metacritic.com/game/playstation-4")
	this_score=score_set.json_score(title)
	if this_score != None:
		return(Response(this_score,mimetype='application/json'))
	else:
		abort(404)
		
@app.errorhandler(404)
def not_found(error):
	return Response(dumps({'error': 'Not Found'},indent=4, separators=(',', ': ')), mimetype='application/json', status='404')

if __name__ == '__main__':
	port = int(port)
	app.run(debug=True,host=host,port=port)
