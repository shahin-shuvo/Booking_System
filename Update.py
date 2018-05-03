from flask import render_template, request,session,redirect,url_for


class ClassUpdate:
    def __init__(self,mysql):
        self.mysql=mysql

    def class_info(self):
        try:
            user_name=session['username']
        except:
            return redirect(url_for('login'))
        conn = self.mysql.connect()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT room_name,capacity from class_info")
        data = cursor.fetchall()
        return render_template('ClassUpdate.html', data=data,user_name=user_name)

    def class_delete(self):
        name = request.args["name"]
        print(name)
        conn = self.mysql.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("""DELETE FROM class_info 
                              WHERE room_name = %s"""
                           , (name,))
            conn.commit()
            return "Success"
        except Exception as e:
            return "Error"

    def class_update(self):
        old_name = request.args['old_name']
        new_name = request.args['new_name']
        capacity = request.args['capacity']
        conn = self.mysql.connect()
        cursor = conn.cursor()
        print(old_name + " " + new_name + " " + capacity)

        try:
            cursor.execute("UPDATE class_info SET room_name=%s,capacity=%s WHERE room_name=%s",
                           (new_name, capacity, old_name))
            conn.commit()
        except Exception as e:
            return "error"
        return "success"

    def class_insert(self):
        new_name = request.args['new_name']
        capacity = request.args['capacity']
        conn = self.mysql.connect()
        cursor = conn.cursor()

        try:
            # TODO: dept name should be replaced by sessions dept name
            cursor.execute("INSERT INTO class_info (room_name,capacity,dept_name) VALUES (%s,%s,%s)",
                           (new_name, capacity, "CSE",))
            conn.commit()
        except Exception as e:
            return "error"
        return "success"


class LabUpdate:
    def __init__(self,mysql):
        self.mysql=mysql

    def lab_info(self):
        try:
            user_name=session['username']
        except:
            return redirect(url_for('login'))
        conn = self.mysql.connect()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT room_name,capacity from lab_info")
        data = cursor.fetchall()
        return render_template('LabUpdate.html', data=data,user_name=user_name)

    def lab_delete(self):
        name = request.args["name"]
        conn = self.mysql.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("""DELETE FROM lab_info 
                              WHERE room_name = %s"""
                           , (name,))
            conn.commit()
            return "Success"
        except Exception as e:
            return "Error"

    def lab_update(self):
        old_name = request.args['old_name']
        new_name = request.args['new_name']
        capacity = request.args['capacity']
        conn = self.mysql.connect()
        cursor = conn.cursor()

        try:
            cursor.execute("UPDATE lab_info SET room_name=%s,capacity=%s WHERE room_name=%s",
                           (new_name, capacity, old_name))
            conn.commit()
        except Exception as e:
            return "error"
        return "success"

    def lab_insert(self):
        new_name = request.args['new_name']
        capacity = request.args['capacity']
        conn = self.mysql.connect()
        cursor = conn.cursor()

        try:
            # TODO: dept name should be replaced by sessions dept name
            cursor.execute("INSERT INTO lab_info (room_name,capacity,dept_name) VALUES (%s,%s,%s)",
                           (new_name, capacity, "CSE",))
            conn.commit()
        except Exception as e:
            return "error"
        return "success"


class AuditoriumUpdate:
    def __init__(self,mysql):
        self.mysql=mysql

    def auditorium_info(self):
        try:
            user_name=session['username']
        except:
            return redirect(url_for('login'))
        conn = self.mysql.connect()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * from Auditorium_Info")
        data = cursor.fetchall()
        return render_template('AuditoriumUpdate.html', data=data,user_name=user_name)

    def auditorium_delete(self):
        name = request.args["name"]
        print(name)
        conn = self.mysql.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("""DELETE FROM Auditorium_Info 
                              WHERE Name = %s"""
                           , (name,))
            conn.commit()
            return "Success"
        except Exception as e:
            return "Error"

    def auditorium_update(self):
        old_name = request.args['old_name']
        new_name = request.args['new_name']

        address=request.args['address']
        capacity = request.args['capacity']
        details=request.args['details']
        conn = self.mysql.connect()
        cursor = conn.cursor()
        print(old_name + " " + new_name + " " + capacity)

        try:
            cursor.execute("UPDATE Auditorium_Info SET Name=%s,Address=%s,Capacity=%s,Details=%s WHERE Name=%s",
                           (new_name,address,capacity,details,old_name))
            conn.commit()
        except Exception as e:
            return "error"
        return "success"

    def auditorium_insert(self):
        new_name = request.args['new_name']
        address= request.args['address']
        details=request.args['details']
        capacity = request.args['capacity']
        conn = self.mysql.connect()
        cursor = conn.cursor()
        print(new_name+address+details+capacity)
        try:
            cursor.execute("INSERT INTO Auditorium_Info (Name,Address,Capacity,Details) VALUES (%s,%s,%s,%s)",
                           (new_name, address,capacity,details,))
            conn.commit()
        except Exception as e:
            return "error"
        return "success"

class FieldUpdate:
    def __init__(self,mysql):
        self.mysql=mysql

    def field_info(self):
        try:
            user_name=session['username']
        except:
            return redirect(url_for('login'))

        conn = self.mysql.connect()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * from Field_Info")
        data = cursor.fetchall()
        return render_template('FieldUpdate.html', data=data,user_name=user_name)

    def field_delete(self):
        name = request.args["name"]
        print(name)
        conn = self.mysql.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("""DELETE FROM Field_Info 
                              WHERE Name = %s"""
                           , (name,))
            conn.commit()
            return "Success"
        except Exception as e:
            return "Error"

    def field_update(self):
        old_name = request.args['old_name']
        new_name = request.args['new_name']

        address=request.args['address']
        capacity = request.args['capacity']
        details=request.args['details']
        conn = self.mysql.connect()
        cursor = conn.cursor()
        print(old_name + " " + new_name + " " + capacity)

        try:
            cursor.execute("UPDATE Field_Info SET Name=%s,Address=%s,Capacity=%s,Details=%s WHERE Name=%s",
                           (new_name,address,capacity,details,old_name))
            conn.commit()
        except Exception as e:
            return "error"
        return "success"

    def field_insert(self):
        new_name = request.args['new_name']
        address= request.args['address']
        details=request.args['details']
        capacity = request.args['capacity']
        conn = self.mysql.connect()
        cursor = conn.cursor()
        print(new_name+address+details+capacity)
        try:
            cursor.execute("INSERT INTO Field_Info (Name,Address,Capacity,Details) VALUES (%s,%s,%s,%s)",
                           (new_name, address,capacity,details,))
            conn.commit()
        except Exception as e:
            return "error"
        return "success"

