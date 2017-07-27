from flask import Flask, request
import json
import requests

import pyodbc
app = Flask(__name__)

@app.route('/')
def hello_world():
  return 'Hello, World!'



@app.route('/login',methods=['POST'])
def login():
    print("Start")
    file = open("D:/New folder (26)/dbc.txt", "r")
    text = file.readline().split(",")
    print("File open")
    # Asign values to  send

    # Asign database connection details
    server = text[0]

    database = text[1]

    username = text[2]

    password = text[3]
   
    driver=text[4]    
    file.close()
    print("File close")

    #Driver={ODBC Driver 13 for SQL Server};Server=tcp:kappaorbanned.database.windows.net,1433;Database=TwitchStats;Uid=Dilhan@kappaorbanned;Pwd={your_password_here};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;
    db = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
    print("DB Set")
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    cursor.execute("SELECT count(*) From user_account where username="+request.form['username']+" and password ="+request.form['password']+";")
    row = cursor.fetchone()
    if row.count==1:
      return {'status': 'login'}
    else:
      return {'status': 'incorrect'}



if __name__ == '__main__':
  app.run()
