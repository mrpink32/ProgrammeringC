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
            if operation == operations[0]:
                QuadraticEquation.quadraticFormula()
            elif operation == operations[1]:
                Table.table()
            elif operation == operations[2]:
                CPRChecker.CPRVerifier()
            elif operation == operations[3]:
                exit()
            else:
                print("Illegal action, input has to be a valid number...")
        except ValueError:
            print("Illegal action, input has to be a valid number...")


if __name__ == "__main__":
    main()
