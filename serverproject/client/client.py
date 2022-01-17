import json
import ffmpeg
from socket import *
from tkinter import *


def config_setup():
    return CLIENT_CONFIG['host'], CLIENT_CONFIG['port']


def lang_setup():
    match  CLIENT_CONFIG['language']:
        case "en":
            return json.load(open("lang/en_us.json"))
        case "da":
            return json.load(open("lang/da_dk.json", encoding="utf-8"))
        case "ja":
            return json.load(open("lang/ja_jp.json", encoding="utf-8"))


# def send_message(receiver, message, header_size=SERVER_CONFIG['header_size']):
#     message = f"{len(message):<{header_size}}" + message
#     return receiver.send(message.encode("utf-8"))


def receive_string(receiver):
    # while True:
    #     message = receiver.recv(CLIENT_CONFIG['buffer_size'])
    #     if not message: 
    #         break
    # return str(message.decode("utf-8"))
    message = receiver.recv(CLIENT_CONFIG['buffer_size'])
    return str(message.decode("utf-8"))


def main():
    ip, port = config_setup()
    client = socket(AF_INET, SOCK_STREAM)
    while True:
        try:
            client.connect((ip, port))
            break
        except:
            print(LANG['connection_fail_message'])
            continue
    print(LANG['connected_message'])
    print(receive_string(client))
    client_handler(client)
    exit()
    # todo make a simple ui for easier interaction with the client


def client_handler(client):
    while True:
        message = str(input("Type command for server: "))
        client.sendall(message.encode("utf-8"))
        match message:
            case "disconnect":
                client.close()
                break
            case "music":
                something(client)
                continue
            case _:
                continue


def something(client):
    with open('temp', 'wb') as f:
        while True:
            l = client.recv(CLIENT_CONFIG['buffer_size'])
            if not l: break
            f.write(l)
    


if __name__ == "__main__":
    CLIENT_CONFIG = json.load(open("utils/client_config.json"))
    LANG = lang_setup()
    main()
