from flask import render_template

admin_img='../static/img/admin/'
def img_link(name):
    name=name.lower()
    link= admin_img+name+'.jpg'
    return link

class Login:
    def login(self):
        return render_template('login.html')