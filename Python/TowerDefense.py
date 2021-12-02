from tkinter import *
from tkinter import ttk
from math import *
from PIL import Image, ImageTk

class TDG(Frame):
    def __init__(self, master = None):
        Frame.__init__(self,master) 
        self.grid(sticky = N+S+E+W)

    def createboard():
        