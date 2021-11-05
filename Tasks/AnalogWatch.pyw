from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import datetime
from math import *


def main():
    root = Tk()
    root.title("AnalogWatch") 

    canvas = Canvas(root, width=400, height=400, background="#ffffff")
    canvas.pack(expand=1, fill="both")

    changeTimeIntervalButton = Button(canvas, text="Change time interval")
    changeTimeIntervalButton.place(anchor="nw")

    Colorbutton = Button(canvas, text="Color changer", command = changethecolor)
    Colorbutton.place(relx=0.70,height=25,width=120)

    #image = Image.open("D:\GitHub\ProgrammeringC\Extra\Screenshot 2021-10-30 214304.png");
    #image = ImageTk.PhotoImage(image)

    update(root, canvas)
    root.mainloop()


def update(root, canvas):
    # Deleting everything and returning window size
    canvas.delete('all')
    size = root.winfo_height() if root.winfo_height() < root.winfo_width() else root.winfo_width()
    coolcolor = "#ffffff"
    newestcolor = coolcolor 
    # m�ske boller fill mig, kunne v�re.
    # Creating watch disc
    drawCircle(canvas, size/2, size/2, size/2-15, size/100, color=newestcolor)
    
    #image = Image.open("D:\GitHub\ProgrammeringC\Extra\Screenshot 2021-10-30 214304.png");
    #image = ImageTk.PhotoImage(image)5
    #test = Label(canvas, image=image)
    #test.image = image
    #test.place(x=1, y=1)

    # Creating ticks 
    drawTicks(canvas, size/2, size/2-15)

    # Creates time hands
    drawHourHand(canvas, size/2, size/2, size/5, "#00ff00")
    drawMinuteHand(canvas, size/2, size/2, size/4, "#ff0000")
    drawSecondHand(canvas, size/2, size/2, size/3, "#0000ff")
    
    # Creates a circle in the middle to cover the origin of the hourhands
    drawCircle(canvas, size/2, size/2, size/100, color="black")
    
    root.after(100, update, root, canvas)


def drawCircle(canvas, xCenter, yCenter, r, borderWidth=1, color="#ffffff"):
    canvas.create_oval(xCenter-r, yCenter-r, xCenter+r, yCenter+r, width=borderWidth, fill=color)


def drawHourHand(canvas, x, y, handSize, color="#000000"):
    vinkel = (360/12)*returnTime()[0]-90
    canvas.create_line(x, y, x+cos(radians(vinkel)) * handSize, y+sin(radians(vinkel)) * handSize, width=(x+y)/100, fill=color)


def drawMinuteHand(canvas, x, y, handSize, color="#000000"):
    vinkel = (360/60)*returnTime()[1]-90
    canvas.create_line(x, y, x+cos(radians(vinkel)) * handSize, y+sin(radians(vinkel)) * handSize, width=(x+y)/100, fill=color)


def drawSecondHand(canvas, x, y, handSize, color="#000000"):
    vinkel = (360/60)*returnTime()[2]-90
    canvas.create_line(x, y, x+cos(radians(vinkel)) * handSize, y+sin(radians(vinkel)) * handSize, width=(x+y)/100, fill=color)


# c is the center of the screen
def drawTicks(canvas, c, r, color="#000000"):
    v = 12
    for i in range(1, 13):
        cosTicks = cos(radians(360/v*i-90))
        sinTicks = sin(radians(360/v*i-90))
        canvas.create_line(c+cosTicks*r, c+sinTicks*r, c+cosTicks*(c-c/10), c+sinTicks*(c-c/10), width=c*2/100, fill=color)
    v = 60
    for i in range(1, 61):
        cosTicks = cos(radians(360/v*i-90))
        sinTicks = sin(radians(360/v*i-90))
        canvas.create_line(c+cosTicks*r, c+sinTicks*r, c+cosTicks*(c-c/10), c+sinTicks*(c-c/10), width=1, fill=color)


def returnTime():
    time = datetime.datetime.now()
    return (time.hour%12, time.minute, time.second)
    

def changethecolor():
    for newcolor in range (0,3):
        match newcolor:
            case 0:
                newestcolor = "#AB2330"
                return newestcolor
            case 1:
                newestcolor = "#4169e1"
                return newestcolor
            case _:
                newestcolor = "#136207"
                return newestcolor

if __name__ == "__main__":
	main()
