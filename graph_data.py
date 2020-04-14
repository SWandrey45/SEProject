# This script is to be run daily, on crontab, to insert the data into the 
# graph tables so the data can be retrieved quickly on load of the app

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

#SQL query to insert data into graph table
sql = """insert into SE_Project.Graph
SELECT d.number, d.name, avg(d.available_bikes), avg(d.available_bike_stands), least(time_to_sec(d.time_update) div (60*60), 23)  as time_update 
FROM SE_Project.DynamicBike d
group by d.number, d.name, least(time_to_sec(d.time_update) div (60*60), 23)"""

#truncate Graph table and insert rows into it, if there is an error throw an exception
try:
    res = engine.execute("truncate table SE_Project.Graph")
    res = engine.execute(sql)
except Exception as e:
    print(e)
    
#SQL query to insert data into graphByDay table
sql2 = """insert into SE_Project.GraphByDay
SELECT d.number, d.name, (weekday(d.date_update)) as weekday, (d.available_bikes), avg(d.available_bike_stands), least(time_to_sec(d.time_update) div (60*60), 23)  as time_update 
FROM SE_Project.DynamicBike d
group by d.number, d.name, weekday(d.date_update), least(time_to_sec(d.time_update) div (60*60), 23)"""

#truncate GraphByDay table and insert rows into it, if there is an error throw an exception
try:
    res = engine.execute("truncate table SE_Project.GraphByDay")
    res = engine.execute(sql2)
except Exception as e:
    print(e)
