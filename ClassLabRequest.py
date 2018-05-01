from json import dumps
from flask import Flask, render_template, request, flash, session, url_for, redirect, jsonify, make_response, json
from ConfirmationMail import send_mail
from threading import Thread

class ClassBookingReq:
    def __init__(self,mysql):
        self.mysql=mysql

    def class_booking(self):
        conn = self.mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""SELECT u_name,req_id, room_no,registration_date,start_date, 
                          end_date, slot_1, slot_2, slot_3, slot_4, slot_5,admin_confirmation 
                          from class_booking_request""")
        data = cursor.fetchall()
        return render_template('ClassBookingReq.html', data=data)

    def feedback(self):
        reply = request.args['query']
        user_name = request.args['name']
        email = request.args['email']
        room_name = request.args['room_name']
        start_date = request.args['start_date']
        end_date = request.args['end_date']
        time_range = request.args['time_range']
        time_slot = request.args['time_slot']

        print(user_name + email + start_date + end_date + time_range + time_slot)
        req_id = request.args['reqid']
        req_id_f = int(req_id)
        confirmed = ""
        if reply.lower() == "yes":
            reply = 1
            confirmed = "confirmed"
        else:
            reply = 0
            confirmed = "not confirmed"
        if (end_date != "Not Applicable"):
            msg_body = "Dear " + user_name + "\n" \
                        "Your booking request for Room " + room_name + " is " + confirmed + ".\n\n" \
                        "Your booking booking details :\n" \
                        "Start Date : " + start_date + "\n" \
                        "End Date : " + end_date + "\n" \
                        "Time Range : " + time_range + "\n" \
                        "Slot Numbers : " + time_slot + "\n"
        else:
            msg_body = "Dear " + user_name + "\n" \
            "Your booking request for Room " + room_name + " is " + confirmed + ".\n\n" \
            "Your booking booking details :\n" \
            "Date : " + start_date + "\n" \
             "Time Range : " + time_range + "\n" \
            "Slot Numbers : " + time_slot + "\n"
        msg_body = msg_body + "\nWith Regards\nDU Online Booking System\nFor any query visit https://www.du.ac.bd"
        mailThread = Thread(target=send_mail, args=(msg_body, email))
        mailThread.start()

        print("Request id " + str(req_id_f))
        print(msg_body)
        conn = self.mysql.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("""UPDATE class_booking_request 
                              SET admin_confirmation = %s WHERE req_id = %s"""
                           , (reply, req_id_f,))
            conn.commit()
            return "Success"
        except Exception as e:
            print(e)
            return "Error"


class LabBookingReq:
    def __init__(self,mysql):
        self.mysql=mysql

    def lab_booking(self):
        conn = self.mysql.connect()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT u_name,req_id, room_no,registration_date,start_date, end_date, slot_1,
              slot_2, slot_3, slot_4, slot_5,admin_confirmation
               from lab_booking_request""")
        data = cursor.fetchall()
        return render_template('LabBookingReq.html', data=data)

    def lab_feedback(self):
        reply = request.args['query']
        user_name = request.args['name']
        email = request.args['email']
        room_name = request.args['room_name']
        start_date = request.args['start_date']
        end_date = request.args['end_date']
        time_range = request.args['time_range']
        time_slot = request.args['time_slot']
        req_id = request.args['reqid']
        req_id_f = int(req_id)
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
        conn = self.mysql.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("""UPDATE lab_booking_request 
                               SET admin_confirmation = %s WHERE u_id = %s"""
                           , (reply, req_id_f,))
            conn.commit()
            return "Success"
        except Exception as e:
            print(e)
            return "Error"


class User:
    def __init__(self,mysql):
        self.mysql=mysql

    def row_clicked(self):
        table_row = request.args['query']
        conn = self.mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT username,email,phone,dept from Registration WHERE username = (%s)", (table_row,))
        data = cursor.fetchone()
        return make_response(dumps(data))

    def send_image(self):
        name = request.args["query"]
        conn = self.mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT image from Registration WHERE username= (%s)", (name,))
        data = cursor.fetchone()
        return data[0]