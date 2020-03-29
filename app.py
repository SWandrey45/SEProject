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
    mycursor.execute("SELECT * FROM station GROUP BY number")
    # data = mycursor.fetchall()
    data = []
    for i in mycursor:
        data.append(dict(i))
        # print(i)
    mycursor.close()
    data = json.dumps(data)

    print(data)
    return render_template('map.html', data=data)

if __name__ == "__main__":
    app.run(debug=True)
