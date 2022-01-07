import json
from socket import *
from threading import *
from utils import networking as nw
import utils


def setup():
    SERVER_CONFIG = json.load(open("utils/server_config.json"))
    match  SERVER_CONFIG['language']:
        case "en":
            answers = json.load(open("lang/en_us.json"))
        case "da":
            answers = json.load(open("lang/da_dk.json"))
        case "ja":
            answers = json.load(open("lang/ja_jp.json"))
    return SERVER_CONFIG['host'], SERVER_CONFIG['port'], SERVER_CONFIG['header_size'], answers


def main():
    ip, port, header_size, answers = setup()
    server = socket(AF_INET, SOCK_STREAM)
    print(answers['startup_message'].format(port))
    server.bind((ip, port))
    server.listen(1)
    while True:
        client, client_address = server.accept()
        print(f"Connection from {client_address} has been established!")
        nw.send_string(client, header_size, answers['welcome_message'])
        while True:
            command = nw.receive_string(client)
            print(command)
            #handle_command()
        client.close()


def handle_command(command):
    match command:
        case _:
            pass
        

if __name__ == "__main__":
    main()
