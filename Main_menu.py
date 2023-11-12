from tkinter import *
from PIL import Image, ImageTk
from tkinter.ttk import Combobox
from datetime import date,datetime
from database import Database
from QR_Scanner import GUI

class Main_menu:

    def __init__(self,root,id,FullName):
        self.root=root
        self.id = id
        self.FullName=FullName
        database = Database()

        # Define the font settings
        font_style = "Times New Roman Bold"
        font_color = "black"
        bg_color = '#c1cee3'

        self.division = Frame(self.root)
        self.division.place(relx=0.42, rely=0.20, anchor="center")
        self.division_1= Frame(self.root, bg=bg_color)
        self.division_1.place(relx=0.5, rely=0.4,relheight=0.15, anchor="center")
        self.warning = Frame(root,bg=bg_color)
        self.warning.place(relx=0.5, rely=0.45, anchor="center")

        label_welcome = Label(self.division, text="Welcome "+FullName, font=(font_style, 40), fg="#c41f33")
        label_welcome.grid(row=1,column=0,padx=10, pady=10)
      
        self.label_subject = Label(self.division_1, text="Select Course for Attendance :", font=(font_style, 30), fg=font_color, bg=bg_color)
        self.label_subject.grid(row=1,column=0,padx=10, pady=10)
        
        query = "SELECT code,Name FROM tblsubject join tbllectureenroll on tblsubject.id=tbllectureenroll.Cid where tbllectureenroll.Lid=%s"
        params = (id,)
        row_count, result = database.run_query(query, params)
        if row_count>0 and result:
            value_list=[f"{row['code']} {row['Name']}" for row in result]
            self.select_code = Combobox(self.division_1, font=(font_style, 20), values=value_list)   
        else:
            self.select_code = Combobox(self.division_1, font=(font_style, 20), values="No_Course_Available",state="readonly")
        
        self.select_code.grid(row=1, column=2, padx=10, pady=10) 
        self.submit = Button(self.division_1, text='Process', font=(font_style, 15), fg='black', bg='#11f08f', command=self.process)
        self.root.bind('<Return>', lambda event: submit.invoke())
        self.submit.grid(row=1, column=3, padx=10, pady=10)

    def process(self):
        selected_value = self.select_code.get()
        if not selected_value :
            label_alert = Label(self.warning, text="First Select the Course...", font=("Times New Roman Bold", 20), bg="#c1cee3", fg="red")
            label_alert.grid(row=1, columnspan=2)
            self.root.after(1500, label_alert.destroy)
        else:
            code = selected_value.split()[0]
            id = self.id
            LName = self.FullName
            self.division.destroy()
            self.division_1.destroy()
            GUI(self.root, code, id, LName)



    def run(self):
        self.root.mainloop()
