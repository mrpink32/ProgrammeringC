from tkinter import *
#Thought is to make a CPR checker with only 5 widgets
def main_root():
    #Making and 
    root = Tk()
    root.geometry('300x300')
    root.title('CPR validation program')
    
    frame = Frame(root,bg = "#d2d2d2",bd = 10)
    frame.grid(row = 0, column = 0)

    CPRentry = Entry(root,text = "insert your cpr number")
    CPRentry.grid(row = 0, column = 0)

    exitbutton = Button(frame,width = 4,height = 1, bg = "#ffffff", text = "Quit",command = exit)
    exitbutton.grid(row = 3,column = 3) 

    root.mainloop()

main_root()