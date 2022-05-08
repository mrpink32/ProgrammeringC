from socket import *

PORT=9000
HEADER_SIZE=10
MAX_QUEUE=0
MAX_CONNECTIONS=1
BUFFER_SIZE=16

def send_message(receiver, message, encoding_style="utf-8"):
    message = str(message)
    packet = f"{len(message):<{HEADER_SIZE}}" + message
    packet = packet.encode(encoding_style)
    return receiver.send(packet)
def receive_message(receiver, type=str, encoding_style="utf-8"):
    message = ''
    new_packet = True
    while True:
        packet = receiver.recv(BUFFER_SIZE)
        if new_packet:
            packet_length = int(packet[:HEADER_SIZE])
            new_packet = False
        packet = packet.decode(encoding_style)
        message += packet
        if len(message)-HEADER_SIZE == packet_length:
            return type(message[HEADER_SIZE:])
