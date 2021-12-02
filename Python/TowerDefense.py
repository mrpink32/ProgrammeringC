from tkinter import *
from tkinter import ttk
from math import *
from PIL import Image, ImageTk


class TDG(Frame):
    def __init__(self, master = None):
        Frame.__init__(self,master) 
        self.grid(sticky = N+S+E+W)
    def createboard():
        pass
        

class BasicEnemy:
    def __init__(self, hitPoints, damageCount, moveSpeed):
        self.hitPoints = hitPoints
        self.damageCount = damageCount
        self.moveSpeed = moveSpeed


def main():
    root = Tk()
    app = TDG(root)
    app.master.title("Shitty monkey ripoff")
    gameLoop(app)
    app.mainloop()


def gameLoop(app):

    app.after(100, gameLoop)


if __name__ == "__main__":
    main()
