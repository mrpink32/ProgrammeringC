import math
import datetime


def main():
    while True:
        try:
            cprnum = str(input("cpr-number: ")).replace("-","")
            if len(cprnum) == 10:
                if VerifyDate(cprnum):
                    if VerifyControlDigit(cprnum):
                        print(f"cpr-number is valid!\ndate of birth: {VerifyDate(cprnum)[1]}\ngender: {ReturnGender(int(cprnum[9]))}")
                        break
                    else:
                        print(f"cpr-number cannot be validated with modulus 11 but may still be valid!\ndate of birth: {VerifyDate(cprnum)[1]}\ngender: {ReturnGender(int(cprnum[9]))}")
                        print(f"Your cpr-number is in: {WithoutControlDigit(cprnum, ReturnGender(int(cprnum[9])))}")
                        break
                else:
                    print("Invalid date!")
            else:
                print("Illegal action, input has to be a ten character long number...")
        except ValueError:
            print("Illegal action, input has to be a valid number...")
    while True:
        try:
            command = str(input("try again? [y/n]: "))
            match command:
                case "y":
                    break
                case "n":
                    exit()
                case _:
                    print("Illegal action, input has to be a valid key...")
        except Exception as e:
            print(f"Illegal action, input has to be a valid key... {e}")
    main()
        
    


def VerifyControlDigit(data):
    weightedNumbers = []
    for x in range(0, 10):
        weightedNumbers.append(int(data[x]) * weights[x])
    controlDigitCheck = (sum(weightedNumbers) % 11)
    if controlDigitCheck == 0:
        return True


def WithoutControlDigit(data, gender):
    i = data[7:10]
    match gender:
        case "Male":
            for x in range(1, 1000, 6):
                if x == int(i):
                    return "series 1"
            for x in range(3, 1000, 6):
                if x == int(i):
                    return "series 2"
            for x in range(5, 1000, 6):
                if x == int(i):
                    return "series 3"
        case "Female":
            for x in range(2, 1000, 6):
                if x == int(i):
                    return "series 1"
            for x in range(4, 1000, 6):
                if x == int(i):
                    return "series 2"
            for x in range(6, 1000, 6):
                if x == int(i):
                    return "series 3"


def VerifyDate(data):
    try:
        day = f"{data[0:2]}"
        month = f"{data[2:4]}"
        year = f"{str(GetCentury(int(data[6]), int(data[4:6]))) + data[4:6]}"
        dIQ = datetime.date(int(year), int(month), int(day))
        if datetime.date.min < dIQ < datetime.date.max:
            return True, dIQ
    except (ValueError, TypeError):
        return False


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
    return "Female" if (data % 2) == 0 else "Male"


if __name__ == "__main__":
    weights = (4, 3, 2, 7, 6, 5, 4, 3, 2, 1)
    main()