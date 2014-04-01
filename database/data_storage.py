#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as m
from tweet import *

class DataStorage:
	"""docstring for dataStorage"""
	def __init__(self, host, user, passwd, db):
		self.db = m.connect(host=host,user=user,passwd=passwd,db=db)

	def connect(self, host, user, passwd, db):
		self.db = m.connect(host=host,user=user,passwd=passwd,db=db)

	def close(self):
		self.db.close() 

	def executeQueryWithSingleResult(self,query,params=None):
		c = self.db.cursor()
		
		if params is None:
			c.execute(query)
		else:
			c.execute(query,params)
		
		return c.fetchone()

	def executeQueryWithMultipleResults(self,query,params=None):
		c = self.db.cursor()
		
		if params is None:
			c.execute(query)
		else:
			c.execute(query,params)
		
		return c.fetchall()

	def executeQueryModifyingDatabase(self,query,params=None):
		c = self.db.cursor()

		if params is None:
			c.execute(query)
		else:
			c.execute(query,params)

		self.db.commit()
