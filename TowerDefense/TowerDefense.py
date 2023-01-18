from tkinter import *
from math import *
#from PIL import Image, ImageTk
import Resources


class Application(Frame):  # Application is a Canvas (inheritance from Canvas)
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid(sticky=N+S+E+W)  # put canvas in toplevel window
        self.populateCanvas()

    def populateCanvas(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        img = PhotoImage(file="Resources\download.png")
        self.create_image(0, 0, anchor=NW, image=img)
        self.image = img
        self.create_line(0, 0, 50, 50)

    def update(self):
        self.master.after(1, self.update)


def main():
    app = Application(Tk())
    app.master.title("Monkey")
    #img = PhotoImage(file="Resources\download.png")
    #app.create_image(0, 0, anchor=NW, image=img)

    app.master.mainloop()


if __name__ == "__main__":
    main()
