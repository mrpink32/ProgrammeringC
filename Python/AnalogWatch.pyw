from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import datetime
from math import *


class WatchColor:
    colorList = ("#ffffff", "#AB2330", "#4169e1", "#136207")
    def __init__(self, index=0):
        self.index = index
        self.currentColor = self.colorList[self.index]
    def colorChange(self):
        self.index += 1 if self.index < len(colorList)-1 else (-self.index)
        #print(self.index)
        self.currentColor = self.colorList[self.index]
    def Insertcolor(self, newcolor):
        pass    



def main():
    root = Tk()
    root.title("AnalogWatch") 

    canvas = Canvas(root, width=400, height=400, background="#ffffff")
    canvas.pack(expand=True, fill="both")

    #changeTimeIntervalButton = Button(canvas, text="Useless button\n(Change time interval)")
    #changeTimeIntervalButton.place(anchor="nw")

    wc = WatchColor()
    colorbutton = Button(canvas, text="Color changer", command=wc.colorChange)
    colorbutton.place(relx=0.70,height=25,width=120)

    Colorinsertentry=Entry(canvas, text="Insert Hex color")
    55Colorinsertentry.place("nw")


    #image = Image.open("D:\GitHub\ProgrammeringC\Extra\Screenshot 2021-10-30 214304.png");
    #image = ImageTk.PhotoImage(image)

    update(root, canvas, wc)
    root.mainloop()


def update(root, canvas, wc):
    # Deleting everything and returning window size
    canvas.delete('all')
    size = root.winfo_height() if root.winfo_height() < root.winfo_width() else root.winfo_width()

    # Creating watch disc
    drawCircle(canvas, size/2, size/2, size/2-15, size/100, color=wc.currentColor)
    drawText(canvas, size/2, size/2, -size/3, f"Date: {getDate()[0]}\nMonth: {gettingmonth()}\nWeek: {getDate()[1]}\nDay: {gettingday()}")
    drawText(canvas, size/2, size/2, size/2.75, f"{getTime()[0]}:{getTime()[1]}:{getTime()[2]}")
    
    #Trash:
    #image = Image.open("D:\GitHub\ProgrammeringC\Extra\Screenshot 2021-10-30 214304.png");
    #image = ImageTk.PhotoImage(image)
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

    root.after(100, update, root, canvas, wc)


def drawCircle(canvas, xCenter, yCenter, r, borderWidth=1, color="#ffffff"):
    canvas.create_oval(xCenter-r, yCenter-r, xCenter+r, yCenter+r, width=borderWidth, fill=color)


def drawHourHand(canvas, x, y, handSize, color="#000000"):
    vinkel = (360/12)*getTime()[0]-90
    vinkelMinuteOffset = ((360/60)*getTime()[1])/12
    canvas.create_line(x, y, x+cos(radians(vinkel+vinkelMinuteOffset)) * handSize, y+sin(radians(vinkel+vinkelMinuteOffset)) * handSize, width=(x+y)/100+2, fill=color)


def drawMinuteHand(canvas, x, y, handSize, color="#000000"):
    vinkel = (360/60)*getTime()[1]-90
    canvas.create_line(x, y, x+cos(radians(vinkel)) * handSize, y+sin(radians(vinkel)) * handSize, width=(x+y)/100+1, fill=color)


def drawSecondHand(canvas, x, y, handSize, color="#000000"):
    vinkel = (360/60)*getTime()[2]-90
    #v3 = ((360/100)*getTime()[3])/1000000
    canvas.create_line(x, y, x+cos(radians(vinkel)) * handSize, y+sin(radians(vinkel)) * handSize, width=(x+y)/100, fill=color)


    # maybe make a hand to show current month, maybe also weekday
    #have done that in terms of displaying the current month


def drawTicks(canvas, x, y, r, color="#000000"):
    v = 12
    for i in range(1, 13):
        cosTicks, sinTicks = cos(radians(360/v*i-90)), sin(radians(360/v*i-90))
        canvas.create_line(x+cosTicks*r, y+sinTicks*r, x+cosTicks*(x-x/5), y+sinTicks*(y-y/5), width=x*2/100, fill=color)
    v = 60
    for i in range(1, 61):
        cosTicks, sinTicks = cos(radians(360/v*i-90)), sin(radians(360/v*i-90))
        canvas.create_line(x+cosTicks*r, y+sinTicks*r, x+cosTicks*(x-x/6), y+sinTicks*(y-y/6), width=1, fill=color)


def drawText(canvas, x, y, yOffset, text):
    canvas.create_text(x, y+yOffset, text=text)


def getTime(timeIntervalBool=True):
    time = datetime.datetime.now()
    print(time.hour%12, time.minute, time.second, time.microsecond) if time.hour>12 else print(time.hour, time.minute, time.second, time.microsecond)
    return (time.hour%12, time.minute, time.second, time.microsecond) if time.hour>12 else (time.hour, time.minute, time.second, time.microsecond) 
#if timeIntervalBool == True else (time.hour, time.minute, time.second, time.microsecond)
    

def getDate():
    date = datetime.date.today()
    return (date, date.isocalendar().week, date.isocalendar().weekday)


def gettingday():
    match getDate()[2]:
        case 1:
            return "Monday"
        case 2:
            return "Tuesday"
        case 3:
            return "Wednesday"
        case 4:
            return "Thursday"
        case 5:
            return "Friday"
        case 6:
            return "Saturday"
        case 7:
            return "Sunday"
#Just shows which day it is


def gettingmonth():
    match datetime.datetime.now().month:
        case 1:
            return "January"
        case 2:
            return "February"
        case 3:
            return "March"
        case 4:
            return "April"
        case 5:
            return "May"
        case 6:
            return "June"
        case 7:
            return "July"
        case 8:
            return "August"
        case 9:
            return "September"
        case 10:
            return "October"
        case 11:
            return "November"
        case 12:
            return "December"
        #Just shows which month it is



if __name__ == "__main__":
	main()