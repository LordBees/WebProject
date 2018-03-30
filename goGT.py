#! C:/Users/wildcard/AppData/Local/Programs/Python35/python.exe

from flask import Flask, render_template, request, redirect

from datetime import datetime, date

from wtforms import Form, validators
from wtforms_components import DateRange, SelectField
from wtforms.validators import Length, NumberRange, DataRequired, InputRequired
from wtforms.fields.html5 import DateField

#from wtforms_components import DateTimeField

app = Flask(__name__)


# where we can put our template classes for booking forms, will end up populating it based on the current
# data within the database

class planeForm(Form): # rename for webair database form
	#departDate = DateField('Departure Date', validators=[DateRange(min=date.today())])
	#start_time = DateField(validators=[DateRange(date(2000,1,1), date(2012,4,20))])
	#dt = DateField('Date:', validators=[DateRange(min=date(2000,1,1), max=date(2012,4,20))])
    #dt = DateField(('Date:', validators=[validators.Required()], format='%d-%m-%Y')
	#email = StringField('Email Address',[validators.Length(min=6, max=35)])
	#password = PasswordField('New Password',[
    #    validators.DataRequired(),
	departDateMin = date.today(); # we can pull this from database
	departDateMax = date.today(); # we can pull this from database
	choices2=[(0, 'Newcastle'), (1, 'Bristol'), (2, 'Cardiff'),(3, 'Manchester')]
	##disabled = "true"
	departTime = SelectField(choices=choices2)
	departLocation = SelectField(choices=choices2)
	#departDate = """<input type="date" id="departDate" name="party" min={{form.departDateMin}} max={{form.departDateMax}} disabled= true"""  + "><br><br>"
	#departDate = departDateString + "><br><br>"
    #    validators.EqualTo('confirm', message='Passwords must match')
    #])
	#confirm = PasswordField('Repeat Password')
	#accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])

	
	
	
# basically makes plane travel form the default form that pops up 
@app.route("/")
def root():
	return redirect("/plane")
	
# working for static values atm, here we are going to end up calling some functions for database querying
# so we can build and accurate form
	
@app.route('/<travel_method>/')
def formatToTravMeth(travel_method=""):
	#request.form['testLabel'] = "LOL"
	if travel_method == "plane":
		slideImage = "grandTravellogo.png"
		#disabled="true"
		form = planeForm(request.form)
		
		return render_template("index.html",form=form,slideImage=slideImage)
		
	elif travel_method == "train": # needs changing
		slideImage = "grandTravellogo.png"
		form = planeForm(request.form)
		return render_template("index.html",form=form,slideImage=slideImage)

	elif travel_method == "bus": # needs changing
		slideImage = "grandTravellogo.png"
		form = planeForm(request.form)
		return render_template("index.html",form=form,slideImage=slideImage)
		
	elif travel_method == "taxi": # needs changing
		slideImage = ".png"
		form = planeForm(request.form)
		return render_template("index.html",form=form,slideImage=slideImage)
	
	elif travel_method == "ferry": # needs changing
		slideImage = "grandTravellogo.png"
		form = planeForm(request.form)
		return render_template("index.html",form=form,slideImage=slideImage)
	

@app.route('/<travel_method>/Departure=<depart_location>')
def formatToDepartLoc(travel_method="",depart_location=""):
	#request.form['testLabel'] = "LOL"
	if travel_method == "plane":
		slideImage = "grandTravellogo.png"
		form = planeForm(request.form)
		departOptState = True
		if depart_location == "Cardiff":
			slideImage = ""
		return render_template("index.html",form=form,slideImage=slideImage)
		
	elif travel_method == "train": # needs changing
		slideImage = "grandTravellogo.png"
		form = planeForm(request.form)
		return render_template("index.html",form=form,slideImage=slideImage)

	elif travel_method == "bus": # needs changing
		slideImage = "grandTravellogo.png"
		form = planeForm(request.form)
		return render_template("index.html",form=form,slideImage=slideImage)
		
	elif travel_method == "taxi": # needs changing
		slideImage = ".png"
		form = planeForm(request.form)
		return render_template("index.html",form=form,slideImage=slideImage)
	
	elif travel_method == "ferry": # needs changing
		slideImage = "grandTravellogo.png"
		form = planeForm(request.form)
		return render_template("index.html",form=form,slideImage=slideImage)

# a bit further ahead atm, i need to get data being pulled from the database to accurately 
# start evaluating travel routes

#@app.route('/<travel_method>/Departure=<depart_location>&Arrival=<arrive_location>')
	
# run the flask app (aka. host our website)
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
	#app.run(debug=True)