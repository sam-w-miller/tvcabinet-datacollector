# Code to connect to Adafruit and download data

# Import configparser to read values from config file
import configparser

# Import Adafruit_IO to connect and access data
from Adafruit_IO import *

# Import datetime and dateutil so that we can convert from UTC to the appropriate value for the timezone
from datetime import *
from dateutil import tz

# Import Pandas as we will store the data from Adafruit IO in a dataframe
import pandas as pd

# Import OS so that we can store results in a specific directory
import os

# import logging so that we can check for erros
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename="tvcabinet-datacollector.log", encoding="utf-8", format="%(asctime)s %(message)s", level=logging.DEBUG)
logger.debug("Starting tvcabinent-datacollector.py")

# Read credential information
config = configparser.ConfigParser()
config.read("creds.config")
username = config["Credentials"]["username"]
key = config["Credentials"]["key"]

# Read the directory information
data_dir = config["Data_Location"]["directory"]

# Create an empty dataframe with column names
df = pd.DataFrame(columns=["sensordate", "temperature", "pressure", "humidity", "luminance", "color-temperature"])

# Create instance of the REST client
afclient = Client(username,key)

# Grab the current date and also calculate yesterday's date
current_day = datetime.now()
yesterday = current_day - timedelta(1)

# Set the timezones we will use to convert from UTC to UK timezone
from_tzone = tz.gettz("UTC")
to_tzone = tz.gettz("Europe/London")

# Set how many records we will receive for each metric
record_count = 200

logger.debug("All parameters set")

# This function will gather the data for a specific feed/metric for a specified number of records
def get_metric_data(metric_name, num_records):

	logger.debug("Getting data for feed " + metric_name)

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

# Call the get_metric_data for each of the feeds
get_metric_data("temperature", record_count)
get_metric_data("pressure", record_count)
get_metric_data("humidity", record_count)
get_metric_data("luminance", record_count)
get_metric_data("color-temperature", record_count)

logger.debug("Getting data for yesterday")

# Build a data frame with all of the records from the previous day
daydf = df[(df["sensordate"] > datetime.strftime(yesterday, "%Y-%m-%d")) & (df["sensordate"] < datetime.strftime(current_day, "%Y-%m-%d"))]

# Check to see if we have the directory to store the data files
if not os.path.exists(data_dir):
	os.makedirs(data_dir)

logger.debug("Saving file")

# Save the data to a CSV file
daydf.to_csv(data_dir + "/" + datetime.strftime(yesterday, "%Y-%m-%d") + ".csv", index = False)
