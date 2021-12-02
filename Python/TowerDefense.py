from tkinter import *
from math import *
from PIL import Image, ImageTk


class TDG(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master) 
        self.grid(sticky = N+S+E+W)
        self.createGrid()
    def createGrid(self):
        top = self.winfo_toplevel()
        top.geometry("500x500")
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        for i in range(0, 99):
            self.rowconfigure(i, weight=1)
            self.columnconfigure(i, weight=1)
        self.populateGrid()
    def populateGrid(self):
        # Why no work: https://www.youtube.com/watch?v=NoTM8JciWaQ
        grassImg = ImageTk.PhotoImage(Image.open("D:/HTX/ProgrammeringC/Python/TowerDefenseResources/Grass.png"))
        grassTile = Label(self, bg="#5eff5e", text="test", height=10, width=10) #, image=grassImg
        grassTile.grid(row=1, column=1) #, sticky=N+S+E+W
        print(grassTile.winfo_height(), grassTile.winfo_width())


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

    app.after(100, gameLoop, app)


if __name__ == "__main__":
    main()
