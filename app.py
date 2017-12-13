#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017 Kaushik S Kalmady
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# File              : app.py
# Author            : Kaushik S Kalmady, Siddharth V
# Date              : 07.11.2017
# Last Modified Date: 24.11.2017
# Last Modified By  : Kaushik S Kalmady


import json
import random
import sys
from collections import Counter
from pprint import pprint
from flask import (Flask, flash, jsonify, logging, redirect, render_template,
                   request, session, url_for)
from flask_mysqldb import MySQL
from forms import PostForm, RegisterForm
from passlib.hash import sha256_crypt
from posts import extract_article
from utils import parseme

app = Flask(__name__)

# Enter this information
HOST = "localhost"
USERNAME ="root" # change to your username and password
PASSWORD = "mysqlroot"

app.config['MYSQL_HOST'] = HOST
app.config['MYSQL_USER'] = USERNAME
app.config['MYSQL_PASSWORD'] = PASSWORD
app.config['MYSQL_DB'] = 'project'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#init MYSQL_DB
mysql = MySQL(app)

all_deps = dict([('CO', 'Computer Engineering'), ('EC', 'Electronics & Communication'),\
      ('CH', 'Chemical Engineering'), ('EE', 'Electrical Engineering'),\
       ('ME', 'Mechanical Engineering'), ('IT','Information Technology'),\
       ('MN', 'Mining Engineering'), ('CV', 'Civil Engineering')])

@app.route('/')
def home():
    if 'logged_in' in session:
        return redirect(url_for('dashboard'))

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
            cur.callproc('register', (firstName, lastName, \
                            username, password, email, rollNo, dept))

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
    if 'logged_in' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        # Get form feilds
        username = request.form['username']
        password_candidate = request.form['password']
                # Create a cursor
        cur = mysql.connection.cursor()
        result = cur.execute("""SELECT * FROM users
                                WHERE username = %s""",[username])
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

#Dashboard routes
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'logged_in' in session:
        cur = mysql.connection.cursor()
        cur.execute("""SELECT
                        title,
                        url,
                        description,
                        thumb,
                        P.p_id,
                        b_id,
                        category,
                        read_status+0 as read_status,
                        time_added
                        FROM bookmark B JOIN post P
                        ON B.p_id=P.p_id
                        WHERE username=\'{}\'
                        ORDER BY time_added DESC;""".format(session["username"]))

        data = list(cur.fetchall())
        cur.close()

        if len(data)==0 :
            return render_template('dashboard.html')

        for entry in data:
            entry["shortdescription"] = parseme(entry["description"],150)

        categories = list(set([entry["category"] for entry in data]))
        months = list(set([entry["time_added"].strftime("%B") for entry in data]))
        if request.method == 'POST':
            print request.form
            if 'archive' in request.form:
                data = [item for item in data if item["read_status"]==1]
                return render_template('dashboard.html', articles=data,\
                                        categories=categories, months=months, archive=True)
            elif 'category' in request.form:
                cat = request.form['category']
                data = [item for item in data if item["category"]==cat]
                return render_template('dashboard.html', articles=data,\
                                        categories=categories, months=months, cat=cat)
            elif 'month' in request.form:
                month = request.form['month']
                data = [item for item in data if item["time_added"].strftime("%B")==month]
                return render_template('dashboard.html', articles=data,\
                                        categories=categories, months=months, month=month)
            elif 'search' in request.form:
                query = request.form['search'].lower()
                data = [item for item in data if query in item['title'].lower()\
                         or query in item['description'].lower()]
                return render_template('dashboard.html', articles=data,\
                                        categories=categories, months=months, query=query)
        elif request.method =='GET':
            data = [item for item in data if item["read_status"]==0]
            #pprint(data[0])
            return render_template('dashboard.html', articles=data,\
                                    categories=categories, months=months,)
    else:
        flash('You need to be logged in to access!', 'danger')
        return redirect(url_for('login'))


# Explore page routes
@app.route('/explore', methods=['GET', 'POST'])
def explore():
    if 'logged_in' in session:

        cur = mysql.connection.cursor()
        cur.execute("""SELECT
                        *
                        FROM post P
                        ORDER BY counter DESC;
                        """)
        data = list(cur.fetchall())

        if len(data)==0 :
            return render_template('explore.html')

        for entry in data:
            entry["description"] = parseme(entry["description"],150)

        cur.execute("""SELECT
                        p_id, category
                        FROM
                        bookmark
                        WHERE
                        username=\'{}\'""".format(session["username"]))

        bookmarks = list(cur.fetchall())
        my_pids = [entry["p_id"] for entry in bookmarks]

        cur.execute("""SELECT
                        p_id, category
                        FROM
                        bookmark""")
        bookmarks = list(cur.fetchall())

        cur.execute("""SELECT
                        DISTINCT(d_id)
                        FROM users;""")
        departments = [entry["d_id"] for entry in list(cur.fetchall())]
        cur.close()

        categories = list(set([bookmark["category"] for bookmark in bookmarks]))
        deps = departments
        departments = [{"short" : d, "long":all_deps[d]} for d in departments]


        if request.method == 'POST':

            print request.form

            cond1 = ''
            if request.form.get('LW'):
                cond1='DATEDIFF(DATE(bookmark.time_added), CURDATE())<=7 OR '
            elif request.form.get('LM'):
                cond1='DATEDIFF(DATE(bookmark.time_added), CURDATE())<=30 OR '
            elif request.form.get('LM'):
                cond1='DATEDIFF(DATE(bookmark.time_added), CURDATE())<=365 OR '

            if len(cond1) != 0:
                cond1 = cond1[:-4]
            print cond1

            cond2 = ''
            for category in categories:
                if request.form.get(category):
                    cond2+='bookmark.category=\'{}\' OR '.format(category)

            if len(cond2) != 0:
                cond2 = cond2[:-4]
            print cond2

            cond3 = ''
            for d in deps:
               if request.form.get(d):
                cond3+='users.d_id=\'{}\' OR '.format(d)

            if len(cond3) != 0:
                cond3 = cond3[:-4]
            print cond3

            cond = ''
            if len(cond1) != 0:
                cond += cond1

            if len(cond)!=0 and len(cond2) != 0:
                cond = cond + ' AND ' + cond2
            elif len(cond)==0 and len(cond2) != 0:
                cond += cond2

            if len(cond)!=0 and len(cond3) != 0:
                cond = cond + ' AND ' + cond3
            elif len(cond)==0 and len(cond3) != 0:
                cond += cond3


            if len(cond) != 0:
                cond = 'WHERE '+cond
            print 'Query condition:', cond

            cur = mysql.connection.cursor()
            cur.execute("""SELECT
                            bookmark.p_id
                            FROM users
                            INNER JOIN
                            bookmark
                            ON
                            users.username=bookmark.username
                            {};
                            """.format(cond))

            available = list(cur.fetchall())
            cur.close()

            available = [item['p_id'] for item in available]
            print available
            data = [item for item in data if (item["p_id"] in available)]

            return jsonify({"data":data, "my_pids": my_pids})

        if request.method =='GET':
            return render_template('explore.html', articles=data,\
                                    departments=departments, my_pids=my_pids,\
                                    categories=categories)
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
            cur.execute("""SELECT
                            p_id
                            FROM bookmark
                            WHERE username=\'{}\'
                            AND
                            p_id=(SELECT
                                    p_id
                                    FROM post
                                    WHERE url=\'{}\')""".format(session['username'], url))

            data = cur.fetchall()
            #cur.close()

            if len(data)>0:
                flash('The article has already been bookmarked', 'danger')
                return render_template('add_bookmark.html', form=form)

            else:

                cur.execute("""SELECT
                                p_id
                                FROM post
                                WHERE url=\'{}\'""".format(url))
                data = cur.fetchall()

                if len(data)==0:
                    article = extract_article(url)
                    app.logger.info("ARTICLE PARSED")
                    if article == "Error":
                        flash('The url does not point to a valid article.', 'danger')
                        cur.close()
                        return render_template('add_bookmark.html', form=form)

                    cur.callproc('add_post', (url, article['title'], \
                                    article['text'], article['img']))

                cur.execute("""SELECT
                                p_id
                                FROM post
                                WHERE url=\'{}\'""".format(url))
                data = cur.fetchall()
                cur.callproc('add_bookmark', (session['username'], \
                                data[0]['p_id'], cat))
                cur.close()
                mysql.connection.commit()

                flash('The article has been successfully bookmarked', 'success')

            return redirect(url_for('dashboard'))


        except:

            flash(str(sys.exc_info()[0]), 'danger')
            return render_template('add_bookmark.html', form=form)

    return render_template('add_bookmark.html', form=form)

@app.route('/myaccount', methods=['GET'])
def myaccount():
    if 'logged_in' in session:
        cur = mysql.connection.cursor()
        cur.execute("""SELECT
                        first_name,
                        last_name,
                        d_name,
                        email,
                        roll_no,
                        username
                        FROM users U JOIN department D
                        ON U.d_id=D.d_id
                        WHERE username=\'{}\'
                        """.format(session["username"]))

        myuser = list(cur.fetchall())

        cur.execute("""SELECT
                        read_status+0 as read_status
                        FROM bookmark
                        WHERE username=\'{}\'
                        """.format(session["username"]))

        mybookmarks = list(cur.fetchall())
        unread = sum((d["read_status"] for d in mybookmarks[1:]),\
         mybookmarks[0]["read_status"])
        stats = {"total" : len(mybookmarks),
                 "unread" : len(mybookmarks) - unread,
                 "archived": unread,
                 }
        cur.close()
        #pprint(myuser, stats)
        return render_template('myaccount.html', myuser=myuser[0], stats=stats)

    else:
        flash('You need to be logged in to access!', 'danger')
        return redirect(url_for('login'))

@app.route('/archive-toggle', methods=['POST'])
def archive():
    b_id = request.json["b_id"]
    cur = mysql.connection.cursor()
    cur.execute("""UPDATE
                    bookmark
                    SET read_status = !read_status
                    WHERE b_id=%s"""%b_id)
    cur.close()
    mysql.connection.commit()
    #print json.loads(request.form["b_id"])
    return jsonify({"data":"pass"})

# Data request for doughnut chart comes here
@app.route('/get-pie-data', methods=['GET'])
def getpiedata ():
    cur = mysql.connection.cursor()
    cur.execute("""SELECT
                    category,
                    COUNT(*) as count
                    FROM bookmark
                    WHERE username=\'{}\'
                    GROUP BY
                    category""".format(session["username"]))
    data = cur.fetchall()
    cur.close()
    #pprint(data)
    #print json.loads(request.form["b_id"])
    return jsonify({"data":data})

# Route for adding bookmark from the Explore page
@app.route('/add-mybookmark', methods=['POST'])
def addmybookmark():
    p_id = request.json["p_id"]
    category = request.json["category"]
    cur = mysql.connection.cursor()
    cur.callproc('add_bookmark', (session['username'], \
                                p_id, category))
    cur.close()
    mysql.connection.commit()
    #print json.loads(request.form["b_id"])
    print p_id, category
    return jsonify({"data":"pass"})

# Delete a bookmark
@app.route('/delete-bookmark', methods=['POST'])
def delete():
    b_id, p_id = request.json["b_id-p_id"].split("-")
    cur = mysql.connection.cursor()
    cur.execute("""DELETE
                    FROM bookmark
                    WHERE b_id=%s"""%b_id)
    cur.close()
    mysql.connection.commit()
    print b_id, p_id
    return jsonify({"data":"pass"})

@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))



if __name__ =="__main__":
    app.secret_key = 'secret123'
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host="0.0.0.0", debug=True, threaded=True)
