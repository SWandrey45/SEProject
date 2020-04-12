from flask import Flask, render_template
import mysql.connector
import simplejson as json

app = Flask(__name__)

@app.route('/')
def Menu():
    print("Connecting to database...")
    #setting up a connection to the database
    mydb = mysql.connector.connect(
        host="database-1.cx36tayg9smy.us-east-1.rds.amazonaws.com",
        user="admin",
        passwd="liamstacy",
        database='SE_Project',
        charset='utf8mb4',
    )
    mycursor = mydb.cursor(dictionary=True)
    #Execute SQL query to return the up-to-date station information
    mycursor.execute("select s.number, s.name, s.address, s.position_lat, s.position_lng, d.bike_stands, d.available_bikes, d.available_bike_stands, d.status from SE_Project.station s, SE_Project.DynamicBike d, (select d1.number, max(d1.date_update + INTERVAL time_to_sec(d1.time_update) second) as date_update from SE_Project.DynamicBike d1 group by d1.number) as d2 where s.number = d.number and s.number = d2.number and d.date_update + INTERVAL time_to_sec(d.time_update) second= d2.date_update;")
    #create an empty list
    data = []
    #For loop, to loop through the rows in the cursor
    for i in mycursor:
        #add each row to the list in dictionary format
        data.append(dict(i))

    #close the cursor
    mycursor.close()
    #convert the list into json format
    data = json.dumps(data)

    mycursor = mydb.cursor(dictionary=True)
    #Execute SQL query to return the up-to-date weather information
    mycursor.execute("select w.temp, w.humidity, w.description, w.icon, w.city, w.wind_speed, w.wind_direction from SE_Project.Weather w, (select max(w1.date_update  + INTERVAL time_to_sec(w1.time_update) second) as updated from SE_Project.Weather w1) w2 where w.date_update + INTERVAL time_to_sec(w.time_update) second = w2.updated")
    #create an empty list
    data_weather = []
    #For loop, to loop through the rows in the cursor
    for i in mycursor:
        #add each row to the list in dictionary format
        data_weather.append(dict(i))

    #close the cursor
    mycursor.close()
    #convert the list into json format
    data_weather = json.dumps(data_weather)

    mycursor = mydb.cursor(dictionary=True)
    #Execute SQL query to return the data for graph
    mycursor.execute("SELECT * FROM SE_Project.Graph;")
    #create an empty list
    data_graph = []
    #For loop, to loop through the rows in the cursor
    for i in mycursor:
        #add each row to the list in dictionary format
        data_graph.append(dict(i))

    #close the cursor
    mycursor.close()
    #convert the list into json format
    data_graph = json.dumps(data_graph)

    mycursor = mydb.cursor(dictionary=True)
    #Execute SQL query to return the data for graph
    mycursor.execute("SELECT * FROM SE_Project.GraphByDay;")
    #create an empty list
    data_graphByDay = []
    #For loop, to loop through the rows in the cursor
    for i in mycursor:
        #add each row to the list in dictionary format
        data_graphByDay.append(dict(i))

    #close the cursor
    mycursor.close()
    #convert the list into json format
    data_graphByDay = json.dumps(data_graphByDay)
    
    #render map.html and pass in the json data created above
    return render_template('map.html', data=data, data_weather=data_weather, data_graph=data_graph, data_graphByDay=data_graphByDay)

#Run the app
if __name__ == "__main__":
    app.run(debug=True)
