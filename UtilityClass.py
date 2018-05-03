from json import dumps
from flask import render_template, request,make_response,session
from ConfirmationMail import send_mail
from threading import Thread
from dateutil import parser

admin_img='../static/img/admin/'
def img_link(name):
    name=name.lower()
    link= admin_img+name+'.jpg'
    return link

class Login:
    def login(self):
        return render_template('login.html')