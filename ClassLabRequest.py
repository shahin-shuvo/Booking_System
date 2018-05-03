from json import dumps
from flask import render_template, request,make_response,session,redirect,url_for
from dateutil import parser
from UtilityClass import img_link

class ClassBookingReq:
    def __init__(self,mysql):
        self.mysql=mysql

    def class_booking(self):
        try:
            user_name=session['username']
        except:
            return redirect(url_for('login'))
        conn = self.mysql.connect()
        cursor = conn.cursor()
        cursor.execute("""SELECT u_name,req_id, room_no,registration_date,start_date, 
                          end_date, slot_1, slot_2, slot_3, slot_4, slot_5,admin_confirmation 
                          from class_booking_request""")
        data = cursor.fetchall()
        return render_template('ClassBookingReq.html', data=data,user_name=user_name,admin_image_link=img_link(user_name))

    def feedback(self):
        reply = request.args['query']
        user_name = request.args['name']
        email = request.args['email']
        room_name = request.args['room_name']
        start_date = request.args['start_date']
        end_date = request.args['end_date']
        time_range = request.args['time_range']
        time_slot = request.args['time_slot']

        requested_date=str(parser.parse(start_date)).split(" ")[0]
        print(requested_date + time_range+room_name)
        req_id = request.args['reqid']
        req_id_f = int(req_id)
        confirmed = ""
        r_slot = time_slot.split(",")

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
        # mailThread = Thread(target=send_mail, args=(msg_body, email))
        # mailThread.start()

        print("Request id " + str(req_id_f))
        print(msg_body)
        conn = self.mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM classRoomTable WHERE room_no = %s AND date_date = %s",(room_name,requested_date,))
        data=cursor.fetchall()



        slots=[]
        for i in range(5):
            slots.append(data[0][2+i])
        # print(slots)
        if(reply==1):
            for i in r_slot:
                slots[int(i)-1]='0'
        elif(reply==0):
            for i in r_slot:
                slots[int(i)-1]='2'


        # print(slots)
        try:
            cursor.execute("""UPDATE class_booking_request 
                              SET admin_confirmation = %s WHERE req_id = %s"""
                           , (reply, req_id_f,))
            cursor.execute("""UPDATE classRoomTable SET s1 = %s,s2 = %s,s3 = %s ,s4=%s,s5 = %s
                              WHERE room_no = %s AND date_date = %s""",
                              (slots[0],slots[1],slots[2],slots[3],slots[4],room_name,requested_date,))
            conn.commit()
            return "Success"
        except Exception as e:
            print(e)
            return "Error"


class LabBookingReq:
    def __init__(self,mysql):
        self.mysql=mysql

    def lab_booking(self):
        try:
            user_name=session['username']
        except:
            return redirect(url_for('login'))
        conn = self.mysql.connect()
        cursor = conn.cursor()
        cursor.execute(
            """SELECT u_name,req_id, room_no,registration_date,start_date, end_date, slot_1,
              slot_2,admin_confirmation
               from lab_booking_request""")
        data = cursor.fetchall()
        return render_template('LabBookingReq.html', data=data,user_name=user_name,admin_image_link=img_link(user_name))

    def lab_feedback(self):
        reply = request.args['query']
        user_name = request.args['name']
        email = request.args['email']
        room_name = request.args['room_name']
        start_date = request.args['start_date']
        end_date = request.args['end_date']
        time_range = request.args['time_range']
        time_slot = request.args['time_slot']

        requested_date = str(parser.parse(start_date)).split(" ")[0]

        req_id = request.args['reqid']
        req_id_f = int(req_id)
        print(req_id_f)
        confirmed = ""

        r_slot = time_slot.split(",")

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
        # mailThread = Thread(target=send_mail, args=(msg_body, email))
        # mailThread.start()
        conn = self.mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM LabTable WHERE labNo = %s AND date_date = %s",
                       (room_name, requested_date,))
        data = cursor.fetchall()
        print(room_name+requested_date)
        print(time_slot)
        slots = []
        for i in range(2):
            slots.append(data[0][2 + i])
        # print(slots)
        if (reply == 1):
            for i in r_slot:
                slots[int(i) - 1] = '0'
        elif (reply == 0):
            for i in r_slot:
                slots[int(i) - 1] = '2'

        # print(slots)
        try:
            cursor.execute("""UPDATE lab_booking_request 
                                      SET admin_confirmation = %s WHERE req_id = %s"""
                           , (reply, req_id_f,))
            cursor.execute("""UPDATE LabTable SET s1 = %s,s2 = %s
                                      WHERE labNo = %s AND date_date = %s""",
                           (slots[0], slots[1], room_name, requested_date,))
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