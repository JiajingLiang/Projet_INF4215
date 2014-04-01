#!/usr/bin/python
# -*- coding: utf-8 -*-

from data_storage import *
from twitter import *



db = DataStorage('localhost','root','erperra4','twitter')

twitter = Twitter(db)

tweet = twitter.findTweetByID(371648193660190720)
tweet.show()

comments = twitter.findCommentByTweetID(tweet.tweetID)
for comment in comments:
	comment.show()

#twitter.markTweetAsTreated(347242449497907200)

dictionnary = twitter.loadDictionnary()
for word in dictionnary:
	word.show()

db.close()