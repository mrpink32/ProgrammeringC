import sys
import json
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


def send_string(receiver, header_size, message):
    message = f"{len(message):<{header_size}}" + message
    return receiver.send(message.encode("utf-8"))


def receive_string(receiver):
    message = receiver.recv(1024)
    return str(message.decode("utf-8"))


def client_handler(client, client_address):
    #thread_lock = thread.allocate_lock()
    while True:
        try:
            message = client.recv(1024)
            message = str(message.decode("utf-8"))
            #thread_lock.acquire()
            print(message)
            #thread_lock.release()
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
    thread.exit()
    #sys.exit()