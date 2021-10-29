from tkinter import *
from tkinter import ttk
import datetime
import math
from typing import Any


size = 800


def main():
    root = Tk()
    root.title("Min applikation") 
    root.geometry(f"{size}x{size}")   #  geometry("800x800")

    canvas = Canvas(root, width=size, height=size, background="#ff64ff")
    canvas.pack(expand=1, fill="both")

    update(root, canvas)
    root.mainloop()


def update(root, canvas):
    canvas.delete("all")
    t = datetime.datetime.now()
    print(t)
    canvas.create_oval(size - 50, size - 50, size - 750, size - 750, width=2, fill='yellow')
    canvas.create_line(size/2, size-750, size/2, size/2, width=5, fill='black')
    root.after(1000, update, root, canvas)



if __name__ == "__main__":
	main()
