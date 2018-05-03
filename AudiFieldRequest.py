from json import dumps
from flask import Flask, render_template, request, flash, session, url_for, redirect, jsonify, make_response, json
from ConfirmationMail import send_mail
from threading import Thread

class AuditoriumBookingReq:
    def __init__(self,mysql):
        self.mysql=mysql

    def auditorium_booking(self):
        try:
            user_name=session['username']
        except:
            return redirect(url_for('login'))
        conn = self.mysql.connect()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT Username,req_id,Auditorium,ApplyDate,Date,Status from Auditorium_Table")
        data = cursor.fetchall()
        return render_template('AuditoriumBookingReq.html', data=data,user_name=user_name)

    def audi_payment_image(self):
        req_id = request.args["query"]
        conn = self.mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT Payment from Auditorium_Table WHERE req_id= (%s)", (req_id,))
        data = cursor.fetchone()
        return data[0]

    def auditorium_feedback(self):
        reply = request.args['query']
        user_name = request.args['name']
        email = request.args['email']
        room_name = request.args['room_name']
        start_date = request.args['start_date']

        print(user_name + email + start_date)
        req_id = request.args['req_id']
        req_id_f = int(req_id)
        confirmed = ""
        if reply.lower() == "yes":
            reply = "Booked"
            confirmed = "confirmed"
        else:
            confirmed = "not confirmed"

        msg_body = "Dear " + user_name + "\n" \
                    "Your booking request for Auditorium " + room_name + " is " + confirmed + ".\n\n" \
                    "Your booking booking details :\n" \
                    "Date : " + start_date + "\n\nWith Regards\n DU Online Booking System\nFor any query visit https://www.du.ac.bd"
        mailThread = Thread(target=send_mail, args=(msg_body, email))
        mailThread.start()
        conn = self.mysql.connect()
        cursor = conn.cursor()
        if reply == "Booked":
            try:
                cursor.execute("""UPDATE Auditorium_Table 
                                  SET status = %s WHERE req_id = %s"""
                               , (reply, req_id_f,))
                conn.commit()
                return "Success"
            except Exception as e:
                print(e)
                return "Error"
        else:
            try:
                cursor.execute("""DELETE FROM Auditorium_Table 
                                  WHERE req_id = %s"""
                               , (req_id_f,))
                conn.commit()
                return "Success"
            except Exception as e:
                print(e)
                return "Error"

class FieldBookingReq:
    def __init__(self,mysql):
        self.mysql=mysql

    def field_booking(self):
        try:
            user_name=session['username']
        except:
            return redirect(url_for('login'))
        conn = self.mysql.connect()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT Username,req_id,Field,ApplyDate,Date,Status from Field_Table")
        data = cursor.fetchall()
        return render_template('FieldBookingReq.html', data=data,user_name=user_name)

    def field_payment_image(self):
        req_id = request.args["query"]
        conn = self.mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT Payment from Field_Table WHERE req_id= (%s)", (req_id,))
        data = cursor.fetchone()
        return data[0]

    def field_feedback(self):
        reply = request.args['query']
        user_name = request.args['name']
        email = request.args['email']
        room_name = request.args['room_name']
        start_date = request.args['start_date']

        req_id = request.args['req_id']
        req_id_f = int(req_id)
        confirmed = ""
        if reply.lower() == "yes":
            reply = "Booked"
            confirmed = "confirmed"
        else:
            confirmed = "not confirmed"

        msg_body = "Dear " + user_name + "\n" \
                    "Your booking request for Auditorium " + room_name + " is " + confirmed + ".\n\n" \
                    "Your booking booking details :\n" \
                    "Date : " + start_date + "\n\nWith Regards\n DU Online Booking System\nFor any query visit https://www.du.ac.bd"
        mailThread = Thread(target=send_mail, args=(msg_body, email))
        mailThread.start()
        conn = self.mysql.connect()
        cursor = conn.cursor()
        if reply == "Booked":
            try:
                cursor.execute("""UPDATE Field_Table 
                                  SET status = %s WHERE req_id = %s"""
                               , (reply, req_id_f,))
                conn.commit()
                return "Success"
            except Exception as e:
                print(e)
                return "Error"
        else:
            try:
                cursor.execute("""DELETE FROM Field_Table 
                                  WHERE req_id = %s"""
                               , (req_id_f,))
                conn.commit()
                return "Success"
            except Exception as e:
                print(e)
                return "Error"
