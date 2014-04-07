#!/usr/bin/python
# -*- coding: utf-8 -*-

from data_storage import *
from twitter import *



db = DataStorage('localhost','root','','twitter')

twitter = Twitter(db,24744541)

tweet = twitter.findTweetByID(371648193660190720)
tweet.show()


#comments = twitter.findCommentByTweetID(tweet.tweetID)
#for comment in comments:
#	comment.show()

print '#############################'	
tweet =  twitter.getTweetUntreated()
tweet.show()

print twitter.findNbTweets()

#twitter.markTweetAsTreated(347242449497907200)

print '*****************************'
dictionnary = twitter.loadDictionnary()
for word in dictionnary:
	word.show()

db.close()