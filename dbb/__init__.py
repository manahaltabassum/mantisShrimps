from flask import Flask, render_template, request, redirect, url_for, session, flash
from utils.db import *
from utils import weather
import urllib, os, glob, hashlib
from flask_dropzone import Dropzone
from os import path
from random import randint
app = Flask(__name__)
dropzone = Dropzone(app)
app.secret_key = os.urandom(32)

g = path.dirname(__file__) + "/static/img/"
h = path.dirname(__file__) + "/static/"

print "DIR: " + g

clothId = 0
extension = ""

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

#=================AJAX HELPERS=====================
@app.route("/outHist", methods = ["GET"])
def outHist():
        #print "\n\n\n"
        #print getOutHist(session['username'])
        #print "\n\n\n"
        return str(getOutHist(session['username']))

        
#==================================================
@app.route('/')
def root():
	if in_session():	
                return redirect( url_for('home') )
	else:
	        return render_template("root.html", PATH=h)

@app.route('/home',methods=['GET','POST'])
def home():
	if in_session():
                return redirect(url_for('home_display'))
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
        d = weather.weekly()
        return render_template("calendar.html", keys=d[0], data=d[1])

'''
@app.route('/calendar_helper')
def calendar_helper():
       return str(weather.weekly())
'''

@app.route('/upload', methods=["GET", "POST"])
def upload():
        if request.method == 'POST':
                f = request.files.get('file')
                global extension
                extension = f.filename.split(".")[-1]
                global clothId
                clothId = assignID()
                f.save(os.path.join("." + g, str(clothId) + "." + extension))
        return render_template("upload.html")


@app.route('/home_display', methods=["GET","POST"])
def home_display():
        data = {}
        PATH = g
        select = request.form.get("select_type")
	if select == None:
		select = request.args.get("select_type")
        if select == 'bottom':
                data = getClothes( session['username'], "pants" )
        elif select == 'shoes':
                data = getClothes( session['username'], "shoes" )
	else:
                data = getClothes( session['username'], "top" )
	clothes = []
	for thing in data:
		clothes.append(g + str(thing[1]) + "." + thing[4] )
        outfits = getOutfits(session["username"])
        return render_template("home.html", PATH=g, clothes=clothes, ctr=0, outfits=outfits, keys=outfits.keys() )


@app.route('/upload_clothing', methods=["GET"])
def upload_clothing():
        name = request.args.get("name")
        typeC = request.args.get("type")
        #return name + typeC
        addCloth(session["username"], typeC, name, clothId, extension)
        return redirect (url_for('upload'))

@app.route('/creator')
def creator():
        date = request.args.get("date")
        return render_template("creator.html", tops=getClothes(session["username"], "top"),
                               shoes=getClothes(session["username"], "shoes"),
                               pants=getClothes(session["username"], "pants"),
                               date = date,
			       PATH=g
        )


@app.route('/add_outfit', methods=["GET"])
def add_outfit():
        date = request.args.get("date")
        print "date: " + date
        topSelect = int(request.args.get("topForm"))
        pantSelect = int(request.args.get("pantForm"))
        shoeSelect = int(request.args.get("shoeForm"))
        name = request.args.get("outfitName")
        tops = getClothes(session["username"], "top")
        pants = getClothes(session["username"], "pants")
        shoes = getClothes(session["username"], "shoes")
        topID = tops[topSelect % len(tops)][1]
        pantID = pants[pantSelect % len(pants)][1]
        shoeID = shoes[shoeSelect % len(shoes)][1]
        addOutfit(session["username"], name, topID)
        addOutfit(session["username"], name, pantID)
        addOutfit(session["username"], name, shoeID)
        if (date != None):
                addOutHist(session["username"], name, date)
        return redirect (url_for('creator'))
        #return str([topID, pantID, shoeID])
        #return str([topSelect, pantSelect, shoeSelect])
        #return "hi"

@app.route('/d3_helper')
def helper():
        l = []
        types = ["top", "pants", "shoes"]
        for x in types:
                l.append(len(getClothes(session["username"], x)))
        return str(l)
                




        
@app.route('/logout')
def logout():
        logout_db()
        flash("Logged Out")
        return redirect( url_for('root') )


#@app.route('/upload_helper')
#def upload_helper():
#      return
if __name__ == '__main__':
        app.debug = True
        app.run()

    
