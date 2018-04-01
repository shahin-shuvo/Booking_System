import gc

import MySQLdb
from flask import Flask, render_template, request, flash, session
from flask_mysqldb import MySQL
from requests import Session
from wtforms import Form, TextField, validators, PasswordField, BooleanField
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart, connection

app = Flask(__name__)
app.secret_key = "super secret key"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '$huvo919671'
app.config['MYSQL_DB'] = "Du_Booking_Data"
mysql = MySQL(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/index')
def home():
    return render_template('index.html')


@app.route('/signup', methods=["GET","POST"])
def signup():
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


            cur = mysql.connection.cursor()
            print("ho")
            y= x.execute("SELECT * FROM Registration WHERE username = (%s)",(username,))
            print("huh")
            if int(y) > 0:
                flash("Username already exist.")
                return render_template('registration.html',form=form)

            else:
                data = (username,email,password,phone,dept)

                x.execute("INSERT INTO Registration (username,email,password,phone,dept) VALUES (%s, %s, %s, %s, %s)",data)
                flash("Thanks for Registering")
                conn.commit()
                gc.collect()
                return render_template('index.html')
        return render_template('signup.html', form=form)

    except Exception as e:
        return (str(e))


class Registration(Form):
    username = TextField('Username',[validators.Length(min=4,max=20)])
    email = TextField('Email adress')
    password = PasswordField('Password', [validators.Required(),
                                              validators.EqualTo('confirm',message="Password must match")])
    confirm = PasswordField('Repear Password')
    phone = TextField('Phone no', [validators.Required()])
    dept = TextField('Dept_Name')

if __name__ == '__main__':
    app.debug =True
    app.run(host='127.0.0.1', port=8080)
