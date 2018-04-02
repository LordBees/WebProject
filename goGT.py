#! C:/Users/wildcard/AppData/Local/Programs/Python35/python.exe

from flask import Flask, render_template, request, redirect

from datetime import datetime, date, timedelta

from wtforms import Form, validators
from wtforms_components import DateRange, SelectField
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


app = Flask(__name__)


# space for functions

# create connection to our mysql server
def getConnection():
	conn = mysql.connector.connect(user=user,password=passwd,host=host,database=db)
	return conn

# returns a list of departures
def getListOfDepartures():
	conn = getConnection()   
	cursor = conn.cursor()
	cursor.execute('SELECT *, Departure FROM webairtt') # we prob will need to modify to be used on diff tables
	departures = cursor.fetchall()
	conn.close()
	return departures	

# returns list of arrivals with matched departure
def getListOfArrivalsFromDeparture(departure):
	conn = getConnection()
	cursor = conn.cursor()
	query = 'SELECT *, Arrival FROM webairtt WHERE Departure = %s'
	args = (departure,)
	cursor.execute(query,args)
	arrivals = cursor.fetchall()
	conn.close()
	return arrivals	

# returns a list of depart times based on matching departure/arrival
def getListOfDepartureTimes(departure, arrival):
	conn = getConnection()
	cursor = conn.cursor()
	query = 'SELECT *, Departure Time FROM webairtt WHERE Departure = %s AND Arrival = %s'
	args = (departure, arrival)
	cursor.execute(query,args)
	departTimes = cursor.fetchall()
	conn.close()
	return departTimes	

# builds arrival select field for departure location
def buildArrivalsField(departure):
	arrivals = getListOfArrivalsFromDeparture(departure)
	members = []
	arriveNames = []
	i = 0

	members.append(None)
	arriveNames.append('--')
	i=i+1	
			
	for row in arrivals:
		#print(str(row[1]))
		if(str(row[3]) != 'None'):
			members.append(i)
			arriveNames.append(str(row[3]))
			i=i+1

			
	arriveNames = sorted(set(arriveNames), key=arriveNames.index)
	zip(members,arriveNames)
	arrivals = [(value, value) for value in arriveNames]
	
	return SelectField(choices=arrivals,default=None)

# builds departure select field
def buildDeparturesField():
	departures = getListOfDepartures()
	members = []
	departNames = []	
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
			i=i+1

			
	#departNames = set(departNames) # this changed the order after removing duplicates
	departNames = sorted(set(departNames), key=departNames.index)
	
	zip(members,departNames)
	departs = [(value, value) for value in departNames]
	return SelectField(choices=departs,default=None)

# builds departures time field based on depart/arrive location
def buildDepartTimesField(departure,arrival):
	times = getListOfDepartureTimes(departure,arrival)
	members = []
	departTimes = []
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
	
	return SelectField(choices=times,default=None)


# where we can put our template classes for booking forms, will end up populating it based on the current
# data within the database
def createPlaneForm(depart_location,arrive_location):
	class planeForm(Form):
		# restricting html5 embedded calendar field
		# here we are restricting bookable dates to 3 months at a time(months displayed * days in year/ months in year)		
		departDateMax = date.today() + timedelta(3*365/12) 
		departDateMin = date.today()
		
		# loading our form fields
		departLocation = buildDeparturesField()
		arriveLocation = buildArrivalsField(depart_location)
		departTime = buildDepartTimesField(depart_location,arrive_location)	

	return planeForm()
	
	
	
	
# basically makes plane travel form the default form that pops up 
@app.route("/")
def root():
	return redirect("/plane")
	
# working for static values atm, here we are going to end up calling some functions for database querying
# so we can build and accurate form
	
@app.route('/<travel_method>/')
def formatToTravMeth(travel_method=""):
	#request.form['testLabel'] = "LOL"
	depart_location="--"
	arrive_location="--"
	if travel_method == "plane":
		slideImage = "grandTravellogo.png"
		form = createPlaneForm(depart_location,arrive_location)
		#form.departLocation(default=None)
		#form.arriveLocation(default=None)
		return render_template("index.html",form=form,slideImage=slideImage)
		
	elif travel_method == "train": # needs changing
		slideImage = "grandTravellogo.png"
		form = createPlaneForm(depart_location,arrive_location)
		return render_template("index.html",form=form,slideImage=slideImage)

	elif travel_method == "bus": # needs changing
		slideImage = "grandTravellogo.png"
		form = createPlaneForm(depart_location,arrive_location)
		return render_template("index.html",form=form,slideImage=slideImage)
		
	elif travel_method == "taxi": # needs changing
		slideImage = ".png"
		form = createPlaneForm(depart_location,arrive_location)
		return render_template("index.html",form=form,slideImage=slideImage)
	
	elif travel_method == "ferry": # needs changing
		slideImage = "grandTravellogo.png"
		form = createPlaneForm(depart_location,arrive_location)
		return render_template("index.html",form=form,slideImage=slideImage)
	

@app.route('/<travel_method>/Departure=<depart_location>')
def formatToDepartLoc(travel_method="",depart_location=""):
	arrive_location="--"
	if travel_method == "plane":
		slideImage = "grandTravellogo.png"
		form = createPlaneForm(depart_location,arrive_location)
		#form.arriveLocation = buildArrivalsField(depart_location)
		#form.arriveLocation = buildArrivalsFeild(depart_location)
		if depart_location == "Cardiff": # just a test * remove later
			slideImage = ""
		return render_template("index.html",form=form,slideImage=slideImage)
		
	elif travel_method == "train": # needs changing
		slideImage = "grandTravellogo.png"
		form = createPlaneForm(depart_location,arrive_location)
		return render_template("index.html",form=form,slideImage=slideImage)

	elif travel_method == "bus": # needs changing
		slideImage = "grandTravellogo.png"
		form = createPlaneForm(depart_location,arrive_location)
		return render_template("index.html",form=form,slideImage=slideImage)
		
	elif travel_method == "taxi": # needs changing
		slideImage = ".png"
		form = createPlaneForm(depart_location,arrive_location)
		return render_template("index.html",form=form,slideImage=slideImage)
	
	elif travel_method == "ferry": # needs changing
		slideImage = "grandTravellogo.png"
		form = createPlaneForm(depart_location,arrive_location)
		return render_template("index.html",form=form,slideImage=slideImage)

		
# a bit further ahead atm, i need to get data being pulled from the database to accurately 
# start evaluating travel routes
# *atm this is just as the previous example so it will look nothing like this in the end
@app.route('/<travel_method>/Departure=<depart_location>&Arrival=<arrive_location>')
def formatToArrivalLoc(travel_method="", depart_location="",arrive_location=""):
	if travel_method == "plane":
		slideImage = "grandTravellogo.png"
		form = createPlaneForm(depart_location,arrive_location)
		if depart_location == "Cardiff": # just a test * remove later
			slideImage = ""
		return render_template("index.html",form=form,slideImage=slideImage)
		
	elif travel_method == "train": # needs changing
		slideImage = "grandTravellogo.png"
		form = createPlaneForm(depart_location,arrive_location)
		return render_template("index.html",form=form,slideImage=slideImage)

	elif travel_method == "bus": # needs changing
		slideImage = "grandTravellogo.png"
		form = createPlaneForm(depart_location,arrive_location)
		return render_template("index.html",form=form,slideImage=slideImage)
		
	elif travel_method == "taxi": # needs changing
		slideImage = ".png"
		form = createPlaneForm(depart_location,arrive_location)
		return render_template("index.html",form=form,slideImage=slideImage)
	
	elif travel_method == "ferry": # needs changing
		slideImage = "grandTravellogo.png"
		form = createPlaneForm(depart_location,arrive_location)
		return render_template("index.html",form=form,slideImage=slideImage)
		
# run the flask app (aka. host our website)
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
	#app.run(debug=True)
