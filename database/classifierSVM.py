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
		
		#liste les mots apparaissant dans les tweets avec leur frequence. ex : mot 'toto', 5
		allWordsFreq = dict() 
		
		#liste de tableau de mots: un tableau de mots represente un tweet + commentaires
		matrixWords = list() 
		
		for tweet in tweets:
			str = ""
			str = str + tweet.contentRaw + " "
			comments = self.twitter.findCommentByTweetID(tweet.tweetID)
			for comment in comments:
				str = str + comment.contentRaw + " "
			# analyser le tweet et les commentaires
			# TODO: les bugs a corriger
				
			listWords = self.analysePhrase(str) # liste des mots du tweet analyse
			matrixWords.append(listWords)
			for w in listWords:
				if w in allWordsFreq:
					allWordsFreq[w] = allWordsFreq[w]+1
				else:
					allWordsFreq[w] = 1

		allWordsFreqSortedKey = sorted(allWordsFreq,key=allWordsFreq.__getitem__,reverse=True)
		
		print 'longueur mot cle: ',len(allWordsFreqSortedKey)
		print 'nb de tweet analyse: ',len(matrixWords)
		
		#calculer le poid TF-IDF
		map_TFIDF = self.TF_IDF(allWordsFreqSortedKey,matrixWords)
		
		mapExistanceWords = self.calculateExistanceWords(allWordsFreqSortedKey,matrixWords)
		
		# calculer le information gain pour chaque mot cle
		# afin de choisir celui qui apporte plus d'information
				
		# classe juste pour tester sans les donnees viens de base
		# 0 pour positif, 1 pour negatif, 2 pour neutre
		classe = [0,1,1,2,2,2,1,1,1,1,2,2,1,2,1,0,0]
		
		map_IG = self.informationGain(mapExistanceWords,classe)
		valueIGSortedKey = sorted(map_IG,key=map_IG.__getitem__,reverse=True)
		file = open('IG_values.txt','w')
		for k in valueIGSortedKey:
			file.write(k)
			file.write('\t\t')
			file.write(repr(map_IG[k]))
			file.write('\n')
		file.close()

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
					ww = w.replace('.','').replace(',','').replace('!','').replace('?','').replace('"','')
					wordsReturn.append(ww)	
		return wordsReturn

	# calculer les valeurs TF-IDF pour chaque mot par rappot un tweet
	# weight function
	# @keyWords tous les mots ordones par nombre d'occurence qui apparaitre: dictionnaire mot:frequence
	# @matrixTweetWords une liste de tweets avec chaque element(tweet) est une liste de mot dans ce tweet
	def TF_IDF(self,keyWords,matrixTweetWords):
		#print '*************TF-IDF******************'
		# un map avec mot comme cle et une liste des valeurs TF-IDF
		mapKeyWords_TFIDF = dict()
		for key in keyWords:
			TFs = list()
			nbTweetOccurrence = 0.0
			for tweet in matrixTweetWords:
				if key in tweet:
					nbTweetOccurrence = nbTweetOccurrence + 1.0
				TFs.append(tweet.count(key)/float(len(tweet))) # on stocke la division entre le nombre de fois d'un mot apparait dans le tweet analyse et nombre de mot dans de tweet
			TFs = [x*log(float(len(matrixTweetWords))/nbTweetOccurrence) for x in TFs] # len(matrixTweetWords): nombre de tweet analyse, nbTweetOccurrence: nombre de tweet qu'il existe le mot
			mapKeyWords_TFIDF[key] = TFs
		return mapKeyWords_TFIDF
		
	# cette methode retourne un map avec les mots comme cle
	# et le liste de boolean qui indique si le mot apparait dans chaque tweet analyse ou pas
	def calculateExistanceWords(self,keyWords,matrixTweetWords):
		mapExistanceWords = dict()
		for key in keyWords:
			existances = list()
			for tweet in matrixTweetWords:
				if key in tweet:
					existances.append(True)
				else:
					existances.append(False)
			mapExistanceWords[key] = existances
		return mapExistanceWords
	
	# methode pour calculer la valeurs information Gain pour chaque mot cle
	def informationGain(self,mapExistanceWords,classe):
		print '*************Information Gain******************'
		probClasse0 = float(classe.count(0))/float(len(classe))+pow(10, -20)
		probClasse1 = float(classe.count(1))/float(len(classe))+pow(10, -20)
		probClasse2 = float(classe.count(2))/float(len(classe))+pow(10, -20)
		entropyClass = -(probClasse0*log(probClasse0,2)+probClasse1*log(probClasse1,2)+probClasse2*log(probClasse2,2))
		map_IG = dict()
		for (keyWord,existances) in mapExistanceWords.items():
			classesWithKeyWord = list()
			classesWithoutKeyWord = list()
			counter = 0
			for e in existances:
				if e is False:
					classesWithoutKeyWord.append(classe[counter])
				else:
					classesWithKeyWord.append(classe[counter])
				counter = counter + 1
			
			probClasse0WithKeyWord = float(classesWithKeyWord.count(0))/float(len(classesWithKeyWord))+pow(10, -20)
			probClasse1WithKeyWord = float(classesWithKeyWord.count(1))/float(len(classesWithKeyWord))+pow(10, -20)
			probClasse2WithKeyWord = float(classesWithKeyWord.count(2))/float(len(classesWithKeyWord))+pow(10, -20)
			entropyClassWithKeyWord = -(probClasse0WithKeyWord*log(probClasse0WithKeyWord,2))
			entropyClassWithKeyWord = -(probClasse0WithKeyWord*log(probClasse0WithKeyWord,2)+probClasse1WithKeyWord*log(probClasse1WithKeyWord,2)+probClasse2WithKeyWord*log(probClasse2WithKeyWord,2))
			
			probClasse0WithoutKeyWord = float(classesWithoutKeyWord.count(0))/float(len(classesWithoutKeyWord))+pow(10, -20)
			probClasse1WithoutKeyWord = float(classesWithoutKeyWord.count(1))/float(len(classesWithoutKeyWord))+pow(10, -20)
			probClasse2WithoutKeyWord = float(classesWithoutKeyWord.count(2))/float(len(classesWithoutKeyWord))+pow(10, -20)
			entropyClassWithoutKeyWord = -(probClasse0WithoutKeyWord*log(probClasse0WithoutKeyWord,2)+probClasse1WithoutKeyWord*log(probClasse1WithoutKeyWord,2)+probClasse2WithoutKeyWord*log(probClasse2WithoutKeyWord,2))
			
			IG_value = entropyClass - entropyClassWithKeyWord - entropyClassWithoutKeyWord
			map_IG[keyWord] = IG_value
		return map_IG
	
	# construire le vecteur pour un tweet
	def rangeDataVector(self,tweet):
		return
		
	# construire la matrice des donnees apprentissage
	def	rangeDataMatrix(self,words):
		return
	
	# construire la model a partir les donnees d'apprentissage
	def buildModel(self):
		tweets = self.getDataApprentissage(0.02)
		# for each tweet
		# step1: analyseTweet
		# step2: rangeDataVector
		# step3: rangeDataMatrix
		
		'''#######test#######
		iris = datasets.load_iris()
		self.data = iris.data[:, :2]
		self.target = iris.target
		
		self.model = self.svm.fit(self.data,self.target)'''
		
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
	
	