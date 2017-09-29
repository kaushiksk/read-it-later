from flask import Flask, render_template, request, json, send_from_directory, jsonify, redirect, url_for
import random
from flaskext.mysql import MySQL
import sys


app = Flask(__name__)
mysql = MySQL()
 
# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'project'
app.config['MYSQL_DATABASE_HOST'] = '138.197.183.138'
mysql.init_app(app)
#connection = db.connect(host=HOST, port=PORT, user=USER,  passwd=PASSWORD, db=DB)
connection = mysql.connect()
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
    
    try:
    #print "INSERT INTO user(first_name, last_name, username, password, email, roll_no) VALUES('%s','%s','%s','%s','%s','%s')"%(_firstName, _lastName, _username, _password, _email, str(random.randint(1,100)))
	    dbhandler.execute("INSERT INTO user(first_name, last_name, username, password, email, roll_no) VALUES('%s','%s','%s','%s','%s','%s')"%(_firstName, _lastName, _username, _password, _email, str(random.randint(1,100))))
	    dbhandler.execute("select * from user")
	    result = dbhandler.fetchall()
	    for item in result:
	    	print item
	    data = {'msg':'New User Registered!','type':'msg'}
	    return jsonify(data)

    except:
		data ={'msg': 'Error! Please check that all fields are valid.','type':'error'}
		print sys.exc_info()[0]
		return jsonify(data)
    
    #return render_template('index.html')
    
    
    
    
if __name__ =="__main__":
	dbhandler.execute("describe user")
	result = dbhandler.fetchall()
	for item in result:
	    print item
	app.config['TEMPLATES_AUTO_RELOAD'] = True
	app.run(debug=True)

	connection.commit()
	connection.close()
    
