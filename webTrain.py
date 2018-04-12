##meta name='author' content='Luke Clayton'"
##meta name='description' content='Grand Travel Web Train Func'"


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
	
	
# Updates to webtraintt/webtrainbook
def updateJourneyTablesFromBookingTrain(request,customerIdGend):
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

	# Calculates passenger count for form
	query = "SELECT PassengerCount FROM webtraintt WHERE Departure=%s AND Arrival=%s AND DepartureTime=%s"
	args = (departure_location,arrival_location, departTime)
	cursor.execute(query,args)
	passCount = cursor.fetchone()
	
	# Modifies passenger count
	query = "UPDATE webtraintt SET PassengerCount=%s WHERE Departure=%s AND Arrival=%s AND DepartureTime=%s"
	newPassCount = passengerCount + passCount[0]
	args = (newPassCount,departure_location,arrival_location, departTime)
	cursor.execute(query,args)
	
	# Insert passenger details 
	entry = [bookerFirstName,bookerLastName,vessleNumber,passengerCount*2,finalBookingPrice,customerID]
	cursor.execute("""INSERT INTO webtrainbook 
		(FirstName,LastName,TrainNum,Bags,Price,Cust_ID)
		VALUES(%s,%s,%s,%s,%s,%s)""", entry)
	
	conn.close()
	
	
# Modifies Train timetable
def modifyTrainTT(departLocation, arriveLocation, prevDepartTime, newDepartTime, prevArriveTime, newArriveTime,prevVessleNumber,newVessleNumber,price,status):
	conn = getConnection()   
	cursor = conn.cursor()	
	query = "SELECT COUNT(*) FROM webtraintt WHERE Departure =%s AND Arrival =%s AND DepartureTime = %s AND ArrivalTime =%s"
	args = (departLocation, arriveLocation, prevDepartTime+":00", prevArriveTime+":00")
	cursor.execute(query,args)
	count =  cursor.fetchone()
	print("count is:"+ str(count[0]))
	
	entryCount = count[0]
	
	# Update entry if record exists
	if(entryCount == 1):
		query = "UPDATE webtraintt SET DepartureTime = %s, ArrivalTime =%s, TrainNum =%s, Price =%s, Status = %s WHERE Departure =%s AND Arrival =%s AND DepartureTime = %s AND ArrivalTime =%s"
		args = (newDepartTime,newArriveTime,newVessleNumber,price,status,departLocation, arriveLocation, prevDepartTime+":00", prevArriveTime+":00")
		cursor.execute(query,args)
	
	# Create entry if record does not exist
	elif(entryCount == 0):
		entry = [departLocation,newDepartTime,arriveLocation,newArriveTime,newVessleNumber,price,0,status]
		cursor.execute("""INSERT INTO webtraintt 
		(Departure,DepartureTime,Arrival,ArrivalTime,TrainNum,Price,PassengerCount,Status)
		VALUES(%s,%s,%s,%s,%s,%s,%s,%s)""", entry)

	conn.close()


####################
#GET LISTS	

# Returns list of departures
def getListOfDeparturesTrain():
	conn = getConnection()   
	cursor = conn.cursor()
	cursor.execute('SELECT *, Departure FROM webtraintt') # we prob will need to modify to be used on diff tables
	departures = cursor.fetchall()
	conn.close()
	return departures	
	
# Returns list of departure times if matched in DB
def getListOfDepartureTimesTrain(departure, arrival):
	conn = getConnection()
	cursor = conn.cursor()
	query = 'SELECT *, Departure Time FROM webtraintt WHERE Departure = %s AND Arrival = %s'
	args = (departure, arrival)
	cursor.execute(query,args)
	departTimes = cursor.fetchall()
	conn.close()
	return departTimes	

# Returns list of arrivals
def getListOfArrivalsFromDepartureTrain(departure):
	conn = getConnection()
	cursor = conn.cursor()
	query = 'SELECT *, Arrival FROM webtraintt WHERE Departure = %s'
	args = (departure,)
	cursor.execute(query,args)
	arrivals = cursor.fetchall()
	conn.close()
	return arrivals	


# Returns list of arrival times if matched in DB
def getListOfArrivalTimesTrain(departure, arrival):
	conn = getConnection()
	cursor = conn.cursor()
	query = 'SELECT *, Arrival Time FROM webtraintt WHERE Departure = %s AND Arrival = %s'
	args = (departure, arrival)
	cursor.execute(query,args)
	arriveTimes = cursor.fetchall()
	conn.close()
	return arriveTimes	
	
# Returns number of seats left for route
def getNumOfSeatsLeftTrain(departure,arrival):
	conn = getConnection()
	cursor = conn.cursor()
	query = 'SELECT *,%s FROM webtraintt WHERE Departure = %s AND Arrival = %s'
	args = ("Passenger Count",departure,arrival)
	cursor.execute(query,args)
	passCnt = cursor.fetchone()
	print("passcnt "+ str(passCnt[7]))
	maxPass = 250 # max number of seats for a gt Train
	
	seatsLeft =  maxPass - int(passCnt[7])

	conn.close()
	return seatsLeft

# Returns matching departures in DB
def getPresetPriceTrain(departure,arrival):
	conn = getConnection()
	cursor = conn.cursor()
	query = 'SELECT Price FROM webtraintt WHERE Departure = %s AND Arrival = %s'
	args = (departure,arrival)
	cursor.execute(query,args)
	price = cursor.fetchone()
	#price = "%.2f" %(price)
	conn.close()
	return price[0]		


	
####################
#BUILD LISTS

# Populates arrival field based on departure
def buildArrivalsFieldTrain(departure,arrival):

	arrivals = getListOfArrivalsFromDepartureTrain(departure)
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
		
	return SelectField(choices=arrivals, default = defaultSelection,id="arriveLocation")
	

# Populates departure field
def buildDeparturesFieldTrain(departure):
	departures = getListOfDeparturesTrain()
	members = []
	departNames = []	
	default_selection = 0	
	i = 0
	members.append(None)
	departNames.append('--')
	i=i+1		
	
	for row in departures:
		
		if(i > 0):
			members.append(i)
			departNames.append(str(row[1]))
			print("departure="+departure+"depart from mysql="+str(row[1]))
			i=i+1

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
	
	return SelectField(choices=departs, default = defaultSelection,id="departLocation")

# Populate departure field matching times in DB
def buildDepartTimesFieldTrain(departure,arrival,time):
	times = getListOfDepartureTimesTrain(departure,arrival)
	members = []
	departTimes = []
	default_selection = 0
	i = 0
	members.append(None)
	departTimes.append('--')
	i=i+1	
			
	for row in times:
		
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
	
	return SelectField(choices=times,default=defaultSelection,id="departTime")

	

def calcJourneyTimeTrain(depart_location,arrive_location):
	journeyTime = 0
	if(depart_location != "--" and arrive_location != "--"):

		# just grab a departure time, its not a sophisticated time table so anyone for same depart/arrive is the same amount of time
		arrivalTime = getListOfArrivalTimesTrain(depart_location,arrive_location)
		departureTime = getListOfDepartureTimesTrain(depart_location,arrive_location)
				
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
	

# Database date allows creating of forms. Index calls last so must remain at end
def createTrainForm(depart_location,arrive_location,passenger_count,dtime,depart_date):
	class TrainForm(Form):
		departDateMax = date.today() + timedelta(3*365/12) 
		departDateMin = date.today()
		if(depart_date != 0):
			departDateDefault = depart_date
		else:
			departDateDefault = 0
		
		passCnt = passenger_count

		if(int(passenger_count) > 0):
			passCntMin= 1
		else:
			passCntMin=0

		#calculate journeyTime			
		journeyTime = calcJourneyTimeTrain(depart_location,arrive_location)
					
           
		if(depart_location != "--" and arrive_location != "--"): 
			passCntMax = getNumOfSeatsLeftTrain(depart_location,arrive_location)
					
		else:
			passCntMax = 1 

		departLocation = buildDeparturesFieldTrain(depart_location)
		arriveLocation = buildArrivalsFieldTrain(depart_location,arrive_location)	
		departTime = buildDepartTimesFieldTrain(depart_location,arrive_location,dtime)


	return TrainForm()
