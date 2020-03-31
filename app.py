from flask import Flask, render_template
import mysql.connector
import json

app = Flask(__name__)

@app.route('/')
def Menu():
    print("Connecting to database...")
    mydb = mysql.connector.connect(
        host="database-1.cx36tayg9smy.us-east-1.rds.amazonaws.com",
        user="admin",
        passwd="liamstacy",
        database='SE_Project',
        charset='utf8mb4',
    )
    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("select s.number, s.name, s.address, s.position_lat, s.position_lng, d.bike_stands, d.available_bikes, d.available_bike_stands, d.status from SE_Project.station s, SE_Project.DynamicBike d, (select d1.number, max(d1.date_update + INTERVAL time_to_sec(d1.time_update) second) as date_update from SE_Project.DynamicBike d1 group by d1.number) as d2 where s.number = d.number and s.number = d2.number and d.date_update + INTERVAL time_to_sec(d.time_update) second= d2.date_update;")
    # data = mycursor.fetchall()
    data = []
    for i in mycursor:
        data.append(dict(i))
        # print(i)
    mycursor.close()
    data = json.dumps(data)

    mycursor = mydb.cursor(dictionary=True)
    mycursor.execute("select w.temp, w.humidity, w.description, w.icon, w.city, w.wind_speed, w.wind_direction from SE_Project.Weather w, (select max(w1.date_update  + INTERVAL time_to_sec(w1.time_update) second) as updated from SE_Project.Weather w1) w2 where w.date_update + INTERVAL time_to_sec(w.time_update) second = w2.updated")
    # data = mycursor.fetchall()
    data_weather = []
    for i in mycursor:
        data_weather.append(dict(i))
        # print(i)
    mycursor.close()
    data_weather = json.dumps(data_weather)

    print(data)
    return render_template('Map_Menu_for_app.html', data=data, data_weather=data_weather)

if __name__ == "__main__":
    app.run(debug=True)
