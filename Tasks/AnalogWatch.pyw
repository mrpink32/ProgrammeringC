from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import datetime
from math import *


colorNumber = 0
currentColor = "#ffffff"


def main():
    root = Tk()
    root.title("AnalogWatch") 

    canvas = Canvas(root, width=400, height=400, background="#ffffff")
    canvas.pack(expand=1, fill="both")

    changeTimeIntervalButton = Button(canvas, text="Change time interval")
    changeTimeIntervalButton.place(anchor="nw")

    colorbutton = Button(canvas, text="Color changer", command=changethecolor)
    colorbutton.place(relx=0.70,height=25,width=120)

    #image = Image.open("D:\GitHub\ProgrammeringC\Extra\Screenshot 2021-10-30 214304.png");
    #image = ImageTk.PhotoImage(image)

    update(root, canvas)
    root.mainloop()


def update(root, canvas):
    # Deleting everything and returning window size
    canvas.delete('all')
    size = root.winfo_height() if root.winfo_height() < root.winfo_width() else root.winfo_width()
    print(colorNumber, currentColor)
    # m�ske boller fill mig, kunne v�re.

    # Creating watch disc
    drawCircle(canvas, size/2, size/2, size/2-15, size/100, color=currentColor)
    
    #image = Image.open("D:\GitHub\ProgrammeringC\Extra\Screenshot 2021-10-30 214304.png");
    #image = ImageTk.PhotoImage(image)5
    #test = Label(canvas, image=image)
    #test.image = image
    #test.place(x=1, y=1)

    # Creating ticks 
    drawTicks(canvas, size/2, size/2, size/2-15)

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
    canvas.create_line(x, y, x+cos(radians(vinkel)) * handSize, y+sin(radians(vinkel)) * handSize, width=(x+y)/100+2, fill=color)


def drawMinuteHand(canvas, x, y, handSize, color="#000000"):
    vinkel = (360/60)*returnTime()[1]-90
    canvas.create_line(x, y, x+cos(radians(vinkel)) * handSize, y+sin(radians(vinkel)) * handSize, width=(x+y)/100+1, fill=color)


def drawSecondHand(canvas, x, y, handSize, color="#000000"):
    vinkel = (360/60)*returnTime()[2]-90
    canvas.create_line(x, y, x+cos(radians(vinkel)) * handSize, y+sin(radians(vinkel)) * handSize, width=(x+y)/100, fill=color)


def drawTicks(canvas, x, y, r, color="#000000"):
    v = 12
    for i in range(1, 13):
        cosTicks, sinTicks = cos(radians(360/v*i-90)), sin(radians(360/v*i-90))
        canvas.create_line(x+cosTicks*r, y+sinTicks*r, x+cosTicks*(x-x/5), y+sinTicks*(y-y/5), width=x*2/100, fill=color)
    v = 60
    for i in range(1, 61):
        cosTicks, sinTicks = cos(radians(360/v*i-90)), sin(radians(360/v*i-90))
        canvas.create_line(x+cosTicks*r, y+sinTicks*r, x+cosTicks*(x-x/6), y+sinTicks*(y-y/6), width=1, fill=color)


def returnTime():
    time = datetime.datetime.now()
    return (time.hour%12, time.minute, time.second)
    

def changethecolor():
    global currentColor
    global colorNumber
    match colorNumber:
        case 0:
            #newestcolor = "#AB2330"
            colorNumber += 1
            currentColor = "#AB2330"
            #return "#AB2330"
        case 1:
            #newestcolor = "#4169e1"
            colorNumber += 1
            currentColor = "#4169e1"
            #return "#4169e1"
        case 2:
            #newestcolor = "#136207"
            colorNumber += 1
            currentColor = "#136207"
            #return "#136207"
        case _:
            colorNumber = 0
            currentColor = "#ffffff"


if __name__ == "__main__":
	main()
