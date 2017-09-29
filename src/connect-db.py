import MySQLdb as db

HOST = "174.138.56.33"
PORT = 3306
USER = "kausid"
PASSWORD = "kausid"
DB = "project"

try:
        connection = db.connect(host=HOST, port=PORT, user=USER,
                                  passwd=PASSWORD, db=DB)
        dbhandler = connection.cursor()
        dbhandler.execute("describe test")
        result = dbhandler.fetchall()
        for item in result:
            print item
        connection.close()

except Exception as e:
        print e
        connection.close()
