from tkinter import *
from tkinter import ttk

class Application(Frame):  

    def __init__(self, master):
        Frame.__init__(self, master) 
        self.grid(sticky=N+S+E+W)
        self.shell()

    def shell(self):
        # window stuff
        mainWin = self.winfo_toplevel()
        for row in range(0,4):
            mainWin.rowconfigure(row, weight=1)     
        mainWin.columnconfigure(0, weight=1, minsize = 10)
        
        #texts
        ipT = Text(mainWin,width=10, height = 1)
        ipT.grid(row = 1, column = 0, sticky=N+S+E+W)
        pT = Text(mainWin,width=10, height = 1)
        pT.grid(row = 3, column = 0, sticky=N+S+E+W)

        # labels
        ipL = Label(mainWin, text="Enter the ip")
        ipL.grid(row=0, column=0, sticky=N+S+E+W)
        poL = Label(mainWin, text="Enter port")
        poL.grid(row=2, column=0, sticky=N+S+E+W)

        #button
        eB = Button(mainWin,text="Exit", command = quit,bg ="#f0f0f0")
        eB.grid(row=4,column=0,sticky=N+S+E+W)
       
         #checkbox(hvis den findes)
root = Tk()
app = Application(root)
app.master.title(" ")
app.mainloop()
