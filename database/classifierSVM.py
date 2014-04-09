#!/usr/bin/python
# -*- coding: utf-8 -*-

from sklearn import svm,datasets

from math import *
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
		allWordsFreq = dict()
		matrixWords = list()
		for tweet in tweets:
			str = ""
			str = str + tweet.contentRaw + " "
			comments = self.twitter.findCommentByTweetID(tweet.tweetID)
			for comment in comments:
				str = str + comment.contentRaw + " "
			# analyser le tweet et les commentaires
			# TODO: les bugs a corriger
			listWords = self.analysePhrase(str)
			matrixWords.append(listWords)
			for w in listWords:
				if w in allWordsFreq:
					allWordsFreq[w] = allWordsFreq[w]+1
				else:
					allWordsFreq[w] = 1
		allWordsFreqSortedKey = sorted(allWordsFreq,key=allWordsFreq.__getitem__,reverse=True)
		#print len(allWordsFreqSortedKey)
		
		map_TFIDF = self.TF_IDF(allWordsFreqSortedKey,matrixWords)
		print allWordsFreqSortedKey[0]
		print map_TFIDF[allWordsFreqSortedKey[0]]
		print allWordsFreqSortedKey[1]
		print map_TFIDF[allWordsFreqSortedKey[1]]
		print allWordsFreqSortedKey[2]
		print map_TFIDF[allWordsFreqSortedKey[2]]
		print allWordsFreqSortedKey[3]
		print map_TFIDF[allWordsFreqSortedKey[3]]
		print allWordsFreqSortedKey[4]
		print map_TFIDF[allWordsFreqSortedKey[4]]
		print allWordsFreqSortedKey[5]
		print map_TFIDF[allWordsFreqSortedKey[5]]
		print allWordsFreqSortedKey[6]
		print map_TFIDF[allWordsFreqSortedKey[6]]
		print allWordsFreqSortedKey[7]
		print map_TFIDF[allWordsFreqSortedKey[7]]
		print allWordsFreqSortedKey[8]
		print map_TFIDF[allWordsFreqSortedKey[8]]
		print allWordsFreqSortedKey[9]
		print map_TFIDF[allWordsFreqSortedKey[9]]
		print allWordsFreqSortedKey[10]
		
		#print map_TFIDF
		return
	
	# methode pour analyser une phrase 
	# enlever les mots non alphabet
	def analysePhrase(self,phrase):
		#print '*************Analyser Phrase******************'
		words = phrase.split()
		regex = re.compile(r'(\w)+')
		wordsReturn = list()
		for w in words:
			if w[0] is not '@' and w[0] is not'#':
				if w.find('/') is -1 and regex.match(w) is not None:
					ww = w.replace('.','').replace(',','').replace('!','').replace('?','')
					wordsReturn.append(ww)
			
				
		'''print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
		for w in wordsReturn:
			print w'''
	
		return wordsReturn

	# calculer les valeurs TF-IDF pour chaque mot par rappot un tweet
	def TF_IDF(self,keyWords,matrixTweetWords):
		print '*************TF-IDF******************'
		mapKeyWords_TFIDF = dict()
		for key in keyWords:
			TFs = list()
			nbTweetOccurrence = 0.0
			for tweet in matrixTweetWords:
				if key in tweet:
					nbTweetOccurrence = nbTweetOccurrence + 1.0
				TFs.append(tweet.count(key)/float(len(tweet)))
			TFs = [x*log(float(len(matrixTweetWords))/nbTweetOccurrence) for x in TFs]
			mapKeyWords_TFIDF[key] = TFs
		#print mapKeyWords_TFIDF
		return mapKeyWords_TFIDF
	
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
	
	