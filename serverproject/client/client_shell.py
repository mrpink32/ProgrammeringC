import json, os
from threading import *
from socket import *
from tkinter import *
import _thread as thread

class Application(Frame):  
    def __init__(self, master):
        Frame.__init__(self, master) 
        self.grid(sticky=N+S+E+W)
        with open("utils/client_config.json") as config: self.CLIENT_CONFIG = json.load(config)
        match  self.CLIENT_CONFIG['language']:
            case "en":
                with open("lang/en_us.json", encoding="utf-8") as lang_config: self.LANG = json.load(lang_config)
            case "da":
                with open("lang/en_us.json", encoding="utf-8") as lang_config: self.LANG = json.load(lang_config)
            case "ja":
                with open("lang/en_us.json", encoding="utf-8") as lang_config: self.LANG = json.load(lang_config)
        self.message_variable = StringVar()
        self.custom_ip = StringVar()
        self.custom_port = StringVar()
        self.use_custom_ip = False
        self.use_custom_port = False

    def clear_frame(self):
        for widget in self.main_window.winfo_children():
            widget.destroy()
        #https://stackoverflow.com/questions/49313874/how-to-remove-columns-or-rows-while-redrawing-a-grid-in-python3-tkinter
        for i in range(0, 5):
            self.main_window.grid_columnconfigure(i, weight=0)
            self.main_window.grid_rowconfigure(i, weight=0)

    def create_connection_window(self):
        # window stuff
        self.main_window = self.winfo_toplevel()
        for row in range(0,5):
            self.main_window.rowconfigure(row, weight=1)     
        for column in range(0,2):
            self.main_window.columnconfigure(column, weight=1, minsize=10)
        #texts
        self.ip_entry = Entry(self.main_window,width=10, state="disabled", textvariable=self.custom_ip)
        self.ip_entry.grid(row=1, column=0, sticky=N+S+E+W)
        self.port_entry = Entry(self.main_window,width=10, state="disabled", textvariable=self.custom_port)
        self.port_entry.grid(row=3, column=0, sticky=N+S+E+W)
        # labels
        ip_label = Label(self.main_window, text="Enter the ip")
        ip_label.grid(row=0, column=0, sticky=N+S+E+W)
        port_label = Label(self.main_window, text="Enter port")
        port_label.grid(row=2, column=0, sticky=N+S+E+W)
        #button
        connect_button = Button(self.main_window, text="Connect", command=self.create_main_window, bg="#f0f0f0")
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
            self.ip_entry.configure(state="normal")
        else:
            self.use_custom_ip = False
            self.ip_entry.configure(state="disabled")

    def toggle_port_check(self):
        if self.use_custom_port == False:
            self.use_custom_port = True
            self.port_entry.configure(state="normal")
        else:
            self.use_custom_port = False
            self.port_entry.configure(state="disabled")

    def create_main_window(self):
        self.clear_frame()
        for row in range(0,4):
            self.main_window.rowconfigure(row, weight=1)
        self.main_window.columnconfigure(0, weight=1, minsize=10)
        #Labels
        message_label = Label(self.main_window, textvariable=self.message_variable)
        message_label.grid(row=0, column=0, sticky=N+S+E+W)
        #buttons
        upload_button = Button(self.main_window, text="Upload a file to the server", command=lambda : Thread(target=self.send_file).start(), bg="#f0f0f0")
        upload_button.grid(row=1, column=0, sticky=N+S+E+W)
        download_button = Button(self.main_window, text="Download a file from the server", command=lambda : Thread(target=self.receive_file).start(), bg="#f0f0f0")
        download_button.grid(row=2, column=0, sticky=N+S+E+W)
        exit_button = Button(self.main_window, text="Exit", command=self.disconnect, bg="#f0f0f0")
        exit_button.grid(row=3, column=0, sticky=N+S+E+W)
        self.connect()
        #thread.start_new_thread(self.connect())

    def open_file_overview(self):
        file_overview_window = Toplevel()
        # receive the name of all files located on the server
        file_list = Listbox(file_overview_window)

    def connect(self):
        ip, port = self.CLIENT_CONFIG['host'], self.CLIENT_CONFIG['port']
        ip = self.custom_ip.get() if self.use_custom_ip else self.CLIENT_CONFIG['host']
        port = self.custom_port.get() if self.use_custom_port else self.CLIENT_CONFIG['port']
        self.client = socket(AF_INET, SOCK_STREAM)
        while True:
            try:
                self.client.connect((ip, port))
                break
            except:
                #self.message_variable.set(self.LANG['connection_fail_message'])
                print(self.LANG['connection_fail_message'])
                continue
        self.message_variable.set(self.LANG['connected_message'])
        self.message_variable.set(self.receive_message())
        #self.handler(self.client)

    def disconnect(self):
        self.send_message("!disconnect")
        self.client.close()
        exit()

    def handler(self, client):
        while True:
            message = str(input("Type command for server: "))
            self.send_message(message)
            match message:
                case "!disconnect":
                    client.close()
                    break
                case "receive_from_server":
                    self.open_file_overview()
                    self.receive_file()
                    continue
                case "send_to_server":
                    path = "temp"
                    self.send_file(path)
                    continue
                case _:
                    continue

    def send_message(self, message, encode=True):
        message = str(message)
        packet = f"{len(message):<{self.CLIENT_CONFIG['header_size']}}" + message
        if encode:
            packet = packet.encode("utf-8")
        return self.client.send(packet)

    def receive_message(self, encode=True):
        message = ''
        new_packet = True
        while True:
            packet = self.client.recv(self.CLIENT_CONFIG['buffer_size'])
            #print(packet)
            if new_packet:
                packet_length = int(packet[:self.CLIENT_CONFIG['header_size']])
                #print(packet[:self.CLIENT_CONFIG['header_size']])
                new_packet = False
            if encode:
                packet = packet.decode("utf-8")
            message += packet
            if len(message)-self.CLIENT_CONFIG['header_size'] == packet_length:
                return str(message[self.CLIENT_CONFIG['header_size']:])

    def send_file(self):
        self.send_message("send_to_server")
        path = "temp.wav"
        filesize = os.path.getsize(path)
        self.send_message(filesize)
        with open(path, "rb") as file:
            sent = 0
            #print(filesize)
            while True:
                bytes_read = file.read(self.CLIENT_CONFIG['buffer_size'])
                sent += self.client.send(bytes_read)
                progress = sent/filesize
                #print(f"{progress*100}%")
                self.message_variable.set(f"{progress*100}%")
                if progress == 1:
                    break

    def receive_file(self):
        self.open_file_overview()
        self.send_message("receive_from_server")
        filesize = int(self.receive_message())
        received = 0
        with open("temp.txt", "wb") as file:
            while True:
                bytes_read = self.client.recv(self.CLIENT_CONFIG['buffer_size'])
                received += len(bytes_read)
                file.write(bytes_read)
                progress = received/filesize
                #print(f"{progress*100}%")
                self.message_variable.set(f"{progress*100}%")
                if progress == 1:
                    break


def main():
    app = Application(Tk())
    app.master.title("Client")
    app.create_connection_window()
    app.mainloop()


if __name__ == "__main__":
    main()
