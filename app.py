from flask import Flask, render_template, request, json, send_from_directory, jsonify, redirect, url_for
import random
import MySQLdb as db
from test import test

HOST = "138.197.183.138"
PORT = 3306
USER = "root"
PASSWORD = "root"
DB = "project"

app = Flask(__name__)
connection = db.connect(host=HOST, port=PORT, user=USER,
		                          passwd=PASSWORD, db=DB)
dbhandler = connection.cursor()

@app.route('/')
def home():
        return render_template('index.html')
        
@app.route('/showHome')
def showHome():
        return render_template('index.html')
        
@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/signUp',methods=['POST'])
def signUp():
 
    # read the posted values from the UI
    _firstName = request.form['inputFirstName']
    _lastName = request.form['inputLastName']
    _username = request.form['username']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
    
     
    #print "INSERT INTO user(first_name, last_name, username, password, email, roll_no) VALUES('%s','%s','%s','%s','%s','%s')"%(_firstName, _lastName, _username, _password, _email, str(random.randint(1,100)))
    dbhandler.execute("INSERT INTO user(first_name, last_name, username, password, email, roll_no) VALUES('%s','%s','%s','%s','%s','%s')"%(_firstName, _lastName, _username, _password, _email, str(random.randint(1,100))))
    dbhandler.execute("select * from user")
    result = dbhandler.fetchall()
    for item in result:
    	print item
    
	
    
    return render_template('index.html')
    
    #return json.dumps({'html':'New User Registered!'})
    
    
if __name__ =="__main__":
	test()
	app.run()
	connection.commit()
	connection.close()
    
