from socket import *
from threading import *
from utils.networking import *


def main():
    (ip, port, header_size, max_qeueu, max_connections, answers) = config_setup()
    server = socket(AF_INET, SOCK_STREAM)
    print(answers['startup_message'].format(port))
    server.bind((ip, port))
    server.listen(max_qeueu)
    while True:
        client, client_address = server.accept()
        print(answers['connected_message'].format(client_address))
        send_string(client, header_size, answers['welcome_message'])
        while True:
            try:
                command = receive_string(client)
                print(command)
            except:
                print(answers['client_disconnect'].format(client_address))
                client.close()
                break
            #handle_command(command)
        

if __name__ == "__main__":
    main()
