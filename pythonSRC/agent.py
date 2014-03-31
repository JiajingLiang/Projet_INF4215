from classifierSVM import *
from dbConnector import *

class Agent:
	def __init__(self):
		dbConnector = DBConnector('localhost','root','','twitter')
		self.classifier = ClassifierSVM('rbf',0.5,1,dbConnector)
		self.classifier.buildModel()
		
	def testing(self):
		self.classifier.predictEmotion(None)