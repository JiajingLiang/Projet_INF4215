#!/usr/bin/python
# -*- coding: utf-8 -*-

class Comment:
	"""docstring for Comment"""
	def __init__(self,cmtID=None,twtFK=None,pstDate=None,cntHtml=None,cntRaw=None):
		self.commentID = cmtID
		self.tweetFK = twtFK
		self.postDate = pstDate
		self.contentHtml = cntHtml
		self.contentRaw = cntRaw

	def show(self):
		print " commentID : {} \n tweetFK : {} \n postDate : {} \n contentHtml : {} \n contentRaw : {} \n".format(self.commentID,self.tweetFK,self.postDate,self.contentHtml,self.contentRaw)