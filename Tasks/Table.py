import Main


def table():
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
        command = str(input("try again? [y/n]: "))
        if command == "y":
            table()
            break
        elif command == "n":
            Main.main()
            break
        else:
            print("Illegal action, input not valid...")
