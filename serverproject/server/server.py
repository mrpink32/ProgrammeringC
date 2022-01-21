import json
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


def send_message(receiver, message):
    packet = f"{len(message):<{SERVER_CONFIG['header_size']}}" + message
    return receiver.send(packet.encode("utf-8"))


def receive_message(receiver):
    message = ''
    new_packet = True
    while True:
        packet = receiver.recv(SERVER_CONFIG['buffer_size'])
        if new_packet:
            packet_length = int(packet[:SERVER_CONFIG['header_size']])
            new_packet = False
        message += packet.decode("utf-8")
        if len(message)-SERVER_CONFIG['header_size'] == packet_length:
            return str(message[SERVER_CONFIG['header_size']:])


def send_file(receiver, path):
    with open(path, "rb") as file:
        for line in file: 
            receiver.sendall(line)


def receive_file(receiver): # take path as argument
        with open("temp.wav", "wb") as file:
            while True:
                packet = receiver.recv(1024)
                if not packet: 
                    break
                file.write(packet)


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
            send_message(client, LANG['welcome_message'])
            thread.start_new_thread(client_handler, (client, client_address, lock))
            current_connections += 1
            print(LANG['connection_count'].format(current_connections)) #threading.enumerate()


def client_handler(client, client_address, lock):
    while True:
        try:
            message = receive_message(client)
            print(LANG['client_message'].format(message))
            match message:
                case "disconnect":
                    client.close()
                    break
                case "send":
                    path = "music\TeraIO_wav\09 Flamewall.wav"
                    send_file(client, path)
                    continue
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
