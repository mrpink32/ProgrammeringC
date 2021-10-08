import math
import Main


ansFormat = float(8.4)


def quadraticFormula():
    a, b, c = None, None, None
    while True:
        try:
            if a is None:
                a = float(input("a: "))
            if a is not None and b is None:
                b = float(input("b: "))
            if b is not None and c is None:
                c = float(input("c: "))
            break
        except ValueError:
            print("Illegal action, input has to be a valid number...")
            if b is None:
                print(f"a: {a}")
            elif c is None:
                print(f"a: {a}")
                print(f"b: {b}")
    d = (math.pow(b, 2) - 4 * a * c)
    if d > 0:
        ans1 = (-b + math.sqrt(d)) / 2 * a
        ans2 = (-b - math.sqrt(d)) / 2 * a
        print(f"This quadratic formula has 2 answers: \n1: {ans1:>{ansFormat}f} \n2: {ans2:>{ansFormat}f}")
    elif d == 0:
        ans = (-b + math.sqrt(d)) / 2 * a
        print(f"This quadratic formula has 1 answer: {ans:>{ansFormat}f}")
    elif d < 0:
        print("This quadratic formula has 0 answers:")
    while True:
        command = str(input("try again? [y/n]: "))
        if command == "y":
            quadraticFormula()
            break
        elif command == "n":
            Main.main()
            break
        else:
            print("Illegal action, input not valid...")
