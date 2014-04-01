#!/usr/bin/python
# -*- coding: utf-8 -*-

class Dictionnary:
	"""docstring for Dictionnary"""
	def __init__(self, id=None, tag=None, meaning=None, relevance=None):
		self.id = id
		self.tag = tag
		self.meaning = meaning
		self.relevance = relevance

	def show(self):
		print " dictionnaryID : {} \n tag : {} \n meaning : {} \n relevance : {} \n".format(self.id,self.tag,self.meaning,self.relevance)
