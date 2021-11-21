from tkinter import *
from tkinter import ttk

#Thought is to make a CPR checker with 5 or less widgets
def main_root():
    root = Tk()
    print(root.winfo_geometry())
    root.geometry('400x400')
    root.update()
    print(root.winfo_geometry())
    #root.title('CPR validation program')
    
    root.rowconfigure(0,weight = 1)
    root.columnconfigure(0,weight = 1)

    frame = Frame(root,bg = "#d2d2d2",width = 100,height = 100)
    frame.grid(sticky = N+S+E+W)
    print(root.winfo_geometry())

    #CPR_EUL = Label(frame,bg = "#555555",width = 10, height = int(10/3))
    #CPR_EUL.grid(row = 0,column = 0)
    CPRentry = Entry(root,text = "insert your cpr number",width = int(root.winfo_width()/2))
    CPRentry.grid(row = 0, column = 0,sticky = N+W)
    print(root.winfo_geometry())
    
    #Entry doesnt quite work with .grid it seems, i think it doenst registre it as a object in the grid.
    #CPRentry was supposed to be in the far left corner but the exit button just underlaps it. i might work around it. by placing a lable underneath.

    

    #exitbutton = Button(frame,width = 4,height = 1, bg = "#ffffff", text = "Quit",command = exit)
    #exitbutton.grid 

    root.mainloop()


main_root()