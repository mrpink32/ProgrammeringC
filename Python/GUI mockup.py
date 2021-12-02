from tkinter import *
from tkinter import ttk

def main_root():
    root = Tk()
    root.geometry('400x400')
    root.title('CPR validation program')
    root.rowconfigure(0,weight = 1)
    root.columnconfigure(0,weight = 1)

    frame = Frame(root,bg = "#555555",width = 100,height = 100)
    frame.grid(sticky = N+S+E+W)
    frame.rowconfigure(0,weight = 1)
    frame.rowconfigure(1,weight = 1)
    frame.rowconfigure(2,weight = 1)
    frame.columnconfigure(0,weight = 2)
    frame.columnconfigure(1,weight = 1)

    Data_L = Text(frame,bg = "#ffffff",width = 10, height = 1)
    Data_L.grid(row = 0,column = 0, sticky = N+S+E+W)

    R_CPR_B = Button(frame, bg ="grey",text = "I am useless", width = 10, height = 1)
    R_CPR_B.grid(row = 1, column = 0, sticky = N+S+E+W)

    CPRD_L = Label(frame,bg ="red",width = 10, height = 3)
    CPRD_L.grid(row=0, rowspan = 3, column = 1, sticky = N+S+E+W)

    E_B = Button(frame,width = 4,height = 1, bg = "white", text = "Quit",command = exit)
    E_B.grid(row = 2, column = 0, sticky = N+S+E+W)

    root.mainloop()


main_root()