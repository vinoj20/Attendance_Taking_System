from tkinter import *

class End:
    def __init__(self,root):
        self.root=root

         # Define the font settings
        font_style = "Times New Roman Bold"
        font_color = "black"
        bg_color = '#c1cee3'
        font_size=20
        
        self.division = Frame(self.root,bg='#c1cee3')
        self.division.place(relx=0.5, rely=0.4, anchor="center")

        label_alert = Label(self.division, text="Attendance Marked Succesfully..", font=("Times New Roman Bold", 40), bg='#c1cee3', fg="green")
        label_alert.grid(row=0, column=1)

        submit = Button(self.division, text='Click to End', font=(font_style, 20), fg='black', bg='red',command=self.End)
        self.root.bind('<Return>', lambda event: submit.invoke())
        submit.grid(row=1, columnspan=2, padx=10, pady=10)

    def End(self):
        self.root.destroy()