#!/usr/bin/python
# -*- coding: utf-8 -*-

from sklearn import svm,datasets,cross_validation
from sklearn.externals import joblib

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
		
	# methode pour recuperer les donnees pour contruire le modele
	# il va retourne un map avec un cle 'keyWords' : une liste des mots cles
	# un cle 'data': une matrice presente les valeurs TFIDF pour chaque tweets
	# un cle 'target': une liste presente les classe de chaque tweet
	def getDataForModelBuilding(self,nbTweets):		
		tweets = self.twitter.getTweets(nbTweets)
		
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
		
		#calculer le poid TF-IDF
		map_TFIDF = self.TF_IDF(allWordsFreqSortedKey,matrixWords)
		
		mapExistanceWords = self.calculateExistanceWords(allWordsFreqSortedKey,matrixWords)
		
		# calculer le information gain pour chaque mot cle
		# afin de choisir celui qui apporte plus d'information
				
		# classe juste pour tester sans les donnees viens de base
		# 0 pour positif, 1 pour negatif, 2 pour neutre
		print 'nbTweets : ',nbTweets
		classe = [0,1,1,2,2,2,1,1,1,1,2,2,1,2,1,0,0]
		
		map_IG = self.informationGain(mapExistanceWords,classe)
		
		
		# ecrire les valeur de gain dans un ficher pour debug
		'''valueIGSortedKey = sorted(map_IG,key=map_IG.__getitem__,reverse=True)
		file = open('IG_values.txt','w')
		for k in valueIGSortedKey:
			file.write(k)
			file.write('\t\t')
			file.write(repr(map_IG[k]))
			file.write('\n')
		file.close()'''
		
		data_Matrix = self.rangeDataMatrix(map_TFIDF,map_IG,-0.03)
		# on ajoute un cle 'target' pour dire chaque tweet est de quelle classe
		data_Matrix['target'] = classe		

		return data_Matrix
	
	# methode pour analyser une phrase 
	# enlever les mots non alphabet
	def analysePhrase(self,phrase):
		#print '*************Analyser Phrase******************'
		phrase = re.sub("((http:\/\/|https:\/\/)?(www.)?(([a-zA-Z0-9-]){2,}\.){1,4}([a-zA-Z]){2,6}(\/([a-zA-Z-_\/\.0-9#:?=&;,]*)?)?)",'',phrase)
		phrase = re.sub("(,|!|\.|;|:|\?|\(|\)|\/|\\\\|\[|\]|{|}|\")",'',phrase)
		words = phrase.split()

		wordsReturn = list()
		for w in words:
			w = w.lower()
			if w[0] is '@' or w[0] is '#': continue
			if w not in ['le','la','les',"l'",'de','des',"d'",'que','qui','mais','ou','et','donc','or','ni','car','dont','ne','pas']:
				wordsReturn.append(w.decode('latin-1'))	
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
			mapKeyWords_TFIDF[key] = TFs #on map pour chaque mot la pertinence obtenu pour chaque tweet
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
		#print '*************Information Gain******************'
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
			entropyClassWithKeyWord = -(probClasse0WithKeyWord*log(probClasse0WithKeyWord,2)+probClasse1WithKeyWord*log(probClasse1WithKeyWord,2)+probClasse2WithKeyWord*log(probClasse2WithKeyWord,2))
			
			probClasse0WithoutKeyWord = float(classesWithoutKeyWord.count(0))/float(len(classesWithoutKeyWord))+pow(10, -20)
			probClasse1WithoutKeyWord = float(classesWithoutKeyWord.count(1))/float(len(classesWithoutKeyWord))+pow(10, -20)
			probClasse2WithoutKeyWord = float(classesWithoutKeyWord.count(2))/float(len(classesWithoutKeyWord))+pow(10, -20)
			entropyClassWithoutKeyWord = -(probClasse0WithoutKeyWord*log(probClasse0WithoutKeyWord,2)+probClasse1WithoutKeyWord*log(probClasse1WithoutKeyWord,2)+probClasse2WithoutKeyWord*log(probClasse2WithoutKeyWord,2))
			
			IG_value = entropyClass - entropyClassWithKeyWord - entropyClassWithoutKeyWord
			map_IG[keyWord] = IG_value
		return map_IG
			
	# construire la matrice des donnees apprentissage
	# il va retourne un map avec un cle 'keyWords' : une liste des mots cles
	# un cle 'data': une matrice presente les valeurs TFIDF pour chaque tweets
	def	rangeDataMatrix(self,map_TFIDF,map_IG,threshold):
		#print '*************rangeDataMatrix******************'
		# supprimer les mots cles dont le gain est plus petit que un seuil
		for (keyWord,IG_value) in map_IG.items():
			if IG_value < threshold:
				map_TFIDF.pop(keyWord)
				
		# ranger la matrice de data
		nbTweets = len(map_TFIDF.itervalues().next())
		tweets_Matrix = list()
		keyWords = list()
		for i in range(nbTweets):#Pour chaque tweet ...
			tweet_TFIDF_values = list()
			for (keyWord,TFIDF_value) in map_TFIDF.items():# ... pour chaque mot ...
				tweet_TFIDF_values.append(TFIDF_value[i])# ... on recupère la pertinence du mot pour le tweet i ...
				if i is 0:
					keyWords.append(keyWord)# ... on ajoute le mot dans la list keyWords ...
			tweets_Matrix.append(tweet_TFIDF_values)# ... et on ajoute la liste de pertinence des mots de keyWords pour chaque tweet
		
		data_Matrix = dict()
		data_Matrix['keyWords'] = keyWords# Liste de mots
		data_Matrix['data'] = tweets_Matrix#Liste de tweet ou chaque tweet correspond à la liste de pertinence des mots definis par keyWords
		
		return data_Matrix
	
	# construire la model a partir les donnees d'apprentissage
	def buildModel(self):
		dataTweets = self.getDataForModelBuilding(17)
		print 'nb mots cles choisit: ',len(dataTweets['keyWords'])
		print 'nb de tweet analyse: ',len(dataTweets['target'])
		
		#######apprentissage et test -- cross validation #######		
		#self.model = self.svm.fit(dataTweets['data'],dataTweets['target'])
		data_train,data_test,target_train,target_test = cross_validation.train_test_split(dataTweets['data'], dataTweets['target'], test_size=0.4, random_state=0)
		self.svm.fit(data_train,target_train)
		
		#------- TEST load -------
		joblib.dump(self.svm,"tweetsModel.pkl")
		self.model = joblib.load("tweetsModel.pkl")
		print 'score : ',self.model.score(data_test,target_test)
		
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
	
	