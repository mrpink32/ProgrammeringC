from tkinter import *
from tkinter import ttk
import datetime
import math


size = 800
handSizes = 300, 200, 150


def main():
    root = Tk()
    root.title("Watch") 
    root.geometry(f"{size}x{size}")

    canvas = Canvas(root, width=size, height=size, background="#ff64ff")
    canvas.pack(expand=1, fill="both")
    #changeTimeInterval = Button(root)
    

    update(root, canvas)
    root.mainloop()


def update(root, canvas):
    timeHour = returnTime()[0]
    timeMinute = returnTime()[1]
    timeSecond = returnTime()[2]
    print(f"Time: {timeHour, timeMinute, timeSecond}")
    canvas.create_oval(size - 50, size - 50, size - 750, size - 750, width=5, fill="yellow")
    canvas.create_line(size/2, 100, size/2, 45, width=3, fill="#ffffff")
    canvas.create_line(size/2, size/2, size/2+returnPalcementWeights(hour=timeHour)[0], size/2+returnPalcementWeights(hour=timeHour)[1], width=5, fill="#00ff00")
    canvas.create_line(size/2, size/2, size/2+returnPalcementWeights(minute=timeMinute)[2], size/2+returnPalcementWeights(minute=timeMinute)[3], width=3, fill="#ff0000")
    canvas.create_line(size/2, size/2, size/2+returnPalcementWeights(second=timeSecond)[4], size/2+returnPalcementWeights(second=timeSecond)[5], width=1, fill="#000000")
    root.after(1000, update, root, canvas)


def returnPalcementWeights(hour=0, minute=0, second=0):
    vinkelHour = 90-(360/12)*(math.pi/180)*hour
    vinkelMinute = 90-(360/60)*(math.pi/180)*minute
    vinkelSecond = 90-(360/60)*(math.pi/180)*second
    #print(f"Angle: {vinkelHour, vinkelMinute, vinkelSecond}")
    xWeightHour = math.cos(-vinkelHour+0.465) * handSizes[0]
    yWeightHour = math.sin(-vinkelHour+0.465) * handSizes[0]
    xWeightMinute = math.cos(-vinkelMinute+0.465) * handSizes[1]
    yWeightMinute = math.sin(-vinkelMinute+0.465) * handSizes[1]
    xWeightsecond = math.cos(-vinkelSecond+0.465) * handSizes[2]
    yWeightsecond = math.sin(-vinkelSecond+0.465) * handSizes[2]
    #print(xWeightHour, yWeightHour, xWeightMinute, yWeightMinute, xWeightsecond, yWeightsecond)
    return xWeightHour, yWeightHour, xWeightMinute, yWeightMinute, xWeightsecond, yWeightsecond


def returnTime():
    time = datetime.datetime.now()
    #print(f"{time.hour}")
    return (time.hour-12, time.minute, time.second) if time.hour>12 else (time.hour, time.minute, time.second)


if __name__ == "__main__":
	main()
