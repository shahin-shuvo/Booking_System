import base64
import time
from datetime import datetime, date
from json import dumps

from flask import Flask, render_template, request, session, make_response

username = "Guest"


class field_class:
    def __init__(self, mysql):
        self.mysql = mysql

    def field_final(self):
        date_current = str(date.today())
        session['date_field'] = date_current
        # date_current ="2018-04-04"
        conn = self.mysql.connect()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT  Field_Info.Name, Field_Table.Status FROM Field_Info LEFT OUTER JOIN  Field_Table  ON Field_Info.Name=Field_Table.Field AND Field_Table.Date= %s ORDER BY Field_Info.Name DESC",
            (date_current,))

        data = cursor.fetchall()
        print(data)
        if 'logged_in' in session:
            username = session['username']
        else:
            username = "Guest"
        return render_template("field_main.html", data=data, username=username, date=date_current)

    def field_query(self):
        # initialize
        date_current = request.args['query']
        if (date_current == ""):
            date_current = str(date.today())
        session['date_field'] = date_current
        conn = self.mysql.connect()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT  Field_Info.Name, Field_Table.Status FROM Field_Info LEFT OUTER JOIN  Field_Table  ON Field_Info.Name=Field_Table.Field AND Field_Table.Date= %s ORDER BY Field_Info.Name ASC",
            (date_current,))

        data = cursor.fetchall()
        print(data)
        return make_response(dumps(data))

    def field_book_helper(self):
        try:
            field = request.args['query']
            session['field_applied'] = field
            print(field)
            return "0"
        except Exception as e:
            return "1"

    def field_book(self):
        # initialize
        status = "Already Applied"
        field = session['field_applied']
        file = request.args['query2']
        date_apply = session['date_field']
        username = session['username']
        print(field)
        print(date_apply)
        print(username)
        conn = self.mysql.connect()
        cursor = conn.cursor()
        try:
            with open('/home/shuvo/Pictures/' + file, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
            cursor.execute(
                "INSERT INTO Field_Table (Field,Date,Status,Payment,Username,Applydate) VALUES (%s, %s, %s,  %s, %s, %s)",
                (field, date_apply, status, encoded_string, username, date_apply))
            # x.execute("UPDATE Auditorium_table SET Status = %s WHERE username = %s",(table,username,))
            conn.commit()
            conn.close()
            return "0"

        except Exception as e:
            return "1"