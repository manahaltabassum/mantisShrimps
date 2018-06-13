import sqlite3, hashlib   #enable control of an sqlite database
from os import path
from random import randint

f = path.dirname(__file__) + "/../data/closet.db"

print "DIR: " + f

def assignID():
    return randint(0, 100000000000)

#get a dict for  {date: outfit ..,} for given username
def getOutHist(username):
    db = sqlite3.connect(f)
    c = db.cursor()
    c.execute('SELECT date, outName FROM outfit_history WHERE username="%s";' %(username) )
    ans = {}; 
    for item in c:
        print item
        ans[item[0]] = item[1]
        
    db.close()
    return ans;

def getOutfits(username):
    db = sqlite3.connect(f)
    c = db.cursor()
    outfits = c.execute('SELECT * FROM outfits WHERE username="%s";' %(username))
    my_dict = {}
    for entry in outfits:
        print entry
        if entry[1] in my_dict:
            my_dict[entry[1]].append(entry[2])
        else:
            my_dict[entry[1]] = [entry[2]]
    dates = c.execute('SELECT * FROM outfit_history WHERE username="%s";' %(username))
    for entry in dates:
        print entry[2]
        if entry[1] in my_dict:
            my_dict[entry[1]].append(entry[2])
    exten = c.execute('SELECT * FROM clothes WHERE username="%s";' %(username))
    for entry in exten:
        for key in my_dict:
            for val in my_dict[key]:
                if (val == entry[1]):
                    my_dict[key].append(entry[4])
    print my_dict
    db.close()
    return outfits

def addOutHist(user, outName, date):
    db = sqlite3.connect(f)
    c = db.cursor()
    c.execute('INSERT INTO outfit_history VALUES("%s", "%s", "%s");' %(user, outName, date) )
    db.commit()
    db.close()

#add cloth to clothes
def addCloth(user, typeC, clothName, clothId, extension):
    db = sqlite3.connect(f)
    c = db.cursor()
    c.execute('INSERT INTO clothes (username,type,clothName,id,extension) VALUES("%s", "%s", "%s", "%s", "%s");' %(user, typeC, clothName, clothId, extension))
    db.commit()
    db.close()

#add item to outfits
def addOutfit(user, outName, clothId):
    db = sqlite3.connect(f)
    c = db.cursor()
    c.execute('INSERT INTO outfits VALUES("%s", "%s", "%s");' %(user, outName, clothId) )
    db.commit()
    db.close()

#returns a list of clothes of same type the user have
def getClothes(user, Type):
    db = sqlite3.connect(f)
    c = db.cursor()
    c.execute('SELECT * FROM clothes WHERE username = "%s" AND type = "%s";' %(user, Type) )
    results = c.fetchall()
    db.close()
    return results
    
#returns a list of clothes the user have
def itemlist(user, Type):
    db = sqlite3.connect(f)
    c = db.cursor()
    c.execute('SELECT * FROM clothes WHERE username = "%s";' %(user) )
    results = c.fetchall()
    db.close()
    return results

#checks if the item being added is a duplicate
def isunique(user,item):
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

#add the user to the database
def adduser(user,password):
	db = sqlite3.connect(f)
	c = db.cursor()
	if get_pass(user) is None:
		password = hashlib.sha224(password).hexdigest()
		c.execute('INSERT INTO users VALUES("%s", "%s");' %(user, password))
        	db.commit()
        	db.close()
        	return True
	db.close()
	return False

#returns the password of the user
def get_pass(user):
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


#====================GENERAL DB HELPERS==========================

#NOTE: when putting in a string in the values array u have to do this: "'josh'"
#values is an array with values to insert for that row
def insertRow (tableName, fields, values, cursor):
    parameter = ' ('

    for field in fields:
        parameter += field + ", "
    parameter = parameter[0:-2] + ") VALUES ("
    #print parameter

    for value in values:
        val = str(value)
        if isinstance(value, basestring):
            val = "'" + val + "'"
        parameter += val + ", "
    parameter = parameter[0:-2] + ");"

    insert = "INSERT INTO " + tableName + parameter
    print "\n\n" + insert + "\n\n"

    cursor.execute(insert)



#condition is string type and follows WHERE statement for UPDATE
def update (tableName, field, newVal, condition, cursor):
    update = "UPDATE " + tableName + " SET " + field + " = " + str(newVal)
    if len(condition) != 0:
        update += " WHERE " + condition + ";"

    print "\n\n" + update + "\n\n"
    cursor.execute(update)

def table_gen(c):
    create_users = "CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY, password TEXT);"
    
    
    create_clothes = "CREATE TABLE IF NOT EXISTS clothes(username TEXT, id INTEGER PRIMARY KEY, type TEXT, clothName TEXT, extension TEXT, frequency INTEGER);"


    create_outfits = "CREATE TABLE IF NOT EXISTS outfits(username TEXT, outName TEXT, clothId INTEGER);"

    create_outhistory = "CREATE TABLE IF NOT EXISTS outfit_history(username TEXT, outName TEXT, date TEXT);"
    
    c.execute(create_users)
    #print "\n" + create_users + "\n"
    
    c.execute(create_clothes)
   # print "\n" + create_clothes + "\n"
    
    c.execute(create_outfits)
   # print "\n" + create_outfits + "\n"
    
    c.execute(create_outhistory)
   # print "\n" + create_outhistory + "\n" 
#===========================================================================================
db = sqlite3.connect(f)
c = db.cursor()
table_gen(c)
db.commit()
db.close()

    
#print getClothes("c", "top");

#print getOutHist("c");
