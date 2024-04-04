# Code to connect to Adafruit and download data

import configparser

config = configparser.ConfigParser()
config.read("creds.config")

username = config['Credentials']['username']
key = config['Credentials']['key']

print(username)
