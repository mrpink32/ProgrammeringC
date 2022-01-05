

def main():
    while True:
        try:
            size = int(input("please input your desired size of the table: "))
            break
        except ValueError:
            print("Illegal action, input has to be a valid number...")
    for i in range(1, size + 1):
        for j in range(1, size + 1):
            print(f"|{i*j:>5}", end="")
        print("|")
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


if __name__ == "__main__":
    main()