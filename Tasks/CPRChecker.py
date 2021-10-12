import Main
import math
import datetime


weights = (4, 3, 2, 7, 6, 5, 4, 3, 2, 1)


def CPRVerifier():
    while True:
        try:
            cprnum = str(input("cpr-number: "))
            if len(cprnum) == 10:
                break
            else:
                print("Illegal action, input has to be ten characters long...")
        except (IndexError, ValueError):
            print("Illegal action, input has to be a valid number...")
    if VerifyDate(cprnum):
        if VerifyControlDigit(cprnum):
            print(f"cpr-number is valid!\ndate of birth: {dIQ}\ngender: {ReturnGender(int(cprnum[9]))}")
        elif VerifyWithoutControlDigit(cprnum, ReturnGender(int(cprnum[9]))):
            print(f"cpr-number is valid!\ndate of birth: {dIQ}\ngender: {ReturnGender(int(cprnum[9]))}")
            print(f"You are ugly, your cpr-number is in: {VerifyWithoutControlDigit(cprnum, ReturnGender(int(cprnum[9])))[1]}")
        else:
            print("You actually didn't input a valid cpr-number how are you so bad?")
    else:
        print(f"date is invalid!")


def VerifyControlDigit(data):
    weightedNumbers = []
    for x in range(0, 10):
        weightedNumbers.append(int(data[x]) * weights[x])
    controlDigitCheck = (sum(weightedNumbers) % 11)
    if controlDigitCheck == 0:
        return True


def VerifyWithoutControlDigit(data, gender):
    i = data[7:10]
    match gender:
        case "Male":
            for x in range(1, 1000, 6):
                if x == int(i):
                    return True, "series 1"
            for x in range(3, 1000, 6):
                if x == int(i):
                    return True, "series 2"
            for x in range(5, 1000, 6):
                if x == int(i):
                    return True, "series 3"
        case "Female":
            for x in range(2, 1000, 6):
                if x == int(i):
                    return True, "series 1"
            for x in range(4, 1000, 6):
                if x == int(i):
                    return True, "series 2"
            for x in range(6, 1000, 6):
                if x == int(i):
                    return True, "series 3"


def VerifyDate(data):
    day = f"{data[0:2]}"
    month = f"{data[2:4]}"
    year = f"{str(GetCentury(int(data[6]), int(data[4:6]))) + data[4:6]}"
    global dIQ
    dIQ = datetime.date(int(year), int(month), int(day))
    if datetime.date.min < dIQ < datetime.date.max:
        return True


def GetCentury(x, y):
    match x:
        case 0 | 1 | 2 | 3:
            return 19
        case 4:
            return 20 if 0 < y < 37 else 19
        case 5 | 6 | 7 | 8:
            return 20 if 0 < y < 58 else 18 
        case 9:
            return 20 if 0 < y < 37 else 19


def ReturnGender(data):
    if (data % 2) == 0:
        return "Female"
    elif (data % 2) == 1:
        return "Male"
