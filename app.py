from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
import random
import sys
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt

from forms import RegisterForm, PostForm
from posts import extract_article

app = Flask(__name__)

app.config['MYSQL_HOST'] = '138.197.183.138'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'dbmsproject'
app.config['MYSQL_DB'] = 'project'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#init MYSQL_DB
mysql = MySQL(app)


@app.route('/')
def home():
        return render_template('index.html')

# User signup
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


        try:
            # Create cursor
            cur = mysql.connection.cursor()

            # Execute query 
            cur.callproc('register', (firstName, lastName, username, password, email, rollNo, dept))
            

            data = cur.fetchone()

            app.logger.info(data.keys()[0])
            cur.close()
            

            mysql.connection.commit()

            msg = data.keys()[0] 
            # Close connection


            if msg=='success':
                flash('You are now registered and can log in', 'success')
                return redirect(url_for('login'))

            else:
                error_msg = (" ").join(msg.split('_')[1:])
                flash('The %s already exists'%error_msg, 'danger')

        except:

            flash(str(sys.exc_info()[0]), 'danger')
            return render_template('register.html', form=form)

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

    if 'logged_in' in session:
        return render_template('dashboard.html')
    else:
        flash('You need to be logged in to access!', 'danger')
        return redirect(url_for('login'))

@app.route('/add_bookmark', methods=['GET', 'POST'])
def add_bookmark():
    form = PostForm(request.form)
    if  request.method == 'POST' and form.validate():
        url = form.url.data
        cat = form.cat.data
        
        try: 
            cur = mysql.connection.cursor()       
  
            cur.execute('SELECT p_id FROM bookmark WHERE username=\'{}\' AND p_id=(SELECT p_id FROM post WHERE url=\'{}\')'.format(session['username'], url))
            
            data = cur.fetchall()
            
            cur.close()
            
            if len(data)>0:
                flash('The article has already been bookmarked', 'success')
            
            else:
        
                cur = mysql.connection.cursor()       
      
                cur.execute('SELECT p_id FROM post WHERE url=\'{}\''.format(url))
                
                data = cur.fetchall()
                
                cur.close()
                
                if len(data)==0:  
                    article = extract_article(url)
                    
                    cur = mysql.connection.cursor()                              
                   
                    cur.callproc('add_post', (url, article['title'], article['text'], article['img']))
                    
                    cur.close()
                    
                    mysql.connection.commit()
                    
                    
                cur = mysql.connection.cursor()  

                cur.execute('SELECT p_id FROM post WHERE url=\'{}\''.format(url))
                
                data = cur.fetchall()                 
                
                cur.callproc('add_bookmark', (session['username'], data[0]['p_id']))
                
                cur.close()        
                
                mysql.connection.commit()
                
                flash('The article has been successfully bookmarked', 'success')
            
            return render_template('dashboard.html')
            
        
        except:

            flash(str(sys.exc_info()[0]), 'danger')
            return render_template('add_bookmark.html', form=form) 
                  
    return render_template('add_bookmark.html', form=form)        

    
	
	
    
    


@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))



if __name__ =="__main__":
    app.secret_key = 'secret123'
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)
