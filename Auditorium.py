import base64
import time
from datetime import datetime, date
from json import dumps

from flask import Flask, render_template, request, session, make_response

username = "Guest"


class auditorium_book_class:
    def __init__(self, mysql):
        self.mysql = mysql

    def auditorium_final(self):
        date_current = str(date.today())
        session['date'] = date_current
        # date_current ="2018-04-04"
        conn = self.mysql.connect()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT  Auditorium_Info.Name, Auditorium_Table.Status FROM Auditorium_Info LEFT OUTER JOIN  Auditorium_Table  ON Auditorium_Info.Name=Auditorium_Table.Auditorium AND Auditorium_Table.Date= %s ORDER BY Auditorium_Info.Name DESC",
            (date_current,))

        data = cursor.fetchall()
        print(data)
        if 'logged_in' in session:
            username = session['username']
        else:
            username = "Guest"
        return render_template("auditorium_main.html", data=data, username=username, date=date_current)

    def auditorium_query(self):
        # initialize
        date_current = request.args['query']
        if (date_current == ""):
            date_current = str(date.today())
        session['date'] = date_current
        conn = self.mysql.connect()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT  Auditorium_Info.Name, Auditorium_Table.Status FROM Auditorium_Info LEFT OUTER JOIN  Auditorium_Table  ON Auditorium_Info.Name=Auditorium_Table.Auditorium AND Auditorium_Table.Date= %s  ORDER BY Auditorium_Info.Name ASC",
            (date_current,))
        data = cursor.fetchall()
        print(data)
        return make_response(dumps(data))

    def auditorium_book_helper(self):
        try:
            auditorium = request.args['query']
            session['auditorium_applied'] = auditorium
            print(auditorium)
            return "0"
        except Exception as e:
            return "1"

    def auditorium_book(self):
        # initialize
        status = "Already Applied"
        auditorium = session['auditorium_applied']
        file = request.args['query2']
        date_apply = session['date']
        username = session['username']
        print(auditorium)
        print(date_apply)
        print(username)
        conn = self.mysql.connect()
        cursor = conn.cursor()
        try:
            with open('/home/shuvo/Pictures/' + file, "rb") as image_file:
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