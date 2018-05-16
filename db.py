import sqlite3
import os
import hashlib
from flask import session

f = "app.db"
db = sqlite3.connect(f)
c = db.cursor()
#if a item has 0 the user is not using the item. If it is 1 they user is using
c.execute('CREATE TABLE IF NOT EXISTS items (user TEXT, item TEXT, playing INTEGER);')
c.execute('CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT, cash FLOAT);')
c.execute('CREATE TABLE IF NOT EXISTS highscore (username TEXT, score INTEGER);')
db.close()

#changes cash amount
def changevalue(change,user):
    f = "app.db"
    db = sqlite3.connect(f)
    c = db.cursor()
    c.execute('UPDATE users SET cash = "%d" WHERE username = "%s";' %(change,user))
    db.commit()
    db.close()

#get the amount of cash player has
def getcash(user):
    f = "app.db"
    db = sqlite3.connect(f)
    c = db.cursor()
    c.execute("SELECT cash FROM users WHERE username = '%s';" %(user) )
    results = c.fetchall()[0][0]
    db.commit()
    db.close()
    return float(results)

#checks if program can purchase
def canpurchase(user,value):
    money = getcash(user)
    return money > value


#add item to list
def additem(user,item):
    f = "app.db"
    db = sqlite3.connect(f)
    c = db.cursor()
    c.execute('INSERT INTO items VALUES("%s", "%s", 0);' %(user,item) )
    db.commit()
    db.close()

#returns a list of items the user is using
def itemlist(user):
    f = "app.db"
    db = sqlite3.connect(f)
    c = db.cursor()
    c.execute('SELECT * FROM items WHERE user = "%s";' %(user) )
    results = c.fetchall()
    db.close()
    return results

#returns a list of items the user is using
def itemusinglist(user):
    f = "app.db"
    db = sqlite3.connect(f)
    c = db.cursor()
    c.execute('SELECT * FROM items WHERE user = "%s" AND playing = 1 LIMIT 8;' %(user) )
    results = c.fetchall()
    db.close()
    return results

#helper function for adding that prevents adding if there is 8 items selected
def isnotmax(list):
    return len(list) < 8

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

#allows player to use item
def use(user,item):
    if isnotmax(itemusinglist(user)):
        f = "app.db"
        db = sqlite3.connect(f)
        c = db.cursor()
        c.execute('UPDATE items SET playing = 1 WHERE user = "%s" AND item = "%s";' %(user,item) )
        db.commit()
        db.close()

    #turns off item
def notuse(user,item):
    f = "app.db"
    db = sqlite3.connect(f)
    c = db.cursor()
    c.execute('UPDATE items SET playing = 0 WHERE user = "%s" AND item = "%s" ;' %(user,item) )
    db.commit()
    db.close()

#add score to score table
def addscore(user,score):
    f = "app.db"
    db = sqlite3.connect(f)
    c = db.cursor()
    c.execute('INSERT INTO highscore VALUES("%s", %d);' %(user, score))
    db.commit()
    db.close()

#get 10 highest scores from all users
def gethighscore():
    f = "app.db"
    db = sqlite3.connect(f)
    c = db.cursor()
    c.execute('SELECT * FROM highscore ORDER BY score DESC LIMIT 10;')
    results = c.fetchall()
    db.close
    return results

#return the 5 highest scores for a user
def gethighscore_user(user):
    f = "app.db"
    db = sqlite3.connect()
    c = db.cursor()
    e.execute('SELECT * FROM highscores WHERE username= "%s" ORDER BY score DESC LIMIT 5;' %(user) )
    results = c.fetchall()
    db.close
    return results

#add the user to the databaseh
def adduser(user,password):
	f = "app.db"
	db = sqlite3.connect(f)
	c = db.cursor()
	if get_pass(user) is None:
		password = hashlib.sha224(password).hexdigest()
		c.execute('INSERT INTO users VALUES("%s", "%s", 100.0);' %(user, password))
        c.execute('INSERT INTO items VALUES("%s", "kiwi.png", 0);' %(user) )
        c.execute('INSERT INTO items VALUES("%s", "grapple.png", 0);' %(user) )
        c.execute('INSERT INTO items VALUES("%s", "dragonfruit.png", 0);' %(user) )
        c.execute('INSERT INTO items VALUES("%s", "mango.png", 0);' %(user) )
        c.execute('INSERT INTO items VALUES("%s", "pineapple.png", 0);' %(user) )
        c.execute('INSERT INTO items VALUES("%s", "pomegranate.png", 0);' %(user) )
        c.execute('INSERT INTO items VALUES("%s", "watermelon.png", 0);' %(user) )
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
