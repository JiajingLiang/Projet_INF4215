#!/usr/bin/python
# -*- coding: utf-8 -*-

class Tweet:
	"""docstring for Tweet"""
	def __init__(self,twtID=None,accFK=None,pstDate=None,cntHtml=None,cntRaw=None,treated=0):
		self.tweetID = twtID
		self.accountFK = accFK
		self.postDate = pstDate
		self.contentHtml = cntHtml
		self.contentRaw = cntRaw
		self.treated = treated

	def show(self):
		print " tweetID : {} \n accountFK : {} \n postDate : {} \n contentHtml : {} \n contentRaw : {} \n treated : {} \n ".format(self.tweetID,self.accountFK,self.postDate,self.contentHtml,self.contentRaw,self.treated)
