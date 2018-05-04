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


class Login_Class:
    def __init__(self, mysql):
        self.mysql = mysql

    def login_helper(self):
        error = ''
        try:
            query = request.args['query']
            query = json.loads(query)
            conn = self.mysql.connect()
            c = conn.cursor()
            print(query[0])
            print(query[1])
            if query[2] == "ADMIN":
                data = c.execute("SELECT * FROM Admin WHERE username = (%s) AND password = (%s)",
                                 (query[0], query[1]))
                if int(data) > 0:
                    session['logged_in'] = True
                    session['username'] = query[0]
                    gc.collect()
                    return "OK_Admin"
            elif query[2] == "USER":
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

    def login_user(self):
        error = ''
        try:
            query = request.args['query']
            query = json.loads(query)
            conn = self.mysql.connect()
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