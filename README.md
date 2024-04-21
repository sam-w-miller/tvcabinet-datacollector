# TV Cabinet Data Collector
This is a project that will connect to the data being pushed by a Pimoroni Enviro Indoor to Adafruit IO and save this information locally to this device.

## Prerequisites
- Pimoroni Enviro Indoor - available [here](https://shop.pimoroni.com/products/enviro-indoor).
- Adafruit IO Account - go [here](https://io.adafruit.com/).
- A device, such as a Raspberry Pi, running python.

## Libraries
These libraries are used in the project:
- **configparser** to read parameters from the config file.
- **Adafruit_IO** to connect to Adafruit IO and read the data, see [here](https://learn.adafruit.com/welcome-to-adafruit-io/python-and-adafruit-io).
- **datetime** and **dateutil** to create and manipulate dates.
- **pandas** to create a dataframe to store the data as it is read and output to csv file.

## Program Files
- **creds.config** holds the various configuration parameters, see creds.config.example.
- **tvcabinet-datacollector.py** is the program.
- **the data**, which will be written to the subdirectory specified in the config file.

## High Level Code Flow
The program is broken down into these sections:
1. Import all libraries.
2. Read the configuration information from creds.config. 
3. Set up the main program variables.
4. Define the function that will pull a particular feed from Adafruit IO.
5. Call the function for each feed.
6. Output the resuts to a CSV file.

## Potential Future Improvements
- Further parameterisation, such as:
	- The Group / Device names in Adafruit IO.
	- The different feeds.
	- The target timezone (assume the Enviro Indoor always stores in UTC).
	- The number of records to read each execution.

