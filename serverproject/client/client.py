import json, os
import ffmpeg
from socket import *
from tkinter import *

class Application(Frame):  

    def __init__(self, master):
        Frame.__init__(self, master) 
        self.grid(sticky=N+S+E+W)
        self.shell()

    def shell(self):
        # window stuff
        mainWin = self.winfo_toplevel()
        for row in range(0,4):
            mainWin.rowconfigure(row, weight=1)     
        mainWin.columnconfigure(0, weight=1, minsize = 10)
        
        #texts
        ipT = Text(mainWin,width=10, height = 1)
        ipT.grid(row = 1, column = 0, sticky=N+S+E+W)
        pT = Text(mainWin,width=10, height = 1)
        pT.grid(row = 3, column = 0, sticky=N+S+E+W)

        # labels
        ipL = Label(mainWin, text="Enter the ip")
        ipL.grid(row=0, column=0, sticky=N+S+E+W)
        poL = Label(mainWin, text="Enter port")
        poL.grid(row=2, column=0, sticky=N+S+E+W)

        #button
        eB = Button(mainWin, text="Exit", command = exit, bg ="#f0f0f0")
        eB.grid(row=4, column=0, sticky=N+S+E+W)
       
         #checkbox(hvis den findes)


def config_setup():
    return CLIENT_CONFIG['host'], CLIENT_CONFIG['port']


def lang_setup():
    match  CLIENT_CONFIG['language']:
        case "en":
            return json.load(open("lang/en_us.json"))
        case "da":
            return json.load(open("lang/da_dk.json", encoding="utf-8"))
        case "ja":
            return json.load(open("lang/ja_jp.json", encoding="utf-8"))


def send_message(receiver, message):
    packet = f"{len(message):<{CLIENT_CONFIG['header_size']}}" + message
    return receiver.send(packet.encode("utf-8"))


def receive_message(receiver):
    message = ''
    new_packet = True
    while True:
        packet = receiver.recv(CLIENT_CONFIG['buffer_size'])
        if new_packet:
            packet_length = int(packet[:CLIENT_CONFIG['header_size']])
            new_packet = False
        message += packet.decode("utf-8")
        if len(message)-CLIENT_CONFIG['header_size'] == packet_length:
            return str(message[CLIENT_CONFIG['header_size']:])


def send_file():
    pass


def receive_file(receiver): # take path as argument
    pass
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
    ip, port = config_setup()
    client = socket(AF_INET, SOCK_STREAM)
    while True:
        try:
            client.connect((ip, port))
            break
        except:
            print(LANG['connection_fail_message'])
            continue
    print(LANG['connected_message'])
    print(receive_message(client))
    client_handler(client)
    # todo make a simple ui for easier interaction with the client


def client_handler(client):
    while True:
        message = str(input("Type command for server: "))
        send_message(client, message)
        match message:
            case "disconnect":
                client.close()
                break
            case "music":
                #receive_file(client)
                continue
            case _:
                continue


if __name__ == "__main__":
    CLIENT_CONFIG = json.load(open("utils/client_config.json"))
    LANG = lang_setup()
    app = Application(Tk())
    app.master.title("Client")
    app.mainloop()
    main()
    # lad main være ligesom en update function?
