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
@app.route('/pub_dashboard', methods=['GET', 'POST'])
def pub_dashboard():
    if 'logged_in' in session:
           
        cur = mysql.connection.cursor()
        cur.execute("""SELECT
                        *                    
                        FROM post P 
                        """)

        data = list(cur.fetchall())        
        
        if len(data)==0 :
            return render_template('pub_dashboard.html')
            
        for entry in data:
		#entry["title"] = entry["title"][:45] + " ..."
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
        cur.close()
        
        #print my_pids
        #categories = list(set(['Computer Engineering', 'Electronics & Communication', 'Chemical Engineering', 'Electrical Engineering', 'Mechanical Engineering']))
        departments = dict([('Computer Engineering', 'CO'), ('Electronics & Communication', 'EC'), ('Chemical Engineering', 'CH'), ('Electrical Engineering', 'EE'), ('Mechanical Engineering', 'ME')])
        #categories = list(set([entry["category"] for entry in data]))
        #months = list(set([entry["time_added"].strftime("%B") for entry in data]))
        
        
        #categories = list(set([entry["category"] for entry in bookmarks]))
        #print categories
        categories = ['Academia', 'Entertainment', 'Sports', 'Music', 'Art', 'Politics', 'Science', 'Technology', 'Film', 'India', 'History', 'Other']

        print request.form

        
        if request.method == 'POST':
               
            cond1 = ''
            
            if request.form.get('LW'):
                cond1='DATEDIFF(DATE(bookmark.time_added), CURDATE())<=7 OR '
            elif request.form.get('LM'):
                cond1='MONTH(bookmark.time_added)=MONTH(CURRENT_DATE()) OR '
            elif request.form.get('LM'):
                cond1='YEAR(bookmark.time_added)=YEAR(CURRENT_DATE()) OR '
                
            
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
                      
            if request.form.get('CO'):
                cond3+='users.d_id=\'CO\' OR '
            if request.form.get('EC'):
                cond3+='users.d_id=\'EC\' OR '
            if request.form.get('CH'):
                cond3+='users.d_id=\'CH\' OR '
            if request.form.get('EE'):
                cond3+='users.d_id=\'EE\' OR '
            if request.form.get('ME'):
                cond3+='users.d_id=\'ME\' OR '   
                
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
            available = [item['p_id'] for item in available] 
            
            print available
            
            cur.close()
            
            data = [item for item in data if (item["p_id"] in available)]
            
            err = False
            if len(data) == 0:
                err=True

            return render_template('pub_dashboard.html', articles=data,\
                                    departments=departments.keys(), my_pids=my_pids, \
                                    categories=categories, err=err)      
            
            
        if request.method =='GET':
           
            #pprint(data[0])
            return render_template('pub_dashboard.html', articles=data,\
                                    departments=departments.keys(), my_pids=my_pids)
    else:
        flash('You need to be logged in to access!', 'danger')
        return redirect(url_for('login'))
