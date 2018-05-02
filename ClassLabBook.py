from datetime import date

from flask import Flask, render_template, request, session

class classBookingClass:
    def __init__(self,mysql):
        self.mysql=mysql

    def showClassSlot(self):
        conn = self.mysql.connect()
        cursor = conn.cursor()

        today = ""
        try:
            today = session['today_date']
        except KeyError:
            print("Not Found")

        #today = "'" + today + "'"

        # for selecting the desired date data

        cursor.execute("SELECT * FROM classRoomTable WHERE date_date=%s",(today,))
        slotData = cursor.fetchall()

        # fetch all the room no

        cursor.execute("SELECT room_name FROM class_info WHERE dept_name='CSE'")
        classRoomNoData = cursor.fetchall()

        # fetch the number of class slots
        cursor.execute("SELECT slot FROM classSlotTable")
        numberOfSlot = cursor.fetchall()

        length = len(classRoomNoData)

        limit = len(slotData)

        totalSlots = len(numberOfSlot)

        foundClassRoomArray = [0] * length

        finalData = []

        classRoomNo = [0] * length

        # copy the classRoom no
        for i in range(length):
            classRoomNo[i] = str(classRoomNoData[i][0])

        # copy the class room no based on the selected date
        for i in range(limit):
            #foundClassRoomArray[i] = int(slotData[i][0])
            foundClassRoomArray[i] = slotData[i][0]

        #foundClassRoomArray.sort()

        selectDateData = []

        # append the selected date data based on the selected date
        for i in range(limit):
            selectDateData.append(slotData[i])

        # this part is for those which are fully free on the selected date
        for i in range(len(classRoomNo)):
            flag = 0
            for j in range(len(foundClassRoomArray)):
                if (classRoomNo[i] == foundClassRoomArray[j]):
                    flag = 0
                    break
                else:
                    flag = 1

            if (flag == 1):
                finalData = [classRoomNo[i], today]
                for k in range(totalSlots):
                    finalData.append("2")
                selectDateData.append(finalData)

        classSlots = []

        # this part is for the class slots
        for i in range(totalSlots):
            classSlots.append(numberOfSlot[i][0])

        # print ("data: ", len(numberOfSlot))
        # print ("fnd class room: ", foundClassRoomArray)
        print ("slot: ", selectDateData)

        today_class_date = str(date.today())
        session['today_date'] = today_class_date

        conn.close()
        return render_template('classRoomBooking.html', demoData=selectDateData, data=numberOfSlot)

    def showClassSlotOnFixedDate(self):
        today = request.args['query']
        session['today_date'] = today

        return "0"


class labBookingClass:
    def __init__(self,mysql):
        self.mysql=mysql

    def showLabStatus(self):
        conn = self.mysql.connect()
        cursor = conn.cursor()

        today = ""
        try:
            today = session['today_date1']
        except KeyError:
            print("Not Found")

        #today = "'" + today + "'"

        cursor.execute("SELECT * FROM LabTable WHERE date_date=%s", (today,))
        # cursorClassSlot = conn.execute("SELECT * FROM LabTable")
        slotData = cursor.fetchall()

        cursor.execute("SELECT * FROM LabNoTable")
        labRoomNoData = cursor.fetchall()

        # fetch the number of lab slots
        cursor.execute("SELECT slot FROM labSlotTable")
        numberOfSlot = cursor.fetchall()

        length = len(labRoomNoData)

        totalSlots = len(numberOfSlot)

        limit = len(slotData)

        foundLabRoomArray = [0] * length

        finalData = []

        labRoomNo = [0] * length

        # copy the classRoom no
        for i in range(length):
            labRoomNo[i] = int(labRoomNoData[i][0])

        for i in range(limit):
            foundLabRoomArray[i] = int(slotData[i][0])

        k = 0
        selectDateData = []

        for i in range(limit):
            selectDateData.append(slotData[i])

        # this part is for those which are fully free on the selected date
        for i in range(len(labRoomNo)):
            flag = 0
            for j in range(len(foundLabRoomArray)):
                if (labRoomNo[i] == foundLabRoomArray[j]):
                    flag = 0
                    break
                else:
                    flag = 1

            if (flag == 1):
                finalData = [labRoomNo[i], today]
                for k in range(totalSlots):
                    finalData.append('2')
                selectDateData.append(finalData)

        labSlots = []

        # this part is for the class slots
        for i in range(totalSlots):
            labSlots.append(numberOfSlot[i][0])

        # print ("data: ", labRoomNo)
        # print ("fnd class room: ", foundLabRoomArray)
        print("slot: ", selectDateData)

        todayLabDate = str(date.today())
        session['today_date1'] = todayLabDate

        # print ("lab Data: ", labData)
        conn.close()

        return render_template('labBooking.html', demoData=selectDateData, data=numberOfSlot)


    def showLabSlotOnFixedDate(self):
        today = request.args['query']
        session['today_date1'] = today

        return "1"
