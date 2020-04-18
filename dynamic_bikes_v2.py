import requests
import json
import sqlalchemy as sqla
from sqlalchemy import create_engine
import traceback
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

#create mysql engine
engine = create_engine("mysql+mysqlconnector://{}:{}@{}:{}/{}".format(USER, PASSWORD, URI, PORT, DB), echo=True)

#Retreive the json data
APIKEY = "eb2ccb1179e38c5251aac92c5182497cd4e7222d"
NAME = "Dublin"
STATIONS_URI = "https://api.jcdecaux.com/vls/v1/stations"

#sql code to create the DynamicBike table if it doesn't already exist
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

#try to execute the create table query
try:
    res = engine.execute(sql)
    print(res.fetchall())
    
except Exception as e:
    print(e)

#function to create and execute an SQL query to insert bike information into
#DynamicBike table from the json file text
def dynamic_bikes(text):
    #load json file into an array
    DynamicBikes = json.loads(text)
    #for loop to loop through each row of the array
    for DynamicBike in DynamicBikes:
        vals =  (DynamicBike.get("available_bike_stands"),
        int(DynamicBike.get("available_bikes")),
        int(DynamicBike.get("bike_stands")),
        DynamicBike.get("name"),
        int(DynamicBike.get("number")),
        datetime.now(),
        datetime.now(),         
        DynamicBike.get("status"))
        
        # execute SQL query to insert row into DynamicBike
        engine.execute("insert into DynamicBike values(%s, %s, %s, %s, %s, %s, %s, %s)", vals)
        # execute SQL query to insert row into BikeWeather for graphs
        engine.execute("""insert into BikeWeather2
                            select """ + str(DynamicBike.get('number')) + ", CURDATE(), CURTIME(), w.description, w.date_update + INTERVAL time_to_sec(w.time_update) second, 0, " + str(DynamicBike.get('available_bikes')) + ", " + str(DynamicBike.get('available_bike_stands')) + ', "' + DynamicBike.get("name") + '", weekday(CURDATE()), least(time_to_sec(CURTIME()) div (60*60), 23)' + '''
                            from SE_Project.Weather w, (select max(date_update + INTERVAL time_to_sec(time_update) second) as updated from SE_Project.Weather) as w1
                            where w.date_update + INTERVAL time_to_sec(w.time_update) second = w1.updated''')
                        
        
    return


try:
    #Use requests to retrieve the json file from the bike API
    r = requests.get(STATIONS_URI, params={"apiKey": APIKEY, "contract": NAME})
    #pass the json file into the dynamic_bikes() function to insert the data
    #into the database
    dynamic_bikes(r.text)
except Exception as e:
    #If there is a problem print traceback
    print(e)
