import math


def get_valid_input(text):
    while True:
        try:
            return float(input(text))
        except ValueError:
            print("Illegal action, input has to be a valid number...")
            continue


def quadratic_equation(a, b, c):
    ans_format = float(8.4)
    d = (math.pow(b, 2) - 4 * a * c)
    if d > 0:
        ans1 = (-b + math.sqrt(d)) / 2 * a
        ans2 = (-b - math.sqrt(d)) / 2 * a
        print(f"This quadratic formula has 2 answers: \n1: {ans1:>{ans_format}f} \n2: {ans2:>{ans_format}f}")
    elif d == 0:
        ans = (-b + math.sqrt(d)) / 2 * a
        print(f"This quadratic formula has 1 answer: {ans:>{ans_format}f}")
    elif d < 0:
        print("This quadratic formula has 0 answers:")


def main():
    while True:
        a = get_valid_input("a: ")
        b = get_valid_input("b: ")
        c = get_valid_input("c: ")
        quadratic_equation(a, b, c)
        while True:
            command = str(input("try again? [y/n]: "))
            match command:
                case "y":
                    break
                case "n":
                    exit()
                case _:
                    print("Illegal action, input has to be a valid key...")
                    continue


if __name__ == "__main__":
    main()