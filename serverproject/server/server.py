from socket import *
from utils.networking import *


def main():
    (ip, port, header_size, max_queue, max_connections, answers) = config_setup()
    if (ip != "localhost"):
        ip = gethostname()
    server = socket(AF_INET, SOCK_STREAM)
    print(answers['startup_message'].format(port))
    server.bind((ip, port))
    server.listen(max_queue)
    print(answers['started_message'].format(ip, port))
    while True:
        client, client_address = server.accept()
        print(answers['connected_message'].format(client_address))
        send_string(client, header_size, answers['welcome_message'])
        client_handler(client, client_address)


if __name__ == "__main__":
    main()
