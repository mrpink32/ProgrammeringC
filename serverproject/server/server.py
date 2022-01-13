import json
import threading
from socket import *
import _thread as thread

SERVER_CONFIG = json.load(open("utils/server_config.json"))

def lang_setup():
    match  SERVER_CONFIG['language']:
        case "en":
            return json.load(open("lang/en_us.json"))
        case "da":
            return json.load(open("lang/da_dk.json", encoding="utf-8"))
        case "ja":
            return json.load(open("lang/ja_jp.json", encoding="utf-8"))

language = lang_setup()

def config_setup():
    return (SERVER_CONFIG['host'], SERVER_CONFIG['port'], 
            SERVER_CONFIG['header_size'], SERVER_CONFIG['max_queue'], 
            SERVER_CONFIG['max_connections'], language)


def send_message(receiver, header_size, message):
    message = f"{len(message):<{header_size}}" + message
    return receiver.send(message.encode("utf-8"))


def receive_message(receiver):
    message = receiver.recv(1024)
    return str(message.decode("utf-8"))


def main():
    (ip, port, header_size, max_queue, max_connections, answers) = config_setup()
    if (ip != "localhost"):
        ip = gethostname()
    server = socket(AF_INET, SOCK_STREAM)
    print(answers['startup_message'].format(port))
    server.bind((ip, port))
    server.listen(max_queue)
    global current_connections
    current_connections = 0
    lock = threading.Lock()
    print(answers['started_message'].format(ip, port))
    while True:
        if current_connections < max_connections:
            client, client_address = server.accept()
            print(answers['connected_message'].format(client_address))
            send_message(client, header_size, answers['welcome_message'])
            thread.start_new_thread(client_handler, (client, client_address, lock))
            current_connections += 1
            print(threading.enumerate(), current_connections)
        

def client_handler(client, client_address, lock):
    while True:
        try:
            message = client.recv(1024)
            message = str(message.decode("utf-8"))
            print(message)
            match message:
                case "10        disconnect":
                    client.close()
                    break
                case _:
                    continue
        except:
            print(language['client_disconnect'].format(client_address))
            client.close()
            break
    with lock:
        global current_connections
        current_connections -= 1
    print("current_connections: {current_connections}")


if __name__ == "__main__":
    main()
