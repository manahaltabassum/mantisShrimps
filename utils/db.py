import sqlite3   #enable control of an sqlite database

#add cloth to clothes
def addCloth(user,Id, Type, labels, item, freq):
    f = "data/closet.db"
    db = sqlite3.connect(f)
    c = db.cursor()
    c.execute('INSERT INTO items VALUES("%s", "%s", 0);' %(user,Id, Type, labels, item, freq) )
    db.commit()
    db.close()

#add item to outfits
def addOutfit(user, outName, item):
    f = "data/closet.db"
    db = sqlite3.connect(f)
    c = db.cursor()
    c.execute('INSERT INTO outfits VALUES("%s", "%s", 0);' %(user, outName, item) )
    db.commit()
    db.close()

#returns a list of clothes of same type the user have
def getClothes(user, Type):
    f = "data/closet.db"
    db = sqlite3.connect(f)
    c = db.cursor()
    c.execute('SELECT * FROM clothes WHERE username = "%s" AND type = "%s";' %(user, Type) )
    results = c.fetchall()
    db.close()
    return results
    
#returns a list of clothes the user have
def itemlist(user, Type):
    f = "data/closet.db"
    db = sqlite3.connect(f)
    c = db.cursor()
    c.execute('SELECT * FROM clothes WHERE username = "%s";' %(user) )
    results = c.fetchall()
    db.close()
    return results

#checks if the item being added is a duplicate
def isunique(user,item):
    f = "data/closet.db"
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
	f = "data/closet.db"
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
    f = "data/closet.db"
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
    
    
    create_clothes = "CREATE TABLE IF NOT EXISTS clothes(username TEXT PRIMARY KEY, id INTEGER PRIMARY KEY AUTOINCREMENT, type TEXT, label TEXT, clothName TEXT, frequency INTEGER);"


    create_outfits = "CREATE TABLE IF NOT EXISTS outfits(username TEXT PRIMARY KEY, outName TEXT, id INTEGER PRIMARY KEY);"

    create_outhistory = "CREATE TABLE IF NOT EXISTS outfit_history( username TEXT PRIMARY KEY, outName TEXT, date TEXT);"
    
    c.execute(create_users)
    c.execute(create_clothes)
    c.execute(create_outfits)
    c.execute(create_outhistory)    
#===========================================================================================

db = sqlite3.connect("data/closet.db")
c = db.cursor()
table_gen(c)
db.commit()
db.close()

    
