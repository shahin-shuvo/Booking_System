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
    global logged_in
    try:
        conn = MySQLdb.connect(host="localhost",
                               user="root",
                               passwd="$huvo919671",
                               db="Du_Booking_Data")
        x = conn.cursor()
        form = Registration(request.form)
        if request.method == "POST" and form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data
            phone = form.phone.data
            dept = form.dept.data



            y = x.execute("SELECT * FROM Registration WHERE username = (%s)", (username,))
            if int(y) > 0:

                return render_template('signup.html', form=form)

            else:
                data = (username, email, password, phone, dept)

                x.execute("INSERT INTO Registration (username,email,password,phone,dept) VALUES (%s, %s, %s, %s, %s)",
                          data)
                flash('Thanks for Registering')
                conn.commit()
                conn.close()
                gc.collect()
                session['logged_in'] = True
                session['username'] = username
                return redirect(url_for('index'))
        return render_template('signup.html', form=form)

    except Exception as e:
        return (str(e))


@app.route('/login', methods=["GET", "POST"])
def login_page():
    error = ''
    try:
        form = LoginForm(request.form)

        conn = MySQLdb.connect(host="localhost",
                               user="root",
                               passwd="$huvo919671",
                               db="Du_Booking_Data")
        c = conn.cursor()
        if request.method == "POST" and form.validate():
            username = form.username.data
            password = form.password.data
            data = c.execute("SELECT * FROM Registration WHERE username = (%s)",
                             (username,))
            if int(data) > 0:
                data = c.fetchone()[2]

                if password == data:
                   session['logged_in'] = True
                   session['username'] = request.form['username']

                   return redirect(url_for('index'))
                else:
                    error = "Invalid credentials, try again."

            else:
                error = "Invalid credentials, try again."

        gc.collect()

        return render_template("login.html", form = form, error=error)

    except Exception as e:
        # flash(e)
        error = "Invalid credentials, try again."
        return render_template("login.html", form = form, error =error)


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


class Registration(Form):
    username = TextField('Username', [validators.Length(min=4, max=20)])
    email = TextField('Email adress', [validators.Email("Please enter your email address.")])
    password = PasswordField('Password', [validators.Required(),
                                          validators.EqualTo('confirm', message="Password must match")])
    confirm = PasswordField('Repear Password', [validators.Required()])
    phone = TextField('Phone no', [validators.Required()])
    dept = TextField('Dept_Name')


class LoginForm(Form):
    username = TextField('Username', [validators.Required()])
    password = PasswordField('Password', [validators.Required()])



#for auditorium call

@app.route('/auditorium',methods=["GET", "POST"])
def auditorium():
    today = str(date.today())
    session['date'] = today
    conn = MySQLdb.connect(host="localhost",
                           user="root",
                           passwd="$huvo919671",
                           db="Du_Booking_Data")
    c = conn.cursor()
    # for tabl1
    c.execute("SELECT * FROM TSC WHERE Date = (%s)",
              (today,))
    n1 = c.execute("SELECT * FROM TSC WHERE Date = (%s)",
                   (today,))
    data1 = c.fetchall()
    if (int(n1) > 0):
        for row in data1:
            status1 = row[1]
    else:
        status1 = "Apply for Booking"
    # for table2
    c.execute("SELECT * FROM Majumdar WHERE Date = (%s)",
              (today,))
    n2 = c.execute("SELECT * FROM Majumdar WHERE Date = (%s)",
                   (today,))
    data2 = c.fetchall()
    if (int(n2) > 0):
        for row in data2:
            status2 = row[1]
    else:
        status2 = "Apply for Booking"
    # for table3
    c.execute("SELECT * FROM Senate_Bhaban WHERE Date = (%s)",
              (today,))
    n3 = c.execute("SELECT * FROM Senate_Bhaban WHERE Date = (%s)",
                   (today,))
    data3 = c.fetchall()
    if (int(n3) > 0):
        for row in data3:
            status3 = row[1]
    else:
        status3 = "Apply for Booking"
    # for table4
    c.execute("SELECT * FROM Fine_Arts WHERE Date = (%s)",
              (today,))
    n4 = c.execute("SELECT * FROM Fine_Arts WHERE Date = (%s)",
                   (today,))
    data4 = c.fetchall()
    if (int(n4) > 0):
        for row in data4:
            status4 = row[1]
    else:
        status4 = "Apply for Booking"
    # END
    n1 = str(n1)
    n2 = str(n2)
    n3 = str(n3)
    n4 = str(n4)
    data = [status1, n1, status2, n2, status3, n3, status4, n4]
    return render_template("auditorium.html",data=data)


@app.route('/auditorium_call',methods=["GET","POST"])
def auditorium_helper():
    #initialize
    status1 = ''
    status2 = ''
    status3 = ''
    status4 = ''
    today = request.args['query']
    session['date'] = today
    conn = MySQLdb.connect(host="localhost",
                           user="root",
                           passwd="$huvo919671",
                           db="Du_Booking_Data")
    c = conn.cursor()
    # for tabl1
    c.execute("SELECT * FROM TSC WHERE Date = (%s)",
              (today,))
    n1 = c.execute("SELECT * FROM TSC WHERE Date = (%s)",
                   (today,))
    data1 = c.fetchall()
    if (int(n1) > 0):
        for row in data1:
            status1 = row[1]
    else:
        status1 = "Apply for Booking"
    # for table2
    c.execute("SELECT * FROM Majumdar WHERE Date = (%s)",
              (today,))
    n2 = c.execute("SELECT * FROM Majumdar WHERE Date = (%s)",
                   (today,))
    data2 = c.fetchall()
    if (int(n2) > 0):
        for row in data2:
            status2 = row[1]
    else:
        status2 = "Apply for Booking"
    # for table3
    c.execute("SELECT * FROM Senate_Bhaban WHERE Date = (%s)",
              (today,))
    n3 = c.execute("SELECT * FROM Senate_Bhaban WHERE Date = (%s)",
                   (today,))
    data3 = c.fetchall()
    if (int(n3) > 0):
        for row in data3:
            status3 = row[1]
    else:
        status3 = "Apply for Booking"
    # for table4
    c.execute("SELECT * FROM Fine_Arts WHERE Date = (%s)",
              (today,))
    n4 = c.execute("SELECT * FROM Fine_Arts WHERE Date = (%s)",
                   (today,))
    data4 = c.fetchall()
    if (int(n4) > 0):
        for row in data4:
            status4 = row[1]
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
    return redirect(url_for('login_page'))

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

    if query[2]=="RC Majumdar Arts Auditorium":
        table = "Majumdar"
    elif query[2] == "TSC Auditorium":
        table = "TSC"
    elif query[2] == "Nawab Ali Chowdhury Senate Bhaban":
        table = "Senate_Bhaban"
    elif query[2] == "Lecture Theater, Fine Arts":
        table = "Fine_Arts"
    try:
        with open('/home/shuvo/Pictures/'+query[3], "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        print("2")
        conn = MySQLdb.connect(host="localhost",
                           user="root",
                           passwd="$huvo919671",
                           db="Du_Booking_Data")
        x = conn.cursor()
        x.execute("INSERT INTO "+table+" (Date,Status,Username,Payment) VALUES (%s, %s, %s,  %s)",
              (query[1],status,query[0],encoded_string))
        #x.execute("UPDATE Auditorium_table SET Status = %s WHERE username = %s",(table,username,))

        conn.commit()
        conn.close()

    except Exception as e:
         return "1"
    return "0"

#for showing the Field booking Page with inital data
@app.route('/field',methods=["GET", "POST"])
def field():
    today = str(date.today())
    session['date2'] = today
    conn = MySQLdb.connect(host="localhost",
                           user="root",
                           passwd="$huvo919671",
                           db="Du_Booking_Data")
    c = conn.cursor()
    # for tabl1
    c.execute("SELECT * FROM Central_Field WHERE Date = (%s)",
              (today,))
    n1 = c.execute("SELECT * FROM Central_Field WHERE Date = (%s)",
                   (today,))
    data1 = c.fetchall()
    if (int(n1) > 0):
        for row in data1:
            status1 = row[1]
    else:
        status1 = "Apply for Booking"
    # for table2
    c.execute("SELECT * FROM Jagannath_Hall_Ground WHERE Date = (%s)",
              (today,))
    n2 = c.execute("SELECT * FROM Jagannath_Hall_Ground WHERE Date = (%s)",
                   (today,))
    data2 = c.fetchall()
    if (int(n2) > 0):
        for row in data2:
            status2 = row[1]
    else:
        status2 = "Apply for Booking"
    # for table3
    c.execute("SELECT * FROM Jahurul_Haq_Ground WHERE Date = (%s)",
              (today,))
    n3 = c.execute("SELECT * FROM Jahurul_Haq_Ground WHERE Date = (%s)",
                   (today,))
    data3 = c.fetchall()
    if (int(n3) > 0):
        for row in data3:
            status3 = row[1]
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
    status1 = ''
    status2 = ''
    status3 = ''

    today = request.args['query']
    session['date2'] = today
    conn = MySQLdb.connect(host="localhost",
                           user="root",
                           passwd="$huvo919671",
                           db="Du_Booking_Data")
    c = conn.cursor()
    # for tabl1
    c.execute("SELECT * FROM Central_Field WHERE Date = (%s)",
              (today,))
    n1 = c.execute("SELECT * FROM Central_Field WHERE Date = (%s)",
                   (today,))
    data1 = c.fetchall()
    if (int(n1) > 0):
        for row in data1:
            status1 = row[1]
    else:
        status1 = "Apply for Booking"
    # for table2
    c.execute("SELECT * FROM Jagannath_Hall_Ground WHERE Date = (%s)",
              (today,))
    n2 = c.execute("SELECT * FROM Jagannath_Hall_Ground WHERE Date = (%s)",
                   (today,))
    data2 = c.fetchall()
    if (int(n2) > 0):
        for row in data2:
            status2 = row[1]
    else:
        status2 = "Apply for Booking"
    # for table3
    c.execute("SELECT * FROM Jahurul_Haq_Ground WHERE Date = (%s)",
              (today,))
    n3 = c.execute("SELECT * FROM Jahurul_Haq_Ground WHERE Date = (%s)",
                   (today,))
    data3 = c.fetchall()
    if (int(n3) > 0):
        for row in data3:
            status3 = row[1]
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
    return redirect(url_for('login_page'))

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

    if query[2] == "DU Central Field":
        table = "Central_Field"
    elif query[2] == "Jagannath Hall Field":
        table = "Jagannath_Hall_Ground"
    elif query[2] == "Jahurul Haq Hall Ground":
        table = "Jahuru_Haq_Ground"

    try:
        with open('/home/shuvo/Pictures/' + query[3], "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())

        conn = MySQLdb.connect(host="localhost",
                               user="root",
                               passwd="$huvo919671",
                               db="Du_Booking_Data")
        x = conn.cursor()
        x.execute("INSERT INTO " + table + " (Date,Status,Username,Payment) VALUES (%s, %s, %s,  %s)",
                  (query[1], status, query[0], encoded_string))


        conn.commit()
        conn.close()

    except Exception as e:
        return "1"
    return "0"

if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=8080)
