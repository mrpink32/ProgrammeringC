from socket import *
from threading import *
import networking as nw


def main():
    server = socket(AF_INET, SOCK_STREAM)
    print(f"starting server on port: {nw.NETWORKING_CONFIG['port']}...")
    server.bind((nw.NETWORKING_CONFIG['host'], nw.NETWORKING_CONFIG['port']))
    server.listen(1)
    while True:
        client, client_address = server.accept()
        print(f"Connection from {client_address} has been established!")
        message = "Welcome to the srver!"
        #message = "サーバーへようこそ"
        nw.send_string(client, message)
        while True:
            command = nw.receive_string(client)
            print(command)
            #handle_command()
        client.close()


def handle_command(command):
    match command:
        case _:
            pass
        

if __name__ == "__main__":
    main()
