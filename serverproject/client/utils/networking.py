import json
from socket import *

CLIENT_CONFIG = json.load(open("utils/client_config.json"))

def lang_setup():
    match  CLIENT_CONFIG['language']:
        case "en":
            return json.load(open("lang/en_us.json"))
        case "da":
            return json.load(open("lang/da_dk.json", encoding="utf-8"))
        case "ja":
            return json.load(open("lang/ja_jp.json", encoding="utf-8"))

language = lang_setup()

def config_setup():
    return CLIENT_CONFIG['host'], CLIENT_CONFIG['port'] 


def receive_string(receiver):
    message = receiver.recv(1024)
    return str(message.decode("utf-8"))


def client_handler(client, header_size=CLIENT_CONFIG['header_size']):
    while True:
        message = str(input("Type command for server: "))
        data = f"{len(message):<{header_size}}" + message
        client.send(data.encode("utf-8"))
        match message:
            case "disconnect":
                client.close()
                break
            case "music":
                play_music()
                continue
            case _:
                continue
