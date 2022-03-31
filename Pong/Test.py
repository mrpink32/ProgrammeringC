from tkinter import *
from socket import *
import threading
import math



class Application(Frame):
    def __init__(self, master, frame_target):
        Frame.__init__(self, master)
        self.grid(sticky=N+W+S+E)
        self.screen_width, self.screen_height =10,10 #screeninfo.get_monitors()[0].width, screeninfo.get_monitors()[0].height
        self.frame_time = math.floor(1000 / frame_target)
        self.is_game_running = False
    
    def clear_frame(self):
        for widget in self.main_window.winfo_children():
            widget.destroy()
        #https://stackoverflow.com/questions/49313874/how-to-remove-columns-or-rows-while-redrawing-a-grid-in-python3-tkinter
        for i in range(0, 7):
            self.main_window.grid_columnconfigure(i, weight=0)
            self.main_window.grid_rowconfigure(i, weight=0)

    def main_menu(self):
        self.main_window = self.winfo_toplevel()
        for i in range(0, 5): self.main_window.columnconfigure(i, weight=1)
        for i in range(0, 7): self.main_window.rowconfigure(i, weight=1)
        host_button = Button(self.main_window, text="Host", command=self.start_server)
        host_button.grid(column=2, row=1, sticky=N+W+S+E)
        join_button = Button(self.main_window, text="Join", command=self.start_client)
        join_button.grid(column=2, row=3, sticky=N+W+S+E)
        exit_button = Button(self.main_window, text="Exit", command=exit)
        exit_button.grid(column=2, row=5, sticky=N+W+S+E)

    def game_window(self):
        self.clear_frame()
        self.main_window.columnconfigure(0, weight=1)
        self.main_window.rowconfigure(0, weight=1)
        self.draw_space = Canvas(self.main_window, width=self.screen_width/2, height=self.screen_height/2)
        self.draw_space.grid(sticky=N+W+S+E)
        self.player1 = Player(self.window_height/2)
        self.player2 = Player(self.window_height/2)
        self.is_game_running = True
        self.game_loop()

    def game_loop(self):
        self.draw_space.delete(ALL)
        #receive other players y position
        self.draw_players()
        self.master.after(self.frame_time, self.game_loop)

    def draw_players(self):
        self.player1.x_pos = self.window_width * 0.04
        self.player2.x_pos = self.window_width - self.player1.x_pos
        self.draw_space.create_rectangle(self.player1.x_pos, self.player1.y_pos, self.player1.x_pos + self.player_width, self.player1.y_pos + self.player_height, fill="#0000ff")
        self.draw_space.create_rectangle(self.player2.x_pos - self.player_width, self.player2.y_pos, self.player2.x_pos, self.player2.y_pos + self.player_height, fill="#ff0000")

    def calculate_player_size(self):
        self.player_width = self.window_width * 0.01
        self.player_height = self.window_height * 0.1

    def window_size(self):
        self.window_width, self.window_height = self.main_window.winfo_width(), self.main_window.winfo_height()

    def configure_event(self, event):
        #self.window_width, self.window_height = event.width, event.height
        self.window_size()
        self.calculate_player_size()

    def inputs(self, event):
        match event.char:
            case 'w':
                if self.player1.y_pos > 0:
                    print("moving up...")
                    self.player1.move(-1)
            case 's':
                if self.player1.y_pos < self.window_height - self.player_height:
                    print("moving down...")
                    self.player1.move(1)

    def start_server(self):
        threading.Thread(target=lambda : Server(self)).start()
        self.game_window()
    
    def start_client(self):
        threading.Thread(target=Client).start()
        self.game_window()




class Player:
    def __init__(self, start_height):
        self.x_pos = 0
        self.y_pos = start_height
        self.speed = 5
    def move(self, inputs):
        self.y_pos += inputs * self.speed
        


class Server:
    def __init__(self, app):
        # print(self.LANG['startup_message'].format(self.SERVER_CONFIG['port']))
        print("Starting server!")
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.bind(("localhost", 9000))
        self.server_socket.listen(0)
        self.current_connections = 0
        print("server started!")
        # print(self.LANG['started_message'].format(self.SERVER_CONFIG['host'], self.SERVER_CONFIG['port']))
        while True:
            if self.current_connections < 1:
                client, client_address = self.server_socket.accept()
                print("grim")
                # print(self.LANG['connected_message'].format(client_address))


                #self.send_message(client, self.LANG['welcome_message'])


                # thread.start_new_thread(self.client_handler, (client, client_address, lock)) 


                self.current_connections += 1
                print(self.current_connections)
                # print(self.LANG['connection_count'].format(current_connections))
            else:
                self.server_socket.sendall(app.player1.y_pos)
                client.recv()
        



class Client:
    def __init__(self, app):
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(("localhost", 9000))



def main():
    app = Application(Tk(), 60)
    app.main_menu()
    app.master.bind('<KeyPress>', app.inputs)
    app.master.bind('<Configure>', app.configure_event)
    app.mainloop()


if __name__ == "__main__":
    main()
