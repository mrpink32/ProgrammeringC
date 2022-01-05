from tkinter import *
from math import *
#from PIL import Image, ImageTk
import Resources


class Application(Canvas):  # Application is a Canvas (inheritance from Canvas)
    def __init__(self, master):
        Canvas.__init__(self, master, width=500, height=500) 
        self.grid(sticky=N+S+E+W) # put canvas in toplevel window
        self.populateCanvas()
     
    def populateCanvas(self):
        img = PhotoImage(file="Resources\download.png")
        self.create_image(0, 0, anchor=NW, image=img)
        self.create_line(0,0,50,50)




def main():
    root = Tk()
    app = Application(root)
    app.master.title("Monkey")

    update(root, app)
    root.mainloop()

def update(root, app):
   

    root.after(17, update, root, app)


if __name__ == "__main__":  
	main()