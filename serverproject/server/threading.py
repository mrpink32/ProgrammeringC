from socket import *
import _thread as thread
from utils.networking import *


def main():
    (ip, port, header_size, max_queue, max_connections, answers) = config_setup()
    if (ip != "localhost"):
        ip = gethostname()
    server = socket(AF_INET, SOCK_STREAM)
    print(answers['startup_message'].format(port))
    server.bind((ip, port))
    # todo add server stated message
    current_connections = 0
    clients = []
    while True:
        server.listen(max_queue)
        #if current_connections < max_connections:
        client_handler = thread.allocate_lock()
        client, client_address = server.accept()
        clients.append(client)
        #thread.start_new_thread(handle_command, (clients[current_connections], client_handler))
        #current_connections += 1
        # todo figure out how to thread in python and implement
        print(answers['connected_message'].format(client_address))
        send_string(client, header_size, answers['welcome_message'])
        thread.start_new_thread(handle_command, (clients[current_connections], client_handler))
        current_connections += 1
        while True:
            try:
                command = receive_string(client)
                print(command)
            except:
                print(answers['client_disconnect'].format(client_address))
                client.close()
                current_connections -= 1
                break
            handle_command(command)


if __name__ == "__main__":
    main()
