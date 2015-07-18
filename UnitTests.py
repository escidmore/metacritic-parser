#!/usr/bin/env python3
import unittest
import MetacriticParser
import json
import flask
import sys

class PrimesTestCase(unittest.TestCase):
	"""Tests for MetacriticParser.py"""
	
	def test_can_get_raw_list(self):
		"""Can I successfully retrieve a raw list of scores using the exposed method?"""
		#num_games should be set to the number of games available on the URL being parsed
		#at the time of this writing, there was only one game returned
		num_games = 1
		url = "http://www.metacritic.com/game/playstation-3"
		
		test_scores = MetacriticParser.scores(url)
		score_list = test_scores.get_products_and_scores()
		
		self.assertTrue(len(score_list)==num_games)
    
	def test_can_fetch_ps3_all(self):
		"""Can I successfully retrieve PS3 scores """
		#num_games should be set to the number of games available on the URL being parsed
		#at the time of this writing, there was only one game returned
		num_games = 1
		url = "http://www.metacritic.com/game/playstation-3"

		returned_resp = MetacriticParser.get_all_ps3_scores()
		returned_data = returned_resp.data.decode()
		decoded_json = json.loads(returned_data)
		self.assertTrue(len(decoded_json)==num_games)

    
	def test_can_get_ps3_title(self):
		"""Can I successfully retrieve the score for Steins;Gate (the only ps3 game)"""
		#game_name should be the title of any game from the url
		game_name = "Steins;Gate"
		url = "http://www.metacritic.com/game/playstation-3"
			
		returned_resp = MetacriticParser.get_title_ps3_scores(game_name)
		returned_data = returned_resp.data.decode()
		decoded_json = json.loads(returned_data)
		
		returned_name = decoded_json['title']
		self.assertTrue(returned_name==game_name)
		
	def test_can_fetch_ps4_all(self):
		"""Can I successfully retrieve PS3 scores """
		#num_games should be set to the number of games available on the URL being parsed
		#at the time of this writing, there was only one game returned
		num_games = 10
		url = "http://www.metacritic.com/game/playstation-4"

		returned_resp = MetacriticParser.get_all_ps4_scores()
		returned_data = returned_resp.data.decode()
		decoded_json = json.loads(returned_data)
		self.assertTrue(len(decoded_json)==num_games)

    
	def test_can_get_ps4_title(self):
		"""Can I successfully retrieve the score for a top 10 game?"""
		#game_name should be the title of any game from the url
		game_name = "The Witcher 3: Wild Hunt"
		url = "http://www.metacritic.com/game/playstation-4"
			
		returned_resp = MetacriticParser.get_title_ps4_scores(game_name)
		returned_data = returned_resp.data.decode()
		decoded_json = json.loads(returned_data)
		
		returned_name = decoded_json['title']
		self.assertTrue(returned_name==game_name)
		
	def test_invalid_ps3_title(self):
		"""Verify correct behavior when asking for an invalid PS3 title"""
		#game_name should be the title of any game from the url
		game_name = "Transistor 2"
		url = "http://www.metacritic.com/game/playstation-3"
		
		exep = ""
		try:	
			returned_resp = MetacriticParser.get_title_ps3_scores(game_name)
		except:
			exep = sys.exc_info()[0]
		
		exep = str(exep)
		self.assertTrue(exep=="<class 'werkzeug.exceptions.NotFound'>")
		
	def test_invalid_ps4_title(self):
		"""Verify correct behavior when asking for an invalid PS4 title"""
		#game_name should be the title of any game from the url
		game_name = "Transistor 2"
		url = "http://www.metacritic.com/game/playstation-4"
		
		exep = ""
		try:	
			returned_resp = MetacriticParser.get_title_ps4_scores(game_name)
		except:
			exep = sys.exc_info()[0]
		
		exep = str(exep)
		self.assertTrue(exep=="<class 'werkzeug.exceptions.NotFound'>")

	def test_404_handler(self):
		"""Verify whether the 404 error handler returns correctly"""
		
		returned_resp = MetacriticParser.not_found(404)
		returned_data = returned_resp.data.decode()
		decoded_json = json.loads(returned_data)
		
		self.assertTrue(decoded_json['error']=="Not Found")
		
if __name__ == '__main__':
    unittest.main()
