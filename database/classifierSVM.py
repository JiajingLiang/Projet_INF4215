# -*- coding: utf-8 -*-

from sklearn import svm,datasets

import numpy as np
import re

class ClassifierSVM():
	def __init__(self,kernelFuncName,g,c,twitter):
		self.svm = svm.SVC(kernel = kernelFuncName,gamma=g,C=c)
		# twitter: DB Connnector
		self.twitter = twitter
		self.data = []
		self.target = []
		self.model = None
		
	# methode pour construire les donnees d'apprentissage
	# ratio: rapport sur l'ensemble de donnee d'apprentissage
	def getDataApprentissage(self,ratio):
		nbApprentissage = int(round(self.twitter.findNbTweets()*ratio));
		tweets = self.twitter.getSeveralTweetsUntreated(nbApprentissage)
		for tweet in tweets:
			print '************'
			#print tweet.contentRaw
			self.analysePhrase(tweet.contentRaw)
			comments = self.twitter.findCommentByTweetID(tweet.tweetID)
			#for comment in comments:
				#print '#############'
				#print comment.contentRaw
				#self.analysePhrase(comment.contentRaw)
		return
	
	# methode pour analyser une phrase afin de construire X
	def analysePhrase(self,phrase):
		words = phrase.split()
		#regex = re.compile('^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$')
		for w in words:
			if w[0] == '@' or w[0] == '#':
				words.remove(w)
			if w.find('/') != -1:
				words.remove(w)
		for w in words:
			print w
	
		return		
	
	# construire le vecteur pour un tweet
	def rangeDataVector(self,tweet):
		return
		
	# construire la matrice des donnees apprentissage
	def	rangeDataMatrix(self,words):
		return
	
	# construire la model a partir les donnees d'apprentissage
	def buildModel(self):
		tweets = self.getDataApprentissage(0.4)
		# for each tweet
		# step1: analyseTweet
		# step2: rangeDataVector
		# step3: rangeDataMatrix
		
		#######test#######
		iris = datasets.load_iris()
		self.data = iris.data[:, :2]
		self.target = iris.target
		
		self.model = self.svm.fit(self.data,self.target)
		
		return
		
	# predire l'emotion transmit d'un tweet
	def	predictEmotion(self,tweet):
		#######test#######
		h = .02
	
		x_min, x_max = self.data[:, 0].min() - .5, self.data[:, 0].max() + .5
		y_min, y_max = self.data[:, 1].min() - .5, self.data[:, 1].max() + .5
		xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
		Z = self.model.predict(np.c_[xx.ravel(), yy.ravel()])

		
		return
	
	