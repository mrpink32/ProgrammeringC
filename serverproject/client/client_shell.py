import json, os, time
from socket import *
from tkinter import *
from threading import *
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

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()
        #https://stackoverflow.com/questions/49313874/how-to-remove-columns-or-rows-while-redrawing-a-grid-in-python3-tkinter
        for i in range(0, 5):
            frame.grid_columnconfigure(i, weight=0)
            frame.grid_rowconfigure(i, weight=0)

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
        self.clear_frame(self.main_window)
        for row in range(0,4):
            self.main_window.rowconfigure(row, weight=1)
        self.main_window.columnconfigure(0, weight=1, minsize=10)
        #Labels
        message_label = Label(self.main_window, textvariable=self.message_variable)
        message_label.grid(row=0, column=0, sticky=N+S+E+W)
        #buttons
        upload_button = Button(self.main_window, text="Upload a file to the server", command=lambda : Thread(target=self.send_file).start(), bg="#f0f0f0")
        upload_button.grid(row=1, column=0, sticky=N+S+E+W)
        download_button = Button(self.main_window, text="Download a file from the server", command=lambda : Thread(target=self.open_file_overview).start(), bg="#f0f0f0")
        download_button.grid(row=2, column=0, sticky=N+S+E+W)
        exit_button = Button(self.main_window, text="Exit", command=self.disconnect, bg="#f0f0f0")
        exit_button.grid(row=3, column=0, sticky=N+S+E+W)
        #self.connect()
        Thread(target=self.connect).start()

    def open_file_overview(self):
        file_overview_window = Toplevel()
        file_overview_window.rowconfigure(0, weight=1)
        file_overview_window.columnconfigure(0, weight=1)
        self.send_message("receive_from_server")
        file_count = int(self.receive_message())
        print(file_count)
        file_names = []
        for _ in range(0, file_count):
            file_names.append(self.receive_message())
        print(file_names)
        file_list = Listbox(file_overview_window, activestyle=DOTBOX)
        file_list.grid(row=0, column=0, sticky=N+S+E+W)
        for name in file_names:
            file_list.insert(END, name)
        while True:
            if file_list.curselection():
                time.sleep(0.25)
                item = file_list.get(ACTIVE)
                file_overview_window.destroy()
                print(item)
                self.send_message(item)
                self.receive_file(item)
                break

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
                self.message_variable.set(self.LANG['connection_fail_message'])
                #print(self.LANG['connection_fail_message'])
                continue
        self.message_variable.set(self.LANG['connected_message'])
        self.message_variable.set(self.receive_message())

    def disconnect(self):
        self.send_message("!disconnect")
        self.client.close()
        exit()

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
        #maybe use this try except not sure
        try:
            self.send_message("send_to_server")
            path = "temp.txt"
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
        except:
            print("dead")

    def receive_file(self, path):
        filesize = int(self.receive_message())
        received = 0
        with open(path, "wb") as file:
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
