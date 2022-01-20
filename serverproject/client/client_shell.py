import json, os
import ffmpeg
from socket import *
from tkinter import *

class Application(Frame):  
    def __init__(self, master):
        Frame.__init__(self, master) 
        self.grid(sticky=N+S+E+W)
        self.CLIENT_CONFIG = json.load(open("utils/client_config.json"))
        self.connection_status = StringVar()
        self.setup()

    def setup(self):
        match  self.CLIENT_CONFIG['language']:
            case "en":
                self.LANG = json.load(open("lang/en_us.json", encoding="utf-8"))
            case "da":
                self.LANG = json.load(open("lang/da_dk.json", encoding="utf-8"))
            case "ja":
                self.LANG = json.load(open("lang/ja_jp.json", encoding="utf-8"))

        # window stuff
        mainWin = self.winfo_toplevel()
        for row in range(0,5):
            mainWin.rowconfigure(row, weight=1)     
        mainWin.columnconfigure(0, weight=1, minsize=10)
        
        #texts
        ipT = Text(mainWin,width=10, height=1)
        ipT.grid(row=1, column=0, sticky=N+S+E+W)
        pT = Text(mainWin,width=10, height=1)
        pT.grid(row=3, column=0, sticky=N+S+E+W)

        # labels
        ipL = Label(mainWin, text="Enter the ip")
        ipL.grid(row=0, column=0, sticky=N+S+E+W)
        poL = Label(mainWin, text="Enter port")
        poL.grid(row=2, column=0, sticky=N+S+E+W)

        #button
        cB = Button(mainWin, text="Connect", command=self.main_shell, bg="#f0f0f0")
        cB.grid(row=4, column=0, sticky=N+S+E+W)
        eB = Button(mainWin, text="Exit", command=exit, bg ="#f0f0f0")
        eB.grid(row=5, column=0, sticky=N+S+E+W)
       
         #checkbox(hvis den findes)
         #Checkbutton

    def main_shell(self):
        testWin = Toplevel()
        for row in range(0,5):
            testWin.rowconfigure(row, weight=1)     
        testWin.columnconfigure(0, weight=1, minsize=10)

        connection_status_label = Label(testWin, textvariable=self.connection_status)
        connection_status_label.grid(row=0, column=0, sticky=N+S+E+W)

        dB = Button(testWin, text="Disonnect", command=None, bg="#f0f0f0")
        dB.grid(row=4, column=0, sticky=N+S+E+W)
        eB = Button(testWin, text="Exit", command=exit, bg ="#f0f0f0")
        eB.grid(row=5, column=0, sticky=N+S+E+W)

        self.connect()

    def connect(self):
        ip, port = self.CLIENT_CONFIG['host'], self.CLIENT_CONFIG['port']
        client = socket(AF_INET, SOCK_STREAM)
        while True:
            try:
                client.connect((ip, port))
                break
            except:
                self.connection_status.set(self.LANG['connection_fail_message'])
                continue
        self.connection_status.set(self.LANG['connected_message'])
        self.connection_status.set(self.receive_message(client))
        self.client_handler(client)

    def client_handler(self, client):
        while True:
            message = str(input("Type command for server: "))
            self.send_message(client, message)
            match message:
                case "disconnect":
                    client.close()
                    break
                case "music":
                    #receive_file(client)
                    continue
                case _:
                    continue
    
    def send_message(self, receiver, message):
        packet = f"{len(message):<{self.CLIENT_CONFIG['header_size']}}" + message
        return receiver.send(packet.encode("utf-8"))

    def receive_message(self, receiver):
        message = ''
        new_packet = True
        while True:
            packet = receiver.recv(self.CLIENT_CONFIG['buffer_size'])
            if new_packet:
                packet_length = int(packet[:self.CLIENT_CONFIG['header_size']])
                new_packet = False
            message += packet.decode("utf-8")
            if len(message)-self.CLIENT_CONFIG['header_size'] == packet_length:
                return str(message[self.CLIENT_CONFIG['header_size']:])

# def send_file():
#     pass

# def receive_file(receiver): # take path as argument
#     pass
    # with open("temp.wav", "wb") as file
    #             i = 0
    #             while True:
    #                 print(i)
    #                 i += 1
    #                 b = client.recv(CLIENT_CONFIG['buffer_size'])
    #                 if not b: 
    #                     break
    #                 file.write(b)


def main():
    app = Application(Tk())
    app.master.title("Client")
    app.mainloop()


if __name__ == "__main__":
    main()
