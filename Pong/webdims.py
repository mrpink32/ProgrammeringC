import websocket
import threading

class Server:
    def __init__(self):
        websocket.enableTrace(True)
        socket = "localhost"
        ws = websocket.WebSocketApp(socket,
                                                on_open=self.on_open)#,
                                                #on_message=on_message,
                                                #on_close=on_close)

        wst = threading.Thread(target=lambda: ws.run_forever())
        wst.daemon = True
        wst.start()
    def on_open(self):
        print("grim")


class Client:
    def __init__(self):
        self.test_socket = websocket.WebSocketApp("localhost", on_open=self.grim)
        #self.test_socket = websocket.create_connection("localhost")

    def grim(self, message):
        print(message)


def main():
    s = Server()
    c = Client()

main()
