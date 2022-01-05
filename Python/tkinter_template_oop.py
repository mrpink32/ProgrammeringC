#-------------------------------------------------------------------------------
# Name:        tkinter demo app
# Purpose:
#
# Author:      josa
#
# Created:     15-01-2020
#-------------------------------------------------------------------------------
from tkinter import *
import sys

class Application(Frame):  # Application is a Frame (inheritance from Frame)
    def __init__(self, master):
        Frame.__init__(self, master) 
        self.grid(sticky=N+S+E+W) # put frame in toplevel window
        self.createWidgets()

    def commandHandler(self, bNo):
        print("Cmd handler called: " + str(bNo))
   
    def createWidgets(self):
        top=self.winfo_toplevel()
        #top.geometry("500x500")
        top.rowconfigure(0, weight=1)     # toplevel window rows scalable
        top.columnconfigure(0, weight=1)  # toplevel window colums scalable

        # rows with minimum size and equal weights
        for row in range(0,3):
            self.rowconfigure(row, weight=1 , minsize=100)

        # columns with different scale
        for i in range(0,3):
            self.columnconfigure(i, weight=i, minsize=200)

        # create 2 labels
        colors = ('yellow', 'green')    
        for row in range(0,2):
            l=Label(self, text=f'row:{row}', justify="left", bg=colors[row])
            l.grid(row=row, column=0, sticky=S+W+N+E)

        # create 3 buttons
        for i in range(0,3):
            self.columnconfigure(i, weight=i) # , minsize=200
            def cmd(no=i):  # hidden argument trick
                self.commandHandler(no)  
            Button(self, text=str(i), command=cmd).grid(row=2, column=i, sticky=N+S+E+W)

root = Tk()

app = Application(root)
app.master.title("Min applikation")
app.mainloop()
