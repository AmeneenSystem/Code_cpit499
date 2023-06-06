#------------------------------------------------------
#-------Student: Muna,Nora,Thuray,Arwa , M4
#------------------------------------------------------


from flask import Flask,make_response, url_for,redirect, request, render_template,current_app, g, send_file,session
from werkzeug.utils import secure_filename
from datetime import datetime
import cv2
from hubconf import custom
import sqlite3
import yolov5  # pip install yolov5
import detect
from gmplot import gmplot #pip install gmplot
import Location
from flask_session import Session
#  pip install flask flask_sqlalchemy flask_login flask_bcrypt flask_wtf wtforms email_validator

application = Flask(__name__)
application.config["SESSION_PERMANENT"] = False
application.config["SESSION_TYPE"] = "filesystem"
application.secret_key = 'any random string'
Session(application)
sess = Session()
sess.init_app(application)

# database
databasename = '_database.db'
Data_table = 'files_names_table'
operators_table = 'operators_table'
Location_table = 'locations_table'
upload_folder= "static/uploaded/"
processed_folder= "static/processed/"
#handling database connection error
try:
  print(f'Checking if {databasename} exists or not...')
  conn = sqlite3.connect(databasename, uri=True)
  print(f'Database exists. Succesfully connected to {databasename}')
  conn.execute('CREATE TABLE IF NOT EXISTS ' + Data_table + ' (id INTEGER PRIMARY KEY AUTOINCREMENT,areaimg TEXT UNIQUE NOT NULL,operator_email TEXT NOT NULL, area TEXT NOT NULL, count INTEGER NOT NULL,imagetime timestamp,alarms_count INTEGER NOT NULL)')
  conn.execute('CREATE TABLE IF NOT EXISTS ' + operators_table + ' (id INTEGER PRIMARY KEY AUTOINCREMENT,email TEXT UNIQUE NOT NULL, password TEXT NOT NULL)')
  print(f'Succesfully Created Table {Data_table}')

except sqlite3.OperationalError as err:
  print('Database error,see log')
  print(err)
# calling the weight for yolov5 model
modelx = yolov5.load('best.pt')

# set model parameters
modelx.conf = .4  # NMS confidence threshold
modelx.iou = 0.45  # NMS IoU threshold
modelx.img = 640

#------------------------------------------------------
#-----------------link to html pages  --------------
#------------------------------------------------------
@application.route('/')
def index():
  return render_template("index.html")

@application.route('/login')
def login():
  return render_template("login.html")

@application.route('/validate_login',methods=['POST'])
def validate_login():
  #check if the operator exists
  if request.method == 'POST':
    if request.args.get('email') and request.args.get('password'):
      email = request.args.get('email')
      password = request.args.get('password')
      # print(email,password)
      connt = sqlite3.connect(databasename, uri=True)
      cursor = connt.cursor()
      sql_select_query  = "SELECT * from "  + operators_table + " where email = ? and password = ?;"
      cursor.execute(sql_select_query, (email,password,))
      records = cursor.fetchall()
      for row in records:
        session['id']=row[0]
        # print(session['id'])
        session["email"]=email
        # print("good")
        return "0"
  # print("bad")
  return "-1"

@application.route('/operator')
def operator():
  return render_template("operator.html")

@application.route('/upload_page')
def upload_page():
  # print(session.get("id"))
  if not session.get("id"):
    return redirect("/operator")
  return render_template("upload.html")

@application.route('/dashboard',methods=['GET'])
def dashboard():
  col0 = 0
  col1 = 0
  col2 = 0
  col3 = 0
  col4 = 0
  alarms0_count=0
  alarms1_count=0
  alarms2_count=0
  alarms3_count=0
  alarms4_count=0
  col0color = "0f0"
  col1color = "0f0"
  col2color = "0f0"
  col3color = "0f0"
  col4color = "0f0"
  notifications_count = 0
 #database connection and dispalying the barchart results
  connt = sqlite3.connect(databasename, uri=True)
  cursor = connt.cursor()
  sql_select_query  = "SELECT * from "  + Data_table + " where area = ? ORDER BY id DESC LIMIT 1;"
  cursor.execute(sql_select_query, ("ZamZam",))
  records = cursor.fetchall()
  for row in records:
    col0 = row[4]
    alarms0_count = row[6]
    if row[4] > 200:
      col0color = "f00"
      
  sql_select_query  = "SELECT * from "  + Data_table + " where area = ? ORDER BY id DESC LIMIT 1;"
  cursor.execute(sql_select_query, ("Mina",))
  records = cursor.fetchall()
  for row in records:
    col1 = row[4]
    alarms1_count = row[6]
    if row[4] > 200:
      col1color = "f00"

  sql_select_query  = "SELECT * from "  + Data_table + " where area = ? ORDER BY id DESC LIMIT 1;"
  cursor.execute(sql_select_query, ("Muzdalifah",))
  records = cursor.fetchall()
  for row in records:
    col2 = row[4]    
    alarms2_count = row[6]
    if int(row[4]) > 200:
      print("red")
      col2color = "f00"

  sql_select_query  = "SELECT * from "  + Data_table + " where area = ? ORDER BY id DESC LIMIT 1;"
  cursor.execute(sql_select_query, ("Mount Arafat",))
  records = cursor.fetchall()
  for row in records:
    col3 = row[4]
    alarms3_count = row[6]
    if row[4] > 200:
      col3color = "f00"

  sql_select_query  = "SELECT * from "  + Data_table + " where area = ? ORDER BY id DESC LIMIT 1;"
  cursor.execute(sql_select_query, ("Safa and Marwah",))
  records = cursor.fetchall()
  for row in records:
    col4 = row[4]
    alarms4_count = row[6]
    if row[4] > 200:
      col4color = "f00"

  cursor.close()
 
  fullimgname = ""
  if request.method == 'GET':
    if request.args.get('image') != None:
      #check if the name secure and not repeated
      fullimgname = processed_folder + secure_filename(request.args.get('image'))
  else:  
    connt = sqlite3.connect(databasename, uri=True)
    cursor = connt.cursor()
    sql_select_query  = "SELECT * from "  + Data_table + " ORDER BY id DESC LIMIT 1;"
    cursor.execute(sql_select_query)
    records = cursor.fetchall()
    for row in records:
      fullimgname = row[1]
    cursor.close()
  total_people = col0 + col1 + col2 + col3 + col4 
  notifications_count = int(alarms0_count) + int(alarms1_count) + int(alarms2_count) + int(alarms3_count) + int(alarms4_count)

  return render_template("dashboard.html",fullimgname=fullimgname,col0=col0,col1=col1,col2=col2,col3=col3,col4=col4,total_people=total_people,col0color=col0color,col1color=col1color,col2color=col2color,col3color=col3color,col4color=col4color,notifications_count=notifications_count)
 #getting the picture from the upload page and save it in database with the information
@application.route('/uploadfile',methods=['POST'])

#---------------------------------------------------------------------------------
#------Uploade files (from uploade page "image and area" ) ---------------------
#---------------------------------------------------------------------------------
def uploadfile():
  area = request.args.get('area')
  if request.method == 'POST':
    files = request.files.getlist('file')     
    complete_formate_file  = []
    store_date = secure_filename(str(datetime.now()))
    for file in files:
      filename = secure_filename(file.filename)
      complete_formate_file.append(secure_filename(store_date + "&" + filename))
      file.save(upload_folder+complete_formate_file[-1])
      processOn_image(complete_formate_file[-1],area)  
  return complete_formate_file[-1]

#------------------------------------------------------
#-----------------Get the count,alarm --------------
#------------------------------------------------------
def get_count_alarms(fullimgname):
  count = 0
  alarms = 0
  img = cv2.imread(fullimgname)

  detect.run(source=fullimgname, weights="best.pt", conf_thres=0.4, project="static",name="processed",save_txt=True,save_conf=True, exist_ok=True,hide_labels=True,hide_conf=True,nosave=True)
  file1 = open('static/processed/labels/'+fullimgname.split("/")[-1][:-3]+"txt", 'r')
  count = 0 
  boxes_discription = []  
  while True:
    result = file1.readline()
    if not result:
        break
    count +=1
    cls , x, y, w, h, conf = result.split()
    x = int(float(x)*640)
    y = int(float(y)*640)
    w = int(float(w)*640)
    h = int(float(h)*640)
    
    xc = x + w / 2 #calcu the center of the box 
    yc = y + h / 2
    boxes_discription.append([x, y, w, h, xc, yc ,0])
  
  file1.close()
  #clac the destanse between boxes  
  max_density = 0
  for i,box_ref in enumerate(boxes_discription): # 1st box
    for j,box in enumerate(boxes_discription): # 2st box
      if i != j:
        if abs(box_ref[4] - box[4]) < box_ref[2] and abs(box_ref[5] - box[5]) < box_ref[3]:
          boxes_discription[i][6] +=1 
          if boxes_discription[i][6] > max_density:
            max_density = boxes_discription[i][6]
  
  if max_density ==0:
    max_density = 1

  
  for i,box_ref in enumerate(boxes_discription): 
    cv2.rectangle(img, (box_ref[0]-int(box_ref[2]/2), box_ref[1]-int(box_ref[3]/2)), (box_ref[0]+int(box_ref[2]/2), box_ref[1]+int(box_ref[3]/2)), (255/max_density*(max_density-box_ref[6]), 255/max_density*(max_density-box_ref[6]), 255), 2)
    
    if box_ref[6]>3:
        alarms +=1
  return count,alarms,img

#------------------------------------------------------
#-----------------Process on Image ---------------------
#------------------------------------------------------
def processOn_image(file_name,area=""):
  fullimgname = upload_folder+ file_name
  count,alarms,img = get_count_alarms(fullimgname)
  latitude=21.4359348
  longtitude=39.6817388
  lag, lat = Location.calculatecoor(fullimgname) 
  if lat >0:
    latitude = lat
    longtitude = lag
    
  gmap = gmplot.GoogleMapPlotter(latitude,longtitude,12) # 12 is how much zooming you want in the map
  gmap.marker(latitude,longtitude,"cornflowerblue")
  gmap.draw("static/location.html")  
  cv2.imwrite(processed_folder + file_name , img)     # 255 255 255 white     # 0 0 255  red  
  

  connt = sqlite3.connect(databasename, uri=True)
  cursor = connt.cursor()
  sqlite_insert_with_param = "INSERT INTO "  + Data_table + " ('areaimg', 'area','operator_email', 'count', 'imagetime','alarms_count') VALUES (?,?, ?, ?, ?,?);"
  data_tuple = (file_name, area,session["email"], count, datetime.now(),alarms)
  cursor.execute(sqlite_insert_with_param, data_tuple)
 
  connt.commit()
  
  sqlite_insert_with_param2 = "INSERT INTO "  + Location_table + " ('area', 'alarms_count', 'count', 'long','lat') VALUES (?,?, ?, ?, ?);"
  data_tuple2= ( area,alarms, count,longtitude,latitude)
  cursor.execute(sqlite_insert_with_param2, data_tuple2)
  connt.commit()
  return



if __name__ == '__main__': 
  application.run(debug=True,host="0.0.0.0",use_reloader=False,port=7000)