import MySQLdb

class DBConnector():
	def __init__(self,host,user,passwd,db):
		self.host = host;
		self.user = user;
		self.passwd = passwd;
		self.dbname = db;
		

	