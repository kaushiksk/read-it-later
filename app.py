from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
import random
import sys
# from flaskext.mysql import MySQL
from flask_mysqldb import MySQL
from forms import RegisterForm
from passlib.hash import sha256_crypt

app = Flask(__name__)
#mysql = MySQL()

# MySQL configurations
# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
# app.config['MYSQL_DATABASE_DB'] = 'project'
# app.config['MYSQL_DATABASE_HOST'] = '138.197.183.138'
# mysql.init_app(app)
app.config['MYSQL_HOST'] = '138.197.183.138'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'project'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#init MYSQL_DB
mysql = MySQL(app)

#connection = db.connect(host=HOST, port=PORT, user=USER,  passwd=PASSWORD, db=DB)
#connection = mysql.connect()
#dbhandler = connection.cursor()

@app.route('/')
def home():
        return render_template('index.html')

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
	    dbhandler.execute("INSERT INTO users(first_name, last_name, username, password, email, roll_no) VALUES('%s','%s','%s','%s','%s','%s')"%(_firstName, _lastName, _username, _password, _email, str(random.randint(1,100))))
	    dbhandler.execute("select * from users")
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


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if  request.method == 'POST' and form.validate():
        firstName = form.firstName.data
        lastName = form.lastName.data
        rollNo = form.rollNo.data
        dept = form.dept.data
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("INSERT INTO users(first_name, last_name, username, password, email, roll_no, d_id) VALUES('%s','%s','%s','%s','%s','%s', '%s')"%(firstName, lastName, username, password, email, rollNo, dept))

        # Commit to Database
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('login'))

    return render_template('register.html', form=form)

# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form feilds
        username = request.form['username']
        password_candidate = request.form['password']

        # Create a cursor
        cur = mysql.connection.cursor()

        result = cur.execute("SELECT * FROM users WHERE username = %s",[username])

        if result > 0:
             data = cur.fetchone()
             password = data['password']

             if sha256_crypt.verify(password_candidate, password):
                 app.logger.info('PASSWORD MATCHED')
                 session['logged_in'] = True
                 session['username'] = username
                 #session['firstName'] = result['first_name']
                 #session['lastName'] = result['last_name']

                 flash('You are now logged in', 'success')

                 return redirect(url_for('dashboard'))
             else:
                 app.logger.info('PASSWORD NOT MATCHED')
                 error = 'Incorrect password'
                 return render_template('login.html', error=error)

        else:
            app.logger.info('INVALID USERNAME')
            error = 'Enter a valid username'
            return render_template('login.html', error=error)

        cur.close()

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))



if __name__ =="__main__":
    app.secret_key = 'secret123'
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
