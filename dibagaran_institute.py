#!/uself.SR/bin/python2.7
# -*- coding: utf-8 -*-
##########################################################


##########################################################
# Dibagaran Institute
# Mohammad Mahdavi
# moh.mahdavi.l@gmail.com
# June 2016
# All Rights Reserved
##########################################################


##########################################################
import os
import codecs
import time
import shutil
import Tkinter
import PIL.Image
import PIL.ImageTk
import tkMessageBox
import sqlite3
##########################################################


##########################################################
class DibagaranInstitute:

	RESOURCES_FOLDER = os.path.join(os.path.dirname(__file__),"resources")
	BACKUP_FOLDER = os.path.join(RESOURCES_FOLDER,"backup")
	LOGO_IMAGE_NAME = "logo.jpg"
	LOGO_IMAGE_PATH = os.path.join(RESOURCES_FOLDER,LOGO_IMAGE_NAME)
	DATABASE_PATH = os.path.join(RESOURCES_FOLDER,"database.db")
	ICON_PATH = os.path.join(RESOURCES_FOLDER,"icon.ico")
	REPORT_FILE_PATH = os.path.join(RESOURCES_FOLDER,"report.html")
	BGC = "#E6E6E6"
	BC = "#CECEF6"
	LC = "#D8CEF6"
	SR = 3
	MWW = 30
	LWW = 2 * MWW
	MWH = 2
	BDS = 5

	def __init__(self):
		if not os.path.exists(self.RESOURCES_FOLDER):
			os.mkdir(self.RESOURCES_FOLDER)
		if not os.path.exists(self.BACKUP_FOLDER):
			os.mkdir(self.BACKUP_FOLDER)
		if not os.path.exists(self.DATABASE_PATH):
			self.createDatabase()
		self.root = Tkinter.Tk()
		self.root.title("Dibagaran Institute")
		self.root.configure(bg = self.BGC)
		self.root.wm_iconbitmap(self.ICON_PATH)
		logo_image = PIL.ImageTk.PhotoImage(PIL.Image.open(self.LOGO_IMAGE_PATH))
		logo_label = Tkinter.Label(self.root,relief = Tkinter.GROOVE,image = logo_image)
		logo_label.image = logo_image
		logo_label.grid(row = 0,columnspan = 4)
		Tkinter.Button(self.root,text = "صفحه نخست".decode("utf-8"),bg = self.BC,width = self.MWW,height = self.MWH,command = lambda: self.makeMainForm()).grid(row = 1,column = 3)
		Tkinter.Button(self.root,text = "ثبت‌نام دانش‌آموز".decode("utf-8"),bg = self.BC,width = self.MWW,height = self.MWH,command = lambda: self.addStudentForm()).grid(row = 1,column = 2)
		Tkinter.Button(self.root,text = "ثبت سوابق تحصیلی".decode("utf-8"),bg = self.BC,width = self.MWW,height = self.MWH,command = lambda: self.addEducationForm()).grid(row = 1,column = 1)
		Tkinter.Button(self.root,text = "ثبت سوابق پرداختی".decode("utf-8"),bg = self.BC,width = self.MWW,height = self.MWH,command = lambda: self.addPaymentForm()).grid(row = 1,column = 0)
		Tkinter.Button(self.root,text = "نمایش لیست دانش‌آموزان".decode("utf-8"),bg = self.BC,width = self.MWW,height = self.MWH,command = lambda: self.showStudentListForm()).grid(row = 2,column = 3)
		Tkinter.Button(self.root,text = "جستجوی دانش‌آموز".decode("utf-8"),bg = self.BC,width = self.MWW,height = self.MWH,command = lambda: self.searchStudentForm()).grid(row = 2,column = 2)
		Tkinter.Button(self.root,text = "حذف سوابق".decode("utf-8"),bg = self.BC,width = self.MWW,height = self.MWH,command = lambda: self.removeRecordForm()).grid(row = 2,column = 1)
		Tkinter.Button(self.root,text = "پشتیبان‌گیری از پایگاه داده".decode("utf-8"),bg = self.BC,width = self.MWW,height = self.MWH,command = lambda: self.makeDatabaseBackup()).grid(row = 2,column = 0)
		self.root.mainloop()

	def createDatabase(self):
		conn = sqlite3.connect(self.DATABASE_PATH)
		conn.execute("""CREATE TABLE Student (NationalCode TEXT PRIMARY KEY,FirstName TEXT,LastName TEXT,FatherName TEXT);""")
		conn.execute("""CREATE TABLE Education (ID INTEGER PRIMARY KEY AUTOINCREMENT,NationalCode TEXT,Date TEXT,Level TEXT,Score TEXT);""")
		conn.execute("""CREATE TABLE Payment (ID INTEGER PRIMARY KEY AUTOINCREMENT,NationalCode TEXT,Date TEXT,Amount TEXT,Comment TEXT);""")
		conn.close()

	def addStudentToDatabase(self,NATIONAL_CODE,FIRST_NAME,LAST_NAME,FATHER_NAME):
		if NATIONAL_CODE and FIRST_NAME and LAST_NAME and FATHER_NAME:
			conn = sqlite3.connect(self.DATABASE_PATH)
			cursor = conn.execute("SELECT * from Student WHERE NationalCode = '{}';".format(NATIONAL_CODE))
			row = cursor.fetchone()
			if not row:
				conn.execute("INSERT INTO Student (NationalCode,FirstName,LastName,FatherName) VALUES ('{}','{}','{}','{}');".format(NATIONAL_CODE,FIRST_NAME,LAST_NAME,FATHER_NAME))
				conn.commit()
				conn.close()
				self.makeMainForm()

	def addEducationToDatabase(self,NATIONAL_CODE,DATE,LEVEL,SCORE):
		if NATIONAL_CODE and DATE and LEVEL and SCORE:
			conn = sqlite3.connect(self.DATABASE_PATH)
			cursor = conn.execute("SELECT * from Student WHERE NationalCode = '{}';".format(NATIONAL_CODE))
			row = cursor.fetchone()
			if row:
				conn.execute("INSERT INTO Education (NationalCode,Date,Level,Score) VALUES ('{}','{}','{}','{}');".format(NATIONAL_CODE,DATE,LEVEL,SCORE))
				conn.commit()
				conn.close()
				self.makeMainForm()

	def addPaymentToDatabase(self,NATIONAL_CODE,DATE,AMOUNT,COMMENT):
		if NATIONAL_CODE and DATE and AMOUNT and COMMENT:
			conn = sqlite3.connect(self.DATABASE_PATH)
			cursor = conn.execute("SELECT * from Student WHERE NationalCode = '{}';".format(NATIONAL_CODE))
			row = cursor.fetchone()
			if row:
				conn.execute("INSERT INTO Payment (NationalCode,Date,Amount,Comment) VALUES ('{}','{}','{}','{}');".format(NATIONAL_CODE,DATE,AMOUNT,COMMENT))
				conn.commit()
				conn.close()
				self.makeMainForm()

	def removeStudentFromDatabase(self,NATIONAL_CODE):
		if NATIONAL_CODE:
			conn = sqlite3.connect(self.DATABASE_PATH)
			cursor = conn.execute("SELECT * from Student WHERE NationalCode = '{}';".format(NATIONAL_CODE))
			row = cursor.fetchone()
			if row:
				result = tkMessageBox.askquestion("حذف دانش‌آموز","برای حذف دانش‌آموز مطمئنید؟")
				if result == "yes":
					conn.execute("DELETE FROM STUDENT WHERE NationalCode = '{}';".format(NATIONAL_CODE))
					conn.commit()
					conn.close()
					self.makeMainForm()

	def removeEducationFromDatabase(self,ID):
		if ID:
			conn = sqlite3.connect(self.DATABASE_PATH)
			cursor = conn.execute("SELECT * from Education WHERE ID = '{}';".format(ID))
			row = cursor.fetchone()
			if row:
				result = tkMessageBox.askquestion("حذف سابقه","برای حذف سابقه مطمئنید؟")
				if result == "yes":
					conn.execute("DELETE FROM Education WHERE ID = '{}';".format(ID))
					conn.commit()
					conn.close()
					self.makeMainForm()

	def removePaymentFromDatabase(self,ID):
		if ID:
			conn = sqlite3.connect(self.DATABASE_PATH)
			cursor = conn.execute("SELECT * from Payment WHERE ID = '{}';".format(ID))
			row = cursor.fetchone()
			if row:
				result = tkMessageBox.askquestion("حذف سابقه","برای حذف سابقه مطمئنید؟")
				if result == "yes":
					conn.execute("DELETE FROM Payment WHERE ID = '{}';".format(ID))
					conn.commit()
					conn.close()
					self.makeMainForm()

	def makeDatabaseBackup(self):
		result = tkMessageBox.askquestion("پشتیبان‌گیری","برای پشتیبان‌گیری از پایگاه داده اطمینان دارید؟")
		if result == "yes":
			shutil.copy(self.DATABASE_PATH,self.BACKUP_FOLDER + "/" + "database" + str(int(time.time())) + ".db")
	
	def makeMainForm(self):
		for widget in self.root.grid_slaves():
			if int(widget.grid_info()["row"]) >= self.SR:
				widget.grid_forget()

	def addStudentForm(self):
		self.makeMainForm()
		Tkinter.Label(self.root,text = ":کد ملی".decode("utf-8"),bg = self.LC,relief = Tkinter.GROOVE,width = self.MWW,height = self.MWH).grid(row = self.SR,column = 2)
		Tkinter.Label(self.root,text = ":نام".decode("utf-8"),bg = self.LC,relief = Tkinter.GROOVE,width = self.MWW,height = self.MWH).grid(row = self.SR + 1,column = 2)
		Tkinter.Label(self.root,text = ":نام خانوادگی".decode("utf-8"),bg = self.LC,relief = Tkinter.GROOVE,width = self.MWW,height = self.MWH).grid(row = self.SR + 2,column = 2)
		Tkinter.Label(self.root,text = ":نام پدر".decode("utf-8"),bg = self.LC,relief = Tkinter.GROOVE,width = self.MWW,height = self.MWH).grid(row = self.SR + 3,column = 2)
		national_code_entry = Tkinter.Entry(self.root,relief = Tkinter.FLAT,width = self.MWW,bd = self.BDS)
		first_name_entry = Tkinter.Entry(self.root,relief = Tkinter.FLAT,width = self.MWW,bd = self.BDS)
		last_name_entry = Tkinter.Entry(self.root,relief = Tkinter.FLAT,width = self.MWW,bd = self.BDS)
		father_name_entry = Tkinter.Entry(self.root,relief = Tkinter.FLAT,width = self.MWW,bd = self.BDS)
		national_code_entry.grid(row = self.SR,column = 1)
		first_name_entry.grid(row = self.SR + 1,column = 1)
		last_name_entry.grid(row = self.SR + 2,column = 1)
		father_name_entry.grid(row = self.SR + 3,column = 1)
		Tkinter.Button(self.root,text = "ثبت".decode("utf-8"),bg = self.BC,width = self.LWW,height = self.MWH,command = lambda: self.addStudentToDatabase(national_code_entry.get().encode("utf-8"),first_name_entry.get().encode("utf-8"),last_name_entry.get().encode("utf-8"),father_name_entry.get().encode("utf-8"))).grid(row = self.SR + 4,column = 1,columnspan = 2)

	def showStudentListForm(self):
		self.makeMainForm()
		national_code_list = []
		scrollbar = Tkinter.Scrollbar(self.root)
		student_list = Tkinter.Listbox(self.root,yscrollcommand = scrollbar.set,width = self.MWW,relief = Tkinter.FLAT)
		scrollbar.config(command = student_list.yview)
		conn = sqlite3.connect(self.DATABASE_PATH)
		cursor = conn.execute("SELECT * from Student;")
		for row in cursor:
			name = " ".join(row[1:3])
			student_list.insert(Tkinter.END,name)
			national_code_list.append(row[0])
		conn.close()
		scrollbar.grid(row = self.SR,column = 2)
		student_list.grid(row = self.SR,column = 1,columnspan = 2)
		Tkinter.Button(self.root,text = "انتخاب".decode("utf-8"),bg = self.BC,width = self.LWW,height = self.MWH,command = lambda: self.showStudentInformationForm(national_code_list[student_list.curselection()[0]])).grid(row = self.SR + 1,column = 1,columnspan = 2)

	def searchStudentForm(self):
		self.makeMainForm()
		Tkinter.Label(self.root,text = ":کد ملی".decode("utf-8"),bg = self.LC,relief = Tkinter.GROOVE,width = self.MWW,height = self.MWH).grid(row = self.SR,column = 2)
		national_code_entry = Tkinter.Entry(self.root,relief = Tkinter.FLAT,width = self.MWW,bd = self.BDS)
		national_code_entry.grid(row = self.SR,column = 1)
		Tkinter.Button(self.root,text = "جستجو".decode("utf-8"),bg = self.BC,width = self.LWW,height = self.MWH,command = lambda: self.showStudentInformationForm(national_code_entry.get().encode("utf-8"))).grid(row = self.SR + 1,column = 1,columnspan = 2)

	def addEducationForm(self):
		self.makeMainForm()
		Tkinter.Label(self.root,text = ":کد ملی".decode("utf-8"),bg = self.LC,relief = Tkinter.GROOVE,width = self.MWW,height = self.MWH).grid(row = self.SR,column = 2)
		Tkinter.Label(self.root,text = ":تاریخ".decode("utf-8"),bg = self.LC,relief = Tkinter.GROOVE,width = self.MWW,height = self.MWH).grid(row = self.SR + 1,column = 2)
		Tkinter.Label(self.root,text = ":سطح".decode("utf-8"),bg = self.LC,relief = Tkinter.GROOVE,width = self.MWW,height = self.MWH).grid(row = self.SR + 2,column = 2)
		Tkinter.Label(self.root,text = ":نمره".decode("utf-8"),bg = self.LC,relief = Tkinter.GROOVE,width = self.MWW,height = self.MWH).grid(row = self.SR + 3,column = 2)
		national_code_entry = Tkinter.Entry(self.root,relief = Tkinter.FLAT,width = self.MWW,bd = self.BDS)
		date_entry = Tkinter.Entry(self.root,relief = Tkinter.FLAT,width = self.MWW,bd = self.BDS)
		level_entry = Tkinter.Entry(self.root,relief = Tkinter.FLAT,width = self.MWW,bd = self.BDS)
		score_entry = Tkinter.Entry(self.root,relief = Tkinter.FLAT,width = self.MWW,bd = self.BDS)
		national_code_entry.grid(row = self.SR,column = 1)
		date_entry.grid(row = self.SR + 1,column = 1)
		level_entry.grid(row = self.SR + 2,column = 1)
		score_entry.grid(row = self.SR + 3,column = 1)
		Tkinter.Button(self.root,text = "ثبت".decode("utf-8"),bg = self.BC,width = self.LWW,height = self.MWH,command = lambda: self.addEducationToDatabase(national_code_entry.get().encode("utf-8"),date_entry.get().encode("utf-8"),level_entry.get().encode("utf-8"),score_entry.get().encode("utf-8"))).grid(row = self.SR + 4,column = 1,columnspan = 2)

	def addPaymentForm(self):
		self.makeMainForm()
		Tkinter.Label(self.root,text = ":کد ملی".decode("utf-8"),bg = self.LC,relief = Tkinter.GROOVE,width = self.MWW,height = self.MWH).grid(row = self.SR,column = 2)
		Tkinter.Label(self.root,text = ":تاریخ".decode("utf-8"),bg = self.LC,relief = Tkinter.GROOVE,width = self.MWW,height = self.MWH).grid(row = self.SR + 1,column = 2)
		Tkinter.Label(self.root,text = ":مقدار".decode("utf-8"),bg = self.LC,relief = Tkinter.GROOVE,width = self.MWW,height = self.MWH).grid(row = self.SR + 2,column = 2)
		Tkinter.Label(self.root,text = ":توضیحات".decode("utf-8"),bg = self.LC,relief = Tkinter.GROOVE,width = self.MWW,height = self.MWH).grid(row = self.SR + 3,column = 2)
		national_code_entry = Tkinter.Entry(self.root,relief = Tkinter.FLAT,width = self.MWW,bd = self.BDS)
		date_entry = Tkinter.Entry(self.root,relief = Tkinter.FLAT,width = self.MWW,bd = self.BDS)
		amount_entry = Tkinter.Entry(self.root,relief = Tkinter.FLAT,width = self.MWW,bd = self.BDS)
		comment_entry = Tkinter.Entry(self.root,relief = Tkinter.FLAT,width = self.MWW,bd = self.BDS)
		national_code_entry.grid(row = self.SR,column = 1)
		date_entry.grid(row = self.SR + 1,column = 1)
		amount_entry.grid(row = self.SR + 2,column = 1)
		comment_entry.grid(row = self.SR + 3,column = 1)
		Tkinter.Button(self.root,text = "ثبت".decode("utf-8"),bg = self.BC,width = self.LWW,height = self.MWH,command = lambda: self.addPaymentToDatabase(national_code_entry.get().encode("utf-8"),date_entry.get().encode("utf-8"),amount_entry.get().encode("utf-8"),comment_entry.get().encode("utf-8"))).grid(row = self.SR + 4,column = 1,columnspan = 2)

	def showStudentInformationForm(self,NATIONAL_CODE):
		conn = sqlite3.connect(self.DATABASE_PATH)
		cursor = conn.execute("SELECT * from Student WHERE NationalCode = '{}';".format(NATIONAL_CODE))
		row = cursor.fetchone()
		if row:
			self.makeMainForm()
			education_cursor = conn.execute("SELECT * from Education WHERE NationalCode = '{}';".format(NATIONAL_CODE))
			payment_cursor = conn.execute("SELECT * from Payment WHERE NationalCode = '{}';".format(NATIONAL_CODE))
			Tkinter.Label(self.root,text = ":اطلاعات پرونده",bg = self.LC,relief = Tkinter.GROOVE,width = self.LWW,height = self.MWH).grid(row = self.SR,column = 1,columnspan = 2)
			Tkinter.Label(self.root,text = ":کد ملی".decode("utf-8"),bg = self.LC,relief = Tkinter.GROOVE,width = self.MWW,height = self.MWH).grid(row = self.SR + 1,column = 2)
			Tkinter.Label(self.root,text = ":نام".decode("utf-8"),bg = self.LC,relief = Tkinter.GROOVE,width = self.MWW,height = self.MWH).grid(row = self.SR + 2,column = 2)
			Tkinter.Label(self.root,text = ":نام خانوادگی".decode("utf-8"),bg = self.LC,relief = Tkinter.GROOVE,width = self.MWW,height = self.MWH).grid(row = self.SR + 3,column = 2)
			Tkinter.Label(self.root,text = ":نام پدر".decode("utf-8"),bg = self.LC,relief = Tkinter.GROOVE,width = self.MWW,height = self.MWH).grid(row = self.SR + 4,column = 2)
			Tkinter.Label(self.root,text = ":تعداد سوابق تحصیلی".decode("utf-8"),bg = self.LC,relief = Tkinter.GROOVE,width = self.MWW,height = self.MWH).grid(row = self.SR + 5,column = 2)
			Tkinter.Label(self.root,text = ":تعداد سوابق پرداختی".decode("utf-8"),bg = self.LC,relief = Tkinter.GROOVE,width = self.MWW,height = self.MWH).grid(row = self.SR + 6,column = 2)
			Tkinter.Label(self.root,text = row[0],bg = self.LC,relief = Tkinter.GROOVE,width = self.MWW,height = self.MWH).grid(row = self.SR + 1,column = 1)
			Tkinter.Label(self.root,text = row[1],bg = self.LC,relief = Tkinter.GROOVE,width = self.MWW,height = self.MWH).grid(row = self.SR + 2,column = 1)
			Tkinter.Label(self.root,text = row[2],bg = self.LC,relief = Tkinter.GROOVE,width = self.MWW,height = self.MWH).grid(row = self.SR + 3,column = 1)
			Tkinter.Label(self.root,text = row[3],bg = self.LC,relief = Tkinter.GROOVE,width = self.MWW,height = self.MWH).grid(row = self.SR + 4,column = 1)
			Tkinter.Label(self.root,text = str(len(education_cursor.fetchall())),bg = self.LC,relief = Tkinter.GROOVE,width = self.MWW,height = self.MWH).grid(row = self.SR + 5,column = 1)
			Tkinter.Label(self.root,text = str(len(payment_cursor.fetchall())),bg = self.LC,relief = Tkinter.GROOVE,width = self.MWW,height = self.MWH).grid(row = self.SR + 6,column = 1)
			Tkinter.Button(self.root,text = "چاپ گزارش".decode("utf-8"),bg = self.BC,width = self.LWW,height = self.MWH,command = lambda: self.printReport(NATIONAL_CODE)).grid(row = self.SR + 7,column = 1,columnspan = 2)
		conn.close()

	def removeRecordForm(self):
		self.makeMainForm()
		Tkinter.Label(self.root,text = ":کد ملی".decode("utf-8"),bg = self.LC,relief = Tkinter.GROOVE,width = self.MWW,height = self.MWH).grid(row = self.SR,column = 2)
		Tkinter.Label(self.root,text = ":شماره ردیف".decode("utf-8"),bg = self.LC,relief = Tkinter.GROOVE,width = self.MWW,height = self.MWH).grid(row = self.SR + 2,column = 2)
		national_code_entry = Tkinter.Entry(self.root,relief = Tkinter.FLAT,width = self.MWW,bd = self.BDS)
		id_entry = Tkinter.Entry(self.root,relief = Tkinter.FLAT,width = self.MWW,bd = self.BDS)
		national_code_entry.grid(row = self.SR,column = 1)
		id_entry.grid(row = self.SR + 2,column = 1)
		Tkinter.Button(self.root,text = "حذف دانش‌آموز".decode("utf-8"),bg = self.BC,width = self.LWW,height = self.MWH,command = lambda: self.removeStudentFromDatabase(national_code_entry.get().encode("utf-8"))).grid(row = self.SR + 1,column = 1,columnspan = 2)
		Tkinter.Button(self.root,text = "حذف سابقه تحصیلی".decode("utf-8"),bg = self.BC,width = self.LWW,height = self.MWH,command = lambda: self.removeEducationFromDatabase(id_entry.get().encode("utf-8"))).grid(row = self.SR + 3,column = 1,columnspan = 2)
		Tkinter.Button(self.root,text = "حذف سابقه پرداختی".decode("utf-8"),bg = self.BC,width = self.LWW,height = self.MWH,command = lambda: self.removePaymentFromDatabase(id_entry.get().encode("utf-8"))).grid(row = self.SR + 4,column = 1,columnspan = 2)

	def printReport(self,NATIONAL_CODE):
		self.makeMainForm()
		conn = sqlite3.connect(self.DATABASE_PATH)
		cursor = conn.execute("SELECT * from Student WHERE NationalCode = '{}';".format(NATIONAL_CODE))
		student_record = cursor.fetchone()
		cursor = conn.execute("SELECT * from Education WHERE NationalCode = '{}';".format(NATIONAL_CODE))
		education_record_list = cursor.fetchall()
		education_record_html = ""
		for row in education_record_list:
			education_record_html += "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>\n".decode("utf-8").format(row[0],row[2],row[3],row[4])
		cursor = conn.execute("SELECT * from Payment WHERE NationalCode = '{}';".format(NATIONAL_CODE))
		payment_record_list = cursor.fetchall()
		payment_record_html = ""
		for row in payment_record_list:
			payment_record_html += "<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>\n".decode("utf-8").format(row[0],row[2],row[3],row[4])
		report_file = codecs.open(self.REPORT_FILE_PATH,"w",encoding = "utf-8")
		html = """
		<html dir = "rtl" lang = "fa">
		<head>
		<meta charset = "UTF-8">
		<style>
		table
		{{
			font-family: B Nazanin;
			font-size: 20px;
			text-align: right;
			line-height: 30px;
			border-bottom: 2px solid #975997;
			width: 700px;
			margin: 10px 10px;
		}}
		th
		{{
			text-align: center;
			border-top: 2px solid #975997;
			border-bottom: 2px solid #975997;
		}}
		</style>
		</head>
		<body>
		<img src = "{}">
		<table>
		<tr><th colspan = "2">مشخصات</th></tr>
		<tr><td>کد ملی:</td><td>{}</td></tr>
		<tr><td>نام:</td><td>{}</td></tr>
		<tr><td>نام خانوادگی:</td><td>{}</td></tr>
		<tr><td>نام پدر:</td><td>{}</td></tr>
		</table>
		<table>
		<tr><th colspan = "4">سوابق تحصیلی</th></tr>
		<tr><td>ردیف</td><td>تاریخ</td><td>سطح</td><td>نمره</td></tr>
		{}
		</table>
		<table>
		<tr><th colspan = "4">سوابق پرداختی</th></tr>
		<tr><td>ردیف</td><td>تاریخ</td><td>مقدار</td><td>توضیحات</td></td>
		{}
		</table>
		</body>
		</html>
		""".decode("utf-8").format(self.LOGO_IMAGE_NAME,student_record[0],student_record[1],student_record[2],student_record[3],education_record_html,payment_record_html)
		report_file.write(html)
		conn.close()
		report_file.close()
		os.system("start " + self.REPORT_FILE_PATH)
##########################################################


##########################################################
def main():
	dibagaran_institute = DibagaranInstitute()
##########################################################
	

##########################################################
if __name__ == "__main__":
	main()
##########################################################