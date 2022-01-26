import json, os
from socket import *
from tkinter import *

class Application(Frame):  
    def __init__(self, master):
        Frame.__init__(self, master) 
        self.grid(sticky=N+S+E+W)
        with open("utils/client_config.json") as config: self.CLIENT_CONFIG = json.load(config)
        self.connection_status = StringVar()
        self.setup()
        self.use_custom_port
        self.use_custom_ip = IntVar()

    def setup(self):
        match  self.CLIENT_CONFIG['language']:
            case "en":
                with open("lang/en_us.json", encoding="utf-8") as lang_config: self.LANG = json.load(lang_config)
            case "da":
                with open("lang/en_us.json", encoding="utf-8") as lang_config: self.LANG = json.load(lang_config)
            case "ja":
                with open("lang/en_us.json", encoding="utf-8") as lang_config: self.LANG = json.load(lang_config)
        # window stuff
        mainWin = self.winfo_toplevel()
        for row in range(0,5):
            mainWin.rowconfigure(row, weight=1)     
        for column in range(0,2):
            mainWin.columnconfigure(column, weight=1, minsize=10)
        
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
    
        #Checkbutton
        cbcustomport = Checkbutton(mainWin, text = "Custom port", variable = self.use_custom_ip)
        cbcustomport.grid(row = 2, column = 1, sticky = N+S+E+W)
        cbcustomip = Checkbutton(mainWin, text = "Custom ip")
        cbcustomip.grid(row = 0, column = 1, sticky = N+S+E+W)

    def main_shell(self):
        testWin = Toplevel()
        for row in range(0,5):
            testWin.rowconfigure(row, weight=1)     
        testWin.columnconfigure(0, weight=1, minsize=10)

        connection_status_label = Label(testWin, textvariable=self.connection_status)
        connection_status_label.grid(row=0, column=0, sticky=N+S+E+W)

        dB = Button(testWin, text="Disconnect", command=self.disconnect, bg="#f0f0f0")
        dB.grid(row=4, column=0, sticky=N+S+E+W)
        eB = Button(testWin, text="Exit", command=exit, bg ="#f0f0f0")
        eB.grid(row=5, column=0, sticky=N+S+E+W)

        self.connect()

    def connect(self):
        ip, port = self.CLIENT_CONFIG['host'], self.CLIENT_CONFIG['port']
        self.client = socket(AF_INET, SOCK_STREAM)
        while True:
            try:
                self.client.connect((ip, port))
                break
            except:
                self.connection_status.set(self.LANG['connection_fail_message'])
                continue
        self.connection_status.set(self.LANG['connected_message'])
        self.connection_status.set(self.receive_message(self.client))
        self.client_handler(self.client)

    def disconnect(self):
        self.send_message(self.client, "disconnect")
        exit()

    def client_handler(self, client):
        while True:
            message = str(input("Type command for server: "))
            self.send_message(client, message)
            match message:
                case "disconnect":
                    client.close()
                    break
                case "send":
                    self.receive_file(client)
                    continue
                case _:
                    continue

    def send_message(self, sender, message, encode=True):
        packet = f"{len(message):<{self.CLIENT_CONFIG['header_size']}}" + message
        if encode:
            packet = packet.encode("utf-8")
        return sender.send(packet)

    def receive_message(self, receiver, encode=True):
        message = ''
        new_packet = True
        while True:
            packet = receiver.recv(self.CLIENT_CONFIG['buffer_size'])
            if new_packet:
                packet_length = int(packet[:self.CLIENT_CONFIG['header_size']])
                new_packet = False
            if encode:
                packet = packet.decode("utf-8")
            message += packet
            if len(message)-self.CLIENT_CONFIG['header_size'] == packet_length:
                return str(message[self.CLIENT_CONFIG['header_size']:])

    def send_file(self, sender, path):
        with open(path, "rb") as file:
            lines = []
            for line in file:
                lines.append(line)
            self.send_message(sender, len(lines))
            for line in lines:
                self.send_message(sender, line, False)

    def receive_file(self, receiver): # take path as argument
        with open("temp.wav", "wb") as file:
            packets = self.receive_message(receiver)
            for _ in range(0, len(packets)+1):
                file.write(self.receive_message(receiver, False))


def main():
    app = Application(Tk())
    app.master.title("Client")
    app.mainloop()


if __name__ == "__main__":
    main()
