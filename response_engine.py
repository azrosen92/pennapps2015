from flask import Flask, render_template, request
from pymongo import MongoClient
from bson.json_util import dumps
from flask.ext.cors import CORS

app = Flask(__name__)
cors = CORS(app)
client = MongoClient()
# Database name "devices"
db = client.devices

##
# Home page
##
@app.route("/")
def home():
	return render_template("index.html")

##
# Add and retreive data to and from a device
##
@app.route("/data/<device_id>", methods=["GET", "POST"])
def data(device_id):
	collection = db.devices
	if request.method == "POST":
		time = request.args.get("time")
		heart_rate = request.args.get("heart_rate")
		if collection.find_one({"device_id" : device_id}):
			update = {"$push" : 
						{
							"heartrate_stream" : 
								{
				 					"datetime" : time,
				 					"heart_rate" : heart_rate
								}
						}	
				}
			collection.update({"device_id" : device_id}, update)
			return dumps(collection.find_one({"device_id" : device_id}))
		else: 
			return "Device not registered"
	return dumps(collection.find_one({"device_id" : device_id}))

##
# Register a device with the service.
##
@app.route("/register_device/<device_id>")
def register_device(device_id):
	# Collection name "devices"
	collection = db.devices
	if collection.find({"device_id" : device_id}).count() == 0:
		collection.insert({
			"device_id" : device_id
		})
		return dumps(collection.find_one({"device_id" : device_id}))
	else:
		return "Device already exists!"

##
# Retrieve information about all registered devices.
##
@app.route("/all_devices")
def all_devices():
	collection = db.devices
	return dumps(collection.find())

if __name__ == "__main__":
	app.run(debug=True)