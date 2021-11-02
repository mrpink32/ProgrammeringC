from os import X_OK
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import datetime
import math


offset = 0.465, 0


def main():
    root = Tk()
    root.title("AnalogWatch") 

    canvas = Canvas(root, width=400, height=400, background="#ffffff")
    canvas.pack(expand=1, fill="both")

    changeTimeIntervalButton = Button(canvas, text="Change time interval")
    changeTimeIntervalButton.place(anchor="nw")

    #image = Image.open("D:\GitHub\ProgrammeringC\Extra\Screenshot 2021-10-30 214304.png");
    #image = ImageTk.PhotoImage(image)

    update(root, canvas)
    root.mainloop()


def update(root, canvas):
    print(0.465*(180/math.pi))
    # Gets the time and assigns it
    timeHour = returnTime()[0]
    timeMinute = returnTime()[1]
    timeSecond = returnTime()[2]
    print(f"Time: {timeHour, timeMinute, timeSecond}")

    # Deleting everything and returning window size
    canvas.delete('all')
    size = root.winfo_height() if root.winfo_height() < root.winfo_width() else root.winfo_width()
    #print(size)

    # Creating watch disc
    canvas.create_oval(size/2-(size/2-15), size/2-(size/2-15), size/2+(size/2-15), size/2+(size/2-15), width=size/100, fill="#ff64ff")

    #image = Image.open("D:\GitHub\ProgrammeringC\Extra\Screenshot 2021-10-30 214304.png");
    #image = ImageTk.PhotoImage(image)
    #test = Label(canvas, image=image)
    #test.image = image
    #test.place(x=1, y=1)

    # Creating ticks
    canvas.create_line(size/2, size/2-(size/2-15), size/2, size/10, width=size/100, fill="#000000")#; print(15+size/10)
    canvas.create_line(size/2, size-size/10, size/2, size/2+(size/2-15), width=size/100, fill="#000000")#; print(size-size/10-size-15)
    canvas.create_line(size/2-(size/2-15), size/2, size/10, size/2, width=size/100, fill="#000000")#; print(15+size/10)
    canvas.create_line(size-size/10, size/2, size/2+(size/2-15), size/2, width=size/100, fill="#000000")#; print(size-size/10-size-15)

    # Creates hourhands
    handSizes = size/5, size/4, size/3
    canvas.create_line(size/2, size/2, size/2+returnPalcementWeights(handSizes, hour=timeHour)[0], size/2+returnPalcementWeights(handSizes, hour=timeHour)[1], width=size/100+2, fill="#00ff00")
    canvas.create_line(size/2, size/2, size/2+returnPalcementWeights(handSizes, minute=timeMinute)[2], size/2+returnPalcementWeights(handSizes, minute=timeMinute)[3], width=size/100+1, fill="#ff0000")
    canvas.create_line(size/2, size/2, size/2+returnPalcementWeights(handSizes, second=timeSecond)[4], size/2+returnPalcementWeights(handSizes, second=timeSecond)[5], width=size/100, fill="#0000ff")
    
    # Creates a circle in the middle to cover the origin of the hourhands
    canvas.create_oval(size/2-size/100, size/2-size/100, size/2+size/100, size/2+size/100, fill="#000000")
    
    root.after(100, update, root, canvas)


def returnPalcementWeights(handSizes, hour=0, minute=0, second=0):
    vinkelHour = 90-(360/12)*(math.pi/180)*hour
    vinkelMinute = 90-(360/60)*(math.pi/180)*minute
    vinkelSecond = 90-(360/60)*(math.pi/180)*second
    #print(f"Angle: {vinkelHour, vinkelMinute, vinkelSecond}")
    xWeightHour = math.cos(-vinkelHour+offset[0]) * handSizes[0]
    yWeightHour = math.sin(-vinkelHour+offset[0]) * handSizes[0]
    xWeightMinute = math.cos(-vinkelMinute+offset[0]) * handSizes[1]
    yWeightMinute = math.sin(-vinkelMinute+offset[0]) * handSizes[1]
    xWeightsecond = math.cos(-vinkelSecond+offset[0]) * handSizes[2]
    yWeightsecond = math.sin(-vinkelSecond+offset[0]) * handSizes[2]
    #print(xWeightHour, yWeightHour, xWeightMinute, yWeightMinute, xWeightsecond, yWeightsecond)
    return (xWeightHour, yWeightHour, xWeightMinute, yWeightMinute, xWeightsecond, yWeightsecond)


def returnTime():
    time = datetime.datetime.now()
    #print(f"{time.hour}")
    return (time.hour-12, time.minute, time.second) if time.hour>12 else (time.hour, time.minute, time.second)


def changeTimeInterval():
    pass

if __name__ == "__main__":
	main()
