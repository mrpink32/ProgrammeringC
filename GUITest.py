from tkinter import *
from tkinter import ttk

def main():
	mainWindow = Tk()

	labelStyle = ttk.Style()
	labelStyle.configure("Grim.TLabel", background="yellow")
	
	mainText = ttk.Label(mainWindow, text="Grim", style="Grim.TLabel")
	#.grid(column=5, row=5)
	mainText.pack()

	button1 = ttk.Button(mainWindow, text="Quadratic formula")
	button1.pack()

	button2 = ttk.Button(mainWindow, text="Press me")
	button2.pack()
	#vguguugyug
	button3 = ttk.Button(mainWindow, text="Press me")
	button3.pack()

	button4 = ttk.Button(mainWindow, text="Exit")
	button4.pack()

	print(ReturnWidth(mainWindow))
	mainWindow.mainloop()

	 
def ReturnWidth(item):
	Frame.grid_size
	return item.grid_size()


if __name__ == '__main__':
	main()