# WebProject
web programming assignment

#instructions

to run the flask app (i.e host the website)
	- in / of project do so via gitbash or wherever -> python goGT.py
	- you should see something like...

		$ python goGT.py
		* Restarting with stat
 		* Debugger is active!
 		* Debugger PIN: 133-044-942
 		* Running on http://127.0.0.1:8080/ (Press CTRL+C to quit)
		127.0.0.1 - - [30/Mar/2018 16:35:06] "GET /plane/ HTTP/1.1" 200 -
		127.0.0.1 - - [30/Mar/2018 16:35:06] "GET /static/css/master.css HTTP/1.1" 304 -
		127.0.0.1 - - [30/Mar/2018 16:35:06] "GET /static/js/jquery-3.1.1.js HTTP/1.1" 304 -
		127.0.0.1 - - [30/Mar/2018 16:35:06] "GET /static/css/custom.css HTTP/1.1" 304 -
		127.0.0.1 - - [30/Mar/2018 16:35:06] "GET /static/assets/background.jpg HTTP/1.1" 304 -
		127.0.0.1 - - [30/Mar/2018 16:35:06] "GET /static/assets/grandTravellogo.png HTTP/1.1" 200 -

	- direct your brower to localhost:8080 or 127.0.0.1:8080
	- enjoy a much better development experience than reading apache error logs via xampp XD

*also guys seems like python flask + jinja2 is the way to go for a dynamic page from one main index
still need to do database queries to populate the form tho but i have a good handle on how we can do that now


