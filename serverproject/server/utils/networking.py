from socket import *


def send_string(sender, header_size, message):
    message = f"{len(message):<{header_size}}" + message
    sender.send(message.encode("utf-8"))
def receive_string(receiver):
    message = receiver.recv(1024)
    return str(message.decode("utf-8"))


# class client(socket):
#     header_size = NETWORKING_CONFIG['header_size']
#     def __init__(self, ip=gethostname(), port=NETWORKING_CONFIG['port']):
#         socket.__init__(self, AF_INET, SOCK_STREAM)
#         self.server_address = ip, port
#     def send_string(self, message):
#         data = f"{len(message):<{self.HEADERSIZE}}" + message
#         self.send(data.encode("utf-8"))
#     def receive_string(self):
#         message = self.recv(1024)
#         return str(message.decode("utf-8"))


# class server(socket):
#     header_size = NETWORKING_CONFIG['header_size']
#     def __init__(self, ip=gethostname(), port=NETWORKING_CONFIG['port']):
#         socket.__init__(self, AF_INET, SOCK_STREAM)
#         self.server_address = ip, port
#     def send_string(self, message):
#         data = f"{len(message):<{self.header_size}}" + message
#         self.send(data.encode("utf-8"))
#     def receive_string(self):
#         message = self.recv(1024)
#         return str(message.decode("utf-8"))


# class mysocket(socket):
#     header_size = NETWORKING_CONFIG['header_size']
#     #server_address = gethostname(), NETWORKING_CONFIG['port']
#     def __init__(self, ip=gethostname(), port=NETWORKING_CONFIG['port']):
#         socket.__init__(self, AF_INET, SOCK_STREAM)
#         self.server_address = ip, port
#     def send_string(self, message):
#         data = f"{len(message):<{self.header_size}}" + message
#         self.send(data.encode("utf-8"))
#     def receive_string(self):
#         message = self.recv(1024)
#         return str(message.decode("utf-8"))
