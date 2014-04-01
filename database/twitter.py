#!/usr/bin/python
# -*- coding: utf-8 -*-

from tweet import *
from comment import *
from dictionnary import *

class Twitter:
	"""docstring for Twitter"""
	def __init__(self, db):
		self.db = db

	def findTweetByID(self, tweetID):
		query = """SELECT * FROM Tweets WHERE TweetID = %s"""
		params = (tweetID)
		row = self.db.executeQueryWithSingleResult(query,params)
		return self.__generateTweet(row)

	def getTweetUntreated(self):
		query = """SELECT * FROM Tweets WHERE Treated = 0 LIMIT 1"""
		row = self.db.executeQueryWithSingleResult(query)
		return self.__generateTweet(row)

	def findCommentByTweetID(self, tweetID):
		query = "SELECT * FROM Comments WHERE TweetFK = %s"
		params = (tweetID)
		rows = self.db.executeQueryWithMultipleResults(query,params)
		comments = list()
		for row in rows:
			comments.append(self.__generateComment(row))

		return comments

	def loadDictionnary(self):
		query = "SELECT * FROM Dictionnary"
		rows = self.db.executeQueryWithMultipleResults(query)
		dictionnary = list()
		for row in rows:
			dictionnary.append(self.__generateDictionnary(row))

		return dictionnary

	def markTweetAsTreated(self, tweetID):
		query = "UPDATE Tweets SET Treated = 1 WHERE TweetID = %s"
		params = (tweetID)
		self.db.executeQueryModifyingDatabase(query,params)

	def __generateTweet(self,row):
		return Tweet(row[0],row[1],row[2],row[3],row[4],row[5])

	def __generateComment(self,row):
		return Comment(row[0],row[1],row[2],row[3],row[4])

	def __generateDictionnary(self,row):
		return Dictionnary(row[0],row[1],row[2],row[3])