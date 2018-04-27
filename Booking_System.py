import base64
import gc
from functools import wraps
from datetime import date
from json import dumps
from flask import Flask, render_template, request, flash, session, url_for, redirect, jsonify, make_response, json
from flaskext.mysql import MySQL

from jinja2 import Environment

import formencode_jinja2
jinja_env = Environment(extensions=['jinja2.ext.loopcontrols'])
jinja_env.add_extension(formencode_jinja2.formfill)


app = Flask(__name__)
mysql = MySQL()
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
app.secret_key = "super secret key"
app.config['UPLOAD_FOLDER'] = 'UPLOAD_FOLDER'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '$huvo919671'
app.config['MYSQL_DATABASE_DB'] = "Du_Booking_Data"
mysql.init_app(app)

username = "Guest"

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/index')
def home():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/signup', methods=["GET", "POST"])
def signup():
    return render_template('signup.html')

@app.route('/signup_helper', methods=["GET", "POST"])
def signup_helper():
    global logged_in
    try:
        query = request.args['query']
        query = json.loads(query)
        conn = mysql.connect()
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
        conn = mysql.connect()
        c = conn.cursor()
        print(query[0])
        print(query[1])
        if query[2]=="ADMIN":
            data = c.execute("SELECT * FROM Admin WHERE username = (%s) AND password = (%s)",
                             (query[0], query[1]))
            if int(data) > 0:
                session['logged_in'] = True
                session['username'] = query[0]
                gc.collect()
                return "OK_Admin"
        elif query[2]=="USER":
            data = c.execute("SELECT * FROM Registration WHERE username = (%s) AND password = (%s)",
                             (query[0], query[1]))
            if int(data) > 0:
                session['logged_in'] = True
                session['username'] = query[0]
                gc.collect()
                return "OK_User"

        return "error"


    except Exception as e:
        # flash(e)
        error = "Invalid credentials, try again."
        return "Error"
#This is only for user before booking
@app.route('/login_user', methods=["GET", "POST"])
def login_user():
    error = ''
    try:
        query = request.args['query']
        query = json.loads(query)
        conn = mysql.connect()
        c = conn.cursor()
        data = c.execute("SELECT * FROM Registration WHERE username = (%s) AND password = (%s)",
                         (query[0], query[1]))
        if int(data) > 0:
            session['logged_in'] = True
            session['username'] = query[0]
            gc.collect()
            return "OK_User"

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

@app.route('/Auditorium_Blog',methods=["GET", "POST"])
def blog1():
    return render_template('Auditorium_Blog.html')

@app.route('/field_blog',methods=["GET", "POST"])
def blog2():

    return render_template('field_blog.html')




@app.route('/auditorium_test',methods=['GET'])
def auditorium_final():
    date_current=str(date.today())
    session['date'] = date_current
    #date_current ="2018-04-04"
    conn = mysql.connect()
    cursor = conn.cursor()


    cursor.execute("SELECT  Auditorium_Info.Name, Auditorium_Table.Status FROM Auditorium_Info LEFT OUTER JOIN  Auditorium_Table  ON Auditorium_Info.Name=Auditorium_Table.Auditorium AND Auditorium_Table.Date= %s ORDER BY Auditorium_Info.Name DESC",(date_current,))

    data = cursor.fetchall()
    print(data)
    if 'logged_in' in session:
            username = session['username']
    else: username = "Guest"
    return render_template("auditorium_main.html", data=data, username=username, date =date_current)

@app.route('/auditorium_data_query',methods=["GET","POST"])
def auditorium_query():
    #initialize
    date_current = request.args['query']
    session['date'] = date_current
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT  Auditorium_Info.Name, Auditorium_Table.Status FROM Auditorium_Info LEFT OUTER JOIN  Auditorium_Table  ON Auditorium_Info.Name=Auditorium_Table.Auditorium AND Auditorium_Table.Date= %s  ORDER BY Auditorium_Info.Name ASC",
        (date_current,))
    data = cursor.fetchall()
    print(data)
    return make_response(dumps(data))

@app.route('/auditorium_book_helper',methods=["GET","POST"])
def auditorium_book_helper():
    try:
       auditorium = request.args['query']
       session['auditorium_applied'] = auditorium
       print(auditorium)
       return "0"
    except Exception as e:
        return "1"

@app.route('/auditorium_book',methods=["GET","POST"])
def auditorium_book():
    #initialize
    status = "Already Applied"
    auditorium = session['auditorium_applied']
    file = request.args['query2']
    date_apply = session['date']
    username = session['username']
    print(auditorium)
    print(date_apply)
    print(username)
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        with open('/home/shuvo/Pictures/'+file, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        cursor.execute(
            "INSERT INTO Auditorium_Table (Auditorium,Date,Status,Payment,Username,Applydate) VALUES (%s, %s, %s,  %s, %s, %s)",
            (auditorium, date_apply, status, encoded_string, username, date_apply))
        # x.execute("UPDATE Auditorium_table SET Status = %s WHERE username = %s",(table,username,))
        conn.commit()
        conn.close()
        return "0"

    except Exception as e:
        return "1"



if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=5000)
