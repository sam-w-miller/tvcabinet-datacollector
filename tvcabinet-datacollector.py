# Code to connect to Adafruit and download data

# Import configparser to read values from config file
import configparser
# Import Adafruit_IO to connect and access data
from Adafruit_IO import *

# Import datetime and dateutil so that we can convert from UTC to the appropriate value for the timezone
from datetime import datetime
from dateutil import tz

# Read credential file
config = configparser.ConfigParser()
config.read("creds.config")
username = config['Credentials']['username']
key = config['Credentials']['key']

# Create instance of the REST client
afclient = Client(username,key)

try:
	temperature = afclient.feeds('enviro.tvcabinet-temperature')
except RequestError:
	print('Feed not found')
	feed = Feed(name="enviro.tvcabinet-temperature")
	temperature = afclient.create_feed(feed)

data = afclient.data(temperature.key, max_results=200)
from_tzone = tz.gettz('UTC')
to_tzone = tz.gettz('Europe/London')

for d in data:
	utctime = d.created_at
	utc = datetime.strptime(utctime, '%Y-%m-%dT%H:%M:%SZ')
	utc = utc.replace(tzinfo=from_tzone)
	uk_time = utc.astimezone(to_tzone)

	print(utctime + ' ' + format(uk_time))

	#print('Data value: {0}'.format(d.created_at))
