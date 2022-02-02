import json, os
import threading
from socket import *
import _thread as thread


def config_setup():
    return SERVER_CONFIG['host'], SERVER_CONFIG['port']


def lang_setup():
    match  SERVER_CONFIG['language']:
        case "en":
            with open("lang/en_us.json", encoding="utf-8") as _: return json.load(_)
        case "da":
            with open("lang/da_dk.json", encoding="utf-8") as _: return json.load(_)
        case "ja":
            with open("lang/ja_jp.json", encoding="utf-8") as _: return json.load(_)


def send_message(receiver, message, encode=True):
        message = str(message)
        packet = f"{len(message):<{SERVER_CONFIG['header_size']}}" + message
        if encode:
            packet = packet.encode("utf-8")
        receiver.send(packet)

def receive_message(receiver, encode=True):
        message = ''
        new_packet = True
        while True:
            packet = receiver.recv(SERVER_CONFIG['buffer_size'])
            if new_packet:
                packet_length = int(packet[:SERVER_CONFIG['header_size']])
                print(packet[:SERVER_CONFIG['header_size']])
                new_packet = False
            if encode:
                packet = packet.decode("utf-8")
            message += packet
            if len(message)-SERVER_CONFIG['header_size'] == packet_length:
                return str(message[SERVER_CONFIG['header_size']:])

def send_file(sender, path):
    filesize = os.path.getsize(path)
    send_message(sender, filesize)
    with open(path, "rb") as file:
        sent = 0
        print(filesize)
        while True:
            bytes_read = file.read(SERVER_CONFIG['buffer_size'])
            progress = sent/filesize*100
            print(f"{progress}%")
            if progress == 100:
                break
            sent += sender.send(bytes_read) 

def receive_file(receiver): # take path as argument
    filesize = int(receive_message(receiver))
    received = 0
    with open("temp.mp3", "wb") as file:
        while True:
            bytes_read = receiver.recv(SERVER_CONFIG['buffer_size'])
            received += len(bytes_read)
            progress = received/filesize*100
            print(f"{progress}%")
            if progress == 100:
                break
            file.write(bytes_read)


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
    global clients
    clients = []
    print(LANG['started_message'].format(ip, port))
    while True:
        if current_connections < SERVER_CONFIG['max_connections']:
            client, client_address = server.accept()
            clients.append(client)
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
                case "!disconnect":
                    client.close()
                    break
                case "send":
                    path = "music/09 Flamewall.mp3"
                    send_file(client, path)
                    continue
                case _:
                    continue
        except Exception as e:
            print(e)
            print(LANG['client_disconnect'].format(client_address))
            client.close()
            break
    with lock:
        global current_connections
        current_connections -= 1
    print(LANG['connection_count'].format(current_connections))


if __name__ == "__main__":
    with open("utils/server_config.json") as _: SERVER_CONFIG = json.load(_)
    LANG = lang_setup()
    main()
