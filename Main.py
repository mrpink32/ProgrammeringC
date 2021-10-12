from Tasks import Table
from Tasks import QuadraticEquation
from Tasks import CPRChecker
import sys

operations = [1, 2, 3, 4]


def main():
    print(f"commands: \ntype {operations[0]} for Quadratic formula."
          f"\ntype {operations[1]} to generate a table of a given length."
          f"\ntype {operations[2]} to validate a CPR-number."
          f"\ntype {operations[3]} to exit the application.")
    while True:
        try:
            operation = int(input("choose an operation: "))
            match operation
                case operations[0]:
                    QuadraticEquation.quadraticFormula()
                    Retry(QuadraticEquation.quadraticFormula)
                case operations[1]:
                    Table.table()
                    Retry(Table.table)
                case operations[2]:
                    CPRChecker.CPRVerifier()
                    Retry(CPRChecker.CPRVerifier)
                case operations[3]:
                    exit()
                case _:
                    print("Illegal action, input has to be a valid number...")
        except ValueError:
            print("Illegal action, input has to be a valid number...")


def Retry(func):
    while True:
        command = str(input("try again? [y/n]: "))
        match command:
            case "y":
                func()
            case "n":
                break
            case _:
                print("Illegal action, input not valid...")


if __name__ == "__main__":
    main()
