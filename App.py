from tkinter import *
from PIL import Image, ImageTk
from login import Login

class App:
    def __init__(self):
        self.root = Tk()
        self.root.title("Attendance System")

        # Set the initial size of the window
        initial_width = self.root.winfo_screenwidth()
        initial_height = self.root.winfo_screenheight()
        self.root.geometry(f"{initial_width}x{initial_height}")
        #self.root.resizable(width=False, height=False)

        self.bg_image = ImageTk.PhotoImage(Image.open('Sources\BG/bg_fas.png'))
        self.bg_label = Label(self.root, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        Login(self.root).run()
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    App().run()
