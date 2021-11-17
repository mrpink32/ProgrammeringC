from tkinter import *
from tkinter import ttk
from types import prepare_class
from PIL import Image, ImageTk
import datetime
from math import *


class WatchProperties:
    colorList = ["", "#AB2330", "#4169e1", "#136207"]
    def __init__(self, index=0, timeInterval12 = True):
        self.index = index
        self.watchDiscColor = self.colorList[self.index]
        self.timeInterval12 = timeInterval12
    def colorChange(self):
        self.index += 1 if self.index < len(self.colorList)-1 else (-self.index)
        self.watchDiscColor = self.colorList[self.index]
    def insertColor(self, newColor):
        print(f"{newColor} is already in the list") if newColor in self.colorList else (self.colorList.append(newColor), print(f"{newColor} added"))
    def timeIntervalChange(self):
        self.timeInterval12 = False if self.timeInterval12 else True


def main():
    root = Tk()
    root.title("AnalogWatch") 

    canvas = Canvas(root, width=400, height=400, background="#ffffff")
    canvas.pack(expand=True, fill="both")

    wp = WatchProperties()

    changeTimeIntervalButton = Button(canvas, text="Change time interval", command=wp.timeIntervalChange)
    changeTimeIntervalButton.place(anchor="nw")

    colorbutton = Button(canvas, text="Color changer", command=wp.colorChange)
    colorbutton.place(relx=0.70,height=25,width=120)

    ColorInsertEntry=Entry(canvas, text="Insert Hex color")
    ColorInsertEntry.place(x=0, y=25)
    ColorInsertButton=Button(canvas, text="Add color", command=lambda:wp.insertColor(ColorInsertEntry.get()))
    ColorInsertButton.place(x=0, y=40)

    update(root, canvas, wp)
    root.mainloop()


def update(root, canvas, wp):
    # Deleting everything and returning window size and time
    size = root.winfo_height() if root.winfo_height() < root.winfo_width() else root.winfo_width()
    time = getTime(wp.timeInterval12)
    dateDayMonth = getDate()
    canvas.delete('all')

    # Creating watch disc
    drawCircle(canvas, size/2, size/2, size/2-15, size/100, color=wp.watchDiscColor)

    # Populates watch disc with text showing time and date realted stuff
    drawText(canvas, size/2, size/2, -size/3, f"Date: {dateDayMonth[0]}\nMonth: {getMonth(dateDayMonth[0].month)}\nWeek: {dateDayMonth[1]}\nDay: {getDay(dateDayMonth[2])}")
    drawText(canvas, size/2, size/2, size/2.75, f"{time[0]}:{time[1]}:{time[2]}")
    
    # Creating ticks 
    drawTicks(canvas, size/2, size/2, size/2-15)

    # Creates time hands
    drawHourHand(canvas, size/2, size/2, size/5, time, "#00ff00")
    drawMinuteHand(canvas, size/2, size/2, size/4, time, "#ff0000")
    drawSecondHand(canvas, size/2, size/2, size/3, time, "#0000ff")
    
    # Creates a circle in the middle to cover the origin of the hourhands
    drawCircle(canvas, size/2, size/2, size/100, color="black")

    root.after(100, update, root, canvas, wp)


def drawCircle(canvas, xCenter, yCenter, r, borderWidth=1, color="#ffffff"):
    canvas.create_oval(xCenter-r, yCenter-r, xCenter+r, yCenter+r, width=borderWidth, fill=color)


def drawHourHand(canvas, x, y, handSize, time, color="#000000"):
    vinkel = (360/12)*time[0]-90
    vinkelMinuteOffset = ((360/60)*time[1])/12
    canvas.create_line(x, y, x+cos(radians(vinkel+vinkelMinuteOffset)) * handSize, y+sin(radians(vinkel+vinkelMinuteOffset)) * handSize, width=(x+y)/100+2, fill=color)


def drawMinuteHand(canvas, x, y, handSize, time, color="#000000"):
    vinkel = (360/60)*time[1]-90
    vinkelSecondOffset = ((360/60)*time[2])/60
    canvas.create_line(x, y, x+cos(radians(vinkel+vinkelSecondOffset)) * handSize, y+sin(radians(vinkel+vinkelSecondOffset)) * handSize, width=(x+y)/100+1, fill=color)


def drawSecondHand(canvas, x, y, handSize, time, color="#000000"):
    vinkel = (360/60)*time[2]-90
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


def drawText(canvas, x, y, yOffset, text):
    canvas.create_text(x, y+yOffset, text=text)


def getTime(timeInterval12):
    time = datetime.datetime.now()
    if timeInterval12:
        #print(time.hour%12, time.minute, time.second, time.microsecond) if time.hour>12 else print(time.hour, time.minute, time.second, time.microsecond)
        return (time.hour%12, time.minute, time.second, time.microsecond) #if time.hour>12 else (time.hour, time.minute, time.second, time.microsecond)
    else:
        #print(time.hour, time.minute, time.second, time.microsecond) 
        return (time.hour, time.minute, time.second, time.microsecond) 
    

def getDate():
    date = datetime.date.today()
    return (date, date.isocalendar().week, date.isocalendar().weekday)


def getDay(day):
    match day:
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


def getMonth(month):
    match month:
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


if __name__ == "__main__":
	main()