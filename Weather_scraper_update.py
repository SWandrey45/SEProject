import sqlalchemy as sqla
from sqlalchemy import create_engine
import traceback
import json
import requests
import time
import mysql.connector
from datetime import datetime

#set up the database connection
URI = "database-1.cx36tayg9smy.us-east-1.rds.amazonaws.com"
PORT = "3306"
DB = "SE_Project"
USER = "admin"
PASSWORD = "liamstacy"

#create mysql engine
engine = create_engine("mysql+mysqlconnector://{}:{}@{}:{}/{}".format(USER, PASSWORD, URI, PORT, DB), echo=True)

#Retreive the json data
APIKEY = "2a2021764b2563bfa694c9146727bc6c"
NAME = "Dublin,IE"
WEATHER_URI = "https://api.openweathermap.org/data/2.5/weather"
UNITS = "metric"

#Create the Weather table if it doesn't already exist
sql = """CREATE TABLE IF NOT EXISTS Weather (
        date_update DATE NOT NULL,
        time_update TIME NOT NULL,
        temp REAL,
        humidity REAL,
        description VARCHAR(45),
        icon VARCHAR(45),
        city VARCHAR(45),
        wind_speed REAL,
        wind_direction REAL,
        PRIMARY KEY(date_update, time_update))"""

#try to execute the create table query and throw an exception if there is an
#error
try:
    res = engine.execute(sql)
    print(res.fetchall())
except Exception as e:
    print(e)

#function to create and execute an SQL query to insert weather information into
#Weather table from the json file text
def Weather_to_db(text):
    #load json file into an array
    weathers = json.loads(text)
    
    vals = (datetime.now(), datetime.now(), weathers.get("main").get("temp"), weathers.get("main").get("humidity"), 
            weathers.get("weather")[0].get("description"), weathers.get("weather")[0].get("icon"), weathers.get("name"),
           weathers.get("wind").get("speed"), weathers.get("wind").get("deg"))

    #execute SQL query to insert row into Weather    
    engine.execute("insert into Weather values(%s, %s, %s, %s, %s, %s, %s, %s, %s)", vals)
    return

try:
    #Use requests to retrieve the json file from the Weather API
    r = requests.get(WEATHER_URI, params={"q": NAME, "APPID": APIKEY, "units": UNITS})
    #pass the json file into the dynamic_bikes() function to insert the data
    #into the database
    Weather_to_db(r.text)
        
except Exception as e:
    #If there is a problem print traceback
    print(e)
