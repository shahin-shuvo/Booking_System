import base64
import gc
from functools import wraps
from datetime import date
from json import dumps
from flask import Flask, render_template, request, flash, session, url_for, redirect, jsonify, make_response, json
from flaskext.mysql import MySQL

from jinja2 import Environment
from ClassLabRequest import ClassBookingReq,User,LabBookingReq
from AudiFieldRequest import AuditoriumBookingReq,FieldBookingReq
from Update import *
from ClassLabBook import *
from Pass import DB_PASS

import formencode_jinja2
jinja_env = Environment(extensions=['jinja2.ext.loopcontrols'])
jinja_env.add_extension(formencode_jinja2.formfill)


class Signup_Class:
    def __init__(self, mysql):
        self.mysql = mysql
    def signup_helper(self):
        global logged_in
        try:
            query = request.args['query']
            query = json.loads(query)
            conn = self.mysql.connect()
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