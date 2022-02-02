import json, os
from threading import *
from socket import *
from tkinter import *

class Application(Frame):  
    def __init__(self, master):
        Frame.__init__(self, master) 
        self.grid(sticky=N+S+E+W)
        with open("utils/client_config.json") as config: self.CLIENT_CONFIG = json.load(config)
        self.connection_status = StringVar()
        self.setup()
        self.use_custom_port = False
        self.use_custom_ip = False

    def setup(self):
        match  self.CLIENT_CONFIG['language']:
            case "en":
                with open("lang/en_us.json", encoding="utf-8") as lang_config: self.LANG = json.load(lang_config)
            case "da":
                with open("lang/en_us.json", encoding="utf-8") as lang_config: self.LANG = json.load(lang_config)
            case "ja":
                with open("lang/en_us.json", encoding="utf-8") as lang_config: self.LANG = json.load(lang_config)
        # window stuff
        self.main_window = self.winfo_toplevel()
        for row in range(0,5):
            self.main_window.rowconfigure(row, weight=1)     
        for column in range(0,2):
            self.main_window.columnconfigure(column, weight=1, minsize=10)
        
        #texts
        self.ip_text = Text(self.main_window,width=10, height=1, state="disabled")
        self.ip_text.grid(row=1, column=0, sticky=N+S+E+W)
        self.port_text = Text(self.main_window,width=10, height=1, state="disabled")
        self.port_text.grid(row=3, column=0, sticky=N+S+E+W)

        # labels
        ip_label = Label(self.main_window, text="Enter the ip")
        ip_label.grid(row=0, column=0, sticky=N+S+E+W)
        port_label = Label(self.main_window, text="Enter port")
        port_label.grid(row=2, column=0, sticky=N+S+E+W)

        #button
        connect_button = Button(self.main_window, text="Connect", command=self.main_shell, bg="#f0f0f0")
        connect_button.grid(row=4, column=0, sticky=N+S+E+W)
        exit_button = Button(self.main_window, text="Exit", command=exit, bg ="#f0f0f0")
        exit_button.grid(row=5, column=0, sticky=N+S+E+W)
    
        #Checkbutton
        ip_checkbutton = Checkbutton(self.main_window, text = "Custom ip", command=self.toggle_ip_check)
        ip_checkbutton.grid(row = 0, column = 1, sticky = N+S+E+W)
        port_checkbutton = Checkbutton(self.main_window, text = "Custom port", command=self.toggle_port_check)
        port_checkbutton.grid(row = 2, column = 1, sticky = N+S+E+W)
    
    def toggle_ip_check(self):
        if self.use_custom_ip == False:
            self.use_custom_ip = True
            print("normal")
            self.ip_text.configure(state="normal")
        else:
            self.use_custom_ip = False
            print("disable")
            self.ip_text.configure(state="disabled")

    def toggle_port_check(self):
        if self.use_custom_port == False:
            self.use_custom_port = True
            self.port_text.configure(state="normal")
        else:
            self.use_custom_port = False
            self.port_text.configure(state="disabled")

    def clear_frame(self):
        for widget in self.main_window.winfo_children():
            widget.destroy()
        #https://stackoverflow.com/questions/49313874/how-to-remove-columns-or-rows-while-redrawing-a-grid-in-python3-tkinter
        for i in range(0, 5):
            self.main_window.grid_columnconfigure(i, weight=0)
            self.main_window.grid_rowconfigure(i, weight=0)

    def main_shell(self):
        self.clear_frame()
        for row in range(0,3):
            self.main_window.rowconfigure(row, weight=1)
        self.main_window.columnconfigure(0, weight=1, minsize=10)

        connection_status_label = Label(self.main_window, textvariable=self.connection_status)
        connection_status_label.grid(row=0, column=0, sticky=N+S+E+W)

        disconnect_button = Button(self.main_window, text="Disconnect", command=self.disconnect, bg="#f0f0f0")
        disconnect_button.grid(row=1, column=0, sticky=N+S+E+W)
        exit_button = Button(self.main_window, text="Exit", command=exit, bg ="#f0f0f0")
        exit_button.grid(row=2, column=0, sticky=N+S+E+W)

        self.connect()

    def connect(self):
        ip, port = self.CLIENT_CONFIG['host'], self.CLIENT_CONFIG['port']
        #ip = #string var in text if self.use_custom_ip else self.CLIENT_CONFIG['host']
        #port = #string var in text if self.use_custom_port else self.CLIENT_CONFIG['port']
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
                case "!disconnect":
                    client.close()
                    break
                case "send":
                    self.receive_file()
                    continue
                case _:
                    continue

    def send_message(self, receiver, message, encode=True):
        packet = f"{len(message):<{self.CLIENT_CONFIG['header_size']}}" + message
        if encode:
            packet = packet.encode("utf-8")
        return receiver.send(packet)

    def receive_message(self, receiver, encode=True):
        message = ''
        new_packet = True
        while True:
            packet = receiver.recv(self.CLIENT_CONFIG['buffer_size'])
            print(packet)
            if new_packet:
                packet_length = int(packet[:self.CLIENT_CONFIG['header_size']])
                print(packet[:self.CLIENT_CONFIG['header_size']])
                new_packet = False
            if encode:
                packet = packet.decode("utf-8")
            message += packet
            if len(message)-self.CLIENT_CONFIG['header_size'] == packet_length:
                return str(message[self.CLIENT_CONFIG['header_size']:])

    def send_file(self, path):
        filesize = os.path.getsize(path)
        self.send_message(self.client, filesize)
        with open(path, "rb") as file:
            sent = 0
            print(filesize)
            while True:
                bytes_read = file.read(self.CLIENT_CONFIG['buffer_size'])
                progress = sent/filesize*100
                print(f"{progress}%")
                if progress == 100:
                    break
                sent += self.client.send(bytes_read)

    def receive_file(self): # take path as argument
        filesize = int(self.receive_message(self.client))
        received = 0
        with open("temp.mp3", "wb") as file:
            while True:
                bytes_read = self.client.recv(self.CLIENT_CONFIG['buffer_size'])
                received += len(bytes_read)
                progress = received/filesize*100
                print(f"{progress}%")
                if progress == 100:
                    break
                file.write(bytes_read)


def main():
    app = Application(Tk())
    app.master.title("Client")
    app.mainloop()


if __name__ == "__main__":
    main()
