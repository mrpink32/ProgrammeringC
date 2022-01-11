from socket import *
from tkinter import *
from utils.networking import *


def main():
    ip, port, header_size, answers = config_setup()
    client = socket(AF_INET, SOCK_STREAM)
    while True:
        try:
            client.connect((ip, port))
            break
        except:
            print(answers['connection_fail_message'])
            continue
    print(answers['connected_message'])
    print(receive_string(client))
    client_handler(client)
    exit()
    # todo make a simple ui for easier interaction with the client


if __name__ == "__main__":
    main()
