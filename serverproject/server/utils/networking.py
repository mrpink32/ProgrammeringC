import json
from socket import *


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


def config_setup():
    return (SERVER_CONFIG['host'], SERVER_CONFIG['port'], 
            SERVER_CONFIG['header_size'], SERVER_CONFIG['max_queue'], 
            SERVER_CONFIG['max_connections'], language)


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


# def client_handler(client, client_address, lock):
#     while True:
#         try:
#             message = client.recv(1024)
#             message = str(message.decode("utf-8"))
#             print(message)
#             match message:
#                 case "10        disconnect":
#                     client.close()
#                     break
#                 case _:
#                     continue
#         except:
#             print(language['client_disconnect'].format(client_address))
#             client.close()
#             break
#     with lock:
#         global current_connections
#         current_connections -= 1
#     print("current_connections: {current_connections}")
#     #thread.exit()