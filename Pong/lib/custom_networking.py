from socket import *
import ctypes

PORT=9000
HEADER_SIZE=10
MAX_QUEUE=0
MAX_CONNECTIONS=1
BUFFER_SIZE=16


# sentdex
def send_message(receiver, message, is_encoded=True):
    message = str(message)
    packet = f"{len(message):<{HEADER_SIZE}}" + message
    if is_encoded:
        packet = packet.encode("utf-8")
    return receiver.send(packet)
def receive_message(receiver, type=str, is_encoded=True):
    message = ''
    new_packet = True
    while True:
        packet = receiver.recv(BUFFER_SIZE)
        if new_packet:
            packet_length = int(packet[:HEADER_SIZE])
            new_packet = False
        if is_encoded:
            packet = packet.decode("utf-8")
        message += packet
        if len(message)-HEADER_SIZE == packet_length:
            return type(message[HEADER_SIZE:])


def send_message_two(receiver, message,  is_encoded=True):
    message = str(message)
    packet = message + '\n'
    if is_encoded:
        packet = packet.encode("utf-8")
    return receiver.sendall(packet)
    
            
def receive_message_two(receiver, type=str, is_encoded=True):
    message = ""
    while True:
        packet += receiver.recv(BUFFER_SIZE)
        if is_encoded:
            packet = packet.decode("utf-8")
        message += packet
        for i in range(0, len(message)):
            if message[i] == "\n":
                return type(message[:i])


