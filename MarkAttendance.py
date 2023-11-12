from tkinter import *
from datetime import date,datetime
from database import Database
from tkinter.ttk import Combobox
from End import End

class Mark: 
    def __init__(self,root,Attendanded_list,code,id):
        self.root=root
        
        # Define the font settings
        font_style = "Times New Roman Bold"
        font_color = "black"
        bg_color = '#c1cee3'
        font_size=20

        self.Attendanded_list=Attendanded_list
        self.id=id
        self.code=code
        Total_students=len(Attendanded_list)
        self.enrolled_students=[]

        if Database().isconnected:
            query = "SELECT * FROM tblsubject WHERE code = %s"
            params = (code,)
            row_count, result = Database().run_query(query, params)
            if result:
                for row in result:
                   self.Cid=row['id']

        if Database().isconnected:
            query = "SELECT SRegNumber FROM tblstudentenroll where Cid=%s"
            params=(self.Cid,)
            row,result=Database().run_query(query,params)
            for row in result:
                name=row['SRegNumber']
                self.enrolled_students.append(name)

        if Database().isconnected:
            query ="SELECT sessionName,semesterId from tblacademic WHERE isActive=%s"
            params=("Active",)
            row_count, result = Database().run_query(query, params)
            if result:
                for row in result:
                    self.Academic_year=row['sessionName']
                    self.semester=row['semesterId']
                    
        if Database().isconnected:
            query ="SELECT year from tblsubject WHERE id=%s"
            params=(self.Cid,)
            row_count, result = Database().run_query(query, params)
            if result:
                for row in result:
                    self.year=row['year']


        self.division_top = Frame(self.root,bg='#c1cee3')
        self.division_top.place(relx=0.5, rely=0.2, anchor="center")
        self.division_content=Frame(self.root,bg='#c1cee3')
        self.division_content.place(relx=0.5,rely=0.5,relheight=0.3,relwidth=0.6,anchor='center')
        self.warning = Frame(root,bg='#c1cee3')
        self.warning.place(relx=0.5, rely=0.6, anchor="center")

        label_Date= Label(self.division_top, text="Date : "+str(date.today()), font=(font_style, 25), fg='red',bg='#c1cee3')
        label_Date.grid(row=1, column=1, padx=10, pady=10)
        label_code = Label(self.division_top, text="Course Code : "+str(code), font=(font_style, 30), fg='#c41f33',bg='#c1cee3')
        label_code.grid(row=1, column=3, padx=10, pady=10)

        label_code = Label(self.division_content, text="Total Attendant : "+str(len(self.Attendanded_list))+"/"+str(len(self.enrolled_students)), font=(font_style,30), fg=font_color, bg=bg_color)
        label_code.grid(row=1, column=0, padx=10, pady=10)
        
        #if any Student fail to scan But they Attend
        label_fail = Label(self.division_content, text="If any Student Fail in Scanning process :", font=(font_style, 20), fg=font_color, bg=bg_color)
        label_fail.grid(row=2, column=0, padx=10, pady=10)

        
        self.value_list=[]
        if (len(self.Attendanded_list)==len(self.enrolled_students)):
            self.Add = Combobox(self.division_content, font=(font_style, 20), values="No_Data_Available",state="readonly") 
        else:
            for student in self.enrolled_students:
                if student not in self.Attendanded_list:
                    self.value_list.append(student)
            self.Add = Combobox(self.division_content, font=(font_style, 20), values=self.value_list)  
        self.Add.grid(row=2, column=1, padx=10, pady=10) 

        submit = Button(self.division_content, text='+', font=(font_style, 15), fg='black', bg='white',command=self.AddRegNo)
        self.root.bind('<Return>', lambda event: submit.invoke())
        submit.grid(row=2, column=2, padx=10, pady=10)

        label_hours = Label(self.division_content, text="No of Hours Taken :", font=(font_style, 20), fg=font_color, bg=bg_color)
        label_hours.grid(row=3, column=0, padx=10, pady=10)
        self.entry_hours = Entry(self.division_content, font=(font_style,20), fg=font_color)
        self.entry_hours.grid(row=3, column=1, padx=10, pady=10)
        submit = Button(self.division_content, text='Mark', font=(font_style, 15), fg='black', bg='#11f08f',command=self.process)
        self.root.bind('<Return>', lambda event: submit.invoke())
        submit.grid(row=3, column=2, padx=10, pady=10)
    
    def AddRegNo(self):
        Addstudent=self.Add.get()
        self.Attendanded_list.append(Addstudent)
        self.value_list.remove(Addstudent)
        label_alert = Label(self.warning, text=str(Addstudent)+" Added successfully..", font=("Times New Roman Bold", 20), bg='#c1cee3', fg="green")
        label_alert.grid(row=4, columnspan=2)
        self.root.after(1500, label_alert.destroy)

        self.Add.set("")
        self.Add['values']=self.value_list

    def process(self):
        TotalHours=self.entry_hours.get()
        Attendanded_list=self.Attendanded_list
        enrolled_students=self.enrolled_students
        Academic_year=self.Academic_year
        year=self.year
        semester=self.semester
        Cid=self.Cid
        Lid=self.id
        Date=date.today()
        failedinMark=[]
 
        if not TotalHours:
            label_alert = Label(self.warning, text="Please enter No of Hours...", font=("Times New Roman Bold", 20), bg='#c1cee3', fg="Red")
            label_alert.grid(row=4, columnspan=2)
            self.root.after(1500, label_alert.destroy)
        elif not Attendanded_list or not enrolled_students or not Academic_year or not year or not semester or not Cid or not Lid or not Date:
            label_alert = Label(self.warning, text="There Was An Error Try Again...!", font=("Times New Roman Bold", 20), bg='#c1cee3', fg="red")
            label_alert.grid(row=4, columnspan=2)
            self.root.after(1500, label_alert.destroy)
        else:    
            self.division_top.destroy()
            self.division_content.destroy()
            
            self.division=Frame(self.root,bg='#c1cee3')
            self.division.place(relx=0.5,rely=0.5,relheight=0.3,relwidth=0.6,anchor='center')

            for Regno in enrolled_students:
                if Regno in Attendanded_list:
                    status='1'
                else:
                    status='0'

                if Database().isconnected:
                    insert_query = "INSERT INTO tblattendance (Academic_year,year,semester,Cid,Lid,RegNo,status,dateTaken) VALUES (%s, %s,%s, %s,%s, %s,%s, %s)"
                    insert_params = (Academic_year,year,semester,Cid,Lid,Regno,status,Date)
                    row_count = Database().perform_insert(insert_query, insert_params)
                    if row_count<1:
                        failedinMark.append(Regno)
            row_count =Database().perform_update_subtraction('tblhoursremain', 'RemainHours','courseId',TotalHours,Cid)
            End(self.root)
       
    def run(self):
        self.root.mainloop()


