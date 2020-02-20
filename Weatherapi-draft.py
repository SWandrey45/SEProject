#Was just messing around with John's code! But it wouldn't work for me because I couldn't install dns

import sqlalchemy as sqla
from sqlalchemy import create_engine
import traceback
import glob
import os
from pprint import pprint
import json
import requests
import time
from IPython.display import display
import mysql.connector
response = requests.get("https://api.openweathermap.org/data/2.5/weather?q=Dublin,IE&APPID=2a2021764b2563bfa694c9146727bc6c")
def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


jprint(response.json())

#set up the database connection
URI = "database-1.cx36tayg9smy.us-east-1.rds.amazonaws.com"
PORT = "3306"
DB = "SE_Project"
USER = "admin"
PASSWORD = "liamstacy"

engine = create_engine("mysql+mysqlconnector://{}:{}@{}:{}/{}".format(USER, PASSWORD, URI, PORT, DB), echo=True)

# #Retreive the json data
# APIKEY = "eb2ccb1179e38c5251aac92c5182497cd4e7222d"
# NAME = "Dublin"
# STATIONS_URI = "https://api.jcdecaux.com/vls/v1/stations"

r = requests.get(STATIONS_URI, params={"apiKey": APIKEY, "contract": NAME})

#Create the Stations table
sql = """CREATE TABLE IF NOT EXISTS Weather (
        Temp INTEGER,
        Description VARCHAR(45),
        Icon VARCHAR(45),
        City VARCHAR(45))"""

try:
    res = engine.execute("DROP TABLE IF EXISTS Weather")
    res = engine.execute(sql)
    #print(res.fetchall())
except Exception as e:
    print(e)

#create a function to insert the data to the table
def Weather_to_db(text):
    weathers = json.loads(text)
    for Weather in weathers:
        vals = int(Weather.get("Temp"), (Weather.get("Description")), Weather.get("ICON"), (Weather.get("City")))
        
        engine.execute("insert into Weather values(%s, %s, %s, %s)", vals)
        #break
    return

Weather_to_db(r.text)
