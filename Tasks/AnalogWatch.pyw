from tkinter import *
from tkinter import ttk
import datetime
import math


size = 400
offset = 0.465, 0


def main():
    root = Tk()
    root.title("AnalogWatch") 
    root.geometry(f"{size}x{size}")

    canvas = Canvas(root, width=size, height=size, background="#ffffff")
    canvas.pack(expand=1, fill="both")
    #changeTimeInterval = Button(root)

    update(root, canvas)
    root.mainloop()


def update(root, canvas):
    timeHour = returnTime()[0]
    timeMinute = returnTime()[1]
    timeSecond = returnTime()[2]
    print(f"Time: {timeHour, timeMinute, timeSecond}")

    canvas.delete('all')
    size = root.winfo_height() if root.winfo_height() < root.winfo_width() else root.winfo_width()
    #print(size)

    canvas.create_oval(size/2-(size/2-15), size/2-(size/2-15), size/2+(size/2-15), size/2+(size/2-15), width=size/100, fill="#ff64ff")

    canvas.create_line(size/2, size/2-(size/2-15), size/2, size/10, width=size/100, fill="#000000")#; print(15+size/10)
    canvas.create_line(size/2, size-size/10, size/2, size/2+(size/2-15), width=size/100, fill="#000000")#; print(size-size/10-size-15)
    canvas.create_line(size/2-(size/2-15), size/2, size/10, size/2, width=size/100, fill="#000000")#; print(15+size/10)
    canvas.create_line(size-size/10, size/2, size/2+(size/2-15), size/2, width=size/100, fill="#000000")#; print(size-size/10-size-15)

    handSizes = size/3, size/4, size/5
    canvas.create_line(size/2, size/2, size/2+returnPalcementWeights(handSizes, hour=timeHour)[0], size/2+returnPalcementWeights(handSizes, hour=timeHour)[1], width=size/100+2, fill="#00ff00")
    canvas.create_line(size/2, size/2, size/2+returnPalcementWeights(handSizes, minute=timeMinute)[2], size/2+returnPalcementWeights(handSizes, minute=timeMinute)[3], width=size/100+1, fill="#ff0000")
    canvas.create_line(size/2, size/2, size/2+returnPalcementWeights(handSizes, second=timeSecond)[4], size/2+returnPalcementWeights(handSizes, second=timeSecond)[5], width=size/100, fill="#0000ff")
    
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


if __name__ == "__main__":
	main()
