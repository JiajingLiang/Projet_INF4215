#!/usr/bin/python
# -*- coding: utf-8 -*-

from classifierSVM import *
from data_storage import *
from twitter import *

class Agent:
	def __init__(self):
		db = DataStorage('localhost','root','','twitter')
		twitter = Twitter(db)
		self.classifier = ClassifierSVM('rbf',0.5,1,twitter)
		self.classifier.buildModel()
		
	def testing(self):
		self.classifier.predictEmotion(None)