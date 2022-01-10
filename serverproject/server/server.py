from socket import *
from utils.networking import *


def main():
    (ip, port, header_size, max_queue, max_connections, answers) = config_setup()
    if (ip != "localhost"):
        ip = gethostname()
    server = socket(AF_INET, SOCK_STREAM)
    print(answers['startup_message'].format(port))
    server.bind((ip, port))
    # todo translate server started message
    print(answers['started_message'].format(ip, port))
    while True:
        server.listen(max_queue)
        client, client_address = server.accept()
        # todo figure out how to thread in python and implement
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


if __name__ == "__main__":
    main()
