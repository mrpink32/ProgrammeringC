import json
from socket import *

def config_setup():
    SERVER_CONFIG = json.load(open("utils/server_config.json"))
    match  SERVER_CONFIG['language']:
        case "en":
            answers = json.load(open("lang/en_us.json"))
        case "da":
            answers = json.load(open("lang/da_dk.json", encoding="utf-8"))
        case "ja":
            answers = json.load(open("lang/ja_jp.json", encoding="utf-8"))
    return (SERVER_CONFIG['host'], SERVER_CONFIG['port'], 
            SERVER_CONFIG['header_size'], SERVER_CONFIG['max_queue'], 
            SERVER_CONFIG['max_connections'], answers)


def send_string(sender, header_size, message):
    message = f"{len(message):<{header_size}}" + message
    sender.send(message.encode("utf-8"))


def receive_string(receiver):
    message = receiver.recv(1024)
    return str(message.decode("utf-8"))


def handle_command(client, thread):
    thread.aqquire()
    command = receive_string()
    match command:
        case "disconnect":
            client.close()
            thread.release()
        case _:
            thread.release()
            pass
    

