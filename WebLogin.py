## login updater

# mysql functions
import mysql.connector

# MYSQL CONFIG VARIABLES
host           = "localhost";
db             = "gt";
user           = "root";
passwd         = ""


# space for functions

# create connection to our mysql server
def getConnection():
	conn = mysql.connector.connect(user=user,password=passwd,host=host,database=db)
	return conn

	



def User_exists(userEmail):
	conn = getConnection()
	cursor = conn.cursor()
	query = 'SELECT Cust_ID FROM userlogin WHERE Cust_Email = %s'
	args = (userEmail,)
	cursor.execute(query,args)
	result = cursor.fetchone()
	#price = "%.2f" %(price)
	conn.close()
	#return price[0]
	#	
	if(result[0][0] == userEmail):
        return True
    return False


def User_create(userEmail,userPass):
	conn = getConnection()   
	cursor = conn.cursor()
    query = "INSERT INTO userlogin (Cust_Email,Cust_Pass) VALUES (%s, &s)"
    args = (userEmail,userPass)
    cursor.execute(query,args) # we prob will need to modify to be used on diff tables
    departures = cursor.fetchall()
    conn.close()

##"INSERT INTO MyGuests (firstname, lastname, email) VALUES ('John', 'Doe', 'john@example.com')"

'''/*
conn = getConnection()
	cursor = conn.cursor()
	query = 'SELECT Price FROM webferrytt WHERE Departure = %s AND Arrival = %s'
	args = (departure,arrival)
	cursor.execute(query,args)
	price = cursor.fetchone()
	#price = "%.2f" %(price)
	conn.close()
	return price[0]	
*/'''

def User_changePass(userEmail,userNewPass):
	conn = getConnection()   
	cursor = conn.cursor()
	cursor.execute('SELECT *, Departure FROM webtraintt') # we prob will need to modify to be used on diff tables
	departures = cursor.fetchall()
	conn.close()
	return departures	




##functions to use in userlogin
def addCustomer(UserEmail,UserPass):
    if(not User_exists(UserEmail)):
        User_create(UserEmail,UserPass)
        return True
    return False

###other



def User_create():
	conn = getConnection()   
	cursor = conn.cursor()
	cursor.execute('SELECT *, Departure FROM webtraintt') # we prob will need to modify to be used on diff tables
	departures = cursor.fetchall()
	conn.close()
	return departures	
