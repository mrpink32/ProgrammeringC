from tkinter import *
from tkinter import ttk

def main():
	mainWindow = Tk()
	frame = ttk.Frame(mainWindow, padding=10)
	frame.grid()

	style = ttk.Style()
	style.configure("Grim.TLabel", background="yellow")



	ttk.Label(frame, text="Grim", style="Grim.TLabel").grid(column=5, row=5)

	mainWindow.mainloop()


def ReturnWidth():
	mainWindow


if __name__ == '__main__':
	main()