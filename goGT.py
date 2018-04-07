#! C:/Users/wildcard/AppData/Local/Programs/Python35/python.exe

from flask import Flask, render_template, request, redirect

#import everything from our travel method implementation files
from webAir import *
from webTrain import *
from webFerry import *


app = Flask(__name__)

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
		form = createPlaneForm(depart_location,arrive_location,passenger_count,dtime,depart_date)
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
		form = createPlaneForm(depart_location,arrive_location,passenger_count,dtime,depart_date)
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
# pass	
# time
# date time
# time date
# time pass
# pass time
# time pass date
# time date pass
# date time pass
# date pass time
# pass time date
# pass date time
# ! please fix this chaos with regex!! 
@app.route('/<travel_method>/Departure=<depart_location>&Arrival=<arrive_location>&Date=<depart_date>') 
@app.route('/<travel_method>/Departure=<depart_location>&Arrival=<arrive_location>&passCnt=<passenger_count>') 
@app.route('/<travel_method>/Departure=<depart_location>&Arrival=<arrive_location>&Time=<dtime>') 
@app.route('/<travel_method>/Departure=<depart_location>&Arrival=<arrive_location>&Time=<dtime>&Date=<depart_date>') 
@app.route('/<travel_method>/Departure=<depart_location>&Arrival=<arrive_location>&Date=<depart_date>&Time=<dtime>') 
@app.route('/<travel_method>/Departure=<depart_location>&Arrival=<arrive_location>&Time=<dtime>&passCnt=<passenger_count>') 
@app.route('/<travel_method>/Departure=<depart_location>&Arrival=<arrive_location>&passCnt=<passenger_count>&Time=<dtime>') 
@app.route('/<travel_method>/Departure=<depart_location>&Arrival=<arrive_location>&Time=<dtime>&passCnt=<passenger_count>&Date=<depart_date>')
@app.route('/<travel_method>/Departure=<depart_location>&Arrival=<arrive_location>&Time=<dtime>&Date=<depart_date>&passCnt=<passenger_count>') 
@app.route('/<travel_method>/Departure=<depart_location>&Arrival=<arrive_location>&Date=<depart_date>&Time=<dtime>&passCnt=<passenger_count>') 
@app.route('/<travel_method>/Departure=<depart_location>&Arrival=<arrive_location>&Date=<depart_date>&passCnt=<passenger_count>&Time=<dtime>') 
@app.route('/<travel_method>/Departure=<depart_location>&Arrival=<arrive_location>&passCnt=<passenger_count>&Time=<dtime>&Date=<depart_date>') 
@app.route('/<travel_method>/Departure=<depart_location>&Arrival=<arrive_location>&passCnt=<passenger_count>&Date=<depart_date>&Time=<dtime>') 
def formatToArrivalLoc(travel_method="", depart_location="--",arrive_location="--", passenger_count=0,dtime=0,depart_date=0):
	if travel_method == "plane":
		slideImage = "GTplane.jpg"
		form = createPlaneForm(depart_location,arrive_location,passenger_count,dtime,depart_date)
		if(int(passenger_count) <= form.passCntMax):
			printedPrice = "£" + str(int(getPresetPricePlain(depart_location,arrive_location)) * int(passenger_count))
		else:
			printedPrice = "not enough seats"

		return render_template("index.html",form=form,slideImage=slideImage,bookingPrice=printedPrice)
		
	elif travel_method == "train": # needs changing
		slideImage = "GTtrain.jpg"
		form = createPlaneForm(depart_location,arrive_location,passenger_count,dtime,depart_date)
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
		
# run the flask app (aka. host our website)
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
	#app.run(debug=True)