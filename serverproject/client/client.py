from socket import *
from tkinter import *
import networking as nw


def main():
    client = socket(AF_INET, SOCK_STREAM)
    while True:
        try:
            client.connect(("localhost", 9600))
            break
        except:
            print("Failed to connect to server... retrying...")
            continue
    print("Connection to server has been established!")
    print(nw.receive_string(client))
    while True:
        command = str(input("Type command for server: "))
        nw.send_string(client, command)
    # todo make a simple ui for easier interaction with the client


if __name__ == "__main__":
    main()
