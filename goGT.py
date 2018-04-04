#! C:/Users/wildcard/AppData/Local/Programs/Python35/python.exe

from flask import Flask, render_template, request, redirect

#import everything from webAir.py
from webAir import *
from webTrain import *

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
	
	if travel_method == "plane":
		slideImage = "GTplane.jpg"
		form = createPlaneForm(depart_location,arrive_location,passenger_count)
		#form.departLocation(default=None)
		#form.arriveLocation(default=None)
		return render_template("index.html",form=form,slideImage=slideImage)
		
	elif travel_method == "train": # needs changing
		slideImage = "GTtrain.jpg"
		form = createPlaneForm(depart_location,arrive_location,passenger_count)
		return render_template("index.html",form=form,slideImage=slideImage)

	elif travel_method == "bus": # needs changing
		slideImage = "GTbus.jpg"
		form = createPlaneForm(depart_location,arrive_location,passenger_count)
		return render_template("index.html",form=form,slideImage=slideImage)
		
	elif travel_method == "taxi": # needs changing
		slideImage = "GTtaxi.jpg"
		form = createPlaneForm(depart_location,arrive_location,passenger_count)
		return render_template("index.html",form=form,slideImage=slideImage)
	
	elif travel_method == "ferry": # needs changing
		slideImage = "GTferry.jpg"
		form = createPlaneForm(depart_location,arrive_location,passenger_count)
		return render_template("index.html",form=form,slideImage=slideImage)
	

@app.route('/<travel_method>/Departure=<depart_location>')
def formatToDepartLoc(travel_method="",depart_location="--"):
	#default our variables
	arrive_location="--"
	passenger_count=0
	
	if travel_method == "plane":
		slideImage = "GTplane.jpg"
		form = createPlaneForm(depart_location,arrive_location,passenger_count)
		#form.arriveLocation = buildArrivalsField(depart_location)
		#form.arriveLocation = buildArrivalsFeild(depart_location)

		return render_template("index.html",form=form,slideImage=slideImage)
		
	elif travel_method == "train": # needs changing
		slideImage = "GTtrain.jpg"
		form = createPlaneForm(depart_location,arrive_location,passenger_count)
		return render_template("index.html",form=form,slideImage=slideImage)

	elif travel_method == "bus": # needs changing
		slideImage = "GTbus.jpg"
		form = createPlaneForm(depart_location,arrive_location,passenger_count)
		return render_template("index.html",form=form,slideImage=slideImage)
		
	elif travel_method == "taxi": # needs changing
		slideImage = "GTtaxi.jpg"
		form = createPlaneForm(depart_location,arrive_location,passenger_count)
		return render_template("index.html",form=form,slideImage=slideImage)
	
	elif travel_method == "ferry": # needs changing
		slideImage = "GTferry.jpg"
		form = createPlaneForm(depart_location,arrive_location,passenger_count)
		return render_template("index.html",form=form,slideImage=slideImage)


# a bit further ahead atm, i need to get data being pulled from the database to accurately 
# start evaluating travel routes
# *atm this is just as the previous example so it will look nothing like this in the end
@app.route('/<travel_method>/Departure=<depart_location>&Arrival=<arrive_location>')
# here we can map multiple url routes to the same condition! =)
@app.route('/<travel_method>/Departure=<depart_location>&Arrival=<arrive_location>&passCnt=<passenger_count>') 
def formatToArrivalLoc(travel_method="", depart_location="--",arrive_location="--", passenger_count=1):
	if travel_method == "plane":
		slideImage = "GTplane.jpg"
		form = createPlaneForm(depart_location,arrive_location,passenger_count)
		if(int(passenger_count) <= form.passCntMax):
			printedPrice = "£" + str(int(getPresetPrice(depart_location,arrive_location)) * int(passenger_count))
		else:
			printedPrice = "not enough seats"
		if depart_location == "Cardiff": # just a test * remove later
			slideImage = ""
		return render_template("index.html",form=form,slideImage=slideImage,bookingPrice=printedPrice)
		
	elif travel_method == "train": # needs changing
		slideImage = "GTtrain.jpg"
		form = createPlaneForm(depart_location,arrive_location,passenger_count)
		return render_template("index.html",form=form,slideImage=slideImage)

	elif travel_method == "bus": # needs changing
		slideImage = "GTbus.jpg"
		form = createPlaneForm(depart_location,arrive_location,passenger_count)
		return render_template("index.html",form=form,slideImage=slideImage)
		
	elif travel_method == "taxi": # needs changing
		slideImage = "GTtaxi.jpg"
		form = createPlaneForm(depart_location,arrive_location,passenger_count)
		return render_template("index.html",form=form,slideImage=slideImage)
	
	elif travel_method == "ferry": # needs changing
		slideImage = "GTferry.jpg"
		form = createPlaneForm(depart_location,arrive_location,passenger_count)
		return render_template("index.html",form=form,slideImage=slideImage)
		
# run the flask app (aka. host our website)
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
	#app.run(debug=True)