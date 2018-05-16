import sqlite3
import os
import hashlib
from flask import session

f = "app.db"
db = sqlite3.connect(f)
c = db.cursor()
#if a item has 0 the user is not using the item. If it is 1 they user is using
c.execute('CREATE TABLE IF NOT EXISTS outfits (username TEXT, outName TEXT, item TEXT);')
c.execute('CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, name TEXT);')
c.execute('CREATE TABLE IF NOT EXISTS clothes (username TEXT, id INTEGER, type TEXT, labels TEXT, clothName TEXT, frequency INTEGER);')
c.execute('CREATE TABLE IF NOT EXISTS outfit_history (username TEXT, outName TEXT, date TEXT);')
db.close()

#add cloth to clothes
def addCloth(user,Id, Type, labels, item, freq):
    f = "app.db"
    db = sqlite3.connect(f)
    c = db.cursor()
    c.execute('INSERT INTO items VALUES("%s", "%s", 0);' %(user,Id, Type, labels, item, freq) )
    db.commit()
    db.close()

#add item to outfits
def addOutfit(user, outName, item):
    f = "app.db"
    db = sqlite3.connect(f)
    c = db.cursor()
    c.execute('INSERT INTO outfits VALUES("%s", "%s", 0);' %(user, outName, item) )
    db.commit()
    db.close()

#returns a list of clothes of same type the user have
def getClothes(user, Type):
    f = "app.db"
    db = sqlite3.connect(f)
    c = db.cursor()
    c.execute('SELECT * FROM clothes WHERE username = "%s" AND type = "%s";' %(user, Type) )
    results = c.fetchall()
    db.close()
    return results
    
#returns a list of clothes the user have
def itemlist(user, Type):
    f = "app.db"
    db = sqlite3.connect(f)
    c = db.cursor()
    c.execute('SELECT * FROM clothes WHERE username = "%s";' %(user) )
    results = c.fetchall()
    db.close()
    return results

#checks if the item being added is a duplicate
def isunique(user,item):
    f = "app.db"
    db = sqlite3.connect(f)
    c = db.cursor()
    c.execute('SELECT item FROM items WHERE user = "%s";'  %(user) )
    results = c.fetchall()
    print results
    db.close()
    for result in results:
        print result[0]
        if item == result[0]:
            return True
    return False

#add the user to the databaseh
def adduser(user,password):
	f = "app.db"
	db = sqlite3.connect(f)
	c = db.cursor()
	if get_pass(user) is None:
		password = hashlib.sha224(password).hexdigest()
		c.execute('INSERT INTO users VALUES("%s", "%s", 100.0);' %(user, password))
        db.commit()
        db.close()
        return True
	db.close()
	return False

#returns the password of the user
def get_pass(user):
    f = "app.db"
    db = sqlite3.connect(f)
    c = db.cursor()
    c.execute('SELECT password FROM users WHERE username= "%s";' %(user))
    result = c.fetchall()
    if result == []:
        db.close()
        return None
    else:
        db.close()
        return result[0][0]

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
