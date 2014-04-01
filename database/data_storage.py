#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as m
from tweet import *

class DataStorage:
	"""docstring for dataStorage"""
	def __init__(self, host, user, passwd, db):
		self.db = m.connect(host=host,user=user,passwd=passwd,db=db)

	# Initialise la connexion avec la base de données passé en paramètre
	def connect(self, host, user, passwd, db):
		self.db = m.connect(host=host,user=user,passwd=passwd,db=db)

	# Met fin à la connexion avec la BDD
	def close(self):
		self.db.close() 

	# Execute une requête dont le résultat retourné est unique
	def executeQueryWithSingleResult(self,query,params=None):
		c = self.db.cursor()
		
		if params is None:
			c.execute(query)
		else:
			c.execute(query,params)
		
		return c.fetchone()

	# Execute une requête dont le résultat retourné est multiple
	def executeQueryWithMultipleResults(self,query,params=None):
		c = self.db.cursor()
		
		if params is None:
			c.execute(query)
		else:
			c.execute(query,params)
		
		return c.fetchall()

	# Execute une requête dont l'objectif est de modifier/ajouter/supprimer un élément d'une table 
	def executeQueryModifyingDatabase(self,query,params=None):
		c = self.db.cursor()

		if params is None:
			c.execute(query)
		else:
			c.execute(query,params)

		self.db.commit()
