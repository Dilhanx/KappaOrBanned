from flask import Flask, request, render_template
from logging.handlers import RotatingFileHandler
import json
import requests
import pyodbc 
import logging
import time
import collections
app = Flask(__name__)
def connectdb():# Create connection to sql database
  # app.logger.info("Begining database connection")
  # file = open("dbc.txt", "r")
  # text = file.readline().split(",")
  # app.logger.info("File open")
  # # Asign values to  send

  # # Asign database connection details
  # server = text[0]  # server = "kappaorbannedj.database.windows.net"

  # database = text[1]   # database = "TwitchStats"

  # username = text[2] # username = "Dilhan@kappaorbannedj"

  # password = text[3]   # password = "101Luminous101"
  
  # driver= text[4] # driver="{ODBC Driver 13 for SQL Server}"   
  
 
  # # file.close()
  # app.logger.info("File close")
  # db = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
  # 
  
  return db
@app.route('/banned')
def banned():
  try:
      db = connectdb()
  except Exception as identifier:
    app.logger.error(identifier)
  return "{\"status\": \"No connection to database\"}"
@app.route('/')
def kappa():
  app.logger.info("Kappa")
  return 'Kappa'

@app.route('/search',methods=['POST'])#Search if stearemr exist
def search():
  app.logger.info("Searching "+request.form['streamer']) 
  try:
    db = connectdb()
  except Exception as identifier:
    app.logger.error(identifier)
    return "{\"status\": \"No connection to database\"}"
  app.logger.info("Connection establish")  
  cursor = db.cursor()
  app.logger.info("Send sql statment") 
  cursor.execute("SELECT count(*) As cou From streamer where streamer_name= '"+request.form['streamer'] +"' ;") #Send sql statment to check if streamer exist
  row = cursor.fetchone()  
  if row.cou==1:
    app.logger.info(request.form['streamer']+" is avaliable")
    db.close()
    return "{\"status\": \"Found\"}"#Return valid if found
  else:
    app.logger.info(request.form['streamer']+" does not exist")
    db.close()
    return "{\"status\": \"Not found\"}"#Return valid if not found

@app.route('/streamer/<streamername>')# Retrive streamer detials
def streamer(streamername):
    app.logger.info("Streamer "+streamername) 
    try:
      db = connectdb()
    except Exception as identifier:
      app.logger.error(identifier)
      return "{\"status\": \"No connection to database\"}"
    app.logger.info("Connection establish")  
    cursor = db.cursor()
    app.logger.info("Send sql statment") 
    cursor.execute("SELECT * From streamer where streamer_name= '"+ streamername +"' ;") #Send sql statment to select all data of streamer
    row = cursor.fetchone()  
    #Createing json message
    details =[]
    app.logger.info( streamername +" is avaliable")
    d = collections.OrderedDict()
    d['streamer_name'] = row.streamer_name
    d['real_name'] = row.real_name
    d['img'] = row.img
    d['schedule'] = row.schedule
    d['streamer_type'] = row.streamer_type
    d['bio'] = row.bio
    details.append(d)
    j = json.dumps(details)
    j=(j[1:-1])
    db.close()
    app.logger.info(" Sending json message")
    return j

   
    
 

@app.route('/streamer/<streamername>/comment')
def streamercomment(streamername):
  try:
      db = connectdb()
  except Exception as identifier:
      app.logger.error(identifier)
      return "{\"status\": \"No connection to database\"}"
  app.logger.info("Connection establish")
  app.logger.info("Streamer Comments"+streamername) 
  
  cursor = db.cursor()
  app.logger.info("Send sql statment") 
  cursor.execute("SELECT * From comment where streamer_name= '"+ streamername +"' ;") #Send sql statment to select all data of streamer
  rows = cursor.fetchall()  
  #Createing json message
  details =[]
  app.logger.info( streamername +" is avaliable")
  for row in rows:
    d = collections.OrderedDict()
    d["streamer_name"] = row.streamer_name
    d["user_name"] = row.user_name
    d["comment"] = row.comment
    details.append(d)
  j = json.dumps(details)

  app.logger.info(" Sending json message"+j)
  return j
  
@app.route('/streamer/<streamername>/comment/update',methods=['POST'])
def updatecomment(streamername):
  try:
      db = connectdb()
  except Exception as identifier:
      app.logger.error(identifier)
      return "{\"status\": \"No connection to database\"}"
  app.logger.info("Connection establish")  
  if request.form['type']=='add':#Add comment
      app.logger.info("Add"+request.form['streamername'])     
      cursor = db.cursor()
      app.logger.info("Send sql statment") 
      cursor.execute("SELECT * insert into comment values('"+ request.form['streamername']+"','"+request.form['user']+"','"+ request.form['comment'] +"') ;")
      db.commit()
      db.close()
      return "{\"status\": \"Add\"}"
  elif request.form['type']=='delete':#Delete comment
      app.logger.info("Delete"+streamername)     
      cursor = db.cursor()
      app.logger.info("Send sql statment") 
      cursor.execute("DELETE FROM table_name WHERE streamer_name='"+request.form['streamername']+"',user_name="+request.form['user'] +"',comment="+request.form['comment']+"') ;")
      db.commit()
      db.close()
      return "{\"status\": \"Deleted\"}"
@app.route('/streamer/<streamername>/emote')# Retrive emotes used by streamer
def streameremote(streamername):
  app.logger.info("Streamer Comments"+streamername) 
  try:
    db = connectdb()
  except Exception as identifier:
    app.logger.error(identifier)
    return "{\"status\": \"No connection to database\"}"
  app.logger.info("Connection establish")  
  cursor = db.cursor()
  app.logger.info("Send sql statment") 
  cursor.execute("SELECT * From emote_rank where streamer_name= '"+ streamername +"'order by rank ;") #Send sql statment to select emotes of streamer
  rows = cursor.fetchall()  
  #Createing json message
  details =[]
  app.logger.info( streamername +" is avaliable")
  for row in rows:
    d = collections.OrderedDict()
    d['emote_name'] = row.emote_name
    d['rank'] = row.rank
    details.append(d)
  j = json.dumps(details)
  db.close()
  app.logger.info(" Sending json message")
  return j
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
@app.route('/delete',methods=['POST']) # The delete method
def delete():
  try:
     db = connectdb()
  except Exception as identifier:
    app.logger.error(identifier)
    return "{\"status\": \"No connection to database\"}"
  app.logger.info("Connection establish")  
  cursor = db.cursor()
  app.logger.info("Send sql statment") 
 
  cursor.execute("SELECT count(*) As cou From user_account where user_name= '"+request.form['username'] +"';") #Send sql statment to check if account is  made  
  row = cursor.fetchone()
 
  if row.cou!=1:
    db.close()
    app.logger.info(request.form['username']+" allredy has an account")
    return "{\"status\": \"Account not there\"}"
  else:
    app.logger.info(request.form['username']+" account deleted")
    cursor.execute("Delete From user_account where user_name='"+request.form['username']+"'AND password='"+request.form['password']+"';")
    db.commit()
    db.close()
    return "{\"status\": \"Account deleted\"}"  

if __name__ == '__main__':
  #Create Logger
  formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s") #Set log message formate
  handler = RotatingFileHandler("Log/"+time.strftime("%Y-%m-%d ")+".log",  backupCount=1) # Set log file
  handler.setLevel(logging.INFO) 
  handler.setFormatter(formatter)
  app.logger.addHandler(handler) 
  app.logger.setLevel(logging.INFO)
  
  app.run()
