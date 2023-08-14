from PyQt5.QtCore import *
from PyQt5 import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QTableWidgetItem
import sys
from PyQt5.uic import loadUiType
import mysql.connector as con
import random
import csv

ui, _ = loadUiType("C:/Users/jnave/OneDrive/Documents/PyQt5/School Management System/school01.ui")

class MainApp(QMainWindow, ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.setFixedSize(1050,800)
        self.setWindowTitle("SMS")
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.tabBar().setVisible(False)
        self.menubar.setVisible(False)
        self.b01.clicked.connect(self.login)

        self.menu11.triggered.connect(self.show_add_new_student_tab)
        self.b12.clicked.connect(self.save_student_details)
        self.menu12.triggered.connect(self.show_delete_update_student)
        self.delete_student.clicked.connect(self.delete_student_details)
        self.edit_student.clicked.connect(self.edit_student_details)
        self.menu21.triggered.connect(self.show_mark_delete_edit_student)
        self.save_mark.clicked.connect(self.save_mark_details)
        self.get_details.clicked.connect(self.load_exam_marks)
        self.edit_mark.clicked.connect(self.edit_mark_details)
        self.menu31.triggered.connect(self.show_attendance_details)
        self.save_attendance.clicked.connect(self.save_attendance_details)
        self.edit_attendance.clicked.connect(self.edit_attendance_details)
        self.delete_attendance.clicked.connect(self.delete_attendance_details)
        self.get_details_2.clicked.connect(self.get_details_attendance)
        self.menu41.triggered.connect(self.show_fees_details)
        self.generate_receipt.clicked.connect(self.generate_receipt_number)
        self.save_fees.clicked.connect(self.save_fees_details)
        self.edit_fees.clicked.connect(self.edit_fees_details)
        self.delete_fees.clicked.connect(self.delete_fees_details)
        self.menu51.triggered.connect(lambda : self.show_report("student"))
        self.menu52.triggered.connect(lambda : self.show_report("mark"))
        self.menu53.triggered.connect(lambda : self.show_report("attendance"))
        self.menu54.triggered.connect(lambda : self.show_report("fees"))
        self.download_type = None
        self.download.clicked.connect(self.get1_download_details)
        self.menu61.triggered.connect(self.logout)
    
    def download_details(self,download_type):
        self.download_type = download_type

    def get1_download_details(self):
        self.get_download_details(self.download_type)
        
        
    ####Login Form information###
    def login(self):
        un = self.tb01.text()
        pw = self.tb02.text()
        if(un == "admin" and pw == "admin"):
            self.menubar.setVisible(True)
            self.tabWidget.setCurrentIndex(1)
        else:
            QMessageBox.information(self,"School Management System","Invalid admin login details, Try again!")
            #self.l01.setText("Invalid admin login details, Try again!")
        self.tb01.setText("")
        self.tb02.setText("")

    def logout(self):
        self.tabWidget.setCurrentIndex(0)
    
    def show_add_new_student_tab(self):
        self.tabWidget.setCurrentIndex(2)
        self.fill_next_registration_number()

    def fill_next_registration_number(self):
        try:
            rn = 0
            mydb = con.connect(host="localhost",user = "root",password="naveeth@097",db = "school")
            cursor = mydb.cursor()
            cursor.execute("select * from student")
            result = cursor.fetchall()
            if(result):
                for stud in result:
                    rn += 1
            self.tb11.setText(str(rn+1))
        except con.Error as e:
            print("Error occured in select student reg number",e)

    def save_student_details(self):
        try:
            mydb = con.connect(host="localhost",user="root",password="naveeth@097",db = "school")
            cursor = mydb.cursor()
            registration_number = self.tb11.text()
            full_name = self.tb12.text()
            gender = self.cb11.currentText()
            dfb = self.tb13.text()
            age = self.tb14.text()
            address = self.tb15.text()
            phone = self.tb16.text()
            email = self.tb17.text()
            classes = self.cb12.currentText()

            qry = "insert into student(registration_number,full_name,gender,date_of_birth,age,Address,phone,email,standard) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            value = (registration_number,full_name,gender,dfb,age,address,phone,email,classes)
            cursor.execute(qry,value)
            mydb.commit()
            QMessageBox.information(self,"School Management System","Student details saved successfuly")
        except con.Error as e:
            print("Error occured here",e)
        #after insertion reset the values which has entered
        self.tb11.setText("")
        self.tb12.setText("")
        self.cb11.setCurrentIndex(-1)
        self.tb13.setText("")
        self.tb14.setText("")
        self.tb15.setText("")
        self.tb16.setText("")
        self.tb17.setText("")
        self.cb12.setCurrentIndex(-1)

    #show the delete menu
    def show_delete_update_student(self):
        self.tabWidget.setCurrentIndex(3)
    #delete the student details
    def delete_student_details(self):
        try:
            mydb = con.connect(host="localhost",user="root",password="naveeth@097",db="school")
            cursor = mydb.cursor()
            registration_number = self.tb18.text()
            full_name = self.tb19.text()
            gender = self.cb13.currentText()
            dfb = self.tb20.text()
            age = self.tb21.text()
            address = self.tb22.text()
            phone = self.tb23.text()
            email = self.tb24.text()
            classes = self.cb14.currentText()

            qry = "delete from student where(registration_number = %s AND full_name = %s AND gender = %s AND date_of_birth = %s AND age = %s AND Address=%s AND phone=%s AND email=%s AND standard=%s)"
            values = (registration_number,full_name,gender,dfb,age,address,phone,email,classes)
            cursor.execute(qry,values)
            mydb.commit()
            QMessageBox.information(self,"School Management Sysem","Record deleted Successfully")

        
        except con.Error as e:
            print("Error occured ",e)
        self.tb18.setText("")
        self.tb19.setText("")
        self.cb13.setCurrentIndex(-1)
        self.tb20.setText("")
        self.tb21.setText("")
        self.tb22.setText("")
        self.tb23.setText("")
        self.tb24.setText("")
        self.cb14.setCurrentIndex(-1)
    #edit the student details
    def edit_student_details(self):
        try:
            mydb = con.connect(host="localhost",user="root",password = "naveeth@097",db = "school")
            cursor = mydb.cursor()
            registration_number = self.tb18.text()
            full_name = self.tb19.text()
            gender = self.cb13.currentText()
            dfb = self.tb20.text()
            age = self.tb21.text()
            address = self.tb22.text()
            phone = self.tb23.text()
            email = self.tb24.text()
            classes = self.cb14.currentText()
            
            qry = "UPDATE student SET registration_number = %s, full_name = %s, gender = %s, date_of_birth = %s, age = %s, Address = %s, phone = %s, email = %s, standard = %s WHERE registration_number = %s"
            values = (registration_number, full_name, gender, dfb, age, address, phone, email, classes, registration_number)
            cursor.execute(qry,values)
            mydb.commit()
            QMessageBox.information(self,"School Management System","Record Updated Successfully")
        except con.Error as e:
            print("Error occured as ",e)
        self.tb18.setText("")
        self.tb19.setText("")
        self.cb13.setCurrentIndex(-1)
        self.tb20.setText("")
        self.tb21.setText("")
        self.tb22.setText("")
        self.tb23.setText("")
        self.tb24.setText("")
        self.cb14.setCurrentIndex(-1)
        #show the mark widget
    def show_mark_delete_edit_student(self):
        self.tabWidget.setCurrentIndex(4)
        self.load_registration_number()
        self.load_registration_exam()#for edit or delete student load in database
        self.mcb16.setCurrentIndex(-1)
        self.mcb17.setCurrentIndex(-1)
        #self.gb1.setChecked(True)
        #self.gb2.setChecked(False)
        #load the registration number from database
    def load_registration_number(self):
        try:
            mydb = con.connect(host="localhost",user="root",password="naveeth@097",db="school")
            cursor = mydb.cursor()
            qry = "select registration_number from student"
            cursor.execute(qry)
            register_no = [str(row[0])for row in cursor.fetchall()]
            self.mcb15.addItems(register_no)
        except con.Error as e:
            print("Error occured in ",e)
        #load the register number and exam_name in edit,delete details
    def load_registration_exam(self):
        try:
            mydb = con.connect(host="localhost",user="root",password = "naveeth@097",db = "school")
            cursor = mydb.cursor()
            qry = "select registration_number,exam_name from mark"
            cursor.execute(qry)
            register_exam = [(str(row[0]), str(row[1])) for row in cursor.fetchall()]

            for register,exam_name in register_exam:
                self.mcb16.addItem(register)
                self.mcb17.addItem(exam_name)
        except con.Error as e:
            print("Error occured in ",e)

        #save the details of the mark of a student
    def save_mark_details(self):
        try:
            mydb = con.connect(host="localhost",user="root",password="naveeth@097",db = "school")
            cursor = mydb.cursor()
            registration_number = self.mcb15.currentText()
            exam_name = self.mcb15_2.currentText()
            language = self.mtb12.text()
            english = self.mtb13.text()
            maths = self.mtb14.text()
            science = self.mtb15.text()
            social = self.mtb16.text()

            qry = "insert into mark(registration_number,exam_name,language,english,maths,science,social) values (%s,%s,%s,%s,%s,%s,%s)"
            values = (registration_number,exam_name,language,english,maths,science,social)
            cursor.execute(qry,values)
            mydb.commit()
            QMessageBox.information(self,"School Management System","Marks Saved Successfully")
            self.mcb17.setCurrentIndex(-1)
            self.mcb16.setCurrentIndex(-1)
            self.mtb17.setText("")
            self.mtb18.setText("")
            self.mtb19.setText("")
            self.mtb20.setText("")
            self.mtb21.setText("")
        except con.Error as e:
            print("Error occured in ",e)
            #load the five subjects mark details with correspondent register number, exam_name
    def load_exam_marks(self):
        registration_number = self.mcb16.currentText()
        exam_name = self.mcb17.currentText()

        try:
            mydb = con.connect(host="localhost",user="root",password="naveeth@097",db="school")
            cursor = mydb.cursor()
            qry = "select language, english, maths, science, social from mark where registration_number = %s AND exam_name = %s"
            cursor.execute(qry,(registration_number,exam_name))
            mark_data = cursor.fetchone()

            if(mark_data):
                language,english,maths,science,social = mark_data
                self.mtb17.setText(str(language))
                self.mtb18.setText(str(english))
                self.mtb19.setText(str(maths))
                self.mtb20.setText(str(science))
                self.mtb21.setText(str(social))
            else:
                QMessageBox.information(self,"School Management System","Data Not Found")
        except con.Error as e:
            print("Error occured in ",e)
        #edit_the_marks 
    def edit_mark_details(self):
        try:
            mydb = con.connect(host="localhost",user="root",password="naveeth@097",db = "school")
            cursor = mydb.cursor()
            registration_number = self.mcb16.currentText()
            exam_name = self.mcb17.currentText()
            language = self.mtb17.text()
            english = self.mtb18.text()
            maths = self.mtb19.text()
            science = self.mtb20.text()
            social = self.mtb21.text()

            qry = "update mark set language= %s, english= %s, maths = %s, science = %s, social = %s where registration_number = %s AND exam_name = %s"
            values = (language,english,maths,science,social,registration_number,exam_name)
            cursor.execute(qry,values)
            mydb.commit()
            QMessageBox.information(self,"School Management System","Successfully updated the Marks")
            self.mcb17.setCurrentIndex(-1)
            self.mcb16.setCurrentIndex(-1)
            self.mtb17.setText("")
            self.mtb18.setText("")
            self.mtb19.setText("")
            self.mtb20.setText("")
            self.mtb21.setText("")
        except con.Error as e:
            print("Error occured as ",e)
        #delete the record from the database
    def delete_mark_details(self):
        try:
            mydb = con.connect(host="localhost",user="root",password = "naveeth@097",db = "school")
            cursor = mydb.cursor()
            registration_number = self.mcb16.currentText()
            exam_name = self.mcb17.currentText()
            language = self.mtb17.text()
            english = self.mtb18.text()
            maths = self.mtb19.text()
            science = self.mtb20.text()
            social = self.mtb21.text()

            qry = "delete from mark where(registration_number = %s AND exam_name =%s AND language = %s AND english = %s AND maths = %s AND science = %s AND social =%s)"
            values = (registration_number,exam_name,language,english,maths,science,social)
            cursor.execute(qry,values)
            mydb.commit()
            QMessageBox.information(self,"School Management System","Deleted Record Successfully")
            self.mcb17.setCurrentIndex(-1)
            self.mcb16.setCurrentIndex(-1)
            self.mtb17.setText("")
            self.mtb18.setText("")
            self.mtb19.setText("")
            self.mtb20.setText("")
            self.mtb21.setText("")
        except con.Error as e:
            print("Error occured in ",e)
    #show attendance details
    def show_attendance_details(self):
        self.tabWidget.setCurrentIndex(5)
        self.get_registration_number()#get register number in attendance in combo box
        self.get_registernumber_date()#get registration number and date in edit or delete groupbox
    def get_registration_number(self):
        try:
            mydb = con.connect(host="localhost",user="root",password = "naveeth@097",db="school")
            cursor = mydb.cursor()
            qry = "select registration_number from student"
            cursor.execute(qry)
            register_no = [str(row[0])for row in cursor.fetchall()]
            self.acb11.addItems(register_no)
        except con.Error as e:
            print("Error occured in ",e)
    def save_attendance_details(self):
        try:
            mydb = con.connect(host="localhost",user="root",password="naveeth@097",db="school")
            cursor = mydb.cursor()
            registration_number = self.acb11.currentText()
            date = self.atb11.text()
            morning = self.atb12.text()
            evening = self.atb13.text()

            qry = "insert into attendance(registration_number,attendance_date,morning,evening) values(%s,%s,%s,%s)"
            values = (registration_number,date,morning,evening)
            cursor.execute(qry,values)
            mydb.commit()
            QMessageBox.information(self,"School Management System","Attendance Saved Successfully")

            self.acb11.setCurrentIndex(-1)
            self.atb11.setText("")
            self.atb12.setText("")
            self.atb13.setText("")
        except con.Error as e:
            print("Error occured in ",e)
    def get_registernumber_date(self):
        try:
            mydb = con.connect(host="localhost",user="root",password = "naveeth@097",db = "school")
            cursor = mydb.cursor()
            qry = "select registration_number, attendance_date from attendance"
            cursor.execute(qry)
            register_exam = [(str(row[0]), str(row[1])) for row in cursor.fetchall()]

            for register,exam_name in register_exam:
                self.acb12.addItem(register)
                self.acb13.addItem(exam_name)
        except con.Error as e:
            print("Error occured in ",e)

    def edit_attendance_details(self):
        try:
            mydb = con.connect(host="localhost",user="root",password="naveeth@097",db="school")
            cursor = mydb.cursor()
            registration_number = self.acb11.currentText()
            date = self.atb11.text()
            morning = self.atb12.text()
            evening = self.atb13.text()

            qry = "update attendance set registration_number=%s, attendance_date =%s, date = %s, morning = %s, evening = %s where registration_number = %s AND attendance_date = %s"
            values = (morning,evening,registration_number,date)
            cursor.execute(qry,values)
            mydb.commit()
            QMessageBox.information(self,"School Management System","Data Updated Successfully")
        except con.Error as e:
            print("Error occured in ",e)
    def delete_attendance_details(self):
        try:
            mydb = con.connect(host="localhost",user="root",password="naveeth@097",db="school")
            cursor = mydb.cursor()
            registration_number = self.acb12.currentText()
            date = self.acb13.currentText()
            morning = self.atb14.text()
            evening = self.atb15.text()

            qry = "delete from attendance where(registration_number = %s AND  attendance_date = %s AND  morning = %s AND evening = %s)"
            values = (registration_number, date, morning,evening)
            cursor.execute(qry,values)
            mydb.commit()
            QMessageBox.information(self,"School Management System","Record Removed Successfully")
        except con.Error as e:
            print("Error occured in ",e)      
        
        self.acb12.setCurrentIndex(-1)
        self.acb13.setCurrentIndex(-1)
        self.atb14.setText("")
        self.atb15.setText("")
    def get_details_attendance(self):
        registration_number = self.acb12.currentText()
        date = self.acb13.currentText()
        try:
            mydb = con.connect(host="localhost",user="root",password="naveeth@097",db="school")
            cursor = mydb.cursor()
            qry = "select morning, evening from attendance where registration_number = %s AND attendance_date = %s"
            cursor.execute(qry,(registration_number,date))
            mark_data = cursor.fetchone()

            if(mark_data):
                morning, evening = mark_data
                self.atb14.setText(str(morning))
                self.atb15.setText(str(evening))
                
            else:
                QMessageBox.information(self,"School Management System","Data Not Found")
        except con.Error as e:
            print("Error occured in ",e)    
    def show_fees_details(self):
        self.tabWidget.setCurrentIndex(6)
        #it will generate the unique number
    def generate_receipt_number(self):
        unique_number = set()
        
        unique_number.add(random.randint(1,999999))
        receipt_number = ','.join(map(str,unique_number))
        self.ftb11.setText(str(receipt_number))
        self.ftb11.setEnabled(False)
    def save_fees_details(self):
        self.ftb11.setEnabled(True)
        try:
            mydb = con.connect(host="localhost",user="root",password = "naveeth@097",db = "school")
            cursor = mydb.cursor()
            receipt_number = self.ftb11.text()
            registration_number = self.ftb12.text()
            payment_reason = self.ftb13.text()
            amount = self.ftb14.text()
            date = self.ftb15.text()

            qry = "insert into fees(receipt_number, registration_number, reason, amount, fees_date) values(%s,%s,%s,%s,%s)"
            values = (receipt_number,registration_number,payment_reason,amount,date)
            cursor.execute(qry,values)
            mydb.commit()
            QMessageBox.information(self,"School Management System","Data Added Successfully")
        except con.Error as e:
            print("Error occured in ",e)
        self.ftb11.setText("")
        self.ftb12.setText("")
        self.ftb13.setText("")
        self.ftb14.setText("")
        self.ftb15.setText("")
    def edit_fees_details(self):
        try:
            mydb = con.connect(host="localhost",user="root",password="naveeth@097",db="school")
            cursor = mydb.cursor()
            receipt_number = self.ftb16.text()
            registration_number = self.ftb17.text()
            payment_reason = self.ftb18.text()
            amount = self.ftb19.text()
            date = self.ftb20.text()

            qry = "update fees set reason = %s, amount = %s, fees_date = %s where receipt_number = %s AND registration_number = %s"
            values = (payment_reason,amount,date,receipt_number,registration_number)
            cursor.execute(qry,values)
            mydb.commit()
            QMessageBox.information(self,"School Management System","Data Updated Successfully")
        except con.Error as e:
            print("Error occured in ",e)
        self.ftb16.setText("")
        self.ftb17.setText("")
        self.ftb18.setText("")
        self.ftb19.setText("")
        self.ftb20.setText("")
    def delete_fees_details(self):
        try:
            mydb = con.connect(host="localhost",user="root",password="naveeth@097",db="school")
            cursor = mydb.cursor()
            receipt_number = self.ftb16.text()
            registration_number = self.ftb17.text()
            payment_reason = self.ftb18.text()
            amount = self.ftb19.text()
            date = self.ftb20.text()

            qry = "delete from fees where(receipt_number = %s AND registration_number = %s AND reason = %s AND amount = %s AND fees_date = %s)"
            values = (receipt_number,registration_number,payment_reason,amount,date)
            cursor.execute(qry,values)
            mydb.commit()
            QMessageBox.information(self,"School Management System","Record Removed Successfully")
        except con.Error as e:
            print("Error occured in ",e)
        self.ftb16.setText("")
        self.ftb17.setText("")
        self.ftb18.setText("")
        self.ftb19.setText("")
        self.ftb20.setText("")
    def clear_data(self):
        self.new_table = QStandardItemModel()
        self.new_table.clear()
        self.tableView.setModel(self.new_table)

    def show_report(self,report_type):
        if(report_type == "student"):
            self.show_student_report()
            self.download_details("student")
        elif(report_type == "mark"):
            self.display_mark_report()
            self.download_details("mark")
        elif(report_type == "attendance"):
            self.show_attendance_report()
            self.download_details("attendance")
        else:
            self.show_fees_report()
            self.download_details("fees")



    def show_student_report(self):
        self.clear_data()
        self.tabWidget.setCurrentIndex(7)
        mydb = con.connect(host="localhost",user="root",password="naveeth@097",db="school")
        cursor = mydb.cursor()
        cursor.execute("select * from student")
        data = cursor.fetchall()
        
        rows = len(data[1:])
        columns = len(data[0])
        model = QStandardItemModel(rows, columns)


        headers = ["S.No. ","Registration Number", "Full Name", "Gender", "Date of Birth", "Age", "Address", "Phone", "Email", "Standard"]
        model.setHorizontalHeaderLabels(headers)

        for row_index, row_data in enumerate(data):
            for col_index, cell_value in enumerate(row_data):
                item = QStandardItem(str(cell_value))
                model.setItem(row_index, col_index, item)

        # Set the model to the QTableView
        self.tableView.setModel(model)
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)  # Disable editing
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)  # Select entire rows
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)  # Resize columns to contents
        self.tableView.horizontalHeader().setStretchLastSection(True)

    def show_attendance_report(self):
        self.clear_data()
        self.tabWidget.setCurrentIndex(7)
        mydb = con.connect(host="localhost",user="root",password = "naveeth@097",db = "school")
        cursor = mydb.cursor()
        cursor.execute("select * from attendance")
        data = cursor.fetchall()

        rows = len(data)
        columns = len(data[0])
        model = QStandardItemModel(rows, columns)

        headers = ["S.No","Registration Number","Date","Morning","Evening"]
        model.setHorizontalHeaderLabels(headers)

        for row_index, row_data in enumerate(data):
            for col_index, cell_value in enumerate(row_data):
                item = QStandardItem(str(cell_value))
                model.setItem(row_index,col_index,item)
        self.tableView.setModel(model)
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableView.horizontalHeader().setStretchLastSection(True)
    def display_mark_report(self):
        self.clear_data()
        self.tabWidget.setCurrentIndex(7)
        mydb = con.connect(host="localhost",user="root",password = "naveeth@097",db = "school")
        cursor = mydb.cursor()
        cursor.execute("select * from mark")
        data = cursor.fetchall()

        rows = len(data)
        columns = len(data[1:])
        model = QStandardItemModel(rows,columns)

        headers = ["S.No.","Registration Number","Exam Name","Language","English","Maths","Science","Social Science"]
        model.setHorizontalHeaderLabels(headers)

        for row_index, row_data in enumerate(data):
            for col_index, cell_value in enumerate(row_data):
                item = QStandardItem(str(cell_value))
                model.setItem(row_index, col_index, item)
        self.tableView.setModel(model)
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)  # Disable editing
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)  # Select entire rows
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)  # Resize columns to contents
        self.tableView.horizontalHeader().setStretchLastSection(True)

    def show_fees_report(self):
        self.clear_data()
        self.tabWidget.setCurrentIndex(7)
        mydb = con.connect(host="localhost",user="root",password = "naveeth@097",db="school")
        cursor = mydb.cursor()
        cursor.execute("select * from fees")
        data = cursor.fetchall()

        rows = len(data)
        columns = len(data[1:])
        model = QStandardItemModel(rows,columns)

        headers = ["Receipt Number","Registration Number","Fees Reason","Amount","Date"]
        model.setHorizontalHeaderLabels(headers)

        for row_index, row_data in enumerate(data):
            for col_index, cell_value in enumerate(row_data):
                item = QStandardItem(str(cell_value))
                model.setItem(row_index,col_index, item)

        self.tableView.setModel(model)
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableView.horizontalHeader().setStretchLastSection(True)
    #download the content from the database
    def get_download_details(self,download_type):
        file_path, _ = QFileDialog.getSaveFileName(self,"Save Report","C:/Users/jnave\OneDrive\Documents\PyQt5\School Management System","CSV Files (*.csv)")

        if file_path:
            try:
                mydb = con.connect(host="localhost",user="root",password = "naveeth@097",db = "school")
                cursor = mydb.cursor()
                
                if(download_type == "student"):
                    cursor.execute("select * from student")
                elif(download_type == "mark"):
                    cursor.execute("select * from mark")
                elif(download_type == "attendance"):
                    cursor.execute("select * from attendance")
                else:
                    cursor.execute("select * from fees")

                data = cursor.fetchall()
                with open(file_path,'w',newline='') as csvfile:
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow([i[0] for i in cursor.description])
                    csvwriter.writerows(data)
                QMessageBox.information(self,"School Management System","Report Downloaded")
            except Exception as e:
                QMessageBox.warning(self,"Error",f"An error occurred: {str(e)}")
       
def main():
    app = QApplication(sys.argv)
    window  = MainApp()
    window.show()
    app.exec_()
if __name__ == '__main__':
    main()