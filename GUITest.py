from tkinter import *
from tkinter import ttk


def main():
	root = Tk()

	mainWindow = Frame(root, background="#FF64FF")
	mainWindow.grid()

#region Styles
	labelStyle = ttk.Style()
	labelStyle.configure("Grim.TLabel", background="yellow")

	buttonStyle = ttk.Style()
	buttonStyle.configure("Grim.TButton", background="yellow")
#endregion

	mainText = ttk.Label(mainWindow, text="Grim", style="Grim.TLabel")
	mainText.grid(columnspan=100, row=1)
	 
	button1 = ttk.Button(mainWindow, text="Quadratic formula", style="Grim.TButton")
	button1.grid(columnspan=100, row=2)

	button2 = ttk.Button(mainWindow, text="Table", style="Grim.TButton")
	button2.grid(columnspan=100, row=3)
	
	button3 = ttk.Button(mainWindow, text="CprChecker")
	button3.grid(column=1, row=4)

	button4 = ttk.Button(mainWindow, text="Exit", command=exit)
	button4.grid(column=1, row=6)

	button5 = ttk.Button(mainWindow, text="GUI Mockup", command=exit)
	button5.grid(column=1, row=5)

	mainWindow.mainloop()


if __name__ == '__main__':
	main()