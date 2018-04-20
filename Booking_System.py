import base64
import gc
from functools import wraps
from datetime import date
from json import dumps
import warnings
import MySQLdb
import app as app
import jinja2
import os
from flask import Flask, render_template, request, flash, session, url_for, redirect, jsonify, make_response, json
from flaskext.mysql import MySQL
from flask_wtf import FlaskForm
from jinja2 import Environment
from pymysql.constants.FIELD_TYPE import JSON
from requests import Session
from werkzeug.utils import secure_filename
from wtforms import Form, TextField, validators, PasswordField, BooleanField, StringField
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart, connection
from wtforms.validators import InputRequired, Length
import formencode_jinja2
jinja_env = Environment(extensions=['jinja2.ext.loopcontrols'])
jinja_env.add_extension(formencode_jinja2.formfill)


app = Flask(__name__)

app.jinja_env.add_extension('jinja2.ext.loopcontrols')
app.secret_key = "super secret key"
app.config['UPLOAD_FOLDER'] = 'UPLOAD_FOLDER'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '$huvo919671'
app.config['MYSQL_DB'] = "Du_Booking_Data"
mysql = MySQL(app)
username = "Guest"

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/index')
def home():
    return render_template('index.html')

@app.route('/signup', methods=["GET", "POST"])
def signup():
    return render_template('signup.html')

@app.route('/signup_helper', methods=["GET", "POST"])
def signup_helper():
    global logged_in
    try:
        query = request.args['query']
        query = json.loads(query)
        conn = MySQLdb.connect(host="localhost",
                               user="root",
                               passwd="$huvo919671",
                               db="Du_Booking_Data")
        x = conn.cursor()




        y = x.execute("SELECT * FROM Registration WHERE username = (%s)", (query[0],))
        if int(y) > 0:
            return "Exist"

        else:
            data = (query[0], query[1], query[2], query[3], query[4])

            x.execute("INSERT INTO Registration (username,email,password,phone,dept) VALUES (%s, %s, %s, %s, %s)",
                          data)
            flash('Thanks for Registering')
            conn.commit()
            conn.close()
            gc.collect()
            session['logged_in'] = True
            session['username'] = username
            return "OK"
        return "ERROR"

    except Exception as e:
        return (str(e))
@app.route('/login', methods=["GET", "POST"])
def login():
    return render_template('login.html')

@app.route('/login_helper', methods=["GET", "POST"])
def login_helper():
    error = ''
    try:
        query = request.args['query']
        query = json.loads(query)

        conn = MySQLdb.connect(host="localhost",
                               user="root",
                               passwd="$huvo919671",
                               db="Du_Booking_Data")
        c = conn.cursor()
        if query[2]=="ADMIN":
            data = c.execute("SELECT * FROM Admin WHERE username = (%s) AND password = (%s)",
                             (query[0], query[1]))
            if int(data) > 0:
                session['logged_in'] = True
                session['username'] = query[0]
                gc.collect()
                return "OK"
        elif query[2]=="USER":
            data = c.execute("SELECT * FROM Registration WHERE username = (%s) AND password = (%s)",
                             (query[0], query[1]))
            if int(data) > 0:
                session['logged_in'] = True
                session['username'] = query[0]
                gc.collect()
                return "OK"

        return "error"


    except Exception as e:
        # flash(e)
        error = "Invalid credentials, try again."
        return "Error"


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))

    return wrap


@app.route("/logout")
@login_required
def logout():
    session.clear()
    gc.collect()
    return render_template("index.html")




#for auditorium call

@app.route('/auditorium',methods=["GET", "POST"])
def auditorium():

    tsc = "TSC Auditorium"
    rcm= "RC Majumdar Arts Auditorium"
    senate= "Nawab Ali Chowdhury Senate Bhaban"
    arts= "Lecture Theater, Fine Arts"
    today = str(date.today())
    session['date'] = today
    conn = MySQLdb.connect(host="localhost",
                           user="root",
                           passwd="$huvo919671",
                           db="Du_Booking_Data")
    c = conn.cursor()
    # for tabl1

    c.execute("SELECT * FROM Auditorium_Data WHERE Date = (%s) AND Auditorium = (%s)",
              (today,tsc,))
    n1 = c.execute("SELECT * FROM Auditorium_Data WHERE Date = (%s) AND Auditorium = (%s)",
                   (today,tsc,))
    data1 = c.fetchall()
    if (int(n1) > 0):
        for row in data1:
            status1 = row[3]
    else:
        status1 = "Apply for Booking"

    # for table2
    c.execute("SELECT * FROM Auditorium_Data WHERE Date = (%s) AND Auditorium = (%s)",
              (today,rcm,))
    n2 = c.execute("SELECT * FROM Auditorium_Data WHERE Date = (%s) AND Auditorium = (%s)",
                   (today,rcm,))
    data2 = c.fetchall()
    if (int(n2) > 0):
        for row in data2:
            status2 = row[3]
    else:
        status2 = "Apply for Booking"
    # for table3
    c.execute("SELECT * FROM Auditorium_Data WHERE Date = (%s) AND Auditorium = (%s)",
              (today,senate,))
    n3 = c.execute("SELECT * FROM Auditorium_Data WHERE Date = (%s) AND Auditorium = (%s)",
                   (today,senate,))
    data3 = c.fetchall()
    if (int(n3) > 0):
        for row in data3:
            status3 = row[3]
    else:
        status3 = "Apply for Booking"
    # for table4
    c.execute("SELECT * FROM Auditorium_Data WHERE Date = (%s) AND Auditorium = (%s)",
              (today,arts))
    n4 = c.execute("SELECT * FROM Auditorium_Data WHERE Date = (%s) AND Auditorium = (%s)",
                   (today,arts))
    data4 = c.fetchall()
    if (int(n4) > 0):
        for row in data4:
            status4 = row[3]
    else:
        status4 = "Apply for Booking"
    # END
    n1 = str(n1)
    n2 = str(n2)
    n3 = str(n3)
    n4 = str(n4)
    print(status1)
    data = [status1, n1, status2, n2, status3, n3, status4, n4]
    return render_template("auditorium.html",data=data)


@app.route('/auditorium_call',methods=["GET","POST"])
def auditorium_helper():
    #initialize

    tsc = "TSC Auditorium"
    rcm = "RC Majumdar Arts Auditorium"
    senate = "Nawab Ali Chowdhury Senate Bhaban"
    arts = "Lecture Theater, Fine Arts"

    today = request.args['query']
    session['date'] = today
    conn = MySQLdb.connect(host="localhost",
                           user="root",
                           passwd="$huvo919671",
                           db="Du_Booking_Data")
    c = conn.cursor()
    # for tabl1
    c.execute("SELECT * FROM Auditorium_Data WHERE Date = (%s) AND Auditorium = (%s)",
              (today, tsc,))
    n1 = c.execute("SELECT * FROM Auditorium_Data WHERE Date = (%s) AND Auditorium = (%s)",
                   (today, tsc,))
    data1 = c.fetchall()
    if (int(n1) > 0):
        for row in data1:
            status1 = row[3]
    else:
        status1 = "Apply for Booking"
    # for table2
    c.execute("SELECT * FROM Auditorium_Data WHERE Date = (%s) AND Auditorium = (%s)",
              (today, rcm,))
    n2 = c.execute("SELECT * FROM Auditorium_Data WHERE Date = (%s) AND Auditorium = (%s)",
                   (today, rcm,))
    data2 = c.fetchall()
    if (int(n2) > 0):
        for row in data2:
            status2 = row[3]
    else:
        status2 = "Apply for Booking"
    # for table3
    c.execute("SELECT * FROM Auditorium_Data WHERE Date = (%s) AND Auditorium = (%s)",
              (today, senate,))
    n3 = c.execute("SELECT * FROM Auditorium_Data WHERE Date = (%s) AND Auditorium = (%s)",
                   (today, senate,))
    data3 = c.fetchall()
    if (int(n3) > 0):
        for row in data3:
            status3 = row[3]
    else:
        status3 = "Apply for Booking"
    # for table4
    c.execute("SELECT * FROM Auditorium_Data WHERE Date = (%s) AND Auditorium = (%s)",
              (today, arts))
    n4 = c.execute("SELECT * FROM Auditorium_Data WHERE Date = (%s) AND Auditorium = (%s)",
                   (today, arts,))
    data4 = c.fetchall()
    if (int(n4) > 0):
        for row in data4:
            status4 = row[3]
    else:
        status4 = "Apply for Booking"
    # END
    n1 = str(n1)
    n2 = str(n2)
    n3 = str(n3)
    n4 = str(n4)


    data= [status1,n1,status2,n2,status3,n3,status4,n4]
    return make_response(dumps(data))


@app.route('/auditorium_booking_form')
def booking_form():
    if 'logged_in' in session:
        username = session['username']
        date = session['date']
        print(username)
        return render_template('auditorium_booking_form.html',username=username,date=date)

    flash('You have to Login first!!')
    return redirect(url_for('login'))

@app.route('/auditorium_booking_done',methods=["GET", "POST"])
def auditorium_booking_done():
    table=""
    query = request.args['query']
    query = json.loads(query)
    file = query[3]

    print(query[0])
    print(query[1])
    print(query[2])
    print(query[3])
    status = "Already Applied"


    try:
        with open('/home/shuvo/Pictures/'+query[3], "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())

        conn = MySQLdb.connect(host="localhost",
                           user="root",
                           passwd="$huvo919671",
                           db="Du_Booking_Data")
        x = conn.cursor()
        n = x.execute("SELECT * FROM Auditorium_Data WHERE Date = (%s) AND Auditorium = (%s)",
                       (query[1], query[2],))
        print(n)
        if(int(n)>0):
            return "exist"
        else:
            x.execute(
                "INSERT INTO Auditorium_Data (Auditorium,Date,Status,Payment,Username,Applydate) VALUES (%s, %s, %s,  %s, %s, %s)",
                (query[2], query[1], status, encoded_string, query[0], query[1]))
            # x.execute("UPDATE Auditorium_table SET Status = %s WHERE username = %s",(table,username,))

            conn.commit()
            conn.close()
            return "0"

    except Exception as e:
         return "1"


#for showing the Field booking Page with inital data
@app.route('/field',methods=["GET", "POST"])
def field():
    central = "DU Central Field"
    jagannath ="Jagannath Hall Field"
    jahurul="Jahurul Haq Hall Ground"
    today = str(date.today())
    session['date2'] = today
    conn = MySQLdb.connect(host="localhost",
                           user="root",
                           passwd="$huvo919671",
                           db="Du_Booking_Data")
    c = conn.cursor()
    # for tabl1
    c.execute("SELECT * FROM Field_Data WHERE Date = (%s) AND Field = (%s)",
              (today,central,))
    n1 = c.execute("SELECT * FROM Field_Data WHERE Date = (%s) AND Field = (%s)",
                   (today,central,))
    data1 = c.fetchall()
    if (int(n1) > 0):
        for row in data1:
            status1 = row[3]
    else:
        status1 = "Apply for Booking"
    # for table2
    c.execute("SELECT * FROM Field_Data WHERE Date = (%s) AND Field = (%s)",
              (today,jagannath,))
    n2 = c.execute("SELECT * FROM Field_Data WHERE Date = (%s) AND Field = (%s)",
                   (today,jagannath,))
    data2 = c.fetchall()
    if (int(n2) > 0):
        for row in data2:
            status2 = row[3]
    else:
        status2 = "Apply for Booking"
    # for table3
    c.execute("SELECT * FROM Field_Data WHERE Date = (%s) AND Field = (%s)",
              (today,jahurul,))
    n3 = c.execute("SELECT * FROM Field_Data WHERE Date = (%s) AND Field = (%s)",
                   (today,jahurul,))
    data3 = c.fetchall()
    if (int(n3) > 0):
        for row in data3:
            status3 = row[3]
    else:
        status3 = "Apply for Booking"

    # END
    n1 = str(n1)
    n2 = str(n2)
    n3 = str(n3)

    data = [status1, n1, status2, n2, status3, n3]
    return render_template("field.html",data=data)


#for showing the Field booking Page with selected date
@app.route('/field_call',methods=["GET","POST"])
def field_helper():
    #initialize
    central = "DU Central Field"
    jagannath = "Jagannath Hall Field"
    jahurul = "Jahurul Haq Hall Ground"

    today = request.args['query']
    session['date2'] = today
    conn = MySQLdb.connect(host="localhost",
                           user="root",
                           passwd="$huvo919671",
                           db="Du_Booking_Data")
    c = conn.cursor()
    # for tabl1
    c.execute("SELECT * FROM Field_Data WHERE Date = (%s) AND Field = (%s)",
              (today, central,))
    n1 = c.execute("SELECT * FROM Field_Data WHERE Date = (%s) AND Field = (%s)",
                   (today, central,))
    data1 = c.fetchall()
    if (int(n1) > 0):
        for row in data1:
            status1 = row[3]
    else:
        status1 = "Apply for Booking"
    # for table2
    c.execute("SELECT * FROM Field_Data WHERE Date = (%s) AND Field = (%s)",
              (today, jagannath,))
    n2 = c.execute("SELECT * FROM Field_Data WHERE Date = (%s) AND Field = (%s)",
                   (today, jagannath,))
    data2 = c.fetchall()
    if (int(n2) > 0):
        for row in data2:
            status2 = row[3]
    else:
        status2 = "Apply for Booking"
    # for table3
    c.execute("SELECT * FROM Field_Data WHERE Date = (%s) AND Field = (%s)",
              (today, jahurul,))
    n3 = c.execute("SELECT * FROM Field_Data WHERE Date = (%s) AND Field = (%s)",
                   (today, jahurul,))
    data3 = c.fetchall()
    if (int(n3) > 0):
        for row in data3:
            status3 = row[3]
    else:
        status3 = "Apply for Booking"

    # END
    n1 = str(n1)
    n2 = str(n2)
    n3 = str(n3)


    data= [status1,n1,status2,n2,status3,n3]
    return make_response(dumps(data))

@app.route('/field_booking_form')
def field_form():
    if 'logged_in' in session:
        username = session['username']
        date = session['date2']
        print(username)
        return render_template('field_booking_form.html',username=username,date=date)

    flash('You have to Login first!!')
    return redirect(url_for('login'))

@app.route('/field_booking_done',methods=["GET", "POST"])
def field_booking_done():
    table = ""
    query = request.args['query']
    query = json.loads(query)
    file = query[3]

    print(query[0])
    print(query[1])
    print(query[2])
    print(query[3])
    status = "Already Applied"


    try:
        with open('/home/shuvo/Pictures/' + query[3], "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())

        conn = MySQLdb.connect(host="localhost",
                               user="root",
                               passwd="$huvo919671",
                               db="Du_Booking_Data")
        x = conn.cursor()
        x = conn.cursor()
        n = x.execute("SELECT * FROM Field_Data WHERE Date = (%s) AND Auditorium = (%s)",
                      (query[1], query[2],))
        print(n)
        if (int(n) > 0):
            return "exist"
        else:
            x.execute(
                "INSERT INTO Field_Data (Field,Date,Status,Payment,Username,Applydate) VALUES (%s, %s, %s,  %s, %s, %s)",
                (query[2], query[1], status, encoded_string, query[0], query[1]))

            conn.commit()
            conn.close()
            return "0"


    except Exception as e:
        return "1"


@app.route('/Auditorium_Blog',methods=["GET", "POST"])
def blog1():
    return render_template('Auditorium_Blog.html')

@app.route('/field_blog',methods=["GET", "POST"])
def blog2():
    return render_template('field_blog.html')

if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=8080)
