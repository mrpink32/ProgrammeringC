#install websocket-client

import websocket
from datetime import datetime
import time
import _thread as thread

class websocket_demo:
    def __init__(self):
        pass

    def onMessage(self, *msg):
        print(f'Message received msg:{msg}')

    def onError(self, *msg):
        print(f"Websocket error msg:{msg}")

    def onOpen(self, *msg):
        print(f"Websocket open msg:{msg}")

    def onClose(self, *msg):
        print(f"Websocket closed. msg:{msg}")

    def connect(self, url):
        self.url = url
        #websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp(self.url,
                                         on_message=self.onMessage,
                                         on_error=self.onError,
                                         on_open=self.onOpen,
                                         on_close=self.onClose)
           
        thread.start_new_thread(lambda *args: self.ws.run_forever(), ())

    def disconnect(self):
        self.ws.close()

   
    def send(self, msg):
        self.ws.send(msg)

def test_class():
    print('Websocket Client with websocket-client')
    wsd = websocket_demo()
    wsd.connect('ws://127.0.0.1:1337')

    i = 0
    while True:
        time.sleep(1.0)
        wsd.send(str(i))
        i += 1
        
if __name__ == "__main__":
    test_class()
