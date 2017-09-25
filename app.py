from flask import Flask, render_template, request, json, send_from_directory, jsonify

app = Flask(__name__)

@app.route('/')
def home():
        return render_template('index.html')
        
@app.route('/showHome')
def showHome():
        return render_template('index.html')
        
@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

if __name__ =="__main__":
        app.run()
