import base64
import time
from datetime import datetime, date
from json import dumps

from flask import Flask, render_template, request, session, make_response

username = "Guest"


class profile_class:
    def __init__(self, mysql):
        self.mysql = mysql

    def view_profile(self):
        accepted = 0
        process = 0
        date_current = str(date.today())
        username = session['username']
        # date_current ="2018-04-04"
        conn = self.mysql.connect()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT  room_no,registration_date,start_date,end_date,admin_confirmation FROM   class_booking_request WHERE u_name = %s",
            (username,))

        dataC = cursor.fetchall()
        for row in dataC:
            if row[4]==1:
                accepted = accepted + 1
            elif  row[4]==0 :
                process = process + 1

        clas = len(dataC)

        cursor.execute(
            "SELECT  room_no,registration_date,start_date,end_date,admin_confirmation FROM   lab_booking_request WHERE u_name = %s",
            (username,))

        dataL = cursor.fetchall()
        for row in dataL:
            if row[4] == 1:
                accepted = accepted + 1
            elif row[4] == 0:
                process = process + 1

        lab = len(dataL)

        cursor.execute(
            "SELECT  Auditorium,Status,Date FROM   Auditorium_Table WHERE Username = %s",
            (username,))

        dataA = cursor.fetchall()
        for row in dataA:
            if row[1] == "Booked":
                accepted = accepted + 1
            else:
                process = process + 1

        Aud = len(dataA)

        cursor.execute(
            "SELECT  Field,Status,Date FROM   Field_Table WHERE Username = %s",
            (username,))
        dataF = cursor.fetchall()
        for row in dataF:
            if row[1] == "Booked":
                accepted = accepted + 1
            else:
                process = process + 1
        Fild = len(dataF)
        cursor.execute(
            "SELECT  username,email,phone,dept FROM   Registration WHERE Username = %s",
            (username,))
        dataP = cursor.fetchall()
        dataNum = [Aud, Fild, accepted, process,clas,lab]

        return render_template('user_profile.html', dataA=dataA, dataF=dataF, dataP=dataP, dataNum=dataNum,dataC=dataC,dataL=dataL)
        # return render_template('profile.html')


