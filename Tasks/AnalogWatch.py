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
    canvas.pack(expand=YES, fill=BOTH)

    update(root, canvas)
    root.mainloop()


def update(root, canvas):
    canvas.delete(all)



if __name__ == "__main__":
	main()
