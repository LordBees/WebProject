
from datetime import datetime, date, timedelta

from wtforms import Form, validators
from wtforms_components import DateRange, SelectField, IntegerField
from wtforms.validators import Length, NumberRange, DataRequired, InputRequired
from wtforms.fields.html5 import DateField

#from wtforms_components import DateTimeField

# mysql functions
import mysql.connector
import WebSQLUtil as Qman

# import my lib
#import WebSQLUtil as Qman

# MYSQL CONFIG VARIABLES
host           = "localhost";
db             = "gt";
user           = "root";
passwd         = ""


# space for functions

# update/insert to webferrytt/webferrybook
def updateJourneyTablesFromBookingFerry(request,customerIdGend):
	departure_location = request.form.get('departure_location')
	arrival_location = request.form.get('arrival_location')
	departTime = request.form.get('departTime')
	departDate = request.form.get('departDate')
	passengerCount = int(request.form.get('passengerCount'))
	finalBookingPrice =	float(request.form.get('discountedPrice'))
	bookerFirstName= request.form.get('FirstName')
	bookerLastName= request.form.get('LastName')
	customerIdForm = request.form.get('customerID')
	vessleNumber = str(request.form.get('vessleNumber'))

	if(customerIdForm != 0):
		customerID = customerIdGend
	else:
		customerID = customerIdForm
	
	conn = getConnection()   
	cursor = conn.cursor()	

	# find out the passenger count for this route currently
	query = "SELECT PassengerCount FROM webferrytt WHERE Departure=%s AND Arrival=%s AND DepartureTime=%s"
	args = (departure_location,arrival_location, departTime)
	cursor.execute(query,args)
	passCount = cursor.fetchone()
	
	# adjust passenger count
	query = "UPDATE webferrytt SET PassengerCount=%s WHERE Departure=%s AND Arrival=%s AND DepartureTime=%s"
	newPassCount = passengerCount + passCount[0]
	args = (newPassCount,departure_location,arrival_location, departTime)
	cursor.execute(query,args)
	
	# insert passenger details into journey booking table
	entry = [bookerFirstName,bookerLastName,vessleNumber,passengerCount*2,finalBookingPrice,customerID]
	cursor.execute("""INSERT INTO webferrybook 
		(FirstName,LastName,FerryNum,Bags,Price,Cust_ID)
		VALUES(%s,%s,%s,%s,%s,%s)""", entry)
	
	conn.close()
	
# modify the time table
def modifyFerryTT(departLocation,	arriveLocation,	prevDepartTime, newDepartTime, prevArriveTime,	newArriveTime,prevVessleNumber,newVessleNumber,price,status):
	conn = getConnection()   
	cursor = conn.cursor()	
	query = "SELECT COUNT(*) FROM webferrytt WHERE Departure =%s AND Arrival =%s AND DepartureTime = %s AND ArrivalTime =%s"
	args = (departLocation, arriveLocation, prevDepartTime+":00", prevArriveTime+":00")
	cursor.execute(query,args)
	count =  cursor.fetchone()
	print("count is:"+ str(count[0]))
	
	entryCount = count[0]
	
	# if the entry exists update it
	if(entryCount == 1):
		query = "UPDATE webferrytt SET DepartureTime = %s, ArrivalTime =%s, FerryNum =%s, Price =%s, Status = %s WHERE Departure =%s AND Arrival =%s AND DepartureTime = %s AND ArrivalTime =%s"
		args = (newDepartTime,newArriveTime,newVessleNumber,price,status,departLocation, arriveLocation, prevDepartTime+":00", prevArriveTime+":00")
		cursor.execute(query,args)
	
	# if it doesnt then make insert it
	elif(entryCount == 0):
		entry = [departLocation,newDepartTime,arriveLocation,newArriveTime,newVessleNumber,price,0,status]
		cursor.execute("""INSERT INTO webferrytt 
		(Departure,DepartureTime,Arrival,ArrivalTime,FerryNum,Price,PassengerCount,Status)
		VALUES(%s,%s,%s,%s,%s,%s,%s,%s)""", entry)

	
	conn.close()
	
# create connection to our mysql server
def getConnection():
	conn = mysql.connector.connect(user=user,password=passwd,host=host,database=db)
	return conn

	

# returns a list of departures
def getListOfDeparturesFerry():
	conn = getConnection()   
	cursor = conn.cursor()
	cursor.execute('SELECT *, Departure FROM webferrytt') # we prob will need to modify to be used on diff tables
	departures = cursor.fetchall()
	conn.close()
	return departures	

# returns list of arrivals with matched departure
def getListOfArrivalsFromDepartureFerry(departure):
	#conn = getConnection()
	#cursor = conn.cursor()
	query = 'SELECT *, Arrival FROM webferrytt WHERE Departure = %s'
	args = (departure,)
	#cursor.execute(query,args)
	#arrivals = cursor.fetchall()
	arrivals = Qman.executeSQLFetchAll_args(query,args)
	#conn.close()
	return arrivals	

# returns a list of depart times based on matching departure/arrival
def getListOfDepartureTimesFerry(departure, arrival):
	#conn = getConnection()
	#cursor = conn.cursor()
	query = 'SELECT *, Departure Time FROM webferrytt WHERE Departure = %s AND Arrival = %s'
	args = (departure, arrival)
	#cursor.execute(query,args)
	#departTimes = cursor.fetchall()
	#conn.close()
	departTimes = Qman.executeSQLFetchAll_args(query,args)
	return departTimes	

# returns a list of depart times based on matching departure/arrival
def getListOfArrivalTimesFerry(departure, arrival):
	#conn = getConnection()
	#cursor = conn.cursor()
	query = 'SELECT *, Arrival Time FROM webferrytt WHERE Departure = %s AND Arrival = %s'
	args = (departure, arrival)
	#cursor.execute(query,args)
	#arriveTimes = cursor.fetchall()
	#conn.close()
	arriveTimes = Qman.executeSQLFetchAll_args(query,args)
	return arriveTimes	

# returns list of arrivals with matched departure
def getPresetPriceFerry(departure,arrival):
	#conn = getConnection()
	#cursor = conn.cursor()
	query = 'SELECT Price FROM webferrytt WHERE Departure = %s AND Arrival = %s'
	args = (departure,arrival)
	#cursor.execute(query,args)
	#price = cursor.fetchone()
	##price = "%.2f" %(price)
	#conn.close()
	price = Qman.executeSQLFetchOne_args(query,args)
	return price[0]		

# returns number of seats left to book for this route
def getNumOfSeatsLeftFerry(departure,arrival):
	#conn = getConnection()
	#cursor = conn.cursor()
	query = 'SELECT *,%s FROM webferrytt WHERE Departure = %s AND Arrival = %s'
	args = ("Passenger Count",departure,arrival)
	#cursor.execute(query,args)
	#passCnt = cursor.fetchone()
	passCnt = Qman.executeSQLFetchOne_args(query,args)
	print("passcnt "+ str(passCnt[7]))
	maxPass = 500 # max number of seats for a gt ferry
	
	seatsLeft =  maxPass - int(passCnt[7])

	#conn.close()
	return seatsLeft
	
# regular functions	
# builds arrival select field for departure location
def buildArrivalsFieldFerry(departure,arrival):

	arrivals = getListOfArrivalsFromDepartureFerry(departure)
	members = []
	arriveNames = []	
	default_selection = 0
	
		
	i = 0

	members.append(None)
	arriveNames.append('--')
	i=i+1		
	
	for row in arrivals:
		#print(str(row[1]))
	
		#if(str(row[1]) != 'None' and i > 0):
		if(i > 0):
			members.append(i)
			arriveNames.append(str(row[3]))
			i=i+1
		
	arriveNames = sorted(set(arriveNames), key=arriveNames.index)
	zip(members,arriveNames)
	arrivals = [(value, value) for value in arriveNames]
	
	d = 0
	for name in arriveNames:
		if(name == arrival):
			default_selection = d
		d = d+1
		
	if default_selection != 0:
		defaultSelection = arriveNames[default_selection]
	else:
		defaultSelection = 0
	
	return SelectField(choices=arrivals, default = defaultSelection)
	
	

# builds departure select field
def buildDeparturesFieldFerry(departure):
	departures = getListOfDeparturesFerry()
	members = []
	departNames = []	
	default_selection = 0
	
		
	i = 0

	members.append(None)
	departNames.append('--')
	i=i+1		
	
	for row in departures:
		#print(str(row[1]))
	
		#if(str(row[1]) != 'None' and i > 0):
		if(i > 0):
			members.append(i)
			departNames.append(str(row[1]))
			print("departure="+departure+"depart from mysql="+str(row[1]))
			i=i+1
		
	#departNames = set(departNames) # this changed the order after removing duplicates
	departNames = sorted(set(departNames), key=departNames.index)
	zip(members,departNames)
	departs = [(value, value) for value in departNames]
	
	d = 0
	for name in departNames:
		if(name == departure):
			default_selection = d
		d = d+1
		
	if default_selection != 0:
		defaultSelection = departNames[default_selection]
	else:
		defaultSelection = 0
	
	return SelectField(choices=departs, default = defaultSelection)

# builds departures time field based on depart/arrive location
def buildDepartTimesFieldFerry(departure,arrival,time):
	times = getListOfDepartureTimesFerry(departure,arrival)
	members = []
	departTimes = []
	default_selection = 0
	
	i = 0

	members.append(None)
	departTimes.append('--')
	i=i+1	
			
	for row in times:
		#print(str(row[1]))
		if(str(row[2]) != 'None'):
			members.append(i)
			departTimes.append(str(row[2]))
			i=i+1

			
	departTimes = sorted(set(departTimes), key=departTimes.index)
	zip(members,departTimes)
	times = [(value, value) for value in departTimes]
	
	d = 0
	for t in departTimes:
		if(time == t):
			default_selection = d
		d=d+1
	
	if(time != 0):
			defaultSelection = departTimes[default_selection] 
	else:
		defaultSelection = 0
	
	return SelectField(choices=times,default=defaultSelection)

def calcJourneyTimeFerry(depart_location,arrive_location):
	journeyTime = 0
	if(depart_location != "--" and arrive_location != "--"):

		# just grab a departure time, its not a sophisticated time table so anyone for same depart/arrive is the same amount of time
		arrivalTime = getListOfArrivalTimesFerry(depart_location,arrive_location)
		departureTime = getListOfDepartureTimesFerry(depart_location,arrive_location)
				
		#first one we get from list
		atime = arrivalTime[0]
		dpttime = departureTime[0]
				
		# calculate the difference
		calcTime = atime[4] - dpttime[2]
		# find out how many hours it is and store the remainder
		hours, remainder = divmod(calcTime.seconds, 3600)			
		# divide the remainder into seconds/minutes left
		minutes, seconds = divmod(remainder, 60)
				
		#just some general output formatting, when will minutes ever be 1? prob never
		if(minutes == 0):
			if(hours > 1):
				journeyTime = "%d hours" % (hours)
			else:
				journeyTime = "%d hour" % (hours)					
				
		else:
			if(hours > 1):
				journeyTime = "%d hours and %d minutes" % (hours,minutes)
			else:
				if(hours == 0):
					journeyTime = "%d minutes" % (minutes)
				else:
					journeyTime = "%d hour and %d minutes" % (hours,minutes)	

	return journeyTime	
	

# where we can put our template classes for booking forms, will end up populating it based on the current
# data within the database
def createFerryForm(depart_location,arrive_location,passenger_count,dtime,depart_date):
	class ferryForm(Form):
		# restricting html5 embedded calendar field
		# here we are restricting bookable dates to 3 months at a time(months displayed * days in year/ months in year)		
		departDateMax = date.today() + timedelta(3*365/12) 
		departDateMin = date.today()
		if(depart_date != 0):
			departDateDefault = depart_date
		else:
			departDateDefault = 0
		
		passCnt = passenger_count
		#passCntMin= 1
		
		if(int(passenger_count) > 0):
			passCntMin = 1
		else:
			passCntMin = 0

		#calculate journeyTime
		journeyTime = calcJourneyTimeFerry(depart_location,arrive_location)
			
		# previous issue here was checking "" when they were sometimes set to "--", its consistent now for "--"
		if(depart_location != "--" and arrive_location != "--"): 
			passCntMax = getNumOfSeatsLeftFerry(depart_location,arrive_location)
			
		else:
			passCntMax = 1 # when the field is grayed out we still need to assign it something
		
		# loading our form fields
		departLocation = buildDeparturesFieldFerry(depart_location)
		arriveLocation = buildArrivalsFieldFerry(depart_location,arrive_location)	
		departTime = buildDepartTimesFieldFerry(depart_location,arrive_location,dtime)
		
		


	return ferryForm()
	
	
