#!/usr/bin/python
# -*- coding: utf-8 -*-

from sklearn import svm,datasets,cross_validation
from sklearn.externals import joblib

from math import *
import numpy as np
import re
import pickle
from nltk import stem

pattern = "erais$|erait$|erions$|eriez$|eraient$|irais$|irait$|irions$|iriez$|iraient$|oir$|aitre$|ssons$|ssez$|ssent$|cs$|c$|quons$|quez$|quent$|ais$|ait$|ions$|iez$|aient$|e$|es$|ons$|ez$|ent$|s$|t$|ai$|as$|a$|erent$|irent$|us$|ut$|erai$|eras$|era$|erons$|erez$|eront$|irai$|iras$|ira$|irons$|irez$|iront$|rai$|ras$|ra$|rons$|rez$|ront$|er$|ir$|ant$|ée$|ées$|ie$|is$|ies$|u$|ue$|us$|ues$|i$|ses$|se$|te$|ts$|tes$|é$|"

class ClassifierSVM():
	def __init__(self,kernelFuncName,g,c,twitter):
		self.svm = svm.SVC(kernel = kernelFuncName,gamma=g,C=c)
		# twitter: DB Connnector
		self.twitter = twitter
		self.model = None
		
	# methode pour recuperer les donnees pour contruire le modele
	# il va retourne un map avec un cle 'keyWords' : une liste des mots cles
	# un cle 'data': une matrice presente les valeurs TFIDF pour chaque tweets
	# un cle 'classes': une liste presente les classe de chaque tweet
	def getDataForModelBuilding(self,nbTweets):		
		tweets = self.twitter.getTweets(nbTweets)
		
		#liste les mots apparaissant dans les tweets avec leur frequence. ex : mot 'toto', 5
		allWordsFreq = dict() 
		
		#liste de tableau de mots: un tableau de mots represente un tweet + commentaires
		matrixWords = list() 
		classe = list()
		for tweet in tweets:
			if tweet.meaning is 'POSITIVE':
				classe.append(0)
			elif tweet.meaning is 'NEGATIVE':
				classe.append(1)
			else:
				classe.append(2)
			str = ""
			str = str + tweet.contentRaw + " "
			
			comments = self.twitter.findCommentByTweetID(tweet.tweetID)
			for comment in comments:
				str = str + comment.contentRaw + " "
				
			# analyser le tweet et les commentaires				
			listWords = self.analysePhrase(str) # liste des mots du tweet analyse
			matrixWords.append(listWords)
			for w in listWords:
				if w in allWordsFreq:
					allWordsFreq[w] = allWordsFreq[w]+1
				else:
					allWordsFreq[w] = 1

		allWordsFreqSortedKey = sorted(allWordsFreq,key=allWordsFreq.__getitem__,reverse=True)
				
		#calculer le poid TF-IDF
		map_TFIDF = self.TF_IDF(allWordsFreqSortedKey,matrixWords)
		
		# Map ou key = mot et value = liste qui détermine si le mot est présent dans chaque tweet... ou pas (True,False) 
		mapExistanceWords = self.calculateExistanceWords(allWordsFreqSortedKey,matrixWords)
				
		# classe juste pour tester sans les donnees viens de base
		# 0 pour positif, 1 pour negatif, 2 pour neutre
		print classe
		classe = [0,1,1,2,2,2,1,1,1,1,2,2,1,2,1,0,0,1,0,1]
		
		# calculer le information gain pour chaque mot cle
		# afin de choisir celui qui apporte plus d'information
		map_IG = self.informationGain(mapExistanceWords,classe)
			
		'''# ecrire les valeur de gain dans un ficher pour debug
		valueIGSortedKey = sorted(map_IG,key=map_IG.__getitem__,reverse=True)
		file = open('IG_values.txt','w')
		for k in valueIGSortedKey:
			file.write(k)
			file.write('\t\t')
			file.write(repr(map_IG[k]))
			file.write('\n')
		file.close()'''
		
		data_Matrix = self.rangeDataMatrix(map_TFIDF,map_IG,-0.03)
		# on ajoute un cle 'classes' pour dire chaque tweet est de quelle classe
		data_Matrix['classes'] = classe
		data_Matrix['existanceWords'] = mapExistanceWords

		return data_Matrix
	
	# methode pour analyser une phrase 
	# enlever les mots non alphabet
	def analysePhrase(self,phrase):
		#print '*************Analyser Phrase******************'
		phrase = re.sub("((http:\/\/|https:\/\/)?(www.)?(([a-zA-Z0-9-]){2,}\.){1,4}([a-zA-Z]){2,6}(\/([a-zA-Z-_\/\.0-9#:?=&;,]*)?)?)",'',phrase)
		phrase = re.sub("(,|!|\.|;|:|\?|\(|\)|\/|\\\\|\[|\]|{|}|\")",'',phrase)
		words = phrase.split()
		stemmer = stem.RegexpStemmer(pattern)
		wordsReturn = list()
		for w in words:
			w = w.lower()
			if w[0] is '@' or w[0] is '#': continue
			if w not in ['le','la','les',"l'",'de','des',"d'",'que','qui','ou','et','dont','je','tu','il','nous','vous','ils']:
				w = w.decode('latin-1').encode('utf-8')
				w = stemmer.stem(w)
				wordsReturn.append(w)	
		return wordsReturn

	# calculer les valeurs TF-IDF pour chaque mot par rappot un tweet
	# weight function
	# @keyWords tous les mots ordones par nombre d'occurence qui apparaitre: dictionnaire mot:frequence
	# @matrixTweetWords une liste de tweets avec chaque element(tweet) est une liste de mot dans ce tweet
	def TF_IDF(self,keyWords,matrixTweetWords):
		#print '*************TF-IDF******************'
		# Map avec key = mot, value = une liste de valeurs TF-IDF
		mapKeyWords_TFIDF = dict()
		for key in keyWords:# Pour chaque mot...
			TFs = list()
			nbTweetOccurrence = 0.0
			for tweet in matrixTweetWords:# ...On parcourt les tweets...
				if key in tweet:# ...Si le mot étudié est dans le tweet étudié...
					nbTweetOccurrence = nbTweetOccurrence + 1.0
				TFs.append(tweet.count(key)/float(len(tweet))) # On calcule la fréquence du mot dans le tweet analysé
			TFIDF = [x*log(float(len(matrixTweetWords))/nbTweetOccurrence) for x in TFs] # On calcule l'importance du mot dans l'ensemble des tweets (idf) et on le multiplie avec le TF afin d'obtenir le poids du mot dans chaque tweet
			mapKeyWords_TFIDF[key] = TFIDF #on map pour chaque mot la pertinence obtenue pour chaque tweet
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
		# Calcul de l'entropie des classes (POSITIVE,NEGATIVE,NEUTRAL)
		entropyClass = -(probClasse0*log(probClasse0,2)+probClasse1*log(probClasse1,2)+probClasse2*log(probClasse2,2))
		map_IG = dict()
		for (keyWord,existances) in mapExistanceWords.items():# Pour chaque mot
			classesWithKeyWord = list()
			classesWithoutKeyWord = list()
			counter = 0
			for e in existances:
				if e is False:# Si le mot n'apparait pas dans le tweet
					classesWithoutKeyWord.append(classe[counter])
				else:
					classesWithKeyWord.append(classe[counter])
				counter = counter + 1

			probakeyWordExiste = len(classesWithKeyWord)/(len(classesWithKeyWord)+len(classesWithoutKeyWord))
			probakeyWordNonExiste = len(classesWithoutKeyWord)/(len(classesWithKeyWord)+len(classesWithoutKeyWord))
			
			probClasse0WithKeyWord = float(classesWithKeyWord.count(0))/float(len(classesWithKeyWord))+pow(10, -20)
			probClasse1WithKeyWord = float(classesWithKeyWord.count(1))/float(len(classesWithKeyWord))+pow(10, -20)
			probClasse2WithKeyWord = float(classesWithKeyWord.count(2))/float(len(classesWithKeyWord))+pow(10, -20)
			entropyClassWithKeyWord = -(probClasse0WithKeyWord*log(probClasse0WithKeyWord,2)+probClasse1WithKeyWord*log(probClasse1WithKeyWord,2)+probClasse2WithKeyWord*log(probClasse2WithKeyWord,2))
			
			probClasse0WithoutKeyWord = float(classesWithoutKeyWord.count(0))/float(len(classesWithoutKeyWord))+pow(10, -20)
			probClasse1WithoutKeyWord = float(classesWithoutKeyWord.count(1))/float(len(classesWithoutKeyWord))+pow(10, -20)
			probClasse2WithoutKeyWord = float(classesWithoutKeyWord.count(2))/float(len(classesWithoutKeyWord))+pow(10, -20)
			entropyClassWithoutKeyWord = -(probClasse0WithoutKeyWord*log(probClasse0WithoutKeyWord,2)+probClasse1WithoutKeyWord*log(probClasse1WithoutKeyWord,2)+probClasse2WithoutKeyWord*log(probClasse2WithoutKeyWord,2))
			
			IG_value = entropyClass - probakeyWordExiste*entropyClassWithKeyWord - probakeyWordNonExiste*entropyClassWithoutKeyWord
			map_IG[keyWord] = IG_value
		return map_IG
			
	# construire la matrice des données apprentissage
	# il va retourne un map avec une clé 'keyWords' : une liste des mots clés
	# une clé 'data': une matrice présente les valeurs TFIDF pour chaque tweets
	def	rangeDataMatrix(self,map_TFIDF,map_IG,threshold):
		#print '*************rangeDataMatrix******************'
		# supprimer les mots cles dont le gain est plus petit qu'un seuil
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
		data_Matrix['data'] = tweets_Matrix#Liste de tweets ou chaque tweet correspond à la liste de pertinence des mots definis par keyWords
		
		return data_Matrix
	
	# construire la model a partir les donnees d'apprentissage
	def buildModel(self):
		dataTweets = self.getDataForModelBuilding(20)
		print 'nb mots cles choisit: ',len(dataTweets['keyWords'])
		print 'nb de tweet analyse: ',len(dataTweets['classes'])
		
		#######apprentissage et test -- cross validation #######		
		#self.model = self.svm.fit(dataTweets['data'],dataTweets['classes'])
		
		data_train,data_test,target_train,target_test = cross_validation.train_test_split(dataTweets['data'], dataTweets['classes'], test_size=0.4, random_state=0)
		self.model = self.svm.fit(data_train,target_train)
		
		#------- TEST load -------
		joblib.dump(self.model,"tweetsModel.pkl")
		self.model = joblib.load("tweetsModel.pkl")
		print 'score : ',self.model.score(data_test,target_test)

		joblib.dump(dataTweets,"dataTweets.pkl")
		return
		
	# predire l'emotion transmit des tweets
	def	predictEmotion(self,tweetsToPredict):
		self.model = joblib.load("tweetsModel.pkl")
		data = joblib.load("dataTweets.pkl")
		
		mapExistanceWords = data['existanceWords']
		keyWords = data['keyWords']
		allTFIDFs = list()
		# pour chaque tweet a predire
		for tweet in tweetsToPredict:
			#analyser la phrase
			listWords = self.analysePhrase(tweet)
			# calculer les valeurs TFIDF
			TFIDF = list()
			for keyWord in keyWords:
				TF = float(listWords.count(keyWord))/len(listWords)
				IDF = log(float(len(mapExistanceWords[keyWord]))/mapExistanceWords[keyWord].count(True))
				TFIDF.append(TF*IDF)
			allTFIDFs.append(TFIDF)
		
		return self.model.predict(allTFIDFs)
	
	