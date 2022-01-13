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
        mainWin.columnconfigure(0, weight=1)
        
        #skal gøre sådan de der texts kommer ind.

        # styles
        #labelStyle = ttk.Style(self.master)
        #labelStyle.configure('Tlabel', background="#ff64ff")

        # labels
        ipL = Label(mainWin, text="Enter the ip")
        ipL.grid(row=0, column=0, sticky=N+S+E+W)
        poL = Label(mainWin, text="Enter port")
        poL.grid(row=2, column=0, sticky=N+S+E+W)

        #button
        eB = Button(mainWin,text="Exit", command = quit,bg ="#f0f0f0")
        eB.grid(row=3,column=0,sticky=N+S+E+W)
        # 2 entry 2 label
        # entry til ip, entry port, exit button, checkbox(hvis den findes), label til indikere guide
root = Tk()
app = Application(root)
app.master.title("Min applikation")
app.mainloop()
