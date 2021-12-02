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
        for x in range(0, 99):
            self.rowconfigure(x, weight=1)
            self.columnconfigure(x, weight=1)
        self.populateGrid()
    def populateGrid(self):
        #grassImg = Image.open("D:/HTX/ProgrammeringC/Python/TowerDefenseResources/Grass.png")
        grassImg = PhotoImage(file="D:/HTX/ProgrammeringC/Python/TowerDefenseResources/Grass.png")
        grassImg.configure(height=1, width=1)
        grassTile = Label(self, image=grassImg)
        grassTile.grid(row=1, column=1) #, sticky=N+S+E+W
        print(grassTile.winfo_height(), grassTile.winfo_width())


        #grassImg = Image.
        #grassTile = ImageTk.BitmapImage(image=grassImg)
        #grassTile.grid(row=1,column=1)






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
