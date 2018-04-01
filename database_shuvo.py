from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '$huvo919671'
app.config['MYSQL_DB'] = "Du_Booking_Data"
mysql = MySQL(app)


@app.route('/table')
def table():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM Auditorium_table')
    rv = cur.fetchall()
    return str(rv)



if __name__ == '__main__':
    app.run(debug=True)
