'''Here is my scraper for the dynamic bikes, it is also giving the error "This result object does not return rows. 
It has been closed automatically". I have tried to research this to find out how to fix it and I am going crazy! Not sure what's
missing? 
What does this mean, how can we fix it? thanks for taking a peak!!"

'''


import requests
import json
from pprint import pprint
import sqlalchemy as sqla
from sqlalchemy import create_engine
import traceback
import glob
import os
import time
from IPython.display import display
import mysql.connector
from datetime import datetime

#set up the database connection
URI = "database-1.cx36tayg9smy.us-east-1.rds.amazonaws.com"
PORT = "3306"
DB = "SE_Project"
USER = "admin"
PASSWORD = "liamstacy"

engine = create_engine("mysql+mysqlconnector://{}:{}@{}:{}/{}".format(USER, PASSWORD, URI, PORT, DB), echo=True)

#Retreive the json data
APIKEY = "eb2ccb1179e38c5251aac92c5182497cd4e7222d"
NAME = "Dublin"
STATIONS_URI = "https://api.jcdecaux.com/vls/v1/stations"


sql =  """CREATE TABLE IF NOT EXISTS DynamicBike (
        available_bike_stands INTEGER,
        available_bikes INTEGER,
        bike_stands INTEGER,
        name VARCHAR(256),
        number INTEGER NOT NULL,
        date_update DATE NOT NULL,
        time_update TIME NOT NULL,
        status VARCHAR(256),
        PRIMARY KEY(number, date_update, time_update))"""

try:
    #res = engine.execute("DROP TABLE IF EXISTS DynamicBike")
    res = engine.execute(sql)
    print(res.fetchall())
    
except Exception as e:
    print(e)

def dynamic_bikes(text):
    DynamicBikes = json.loads(text)
    for DynamicBike in DynamicBikes:
        vals =  (DynamicBike.get("available_bike_stands"),
        int(DynamicBike.get("available_bikes")),
        int(DynamicBike.get("bike_stands")),
        DynamicBike.get("name"),
        int(DynamicBike.get("number")),
        datetime.now(),
        datetime.now(),         
        DynamicBike.get("status"))
        
        
        engine.execute("insert into DynamicBike values(%s, %s, %s, %s, %s, %s, %s, %s)", vals)
    return

while True:
    try:
        r = requests.get(STATIONS_URI, params={"apiKey": APIKEY, "contract": NAME})
        dynamic_bikes(r.text)
        
        #sleep for 5 mins
        time.sleep(5*60)
    except Exception as e:
        #If there is a problem print traceback
        print(e)
