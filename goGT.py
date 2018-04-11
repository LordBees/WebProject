#! C:/Users/wildcard/AppData/Local/Programs/Python35/python.exe

import random
import sys
import os
import uuid 
 
from flask import Flask, render_template, request, redirect, url_for

from wtforms import Form, validators, TextField
from wtforms_components import DateRange, SelectField, IntegerField
from wtforms.validators import Length, NumberRange, DataRequired, InputRequired
from wtforms.fields.html5 import DateField

from functools import wraps

#import everything from our travel method implementation files
from webAir import *
from webTrain import *
from webFerry import * 
from WebMakeReciept import *

app = Flask(__name__)

def handleMaintenceRequest(travelMethod,departLocation,	arriveLocation,	prevDepartTime, newDepartTime, prevArriveTime,	newArriveTime,prevVessleNumber,newVessleNumber,price,status):

	tableName = ""

	if(travelMethod == "Plane"):
		modifyAirTT(departLocation,	arriveLocation,	prevDepartTime, newDepartTime, prevArriveTime,	newArriveTime,prevVessleNumber,newVessleNumber,price,status)
	elif(travelMethod == "Bus"):
		modifyAirTT(departLocation,	arriveLocation,	prevDepartTime, newDepartTime, prevArriveTime,	newArriveTime,prevVessleNumber,newVessleNumber,price,status)
	elif(travelMethod == "Taxi"):
		modifyAirTT(departLocation,	arriveLocation,	prevDepartTime, newDepartTime, prevArriveTime,	newArriveTime,prevVessleNumber,newVessleNumber,price,status)
	elif(travelMethod == "Train"):
		modifyTrainTT(departLocation,	arriveLocation,	prevDepartTime, newDepartTime, prevArriveTime,	newArriveTime,prevVessleNumber,newVessleNumber,price,status)
	elif(travelMethod == "Ferry"):
		modifyFerryTT(departLocation,	arriveLocation,	prevDepartTime, newDepartTime, prevArriveTime,	newArriveTime,prevVessleNumber,newVessleNumber,price,status)

	
	
def getbookingPrimaryKey(cid,Ttable):
    conn = getConnection()
    cursor = conn.cursor()
    query = 'SELECT ID FROM '+str(Ttable)+' WHERE Cust_ID = %s'
    args = (cid,)
    cursor.execute(query,args)
    result = cursor.fetchone()
    conn.close()
    return result


ACCESS = {
    'guest': 0,
    'user': 1,
    'admin': 2
}

def createUser(name,email,password,access):
	class User():
		def __init__(self, name, email, password, access=ACCESS['user']):
			self.name = name
			self.email = email
			self.password = password
			self.access = access
		
		def is_admin(self):
			return self.access == ACCESS['admin']
		
		def allowed(self, access_level):
			return self.access >= access_level
			
def requires_access_level(access_level,user):
	def decorator(f):
		@wraps(f)
		def decorated_function(*args, **kwargs):
			
			if not session.get('email'):
				return redirect(url_for('users.login'))
				
			elif(not user.allowed(access_level)):
				return redirect(url_for('users.profile', message="You do not have access to that page. Sorry!"))
			return f(*args, **kwargs)
		return decorated_function
	return decorator

def getVessleId(departure, arrival,travel_method):
	conn = getConnection()
	cursor = conn.cursor()
	if(travel_method == "Plane"):
		query = 'SELECT FlightNum FROM webairtt	WHERE Departure = %s AND Arrival = %s'
		args = (departure, arrival)
	if(travel_method == "Train"):
		query = 'SELECT TrainNum FROM webtraintt	WHERE Departure = %s AND Arrival = %s'
		args = (departure, arrival)
	if(travel_method == "Bus"):
		query = 'SELECT BusNum FROM webbustt	WHERE Departure = %s AND Arrival = %s'
		args = (departure, arrival)	
	if(travel_method == "Taxi"):
		query = 'SELECT TaxiNum FROM webtaxitt	WHERE Departure = %s AND Arrival = %s'
		args = (departure, arrival)		
	if(travel_method == "Ferry"):
		query = 'SELECT FerryNum FROM webferrytt WHERE Departure = %s AND Arrival = %s'
		args = (departure, arrival)
		
	cursor.execute(query,args)
	vessleNum = cursor.fetchone()
	conn.close()
	return vessleNum	
	
def addCustomerLoginDetails(username,password,customerID):
	conn = getConnection()
	cursor = conn.cursor()
	try:
		cursor.execute("""INSERT INTO userlogin VALUES (%s,%s,%s)""",(username,password,customerID))
		conn.commit()
	except:
		conn.rollback()
	conn.close()

def checkAdminPassword(password):
	conn = getConnection()
	cursor = conn.cursor()	
	query = 'SELECT passWord FROM userlogin WHERE userName = %s'
	args = ("admin",)
	cursor.execute(query,args)
	adminPass = cursor.fetchone()
	conn.close()
	if password == adminPass[0]:
		return True
	else:
		return False
	
def getSomeRandomNumberHex(numCount):
	random.seed(datetime.now())
	number = uuid.uuid4().hex
	choppedNumber = number[:numCount]
	return choppedNumber
	
def getSomeRandomNumberDec(numCount):
	random.seed(datetime.now())
	number = str(uuid.uuid4().int)
	choppedNumber = number[:numCount]
	return choppedNumber 
	
def doesCustomerIdExist(customerID):
	conn = getConnection()
	cursor = conn.cursor()
	query = 'SELECT customerID, COUNT(*) FROM receipts WHERE customerID = %s'
	args = (customerID,)	
	cursor.execute(query,args)
	idCount = cursor.rowcount
	conn.close()
	if idCount > 0:
		return True
	else:
		return False	
		
def addReceiptEntry(receiptID,customerID):
	conn = getConnection()
	cursor = conn.cursor()
	try:
		cursor.execute("""INSERT INTO receipts VALUES (%s,%s)""",(receiptID,customerID))
		conn.commit()
	except:
		conn.rollback()
	conn.close()


def isThereAnAdult(form):
	passengerCount = int(form.get('passengerCount'))
	i = 1
	
	while i <= passengerCount:	
		passengerAge = int(form.get('passengerAge'+str(i)))
		#if there is a child, but only discount on children not traveling alone
		if (passengerAge > 16):
			return True
		i=i+1	
		
	return False

def createPassengerForm(passenger_count):
	class passengerForm(Form):
		
		testlist = [5]
		passengerFirstNameFields = []
		passengerLastNameFields = []
		passengerAgeFields = []
		for passenger in passenger_count:
			passengerFirstNameFields.append(TextField('First Name'))
			passengerLastNameFields.append(TextField('Last Name'))
			passengerAgeFields.append(TextField('Age'))
	return passengerForm()

# basically makes plane travel form the default form that pops up 
@app.route("/")
def root():
	return redirect("/plane")
	
# working for static values atm, here we are going to end up calling some functions for database querying
# so we can build and accurate form
	
@app.route('/<travel_method>/')
def formatToTravMeth(travel_method=""):
	#default our variables
	depart_location="--"
	arrive_location="--"
	passenger_count=0
	dtime=0
	depart_date=0
	
	if travel_method == "plane":
		slideImage = "GTplane.jpg"
		form = createPlaneForm(depart_location,arrive_location,passenger_count,dtime,depart_date)
		#form.departLocation(default=None)
		#form.arriveLocation(default=None)
		return render_template("index.html",form=form,slideImage=slideImage)
		
	elif travel_method == "train": # needs changing
		slideImage = "GTtrain.jpg"
		#luke please update your code to now follow the new method here, so create train form with the arguments im using now etc etc..
		# do so for the 2 other instances of it below as well in other app routes
		form = createTrainForm(depart_location,arrive_location,passenger_count,dtime,depart_date)
		return render_template("index.html",form=form,slideImage=slideImage)

	elif travel_method == "bus": # needs changing
		slideImage = "GTbus.jpg"
		form = createPlaneForm(depart_location,arrive_location,passenger_count,dtime,depart_date)
		return render_template("index.html",form=form,slideImage=slideImage)
		
	elif travel_method == "taxi": # needs changing
		slideImage = "GTtaxi.jpg"
		form = createPlaneForm(depart_location,arrive_location,passenger_count,dtime,depart_date)
		return render_template("index.html",form=form,slideImage=slideImage)
	
	elif travel_method == "ferry": # needs changing
		slideImage = "GTferry.jpg"
		form = createFerryForm(depart_location,arrive_location,passenger_count,dtime,depart_date) 
		return render_template("index.html",form=form,slideImage=slideImage)
	

@app.route('/<travel_method>/Departure=<depart_location>')
def formatToDepartLoc(travel_method="",depart_location="--"):
	#default our variables
	arrive_location="--"
	passenger_count=0
	dtime=0
	depart_date=0

	
	if travel_method == "plane":
		slideImage = "GTplane.jpg"
		form = createPlaneForm(depart_location,arrive_location,passenger_count,dtime,depart_date)
		#form.arriveLocation = buildArrivalsField(depart_location)
		#form.arriveLocation = buildArrivalsFeild(depart_location)

		return render_template("index.html",form=form,slideImage=slideImage)
		
	elif travel_method == "train": # needs changing
		slideImage = "GTtrain.jpg"
		form = createTrainForm(depart_location,arrive_location,passenger_count,dtime,depart_date)
		return render_template("index.html",form=form,slideImage=slideImage)

	elif travel_method == "bus": # needs changing
		slideImage = "GTbus.jpg"
		form = createPlaneForm(depart_location,arrive_location,passenger_count,dtime,depart_date)
		return render_template("index.html",form=form,slideImage=slideImage)
		
	elif travel_method == "taxi": # needs changing
		slideImage = "GTtaxi.jpg"
		form = createPlaneForm(depart_location,arrive_location,passenger_count,dtime,depart_date)
		return render_template("index.html",form=form,slideImage=slideImage)
	
	elif travel_method == "ferry": # needs changing
		slideImage = "GTferry.jpg"
		form = createFerryForm(depart_location,arrive_location,passenger_count,dtime,depart_date) 
		return render_template("index.html",form=form,slideImage=slideImage)


# a bit further ahead atm, i need to get data being pulled from the database to accurately 
# start evaluating travel routes
# *atm this is just as the previous example so it will look nothing like this in the end
@app.route('/<travel_method>/Departure=<depart_location>&Arrival=<arrive_location>')
# here we can map multiple url routes to the same condition! =)

@app.route('/<travel_method>/Departure=<depart_location>&Arrival=<arrive_location>&Time=<dtime>') 
@app.route('/<travel_method>/Departure=<depart_location>&Arrival=<arrive_location>&Time=<dtime>&passCnt=<passenger_count>') 
@app.route('/<travel_method>/Departure=<depart_location>&Arrival=<arrive_location>&Time=<dtime>&passCnt=<passenger_count>&Date=<depart_date>') 
def formatToArrivalLoc(travel_method="", depart_location="--",arrive_location="--", passenger_count=0,dtime=0,depart_date=0):
	if travel_method == "plane":
		slideImage = "GTplane.jpg"
		form = createPlaneForm(depart_location,arrive_location,passenger_count,dtime,depart_date)
		if(int(passenger_count) <= form.passCntMax):
			printedPrice = str(int(getPresetPricePlane(depart_location,arrive_location)) * int(passenger_count))
		else:
			printedPrice = "not enough seats"

		return render_template("index.html",form=form,slideImage=slideImage,bookingPrice=printedPrice)
		
	elif travel_method == "train": # needs changing
		slideImage = "GTtrain.jpg"
		form = createTrainForm(depart_location,arrive_location,passenger_count,dtime,depart_date)
		if(int(passenger_count) <= form.passCntMax):
			printedPrice = str(int(getPresetPriceFerry(depart_location,arrive_location)) * int(passenger_count))
		else:
			printedPrice = "not enough seats"

		return render_template("index.html",form=form,slideImage=slideImage,bookingPrice=printedPrice)

	elif travel_method == "bus": # needs changing
		slideImage = "GTbus.jpg"
		form = createPlaneForm(depart_location,arrive_location,passenger_count,dtime,depart_date)
		return render_template("index.html",form=form,slideImage=slideImage)
		
	elif travel_method == "taxi": # needs changing
		slideImage = "GTtaxi.jpg"
		form = createPlaneForm(depart_location,arrive_location,passenger_count,dtime,depart_date)
		return render_template("index.html",form=form,slideImage=slideImage)
	
	elif travel_method == "ferry": # needs changing
		slideImage = "GTferry.jpg"
		form = createFerryForm(depart_location,arrive_location,passenger_count,dtime,depart_date) 
		if(int(passenger_count) <= form.passCntMax):
			printedPrice = str(int(getPresetPriceFerry(depart_location,arrive_location)) * int(passenger_count))
		else:
			printedPrice = "not enough seats"

		return render_template("index.html",form=form,slideImage=slideImage,bookingPrice=printedPrice)
		
		
@app.route('/passenger_form', methods=['POST'])
def passenger_form():
	print("in submitted form")
	#if request.method =='POST':
	travel_method=request.form['travelMethod']
	slideImage=travel_method
	if travel_method == "GTplane.jpg":
		travel_method = "Plane"
	if travel_method == "GTtrain.jpg":
		travel_method = "Train"
	if travel_method == "GTbus.jpg":
		travel_method = "Bus"
	if travel_method == "GTtaxi.jpg":
		travel_method = "Taxi"
	if travel_method == "GTferry.jpg":
		travel_method = "Ferry"
		
	departure_location=request.form['departLocation']
	arrival_location=request.form.get('arriveLocation')
	passengerCount = int(request.form['passengerCnt'])
	departTime=request.form['departTime']
	departDate=request.form['departDate']
	bookingPrice = int(request.form.get('bookingPrice'))
	bookingPrice = "{0:.2f}".format(bookingPrice)

	vessleNumber = getVessleId(departure_location,arrival_location,travel_method)
	vessleNumber=vessleNumber[0].title()
	vessleNumber=str(vessleNumber)
	print("vessleNumber is: "+vessleNumber)
	
	form = createPassengerForm(str(passengerCount))

	
	print("travel: "+ travel_method)
	#print("depart: "+ departure_location)
	#print("arrive: "+ arrival_location)
	print("after prints")
    #projectpath = request.form['projectFilepath']
    # your code
    # return a response
	
	return render_template("passenger_form.html",
							form=form,
							slideImage=slideImage,
							travel_method=travel_method,
							departure_location=departure_location,
							arrival_location=arrival_location,
							departTime=departTime,
							departDate=departDate,
							passengerCount=passengerCount,
							bookingPrice=bookingPrice,
							vessleNumber=vessleNumber)
		
		
@app.route('/purchase_form', methods=['POST'])
def purchase_form():
	print("in purchase form")
	travel_method = request.form.get('travel_method')
	departure_location = request.form.get('departure_location')
	arrival_location = request.form.get('arrival_location')
	departTime = request.form.get('departTime')
	departDate = request.form.get('departDate')
	passengerCount = int(request.form.get('passengerCount'))
	bookingPrice = str(request.form.get('bookingPrice'))
	slideImage=request.form['slideImage']
	vessleNumber = str(request.form.get('vessleNumber'))
	bookerFirstName= request.form.get('FirstName')
	bookerLastName= request.form.get('LastName')
	customerID = request.form.get('customerID')
	
	print("travel_method = " + travel_method)
	print("departure_location = " + departure_location)
	print("arrival_location = " + arrival_location)
	print("departTime = " + departTime)
	print("departDate = " + departDate)
	print("passengerCount = " + str(passengerCount))
	print("bookingPrice = " + bookingPrice)
	
	i = 1
	bookPricePerPassenger = float(bookingPrice) / passengerCount
	print("bookPricePerPassenger = "+ str(bookPricePerPassenger))
	finalBookingPrice = 0
	
	
	while i <= passengerCount:
		print("i = "+ str(i))
	
		passengerAge = int(request.form.get('passengerAge'+str(i)))
		print("passenger "+str(i)+" :"+str(passengerAge))
		#if there is a child, but only discount on children not traveling alone
		if (passengerAge < 10 and passengerCount > 1 and (isThereAnAdult(request.form) == True)):
			finalBookingPrice += (float(bookPricePerPassenger * 0.75))
		else:
			finalBookingPrice += bookPricePerPassenger
		i=i+1
		
	print("after")
	
	#if(
	#float(bookingPrice) 
	finalBookingPrice = "{0:.2f}".format(finalBookingPrice)

	form = createPassengerForm(str(passengerCount))

	return render_template("purchase_form.html",
							form=form,
							slideImage=slideImage,
							travel_method=travel_method,
							departure_location=departure_location,
							arrival_location=arrival_location,
							departTime=departTime,
							departDate=departDate,
							passengerCount=passengerCount,
							bookingPrice=bookingPrice,
							discountedPrice=finalBookingPrice,
							vessleNumber=vessleNumber,
							bookerFirstName=bookerFirstName,
							bookerLastName=bookerLastName,
							customerID=customerID)


@app.route('/reciept_page', methods=['POST'])
def reciept_page():
	print("in receipt page")
	travel_method = request.form.get('travel_method')
	departure_location = request.form.get('departure_location')
	arrival_location = request.form.get('arrival_location')
	departTime = request.form.get('departTime')
	departDate = request.form.get('departDate')
	passengerCount = int(request.form.get('passengerCount'))
	finalBookingPrice =	float(request.form.get('discountedPrice'))
	slideImage=request.form['slideImage']
	bookerFirstName= request.form.get('FirstName')
	bookerLastName= request.form.get('LastName')
	customerID = request.form.get('customerID')
	paymentMethod = request.form.get('payMethod')
	vessleNumber = str(request.form.get('vessleNumber'))

	finalBookingPrice = "{0:.2f}".format(finalBookingPrice)


	#generate a random username
	number = '{:05d}'.format(random.randrange(1, 99999))
	username  = bookerLastName[0:len(bookerLastName)//2] + number
	#generate a random password
	s = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?"
	passlen = 8
	password = "".join(random.sample(s,passlen ))
	
	print("username is: " + username)
	print("password is: " + password)
	
	#generate a receipt/transaction id
	receiptID = str(getSomeRandomNumberDec(16))
	bookingID = receiptID
	# if customerID exists use it - really they should be forced to login
	if(doesCustomerIdExist(customerID)):
                addReceiptEntry(receiptID, customerID)
		
	else:# else create one and login details
		customerID = str(getSomeRandomNumberHex(8))
		addCustomerLoginDetails(username,password,customerID)
		addReceiptEntry(receiptID, customerID)	
	
	#update the timetable as well as the booking table for the journey method
	if(travel_method =="Ferry"):
                updateJourneyTablesFromBookingFerry(request,customerID)
	elif(travel_method == "Train"):
                updateJourneyTablesFromBookingTrain(request,customerID)
	elif(travel_method == "Plane"):
                updateJourneyTablesFromBookingAir(request,customerID)
        #elif(travel_method == "Train"):
        #        updateJourneyTablesFromBookingTrain(request,customerID)
        ##elif(travel_method =="Ferry"):
        ##        updateJourneyTablesFromBookingFerry(request,customerID)
        #elif(travel_method =="Train"):
        #        pass
        #elif(travel_method =="Ferry"):
        #        pass

	#add this info to the database
		#update timetable to increment passenger count
		#pull journey info etc and put into the reciept

	recieptLink=""
	#attempt 2
	table2use = resolve_tname(travel_method)
	Xkey = getbookingPrimaryKey(customerID,table2use)
	recieptLink = WriteReciept(table2use,int(Xkey[0]))
	##
	
	#create receipt and pass it into receipt page
#	if(travel_method == "Plane"):
#		recieptLink = WriteReciept("webairbook",receiptID)
#	if(travel_method == "Train"):
#		recieptLink = WriteReciept("webtrainbook",receiptID)
#	if(travel_method == "ferry"):
#		recieptLink = WriteReciept("webferrybook",receiptID)

        ##END
	return render_template("reciept_page.html",
							slideImage=slideImage,
							travel_method=travel_method,
							departure_location=departure_location,
							arrival_location=arrival_location,
							departTime=departTime,
							departDate=departDate,
							passengerCount=passengerCount,
							discountedPrice=finalBookingPrice,
							recieptLink=recieptLink,
							customerID=customerID,
							bookingID=bookingID,			
							bookerFirstName=bookerFirstName,
							bookerLastName=bookerLastName,
							paymentMethod=paymentMethod)
	
	
	
@app.route('/login', methods=['GET','POST'])
def login_check():
	
	if(request.method == 'POST'):
		username = request.form.get('username')
		password = request.form.get('password')
			
		if(username == "admin"):
			#print("checking password")
			if(checkAdminPassword(password)):
				user = createUser(username,"",password,2)
				# totally unsafe and would in practical use need to be carefully 
				# transitioned and any access verified before routing, but this works for now	
				return render_template("admin.html",userName=username, passwd=password) 		
			else:
				return redirect("/plane")

	
	else:
		return redirect("/plane")

@app.route('/maintenance', methods=['GET','POST'])
def process_maintenance_request():
	
	if(request.method == 'POST'):
		username = request.form.get('username')
		password = request.form.get('password')
		departLocation = request.form.get('departLocation')
		arriveLocation = request.form.get('arriveLocation')
		prevDepartTime = request.form.get('prevDepartTime')
		newDepartTime = request.form.get('newDepartTime')
		prevArriveTime = request.form.get('prevArriveTime')
		newArriveTime = request.form.get('newArriveTime')
		prevVessleNumber = request.form.get('prevVessleNumber')
		newVessleNumber = request.form.get('newVessleNumber')
		status = request.form.get('status')
		price = request.form.get('price')
		travelMethod = request.form.get('travelMethod')
			
		if(username == "admin"):
			#print("checking password")
			if(checkAdminPassword(password)):
				# totally unsafe and would in practical use need to be carefully 
				# transitioned and any access verified before routing, but this works for now	
				
				handleMaintenceRequest(travelMethod,
										departLocation,
										arriveLocation,
										prevDepartTime,
										newDepartTime,
										prevArriveTime,
										newArriveTime,
										prevVessleNumber,
										newVessleNumber,
										price,
										status
										)
				
				return render_template("admin.html",userName=username, passwd=password) 		
			else:
				return redirect("/plane")

	
	else:
		return redirect("/plane")		
	
# run the flask app (aka. host our website)
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
	#app.run(debug=True)
