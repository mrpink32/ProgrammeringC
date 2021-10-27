from tkinter import *
from tkinter import ttk

def main():
	mainWindow = Tk()

	labelStyle = ttk.Style()
	labelStyle.configure("Grim.TLabel", background="yellow")

	mainText = ttk.Label(mainWindow, text="Grim", style="Grim.TLabel")
	mainText.grid(column=1, row=1)
	#mainText.pack()

	

	button1 = ttk.Button(mainWindow, text="Quadratic formula")
	button1.grid(column=1, row=2)

	button2 = ttk.Button(mainWindow, text="Press me")
	button2.grid(column=1, row=3)
	
	button3 = ttk.Button(mainWindow, text="Press me")
	button3.grid(column=1, row=4)

	button4 = ttk.Button(mainWindow, text="Exit")
	button4.grid(column=1, row=5)

	mainWindow.mainloop()

	 
def ReturnWidth(item):
	Frame.grid_size
	return item.grid_size()


if __name__ == '__main__':
	main()