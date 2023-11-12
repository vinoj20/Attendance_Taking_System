from MarkAttendance import Mark
from database import Database
import cv2
#import numpy as np
from pyzbar.pyzbar import decode
from tkinter import *
from PIL import ImageTk, Image
import os
import tkinter as tk
import time
import keyboard
from datetime import date,datetime

class GUI: 
    def __init__(self, root,code,id,LName):
        self.root = root
        self.code=code
        self.LName=LName
        self.id=id
        bg_color = '#c1cee3'
        self.division= tk.Frame(self.root, bg=bg_color)
        self.division.place(relx=0.5, rely=0.45, anchor="center")
        self.submit = Button(self.division, text='Click To Open Scanner', font=( 15), fg='black', bg='#11f08f', command=self.Start)
        self.root.bind('<Return>', lambda event: self.submit.invoke())
        self.submit.grid(row=1, column=3, padx=10, pady=10)
       
    
    def Start(self):
        self.division.destroy()  # Destroy the initial frame
        self.divisionload = tk.Frame(self.root, bg='white')
        self.divisionload.place(relx=0.5, rely=0.45, anchor="center")
        self.loading = ImageTk.PhotoImage(Image.open(r'Sources\BG\progress.png'))
        self.load = tk.Label(self.divisionload, image=self.loading)
        self.load.grid(row=0, column=0, padx=10, pady=30)
        self.root.after(500, self.open_scanner)

    def open_scanner(self):
        Scanner().Scanner(self.root,self.code, self.id, self.LName)

    def run(self):
        self.root.mainloop()
        

class Scanner:
    def Scanner(self,root, code,id,LName):
        self.root=root
        self.code=code
        self.LName=LName
        self.id=id
        
        self.camera = cv2.VideoCapture(0)
        self.students_list=[]
        self.Attendanded_RegNo=[]
        self.modeType=0
        self.counter=0
        self.y=0
        # Importing the mode images into a list
        folderModePath = 'Sources/Modes'
        modePathList = os.listdir(folderModePath)
        self.imgModeList = []
        for path in modePathList:
            self.imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))
        
        global imgBackground
        imgBackground=cv2.imread('Sources\Main.png')
        Date=date.today()

        if code and LName is not None: 
            cv2.putText(imgBackground, str(Date), (283, 572), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (252,3,7),2)
            cv2.putText(imgBackground, code, (242, 635), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (252,3,7),2)
            cv2.putText(imgBackground, LName, (257, 695), cv2.FONT_HERSHEY_SIMPLEX,1.3, (252,3,7),2)

            query = "SELECT * FROM tblstudentenroll WHERE tblstudentenroll.Cid = (SELECT tblsubject.id FROM tblsubject WHERE tblsubject.code = %s)"
            params=(code,)
            if Database().isconnected:
                row_count,result=Database().run_query(query,params)
                enrolled_students=row_count
                cv2.putText(imgBackground,str(enrolled_students), (571, 760), cv2.FONT_HERSHEY_SIMPLEX,1.3, (252,3,7),2)
        
        while True:
            success, frame = self.camera.read()
            if not success:
                break
            if keyboard.is_pressed('Shift+Esc'):
                cv2.destroyAllWindows()
                self.close_scanner(self.Attendanded_RegNo,self.code, self.id)
                break

            frame_resized = cv2.resize(frame, (459, 417))
            imgBackground[7:7 + 417, 7:7 + 459] = frame_resized
            imgBackground[7:7+417,474:474+286] = self.imgModeList[self.modeType]
            
    
            for barcode in decode(frame):
                myData = barcode.data.decode('utf-8')

                if myData not in self.students_list:
                    self.show(4,6,None)
                    self.students_list.append(myData)
                    time.sleep(1)
                    self.show(4,1,myData)
                    time.sleep(3)
                    if myData in self.students_list:
                        self.show(4,2,None)
                        time.sleep(1)
                    else:
                        self.modeType=self.value_change(0,1)
                else:
                    self.show(4,3,None)
                    time.sleep(1)
                    self.modeType=self.value_change(0,1)
            
            cv2.imshow("Attendance System", imgBackground)
            cv2.waitKey(1)     
        self.camera.release()      
        
    def value_change(self,change,seconds):
        time.sleep(seconds)
        return change

    def show(self, camera_division, details_division, data):
        self.data = data
        imgBackground[7:7 + 417, 7:7 + 459] = self.imgModeList[camera_division]
        imgBackground[7:7 + 417, 474:474 + 286] = self.imgModeList[details_division]
       
        if data is not None:
            profile, FullName, Regno = self.getdetails(data)
            
            if profile=="noresult" or profile=="tryagain":
                self.students_list.remove(data)
                imgBackground[7:7 + 417, 474:474 + 286] = self.imgModeList[5]
            else:
                if profile is None or not os.path.exists(r"Sources\students\\" + profile):
                    path = r"Sources\students\\unknown.jpg"
                else:
                    path = r"Sources\students\\" + profile

                student = cv2.imread(path)
                student = cv2.resize(student, (182, 182))
                imgBackground[26:26 + 182, 527:527 + 182] = student

                if FullName and Regno is not None: 
                    cv2.putText(imgBackground, FullName, (485, 265), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (50, 50, 50))
                    cv2.putText(imgBackground, Regno, (485, 310), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (50, 50, 50))
            
                self.Attendanded_RegNo.append(Regno)
                cv2.putText(imgBackground,str(len(self.Attendanded_RegNo))+".  "+Regno, (788, 75+self.y), cv2.FONT_HERSHEY_COMPLEX_SMALL,0.6, (0,0,0))
                current_time = time.localtime()
                timenow = time.strftime("%H:%M:%S", current_time)
                cv2.putText(imgBackground,timenow, (1100, 75+self.y), cv2.FONT_HERSHEY_COMPLEX_SMALL,0.7, (0,0,0))
                self.y+=13
                
        cv2.imshow("Attendance System", imgBackground)
        cv2.waitKey(1)
        
    def getdetails(self, data):
        database=Database()
        if database.isconnected:
            query = """SELECT tblstudents.Title, tblstudents.firstName, tblstudents.lastName,
                    tblstudents.RegNumber, tblprofile.Name
                    FROM tblstudents
                    JOIN tblprofile ON tblstudents.RegNumber = tblprofile.Student
                    Join tblstudentenroll on tblstudentenroll.SregNumber=tblstudents.Regnumber
                    WHERE tblstudents.Nicno = %s AND tblprofile.Student = (
                    SELECT RegNumber FROM tblstudents WHERE NicNo = %s)"""
                    
            params = (data,data) 
            row_count, result = database.run_query(query, params)
            if result:
                for row in result:
                    FullName = row['Title'] + "." + row['firstName'][0]+ "." + row['lastName']
                    Regno = row['RegNumber']
                    profile=row['Name']

                    return profile, FullName, Regno
            else:
                return 'noresult',None,None
        else:
            return 'tryagain',None,None
    
    def close_scanner(self,Attendanded_list,code,id):
        self.Attendanded_list=Attendanded_list
        self.id=id
        self.code=code
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.destroy()
        Mark(self.root,Attendanded_list, code, id)

        
        

