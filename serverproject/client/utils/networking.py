import json
from socket import *

def config_setup():
    CLIENT_CONFIG = json.load(open("utils/client_config.json"))
    match  CLIENT_CONFIG['language']:
        case "en":
            answers = json.load(open("lang/en_us.json"))
        case "da":
            answers = json.load(open("lang/da_dk.json", encoding="utf-8"))
        case "ja":
            answers = json.load(open("lang/ja_jp.json", encoding="utf-8"))
    return (CLIENT_CONFIG['host'], CLIENT_CONFIG['port'], 
            CLIENT_CONFIG['header_size'], answers)


def send_string(sender, header_size, message):
    message = f"{len(message):<{header_size}}" + message
    return sender.send(message.encode("utf-8"))


def receive_string(receiver):
    message = receiver.recv(1024)
    return str(message.decode("utf-8"))


def command_handler(client):
    command = receive_string(client)
    print(command)
    match command:
        case "10        disconnect":
            client.close()
        case _:
            pass
