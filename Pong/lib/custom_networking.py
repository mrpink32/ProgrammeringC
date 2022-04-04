from socket import *


PORT=9000
HEADER_SIZE=10
MAX_QUEUE=0
MAX_CONNECTIONS=1
BUFFER_SIZE=16


def send_message(receiver, message, encode=True):
    message = str(message)
    packet = f"{len(message):<{HEADER_SIZE}}" + message
    if encode:
        packet = packet.encode("utf-8")
    receiver.send(packet)
    #return sent
def receive_message(receiver, encode=True):
    message = ''
    new_packet = True
    while True:
        packet = receiver.recv(BUFFER_SIZE)
        if new_packet:
            packet_length = int(packet[:HEADER_SIZE])
            new_packet = False
        if encode:
            packet = packet.decode("utf-8")
        message += packet
        if len(message)-HEADER_SIZE == packet_length:
            return str(message[HEADER_SIZE:])
