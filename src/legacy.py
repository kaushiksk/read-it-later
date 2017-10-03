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