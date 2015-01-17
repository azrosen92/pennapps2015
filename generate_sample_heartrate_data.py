from pymongo import MongoClient
from datetime import timedelta, datetime
import random

client = MongoClient()
# Database name "devices"
db = client.devices
collection = db.devices

NORMAL_HEART_RATE_MAX = 50
NORMAL_HEART_RATE_MIN = 10

start_time = datetime.now() - timedelta(seconds=1000)

heartrate_data = []
for i in range(1000):
	time = start_time + timedelta(seconds=i)
	heartrate = random.randint(NORMAL_HEART_RATE_MIN, NORMAL_HEART_RATE_MAX)
	heartrate_data.append({'datetime' : time, 'heart_rate' : heartrate})

collection.insert({'device_id' : 'sample_data_2', 'heartrate_stream' : heartrate_data})
