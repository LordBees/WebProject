
from datetime import datetime, date, timedelta

from wtforms import Form, validators
from wtforms_components import DateRange, SelectField, IntegerField
from wtforms.validators import Length, NumberRange, DataRequired, InputRequired
from wtforms.fields.html5 import DateField

#from wtforms_components import DateTimeField

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

	

# returns a list of departures
def getListOfDeparturesPlain():
	conn = getConnection()   
	cursor = conn.cursor()
	cursor.execute('SELECT *, Departure FROM webairtt') # we prob will need to modify to be used on diff tables
	departures = cursor.fetchall()
	conn.close()
	return departures	

# returns list of arrivals with matched departure
def getListOfArrivalsFromDeparturePlain(departure):
	conn = getConnection()
	cursor = conn.cursor()
	query = 'SELECT *, Arrival FROM webairtt WHERE Departure = %s'
	args = (departure,)
	cursor.execute(query,args)
	arrivals = cursor.fetchall()
	conn.close()
	return arrivals	

# returns a list of depart times based on matching departure/arrival
def getListOfDepartureTimesPlain(departure, arrival):
	conn = getConnection()
	cursor = conn.cursor()
	query = 'SELECT *, Departure Time FROM webairtt WHERE Departure = %s AND Arrival = %s'
	args = (departure, arrival)
	cursor.execute(query,args)
	departTimes = cursor.fetchall()
	conn.close()
	return departTimes	

# returns a list of depart times based on matching departure/arrival
def getListOfArrivalTimesPlain(departure, arrival):
	conn = getConnection()
	cursor = conn.cursor()
	query = 'SELECT *, Arrival Time FROM webairtt WHERE Departure = %s AND Arrival = %s'
	args = (departure, arrival)
	cursor.execute(query,args)
	arriveTimes = cursor.fetchall()
	conn.close()
	return arriveTimes	

# returns list of arrivals with matched departure
def getPresetPricePlain(departure,arrival):
	conn = getConnection()
	cursor = conn.cursor()
	query = 'SELECT Price FROM webairtt WHERE Departure = %s AND Arrival = %s'
	args = (departure,arrival)
	cursor.execute(query,args)
	price = cursor.fetchone()
	#price = "%.2f" %(price)
	conn.close()
	return price[0]		

# returns number of seats left to book for this route
def getNumOfSeatsLeftAirPlain(departure,arrival):
	conn = getConnection()
	cursor = conn.cursor()
	query = 'SELECT *,%s FROM webairtt WHERE Departure = %s AND Arrival = %s'
	args = ("Passenger Count",departure,arrival)
	cursor.execute(query,args)
	passCnt = cursor.fetchone()
	print("passcnt "+ str(passCnt[7]))
	maxPass = 80 # max number of seats for a gt plane
	
	seatsLeft =  maxPass - int(passCnt[7])

	conn.close()
	return seatsLeft
	
# regular functions	
# builds arrival select field for departure location
def buildArrivalsFieldPlain(departure,arrival):

	arrivals = getListOfArrivalsFromDeparturePlain(departure)
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
def buildDeparturesFieldPlain(departure):
	departures = getListOfDeparturesPlain()
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
def buildDepartTimesFieldPlain(departure,arrival,time):
	times = getListOfDepartureTimesPlain(departure,arrival)
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


# where we can put our template classes for booking forms, will end up populating it based on the current
# data within the database
def createPlaneForm(depart_location,arrive_location,passenger_count,dtime,depart_date):
	class planeForm(Form):
		# restricting html5 embedded calendar field
		# here we are restricting bookable dates to 3 months at a time(months displayed * days in year/ months in year)		
		departDateMax = date.today() + timedelta(3*365/12) 
		departDateMin = date.today()
		if(depart_date != 0):
			departDateDefault = depart_date
		else:
			departDateDefault = 0
		
		passCnt = passenger_count
		passCntMin= 1
		
		# previous issue here was checking "" when they were sometimes set to "--", its consistent now for "--"
		if(depart_location != "--" and arrive_location != "--"): 
			passCntMax = getNumOfSeatsLeftAirPlain(depart_location,arrive_location)
			
			# just grab a departure time, its not a sophisticated time table so anyone for same depart/arrive is the same amount of time
			arrivalTime = getListOfArrivalTimesPlain(depart_location,arrive_location)
			departureTime = getListOfDepartureTimesPlain(depart_location,arrive_location)

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
						
			
		else:
			passCntMax = 1 # when the field is grayed out we still need to assign it something
		
		# loading our form fields
		departLocation = buildDeparturesFieldPlain(depart_location)
		arriveLocation = buildArrivalsFieldPlain(depart_location,arrive_location)	
		departTime = buildDepartTimesFieldPlain(depart_location,arrive_location,dtime)
		
		


	return planeForm()
	
	