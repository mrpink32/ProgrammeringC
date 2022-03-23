import json, os, time
import threading
from socket import *
import _thread as thread


class Application():
    def __init__(self):
        try:
            with open("utils/server_config.json") as _: self.SERVER_CONFIG = json.load(_)
            match  self.SERVER_CONFIG['language']:
                case "en":
                    with open("lang/en_us.json", encoding="utf-8") as _: 
                        self.LANG = json.load(_)
                case "da":
                    with open("lang/da_dk.json", encoding="utf-8") as _: self.LANG = json.load(_)
                case "ja":
                    with open("lang/ja_jp.json", encoding="utf-8") as _: self.LANG = json.load(_)
            self.start_server()
        except Exception as e:
            print(e)
            time.sleep(10)
            
    
    def start_server(self):
        # computer's ip has to be used if server needs to accept non-local connections
        if (self.SERVER_CONFIG['host'] == ""):
            self.SERVER_CONFIG['host'] = gethostname()
        server = socket(AF_INET, SOCK_STREAM)
        print(self.LANG['startup_message'].format(self.SERVER_CONFIG['port']))
        server.bind((self.SERVER_CONFIG['host'], self.SERVER_CONFIG['port']))
        server.listen(self.SERVER_CONFIG['max_queue'])
        global current_connections
        current_connections = 0
        lock = threading.Lock()
        self.clients = []
        print(self.LANG['started_message'].format(self.SERVER_CONFIG['host'], self.SERVER_CONFIG['port']))
        while True:
            if current_connections < self.SERVER_CONFIG['max_connections']:
                client, client_address = server.accept()
                self.clients.append(client)
                print(self.LANG['connected_message'].format(client_address))
                self.send_message(client, self.LANG['welcome_message'])
                thread.start_new_thread(self.client_handler, (client, client_address, lock))
                current_connections += 1
                print(self.LANG['connection_count'].format(current_connections)) #threading.enumerate()

    def client_handler(self, client, client_address, lock):
        while True:
            try:
                message = self.receive_message(client)
                print(self.LANG['client_message'].format(message))
                match message:
                    case "!disconnect":
                        client.close()
                        break
                    case "receive_from_server":
                        file_names = os.listdir(os.path.curdir + "/files")
                        self.send_message(client, len(file_names))
                        print(len(file_names))
                        for name in file_names:
                            self.send_message(client, name)
                            print(name)
                        path = os.path.curdir + "/files/" + self.receive_message(client)
                        print(path)
                        self.send_file(client, path)
                        continue
                    case "send_to_server":
                        self.receive_file(client)
                        continue
                    case _:
                        continue
            except Exception as e:
                print(e)
                print(self.LANG['client_disconnect'].format(client_address))
                client.close()
                break
        with lock:
            global current_connections
            current_connections -= 1
        print(self.LANG['connection_count'].format(current_connections))

    def send_message(self, receiver, message, encode=True):
        message = str(message)
        packet = f"{len(message):<{self.SERVER_CONFIG['header_size']}}" + message
        if encode:
            packet = packet.encode("utf-8")
        receiver.send(packet)
    
    def receive_message(self, receiver, encode=True):
        message = ''
        new_packet = True
        while True:
            packet = receiver.recv(self.SERVER_CONFIG['buffer_size'])
            if new_packet:
                packet_length = int(packet[:self.SERVER_CONFIG['header_size']])
                new_packet = False
            if encode:
                packet = packet.decode("utf-8")
            message += packet
            if len(message)-self.SERVER_CONFIG['header_size'] == packet_length:
                return str(message[self.SERVER_CONFIG['header_size']:])

    def send_file(self, sender, path):
        filesize = os.path.getsize(path)
        self.send_message(sender, filesize)
        with open(path, "rb") as file:
            sent = 0
            while True:
                bytes_read = file.read(self.SERVER_CONFIG['buffer_size'])
                sent += sender.send(bytes_read) 
                progress = sent/filesize*100
                print(f"{progress}%")
                if progress == 100:
                    break

    def receive_file(self, receiver):
        filename = self.receive_message(receiver)
        filesize = int(self.receive_message(receiver))
        received = 0
        with open(os.path.curdir + "/files/" + filename, "wb") as file:
            while True:
                bytes_read = receiver.recv(self.SERVER_CONFIG['buffer_size'])
                received += len(bytes_read)
                file.write(bytes_read)
                progress = received/filesize*100
                print(f"{progress}%")
                if progress == 100:
                    break


def main():
    app = Application()
    exit()

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
if __name__ == "__main__":
    main()
