from flask import Flask, render_template, request, redirect, url_for, session, flash
from db import *
from utils import ebay
import urllib
import requests
import os
import glob
app = Flask(__name__)
app.secret_key = os.urandom(32)

@app.route('/')
def root():
	if in_session():	
        return redirect( url_for('home') )
	else:
		return render_template("home.html")

@app.route('/home',methods=['GET','POST'])
def home():
	if in_session():
        return redirect( url_for('home') )
	else:
		return render_template('home.html')

@app.route('/login_auth', methods=['POST'])
def login_auth():
    usr = request.form['usr']
    pwd = request.form['pwd']
    if usr != '':
        if match(usr,pwd): # match() is db function
            login_db(usr,pwd)
            return redirect( url_for('login') )
        return render_template('home.html')
    else:
        return render_template('home.html')

    
@app.route('/register_auth', methods=["POST"])
def register_auth():
        usr = request.form['usr']
        pwd = request.form['pwd']
        if get_pass(usr) is None: # get_pass() is db function
                cfm = request.form['cfm']
                if pwd == cfm:
                        adduser(usr,pwd)
                        login_db(usr,pwd)
                        return redirect( url_for('login') )
                else:
                        return render_template("home.html")

        else:
                return render_template("home.html")

if __name__ == '__main__':
    app.debug = True
    app.run()
