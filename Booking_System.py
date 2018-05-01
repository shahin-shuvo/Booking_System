import base64
import gc
from functools import wraps
from datetime import date
from json import dumps
from flask import Flask, render_template, request, flash, session, url_for, redirect, jsonify, make_response, json
from flaskext.mysql import MySQL

from jinja2 import Environment
from ConfirmationMail import send_mail
from threading import Thread
from ClassLabBook import classBook, showLabStatus

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
# app.config['MYSQL_DATABASE_PASSWORD'] = '$huvo919671'
# app.config['MYSQL_DATABASE_DB'] = "Du_Booking_Data"
app.config['MYSQL_DATABASE_PASSWORD'] = 'shanto55'
app.config['MYSQL_DATABASE_DB'] = "Booking_system"
mysql.init_app(app)

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
    conn = mysql.connect()
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
    conn = mysql.connect()
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
        conn = mysql.connect()
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
    conn = mysql.connect()
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
    conn = mysql.connect()
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

        conn = mysql.connect()
        x = conn.cursor()

        n = x.execute("SELECT * FROM Field_Data WHERE Date = (%s) AND Field = (%s)",
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


#Shanto's file

#Class Booking request

@app.route('/ClassBookingReq',methods=['GET'])
#initial page for booking requests this will show
#all request for class booking
def class_booking():
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""SELECT u_name,req_id, room_no,registration_date,start_date, 
                          end_date, slot_1, slot_2, slot_3, slot_4, slot_5,admin_confirmation 
                          from class_booking_request""")
        data = cursor.fetchall()
        return render_template('ClassBookingReq.html', data=data)

@app.route('/table_clicked',methods=['GET'])
#send user details information when a request button is clicked
def row_clicked():
    table_row=request.args['query']
    conn = mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT username,email,phone,dept from Registration WHERE username = (%s)",(table_row,))
    data=cursor.fetchone()
    return make_response(dumps(data))

@app.route('/user_image',methods=['GET','POST'])
#send user image to admin
def send_image():
    name=request.args["query"]
    conn = mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT image from Registration WHERE username= (%s)",(name,))
    data=cursor.fetchone()
    return data[0]

@app.route('/confirmation',methods=['GET','POST'])
#admin confirmations or discarding information will be
#sent to user through email
def feedback():
    reply=request.args['query']
    user_name=request.args['name']
    email=request.args['email']
    room_name=request.args['room_name']
    start_date=request.args['start_date']
    end_date=request.args['end_date']
    time_range=request.args['time_range']
    time_slot=request.args['time_slot']

    print(user_name+email+start_date+end_date+time_range+time_slot)
    req_id=request.args['reqid']
    req_id_f=int(req_id)
    confirmed=""
    if reply.lower()=="yes":
        reply=1
        confirmed="confirmed"
    else:
        reply=0
        confirmed="not confirmed"
    if(end_date != "Not Applicable"):
        msg_body = "Dear " + user_name +"\n" \
                    "Your booking request for Room " + room_name + " is " + confirmed + ".\n\n" \
                    "Your booking booking details :\n"\
                    "Start Date : "+start_date+"\n"\
                    "End Date : "+end_date+"\n"\
                    "Time Range : "+time_range+"\n"\
                    "Slot Numbers : "+time_slot+"\n"
    else:
        msg_body = "Dear " + user_name +"\n" \
                   "Your booking request for Room " + room_name + " is " + confirmed + ".\n\n" \
                    "Your booking booking details :\n" \
                    "Date : " + start_date + "\n" \
                    "Time Range : " + time_range + "\n" \
                    "Slot Numbers : " + time_slot + "\n"
    msg_body=msg_body+"\nWith Regards\nDU Online Booking System\nFor any query visit https://www.du.ac.bd"
    mailThread=Thread(target=send_mail,args=(msg_body,email))
    mailThread.start()

    print("Request id "+str(req_id_f))
    print(msg_body)
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        cursor.execute("""UPDATE class_booking_request 
                          SET admin_confirmation = %s WHERE req_id = %s"""
                            ,(reply,req_id_f,))
        conn.commit()
        return "Success"
    except Exception as e:
        print(e)
        return "Error"




#Lab booking request
@app.route('/LabBookingReq',methods=['GET'])
#page for booking requests this will show
#all request for lab booking
def lab_booking():
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT u_name,req_id, room_no,registration_date,start_date, end_date, slot_1,
              slot_2, slot_3, slot_4, slot_5,admin_confirmation
               from lab_booking_request""")
        data = cursor.fetchall()
        return render_template('LabBookingReq.html', data=data)

@app.route('/lab_confirmation',methods=['GET','POST'])
#admin confirmations or discarding information will be
#sent to user through email
def lab_feedback():
    reply = request.args['query']
    user_name = request.args['name']
    email = request.args['email']
    room_name = request.args['room_name']
    start_date = request.args['start_date']
    end_date = request.args['end_date']
    time_range = request.args['time_range']
    time_slot = request.args['time_slot']
    req_id=request.args['reqid']
    req_id_f=int(req_id)
    print(req_id_f)
    confirmed = ""
    if reply.lower() == "yes":
        reply = 1
        confirmed = "confirmed"
    else:
        reply = 0
        confirmed = "not confirmed"
    if (end_date != "Not Applicable"):
        msg_body = "Dear " + user_name + "\n" \
                    "Your booking request for Lab " + room_name + " is " + confirmed + ".\n\n" \
                    "Your booking booking details :\n" \
                    "Start Date : " + start_date + "\n" \
                    "End Date : " + end_date + "\n" \
                    "Time Range : " + time_range + "\n" \
                    "Slot Numbers : " + time_slot + "\n"
    else:
        msg_body = "Dear " + user_name + "\n" \
                   "Your booking request for Lab " + room_name + " is " + confirmed + ".\n\n" \
                    "Your booking booking details :\n" \
                    "Date : " + start_date + "\n" \
                    "Time Range : " + time_range + "\n" \
                                                                                                                                                                           "Slot Numbers : " + time_slot + "\n"
    msg_body = msg_body + "\nWith Regards\nDU Online Booking System\nFor any query visit https://www.du.ac.bd"
    print(msg_body)
    mailThread = Thread(target=send_mail, args=(msg_body, email))
    mailThread.start()
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        cursor.execute("""UPDATE lab_booking_request 
                          SET admin_confirmation = %s WHERE u_id = %s"""
                            ,(reply,req_id_f,))
        conn.commit()
        return "Success"
    except Exception as e:
        print(e)
        return "Error"


#Auditorium Booking Request
@app.route('/AuditoriumBookingReq',methods=['GET'])
#page for booking requests this will show
#all request for auditorium booking
def auditorium_booking():
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT Username,req_id,Auditorium,ApplyDate,Date,Status from Auditorium_Data")
        data = cursor.fetchall()
        return render_template('AuditoriumBookingReq.html', data=data)


@app.route('/audi_payment_image',methods=['GET','POST'])
#payment image for auditorium will sent to admin
def audi_payment_image():
    req_id=request.args["query"]
    conn = mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT payment from Auditorium_Data WHERE req_id= (%s)",(req_id,))
    data=cursor.fetchone()
    return data[0]


@app.route('/auditorium_confirmation',methods=['GET','POST'])
#admins reply for auditorium booking confirmation
#reply would be send to customer through email
def auditorium_feedback():
    reply=request.args['query']
    user_name=request.args['name']
    email=request.args['email']
    room_name=request.args['room_name']
    start_date=request.args['start_date']

    print(user_name+email+start_date)
    req_id=request.args['req_id']
    req_id_f=int(req_id)
    confirmed=""
    if reply.lower()=="yes":
        reply="Booked"
        confirmed="confirmed"
    else:
        confirmed="not confirmed"

    msg_body = "Dear " + user_name + "\n" \
                "Your booking request for Auditorium " + room_name + " is " + confirmed + ".\n\n" \
                "Your booking booking details :\n" \
                "Date : " + start_date + "\n\nWith Regards\n DU Online Booking System\nFor any query visit https://www.du.ac.bd"
    mailThread=Thread(target=send_mail,args=(msg_body,email))
    mailThread.start()
    conn = mysql.connect()
    cursor = conn.cursor()
    if reply=="Booked":
        try:
            cursor.execute("""UPDATE Auditorium_Data 
                              SET status = %s WHERE req_id = %s"""
                           , (reply, req_id_f,))
            conn.commit()
            return "Success"
        except Exception as e:
            print(e)
            return "Error"
    else:
        try:
            cursor.execute("""DELETE FROM Auditorium_Data 
                              WHERE req_id = %s"""
                           , (req_id_f,))
            conn.commit()
            return "Success"
        except Exception as e:
            print(e)
            return "Error"


#Field Booking Request
@app.route('/FieldBookingReq',methods=['GET'])
#page for booking requests this will show
#all request for field booking
def field_booking():
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT Username,req_id,Field,ApplyDate,Date,Status from Field_Data")
        data = cursor.fetchall()
        return render_template('FieldBookingReq.html', data=data)

#payment image will shown to admin
@app.route('/field_payment_image',methods=['GET','POST'])
def field_payment_image():
    req_id=request.args["query"]
    conn = mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT payment from Field_Data WHERE req_id= (%s)",(req_id,))
    data=cursor.fetchone()
    return data[0]

@app.route('/field_confirmation',methods=['GET','POST'])
#admins reply for field booking confirmation
#reply would be send to customer through email
def field_feedback():
    reply=request.args['query']
    user_name=request.args['name']
    email=request.args['email']
    room_name=request.args['room_name']
    start_date=request.args['start_date']

    req_id=request.args['req_id']
    req_id_f=int(req_id)
    confirmed=""
    if reply.lower()=="yes":
        reply="Booked"
        confirmed="confirmed"
    else:
        confirmed="not confirmed"

    msg_body = "Dear " + user_name + "\n" \
                "Your booking request for Auditorium " + room_name + " is " + confirmed + ".\n\n" \
                "Your booking booking details :\n" \
                "Date : " + start_date + "\n\nWith Regards\n DU Online Booking System\nFor any query visit https://www.du.ac.bd"
    mailThread=Thread(target=send_mail,args=(msg_body,email))
    mailThread.start()
    conn = mysql.connect()
    cursor = conn.cursor()
    if reply=="Booked":
        try:
            cursor.execute("""UPDATE Field_Data 
                              SET status = %s WHERE req_id = %s"""
                           , (reply, req_id_f,))
            conn.commit()
            return "Success"
        except Exception as e:
            print(e)
            return "Error"
    else:
        try:
            cursor.execute("""DELETE FROM Field_Data 
                              WHERE req_id = %s"""
                           , (req_id_f,))
            conn.commit()
            return "Success"
        except Exception as e:
            print(e)
            return "Error"


#Class update method
@app.route('/ClassUpdate',methods=['GET'])
#all available classes would be shown
def class_info():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT room_name,capacity from class_info")
    data = cursor.fetchall()
    return render_template('ClassUpdate.html', data=data)

@app.route('/class_delete')
#admin can delete classroom
def class_delete():
    name=request.args["name"]
    print(name)
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        cursor.execute("""DELETE FROM class_info 
                          WHERE room_name = %s"""
                       , (name,))
        conn.commit()
        return "Success"
    except Exception as e:
        return "Error"


@app.route('/class_update_data',methods=['GET'])
#admin can update class info
def class_update():
    old_name=request.args['old_name']
    new_name=request.args['new_name']
    capacity=request.args['capacity']
    conn = mysql.connect()
    cursor = conn.cursor()
    print(old_name+" "+new_name+" "+capacity)

    try:
        cursor.execute("UPDATE class_info SET room_name=%s,capacity=%s WHERE room_name=%s",
                       (new_name, capacity, old_name))
        conn.commit()
    except Exception as e:
        return "error"
    return "success"
@app.route('/class_insert_data',methods=['GET'])
#admin can add new class
def class_insert():
    new_name=request.args['new_name']
    capacity=request.args['capacity']
    conn = mysql.connect()
    cursor = conn.cursor()

    try:
        #TODO: dept name should be replaced by sessions dept name
        cursor.execute("INSERT INTO class_info (room_name,capacity,dept_name) VALUES (%s,%s,%s)",
                       (new_name, capacity,"CSE",))
        conn.commit()
    except Exception as e:
        return "error"
    return "success"

@app.route('/LabUpdate',methods=['GET'])
#all available lab will shown
def lab_info():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT room_name,capacity from lab_info")
    data = cursor.fetchall()
    return render_template('LabUpdate.html', data=data)

@app.route('/lab_delete')
#delete any lab
def lab_delete():
    name=request.args["name"]
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        cursor.execute("""DELETE FROM lab_info 
                          WHERE room_name = %s"""
                       , (name,))
        conn.commit()
        return "Success"
    except Exception as e:
        return "Error"


@app.route('/lab_update_data',methods=['GET'])
#admin can update lab info
def lab_update():
    old_name=request.args['old_name']
    new_name=request.args['new_name']
    capacity=request.args['capacity']
    conn = mysql.connect()
    cursor = conn.cursor()

    try:
        cursor.execute("UPDATE lab_info SET room_name=%s,capacity=%s WHERE room_name=%s",
                       (new_name, capacity, old_name))
        conn.commit()
    except Exception as e:
        return "error"
    return "success"

@app.route('/lab_insert_data',methods=['GET'])
#admin can add lab
def lab_insert():
    new_name=request.args['new_name']
    capacity=request.args['capacity']
    conn = mysql.connect()
    cursor = conn.cursor()

    try:
        #TODO: dept name should be replaced by sessions dept name
        cursor.execute("INSERT INTO lab_info (room_name,capacity,dept_name) VALUES (%s,%s,%s)",
                       (new_name, capacity,"CSE",))
        conn.commit()
    except Exception as e:
        return "error"
    return "success"



#Munna
today_date = str(date.today())
@app.route('/classRoomBooking', methods=["GET", "POST"])
def showClassSlot():
    res= classBook(self=1)
    today = str(date.today())
    session['today_date']=today
    return res



@app.route('/classRoomFixedDate', methods=["GET", "POST"])
def showClassSlotOnFixedDate():
    conn = mysql.connect()
    cursor = conn.cursor()
    print("Successfully connected")

    today = request.args['query']
    session['today_date'] = today

    return "0"

today_date1 = str(date.today())
@app.route('/labBooking', methods=["GET","POST"])
def showLabSlot():
    res= showLabStatus(self=1)
    today = str(date.today())
    session['today_date1'] = today
    return res

@app.route('/labFixedDate', methods=["GET", "POST"])
def showLabSlotOnFixedDate():
    conn = mysql.connect()
    cursor = conn.cursor()
    print ("Successfully connected")

    today = request.args['query']
    session['today_date1']=today

    return "1"



if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=5000)
