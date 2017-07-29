from flask import Flask, request, render_template
from logging.handlers import RotatingFileHandler
import json
import requests
import pyodbc 
import logging
import time
app = Flask(__name__)
def connectdb():# Create connection to sql database
  app.logger.info("Begining database connection")
  file = open("D:/KappaOrBanned/dbc.txt", "r")
  text = file.readline().split(",")
  app.logger.info("File open")
  # Asign values to  send

  # Asign database connection details
  server = text[0]  # server = "kappaorbannedj.database.windows.net"

  database = text[1]   # database = "TwitchStats"

  username = text[2] # username = "Dilhan@kappaorbannedj"

  password = text[3]   # password = "101Luminous101"
  
  driver= text[4] # driver="{ODBC Driver 13 for SQL Server}"   
  
  file.close()
  app.logger.info("File close")
  db = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
  return db

@app.route('/')
def hello_world():
  app.logger.info("Kappa")
  return 'Kappa'

@app.route('/search',methods=['POST'])
def search():
  try:
     db = connectdb()
    except Exception as identifier:
      app.logger.error(identifier)
      return "{\"status\": \"No connection to database\"}"
  app.logger.info("Connection establish")  
  cursor = db.cursor()
  app.logger.info("Send sql statment") 
  cursor.execute("SELECT count(*) As cou From user_account where user_name= '"+request.form['username']+"' AND password ='"+request.form['password']+"' ;") #Send sql statment to check for account 
  
@app.route('/streamer/<streamername>')
def streamer(streamername):
  return streamername

@app.route('/streamer/<streamername>/comment')
def streamercomment(streamername):
  return ""+streamername+"comment"

@app.route('/login',methods=['POST']) # The login method
def login():
    try:
     db = connectdb()
    except Exception as identifier:
      app.logger.error(identifier)
      return "{\"status\": \"No connection to database\"}"
    app.logger.info("Connection establish")  
    cursor = db.cursor()
    app.logger.info("Send sql statment") 
    cursor.execute("SELECT count(*) As cou From user_account where user_name= '"+request.form['username']+"' AND password ='"+request.form['password']+"' ;") #Send sql statment to check for account 
    
    row = cursor.fetchone()
    db.close()
    if row.cou==1:
      app.logger.info(request.form['username']+" Logged in")
      return "{\"status\": \"login\"}"
    else:
      app.logger.info(request.form['username']+" Login error")
      return "{\"status\": \"Invalid\"}"

@app.route('/register',methods=['POST']) # The register method
def register():
  try:
     db = connectdb()
  except Exception as identifier:
    app.logger.error(identifier)
    return "{\"status\": \"No connection to database\"}"
  app.logger.info("Connection establish")  
  cursor = db.cursor()
  app.logger.info("Send sql statment") 
  cursor.execute("SELECT * From user_account where user_name= '"+request.form['username'] +"';") #Send sql statment to check if account is all ready made
  row = cursor.fetchone()
  print(row)


  cursor.execute("SELECT count(*) As cou From user_account where user_name= '"+request.form['username'] +"';") #Send sql statment to check if account is all ready made
  
  row = cursor.fetchone()
 
  if row.cou!=0:
    db.close()
    app.logger.info(request.form['username']+" allredy has an account")
    return "{\"status\": \"Account allready there\"}"
  else:
    app.logger.info(request.form['username']+" account created")
    cursor.execute("Insert into user_account values('"+request.form['username']+"','"+request.form['email']+"','"+request.form['password']+"');")
    db.commit()
    db.close()
    return "{\"status\": \"Account created\"}"  

if __name__ == '__main__':
  formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s") #Set log message formate
  handler = RotatingFileHandler("log/"+time.strftime("%Y-%m-%d ")+".log", maxBytes=10000, backupCount=1) 
  handler.setLevel(logging.INFO) 
  handler.setFormatter(formatter)
  app.logger.addHandler(handler) 
  app.logger.setLevel(logging.INFO)
  
  app.run()
