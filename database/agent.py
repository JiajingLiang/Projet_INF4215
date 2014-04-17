#!/usr/bin/python
# -*- coding: utf-8 -*-

from classifierSVM import *
from data_storage import *
from twitter import *
import csv
import sys

db = DataStorage('localhost','root','','tweetdb')
twitter = Twitter(db,24744541)
classifier = ClassifierSVM('rbf',0.2,100,twitter)

if len(sys.argv) < 2:
	print 'No parameter specified.'
elif sys.argv[1] == '-buildmodel':
	classifier.buildModel()
	print 'Model Built'
elif sys.argv[1] == '-predict':
	if len(sys.argv) == 3:
		fileName = sys.argv[2]
		listTweetsToPredict = list()
		with open(fileName,'rb') as csvFile:
			reader = csv.reader(csvFile,delimiter=',')
			tweet = ""
			for row in reader:
				if row[0] == 'tweet':
					if tweet is not "":
						listTweetsToPredict.append(tweet)
					tweet = row[1] + " "				
				elif row[0] == 'comment':
					tweet = tweet + row[1] + " "
			listTweetsToPredict.append(tweet)
		#print len(listTweetsToPredict)
		classe = classifier.predictEmotion(listTweetsToPredict)
		print 'prediction: '
		counter = 1
		for c in classe:
			if c == 0:
				print 'Tweet ',counter,' : positive'
			elif c == 1:
				print 'Tweet ',counter,' : negative'
			else:
				print 'Tweet ',counter,' : neutre'
			counter = counter + 1
	else:
		print 'No file input specified'
else:
	print 'Unknown option'
	
sys.exit()