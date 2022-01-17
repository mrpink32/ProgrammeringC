import json
import ffmpeg
import threading
from socket import *
import _thread as thread


def config_setup():
    return SERVER_CONFIG['host'], SERVER_CONFIG['port']


def lang_setup():
    match  SERVER_CONFIG['language']:
        case "en":
            return json.load(open("lang/en_us.json"))
        case "da":
            return json.load(open("lang/da_dk.json", encoding="utf-8"))
        case "ja":
            return json.load(open("lang/ja_jp.json", encoding="utf-8"))


# def send_message(receiver, message, header_size=SERVER_CONFIG['header_size']):
#     message = f"{len(message):<{header_size}}" + message
#     return receiver.send(message.encode("utf-8"))


def receive_message(receiver):
    message = receiver.recv(SERVER_CONFIG['buffer_size'])
    return str(message.decode("utf-8"))


def main():
    ip, port = config_setup()
    if (ip != "localhost"):
        ip = gethostname()
    server = socket(AF_INET, SOCK_STREAM)
    print(LANG['startup_message'].format(port))
    server.bind((ip, port))
    server.listen(SERVER_CONFIG['max_queue'])
    global current_connections
    current_connections = 0
    lock = threading.Lock()
    print(LANG['started_message'].format(ip, port))
    while True:
        if current_connections < SERVER_CONFIG['max_connections']:
            client, client_address = server.accept()
            print(LANG['connected_message'].format(client_address))
            client.sendall(LANG['welcome_message'].encode("utf-8"))
            thread.start_new_thread(client_handler, (client, client_address, lock))
            current_connections += 1
            print(threading.enumerate(), current_connections)


def client_handler(client, client_address, lock):
    while True:
        try:
            message = receive_message(client)
            print(LANG['client_message'].format(message))
            match message:
                case "disconnect":
                    client.close()
                    break
                case "music":
                    file = open("temp.wav", 'rb')
                    for l in file:
                        client.sendall(l)
                    break
                case _:
                    continue
        except:
            print(LANG['client_disconnect'].format(client_address))
            client.close()
            break
    with lock:
        global current_connections
        current_connections -= 1
    print(LANG['connection_count'].format(current_connections))


if __name__ == "__main__":
    SERVER_CONFIG = json.load(open("utils/server_config.json"))
    LANG = lang_setup()
    main()
