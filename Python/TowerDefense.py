from tkinter import *
from tkinter import ttk
from types import prepare_class
from PIL import Image, ImageTk
import datetime
from math import *

class Application(Frame):  # Application is a Frame (inheritance from Frame)
    def __init__(self, master):
        Frame.__init__(self, master) 
        self.grid(sticky=N+S+E+W) # put frame in toplevel window
        self.createWidgets()
   
    def createWidgets(self):
        top=self.winfo_toplevel()
        top.geometry("500x500")
        #canvas = Canvas(self, width=500, height=500)
        #canvas.pack(expand=True, fill="both")


def main():
    root = Tk()
    app = Application(root)
    app.master.title("Min applikation")
    Canvas(app, width=500, height=500).pack()

    update(root,app)
    root.mainloop

def update(root,app):
   

    root.after(17, update, root, app)

if __name__ == "__main__":  
	main()