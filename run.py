from twilio import twiml
import twilio.twiml

#server setup
from flask import Flask, request, redirect 
app = Flask(__name__)

from Data import DATA

secret_key = #google api key here


def address_to_coord (address):
    request_url = 'https://maps.googleapis.com/maps/api/geocode/json?address='+str(address)+'&key=' + secret_key
    response_json = requests.get(request_url)
    response_data_json = json.dumps(ast.literal_eval(response_json.text))
    results_json = json.loads(response_data_json)

    location = results_json.get('results')[0].get('geometry').get('location')
    return (location.get('lat'), location.get('lng'))

def get_places(latitude, longitude, radius):
    # get a url for the api request
    request_url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?location='+str(latitude)+','+str(longitude)+'&radius='+str(radius) + '&query=food&types=convenience_store|pharmacy|grocery_or_supermarket&key='+secret_key
    
    # get a specially formatted data structure that seems to contain detailed info about places
    googleResponse = urllib.urlopen(request_url)
    jsonResponse = json.loads(googleResponse.read())
	
	#gets all the formatted address   
    test = json.dumps([s['formatted_address'] for s in jsonResponse['results']], indent=3)
    return test

def intersection(google, data):
    intersection = []
    for row in data:
        addr = row[3] + ", " + row[5] + ", " + row[6] + " 0" + row[7] + ", United States"
        if (addr in google):
            intersection.append(row)
    return intersection

def dist(origin, destination):
    request_url = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins='+str(origin[0])+','+str(origin[1])+'&destinations='+str(destination[0])+','+str(destination[1])+'&key=' + secret_key
    response_json = requests.get(request_url)
    response_data_json = json.dumps(ast.literal_eval(response_json.text))
    return json.loads(response_data_json).get('rows')[0].get('elements')[0].get('duration').get('value')

def top_n(cross_list, origin, n):
    q = []
    for loc in cross_list:
        d = dist(origin, (float(loc[2]), float(loc[1])))
        heappush(q, {d: loc})
    best = [0] * min(n, len(q))
    for i in range(n):
        if not(q == []):
            best[i] = heappop(q)
    return best


def format_top(top):
    '''takes the top results received by top_n and formats the output.'''
    output = ''
    for place in top:
        info = place.values()[0]
        print(info)
        output += info[0] + ': ' + info[3] + ' ' + info[4] + ' ' + info[5] + ', ' + info[6] + ' 0' + info[7] + ', ' + str(int(place.keys().pop()/60.0)) + ' min drive' '\n'
    return output

@app.route("/", methods=['GET', 'POST']) #accepts heroku requests [texts]
def reply():
	#starts mssg string
	mssg = "Here 3 locations near you that accept SNAP:\n"

	addr = request.values.get('Body', None)
	coord = address_to_coord(addr)
	#data = csv_to_list('ids.csv')
	google = get_places(coord[0], coord[1], 3200)
	places = intersection(google, DATA)
	mssg = format_top(top_n(places, coord, 3))
    #sends reply
	resp = twilio.twiml.Response()

	if (mssg == ""):
		mssg = "No results found"

	resp.message(mssg)
	#for testing purposes, returns the mssg string
	return str(mssg)
 
if __name__ == "__main__":
    app.run(debug=True)