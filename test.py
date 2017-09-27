import MySQLdb as db

HOST = "138.197.183.138"
PORT = 3306
USER = "root"
PASSWORD = "root"
DB = "project"

def test():
	try:
		connection = db.connect(host=HOST, port=PORT, user=USER,
		                          passwd=PASSWORD, db=DB)
		dbhandler = connection.cursor()
		dbhandler.execute("describe user")
		result = dbhandler.fetchall()
		for item in result:
		    print item
		connection.close()

	except Exception as e:
		print e
		connection.close()
