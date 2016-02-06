from twilio import twiml
import twilio.twiml

#server setup
from flask import Flask, request, redirect 
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])

def reply():
	#gets sender's number
	sender = request.values.get('From', None)
	#starts mssg string
	mssg = "Here 3 locations near you that accept SNAP:\n"
	#sends reply
	resp = twilio.twiml.Response()
	resp.message(mssg)
	#for testing purposes, returns the mssg string
	return str(mssg)
 
if __name__ == "__main__":
    app.run(debug=True)