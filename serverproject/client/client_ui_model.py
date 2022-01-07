from tkinter import *
from tkinter import ttk

def somethingtosquikkelprogram():
    #root stuff
    root = Tk()
    root.rowconfigure(0,weight = 1)
    root.columnconfigure(0,weight = 1)
    root.title("Trade offer: you: get cocked i: get to cock someone")

    #window stuff
    mainWin = Frame(root,background="#111119", width = 450, height = 250)
    mainWin.grid(sticky = N+S+E+W)
    mainWin.rowconfigure(0,weight = 1)
    mainWin.columnconfigure(0,weight = 1)
    
    #styles if needed
    labelStyle = ttk.Style()
    labelStyle.configure("labelt", background = "grey")
    #buttonStyle = ttk.Style()
	#buttonStyle.configure("[enternavnpåstyle]", background="yellow")

    #labels
    ipL = Label(mainWin,text = "Enter the ip", style = "labelt")
    ipL.grid(row = 0, column = 0, sticky = N+S+E+W)

	#2 entry 2 label
    #entry til ip, entry port, exit button, checkbox(hvis den findes), label til indikere guide 
    root.mainloop()
    
somethingtosquikkelprogram()