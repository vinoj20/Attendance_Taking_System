from tkinter import *
import bcrypt
from database import Database
from  Main_menu import Main_menu

class Login:
    def __init__(self,root):
        self.root=root
        # Define the font settings
        font_style = "Times New Roman Bold"
        font_size = 40
        font_color = "black"
        self.bg_color = '#c1cee3'

        
        self.division_login = Frame(root,bg=self.bg_color)
        self.division_login.place(relx=0.5, rely=0.45,relheight=0.45, anchor="center")
        self.warning = Frame(root,bg=self.bg_color)
        self.warning.place(relx=0.5, rely=0.6, anchor="center")
        
        label_username = Label(self.division_login, text="UserName :", font=(font_style, font_size), fg=font_color, bg=self.bg_color)
        label_username.grid(row=0, column=0, padx=10, pady=10)
        label_password = Label(self.division_login, text="Password :", font=(font_style, font_size), fg=font_color, bg=self.bg_color)
        label_password.grid(row=1, column=0, padx=10, pady=10)
        self.entry_username = Entry(self.division_login, font=(font_style, font_size), fg=font_color)
        self.entry_username.grid(row=0, column=1, padx=10, pady=10)
        self.entry_password = Entry(self.division_login, show="*", font=(font_style, font_size), fg=font_color)
        self.entry_password.grid(row=1, column=1, padx=10, pady=10)
        submit = Button(self.division_login, text='Login', font=(font_style, 20), fg='black', bg='#11f08f', command=self.login)
        self.root.bind('<Return>', lambda event: submit.invoke())
        submit.grid(row=3, columnspan=4, padx=10, pady=10)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get().encode('utf-8')
     
        if not username or not password:
            label_alert = Label(self.warning, text="Fill all fields", font=("Times New Roman Bold", 20), bg=self.bg_color, fg="red")
            label_alert.grid(row=4, columnspan=2)
            self.root.after(1500, label_alert.destroy)
            self.entry_username.delete(0, END)
            self.entry_password.delete(0, END)
        else:
            database = Database()
            if database.isconnected:
                query = "SELECT * FROM tbllecturer WHERE emailAddress = %s"
                params = (username,)
                row_count, result = database.run_query(query, params)
                if result:
                    for row in result:
                        id=row['Id']
                        pw=row['password'].encode('utf-8')
                        FullName=row['Title']+"."+row['firstName']+" "+row['lastName']
                    if bcrypt.checkpw(password,pw) :  
                        self.division_login.destroy()
                        self.warning.destroy()
                        Main_menu(self.root, id, FullName)
                    else:
                        label_alert = Label(self.warning, text="Incorrect password or username", font=("Times New Roman Bold", 20), bg=self.bg_color, fg="red")
                        label_alert.grid(row=4, columnspan=2)
                        self.root.after(1500, label_alert.destroy)
                        self.entry_username.delete(0, END)
                        self.entry_password.delete(0, END)    
                else:
                    label_alert = Label(self.warning, text="Incorrect password or username", font=("Times New Roman Bold", 20), bg=self.bg_color, fg="red")
                    label_alert.grid(row=4, columnspan=2)
                    self.root.after(1500, label_alert.destroy) 
                    self.entry_username.delete(0, END)
                    self.entry_password.delete(0, END)
            else:
                    label_alert = Label(self.warning, text="An error occured Try Again..later", font=("Times New Roman Bold", 20), bg=self.bg_color, fg="red")
                    label_alert.grid(row=4, columnspan=2)
                    self.root.after(1500, label_alert.destroy) 
                    self.entry_username.delete(0, END)
                    self.entry_password.delete(0, END)

    def run(self):
        self.root.mainloop()


