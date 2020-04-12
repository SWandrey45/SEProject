import sqlalchemy as sqla
from sqlalchemy import create_engine
import traceback
import json
import requests
import time
import mysql.connector

#set up the database connection
URI = "database-1.cx36tayg9smy.us-east-1.rds.amazonaws.com"
PORT = "3306"
DB = "SE_Project"
USER = "admin"
PASSWORD = "liamstacy"

# create mySQL engine
engine = create_engine("mysql+mysqlconnector://{}:{}@{}:{}/{}".format(USER, PASSWORD, URI, PORT, DB), echo=True)

#assign values to api key, name and staions URL
APIKEY = "eb2ccb1179e38c5251aac92c5182497cd4e7222d"
NAME = "Dublin"
STATIONS_URI = "https://api.jcdecaux.com/vls/v1/stations"

#Retreive the json data
r = requests.get(STATIONS_URI, params={"apiKey": APIKEY, "contract": NAME})

#Create the Stations table
sql = """CREATE TABLE IF NOT EXISTS station (
        address VARCHAR(256),
        banking INTEGER,
        bike_stands INTEGER,
        bonus INTEGER,
        contract_name VARCHAR(256),
        name VARCHAR(256),
        number INTEGER,
        position_lat REAL,
        position_lng REAL,
        status VARCHAR(256))"""

#try to create the stations table if there is an error throw an exception
try:
    res = engine.execute("DROP TABLE IF EXISTS station")
    res = engine.execute(sql)
    #print(res.fetchall())
except Exception as e:
    print(e)

#function to create and execute an SQL query to insert bike information into
#stations table from the json file text
def stations_to_db(text):
    #load json file into an array
    stations = json.loads(text)
    #for loop to loop through each row of the array
    for station in stations:
        vals = (station.get("address"), int(station.get("banking")), station.get("bike_stands"), int(station.get("bonus")),
               station.get("contract_name"), station.get("name"), station.get("number"), station.get("position").get("lat"),
               station.get("position").get("lng"), station.get("status"))
        
        # execute SQL query to insert row into station
        engine.execute("insert into station values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", vals)
        #break
    return
#Run station_to_db function to insert data into the station table
stations_to_db(r.text)
    
