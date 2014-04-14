#!/usr/bin/python
# -*- coding: utf-8 -*-

from tweet import *
from comment import *
from dictionnary import *

class Twitter:
	"""docstring for Twitter"""
	def __init__(self, db,accountId):
		self.db = db
		self.accountID = accountId

	# Recherche d'un tweet par son identifiant
	def findTweetByID(self, tweetID):
		query = """SELECT * FROM Tweets WHERE TweetID = %s"""
		params = (tweetID)
		row = self.db.executeQueryWithSingleResult(query,params)
		return self.__generateTweet(row)

	# Récupérer un tweet qui est dans l'état non traité
	def getTweetUntreated(self):
		query = """SELECT * FROM Tweets WHERE Treated = 0 AND AccountFK = %s LIMIT 1"""
		params = (self.accountID)
		row = self.db.executeQueryWithSingleResult(query,params)
		return self.__generateTweet(row)
		
	def getTweetsTreated(self):
		query = "SELECT * FROM Tweets WHERE Treated = 1 AND AccountFK = %s"
		params = (self.accountID)
		rows = self.db.executeQueryWithMultipleResults(query,params)
		tweets = list()
		for row in rows:
			tweets.append(self.__generateTweet(row))
		return tweets

	# Recherche des commentaires associés à un tweet
	def findCommentByTweetID(self, tweetID):
		query = "SELECT * FROM Comments WHERE TweetFK = %s"
		params = (tweetID)
		rows = self.db.executeQueryWithMultipleResults(query,params)
		comments = list()
		for row in rows:
			comments.append(self.__generateComment(row))

		return comments
		
	def findNbTweets(self):
		query = "SELECT COUNT(*) FROM Tweets WHERE AccountFK = %s"
		params = (self.accountID)
		row = self.db.executeQueryWithSingleResult(query,params)
		return row[0]

	# Charger le dictionnaire 
	def loadDictionnary(self):
		query = "SELECT * FROM Dictionnary"
		rows = self.db.executeQueryWithMultipleResults(query)
		dictionnary = list()
		for row in rows:
			dictionnary.append(self.__generateDictionnary(row))

		return dictionnary

	# Marquer un tweet comme étant traité
	def markTweetAsTreated(self, tweetID):
		query = "UPDATE Tweets SET Treated = 1 WHERE TweetID = %s"
		params = (tweetID)
		self.db.executeQueryModifyingDatabase(query,params)

	def __generateTweet(self,row):
		return Tweet(row[0],row[1],row[2],row[3],row[4],row[5],row[6])

	def __generateComment(self,row):
		return Comment(row[0],row[1],row[2],row[3],row[4])

	def __generateDictionnary(self,row):
		return Dictionnary(row[0],row[1],row[2],row[3])