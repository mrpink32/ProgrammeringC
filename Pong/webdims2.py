

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
