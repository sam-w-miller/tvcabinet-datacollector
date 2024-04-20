# Code to connect to Adafruit and download data

# Import configparser to read values from config file
import configparser
# Import Adafruit_IO to connect and access data
from Adafruit_IO import *

# Import datetime and dateutil so that we can convert from UTC to the appropriate value for the timezone
from datetime import datetime
from dateutil import tz

# Import Pandas as we will store the data from Adafruit IO in a dataframe
import pandas as pd

# Read credential file
config = configparser.ConfigParser()
config.read("creds.config")
username = config['Credentials']['username']
key = config['Credentials']['key']

# Create an empty dataframe with column names
df = pd.DataFrame(columns=["sensordate", "temperature", "pressure", "humidity", "luminance", "color-temperature"])

# Create instance of the REST client
afclient = Client(username,key)

# Set the timezones we will use to convert from UTC to UK timezone
from_tzone = tz.gettz("UTC")
to_tzone = tz.gettz("Europe/London")

# Set how many records we will receive for each metric
record_count = 200

# This function will gather the data for a specific feed/metric for a specified number of records
def get_metric_data(metric_name, num_records):

	# Establish a connection to the Adafruit IO Feed for the metric
	try:
		metric = afclient.feeds("enviro.tvcabinet-" + metric_name)
	except RequestError:
		print("Feed not found")
		feed = Feed(name="enviro.tvcabinet-" + metric_name)
		metric = afclient.create_feed(feed)

	# Get the data from the feed
	data = afclient.data(metric.key, max_results=num_records)

	for d in data:
		# Get the time from the record in UTC
		utctime = d.created_at
		utc = datetime.strptime(utctime, '%Y-%m-%dT%H:%M:%SZ')
		# Ensure that it set as UTC
		utc = utc.replace(tzinfo=from_tzone)
		# Convert to the appropriate UK time
		uk_time = utc.astimezone(to_tzone)
		# See if we already have a record with the same sensor date/time value
		if len(df.loc[(df["sensordate"] == uk_time)].index) > 0:
			# Record with the same date/time value exists so just add the new metric to the row
			df.loc[df.loc[(df["sensordate"] == uk_time)].index, metric_name] = float(d.value)
		else:
			# Build record to insert into dataframe
			new_row = {"sensordate": uk_time, metric_name: float(d.value)}
			df.loc[len(df)] = new_row

get_metric_data("temperature", record_count)
get_metric_data("pressure", record_count)
get_metric_data("humidity", record_count)
get_metric_data("luminance", record_count)
get_metric_data("color-temperature", record_count)

#df.to_csv("test.csv",index = False)

daydf = df[(df["sensordate"] > "2024-04-19") & (df["sensordate"] < "2024-04-20")]
print(daydf)
