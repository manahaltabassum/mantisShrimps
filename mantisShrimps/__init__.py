from flask import Flask, render_template, request, redirect, url_for, session, flash
from utils.db import *
from utils import weather
import urllib, os, glob, hashlib
from flask_dropzone import Dropzone
from os import path
app = Flask(__name__)
dropzone = Dropzone(app)
app.secret_key = os.urandom(32)

f = path.dirname(__file__)

print "DIR: " + f

#================LOGIN HELPERS==============================
#checks if the password matches the account referenced by the username
def match(username,password):
	p = get_pass(username)
	if(p == None):
		return False
	else:
		return (p == hashlib.sha224(password).hexdigest())

#checks if the password is correct, then creates a cookie
def login_db(username,password):
	if(match(username,password)):
		session['username'] = username
		session['password'] = hashlib.sha224(password).hexdigest()
		return True
	else:
		return False

#checks if there is a login session and if the credentials are correct
def in_session():
	if(not('username' in session and 'password' in session)):
		return False
	p = get_pass(session.get('username'))
	if(p == None):
		return False
	else:
		return (p == session.get('password'))

#removes the login session
def logout_db():
	if('username' in session):
		session.pop('username')
	if('password' in session):
		session.pop('password')
#==================================================

@app.route('/')
def root():
	if in_session():	
                return redirect( url_for('home') )
	else:
	        return render_template("root.html")

@app.route('/home',methods=['GET','POST'])
def home():
	if in_session():
                return render_template('home.html')
	else:
	        return redirect(url_for('root'))

@app.route('/login_auth', methods=['POST'])
def login_auth():
    usr = request.form['usr']
    pwd = request.form['pwd']
    error = None
    if usr != '':
        if match(usr,pwd):
                login_db(usr,pwd)
                flash("You have successfully logged in!!!")
                return redirect( url_for('home') )
        flash("Invalid Username/Password")
        return redirect( url_for('root') )
    else:
            
        return render_template('root.html')

    
@app.route('/register_auth', methods=["POST"])
def register_auth():
        usr = request.form['usr']
        pwd = request.form['pwd']
        if get_pass(usr) is None: # get_pass() is db function
                cfm = request.form['cfm']
                if pwd == cfm:
                        adduser(usr,pwd)
                        login_db(usr,pwd)
                        flash("You have successfully created your account!!!")
                        return redirect( url_for('home') )
                else:
                        flash("Sorry, your passwords do not match")
                        return redirect( url_for('root') )

        else:
            flash("Sorry, username already exists")
            return redirect( url_for('root') )


@app.route('/calendar')
def calendar():
        return render_template("calendar.html")

@app.route('/calendar_helper')
def calendar_helper():
       return str(weather.weekly())

@app.route('/upload', methods=["GET", "POST"])
def upload():
        if request.method == 'POST':
                f = request.files.get('file')
                f.save(os.path.join('data/img/', f.filename))
        return render_template("upload.html")

@app.route('/getClothes', methods=["GET"])
def getClothes():
        data = {}
        select = request.form.get("select_type")
        if select == 'top':
                data["top"] = getClothes( session['username'], "top" )
        elif select == 'bottom':
                data['bottom'] = getClothes( session['username'], "bottom" )
        else:
                data['shoes'] = getClothes( session['username'], "shoes" )
        return render_template("home.html", clothes=data, ctr=0 )

@app.route('/upload_clothing', methods=["POST"])
def upload_clothing():
        #addCloth(user,Id, Type, labels, item, freq)
        return redirect (url_for('upload'))
        

#@app.route('/upload_helper')
#def upload_helper():
  #      return
if __name__ == '__main__':
    app.debug = True
    app.run()

    
