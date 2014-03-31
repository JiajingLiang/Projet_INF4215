# -*- coding: utf-8 -*-

from sklearn import svm,datasets

import numpy as np
import pylab as pl

class ClassifierSVM():
	def __init__(self,kernelFuncName,g,c,dbConnector):
		self.svm = svm.SVC(kernel = kernelFuncName,gamma=g,C=c)
		self.dbConnector = dbConnector
		self.data = []
		self.target = []
		self.model = None
		
	# methode pour construire les donnees d'apprentissage
	# ratio: rapport sur l'ensemble de donnee d'apprentissage
	def getDataApprentissage(self,ratio):
		return
		
	# methode pour analyser un tweet afin de construire X
	def analyseTweet(self,tweet):
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

		# Put the result into a color plot
		Z = Z.reshape(xx.shape)
		pl.figure(1, figsize=(4, 3))
		pl.pcolormesh(xx, yy, Z, cmap=pl.cm.Paired)

		# Plot also the training points
		pl.scatter(self.data[:, 0], self.data[:, 1], c=self.target, cmap=pl.cm.Paired)
		pl.xlabel('Sepal length')
		pl.ylabel('Sepal width')

		pl.xlim(xx.min(), xx.max())
		pl.ylim(yy.min(), yy.max())
		pl.xticks(())
		pl.yticks(())

		pl.show()
		
		return
	
	