#!/usr/bin/python
# -*- coding: utf-8 -*-

from classifierSVM import *
from data_storage import *
from twitter import *

db = DataStorage('localhost','root','','twitter')
twitter = Twitter(db,24744541)
classifier = ClassifierSVM('rbf',0.2,5,twitter)
classifier.buildModel()

tweetsToPredict = list()
phrase = ""
t = twitter.findTweetByID(453166520223682561)
phrase = phrase + t.contentRaw + " "
comments = twitter.findCommentByTweetID(t.tweetID)
for comment in comments:
	phrase = phrase + comment.contentRaw + " "
print phrase
tweetsToPredict.append(phrase)

phrase = ""
t = twitter.findTweetByID(453140547688222720)
phrase = phrase + t.contentRaw + " "
comments = twitter.findCommentByTweetID(t.tweetID)
for comment in comments:
	phrase = phrase + comment.contentRaw + " "
print phrase	
tweetsToPredict.append(phrase)

print classifier.predictEmotion(tweetsToPredict)
