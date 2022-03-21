from tkinter import *
from socket import *
import threading


class Application(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid(sticky=N+W+S+E)
    
    def clear_frame(self):
        for widget in self.main_window.winfo_children():
            widget.destroy()
        #https://stackoverflow.com/questions/49313874/how-to-remove-columns-or-rows-while-redrawing-a-grid-in-python3-tkinter
        for i in range(0, 5):
            self.main_window.grid_columnconfigure(i, weight=0)
            self.main_window.grid_rowconfigure(i, weight=0)

    def main_menu(self):
        self.main_window = self.winfo_toplevel()
        for i in range(0, 5): self.main_window.columnconfigure(i, weight=1)
        for i in range(0, 7): self.main_window.rowconfigure(i, weight=1)
        host_button = Button(self.main_window, text="Host", command=Server)
        host_button.grid(column=2, row=1, sticky=N+W+S+E)
        join_button = Button(self.main_window, text="Join", command=self.game_window)
        join_button.grid(column=2, row=3, sticky=N+W+S+E)
        exit_button = Button(self.main_window, text="Exit", command=exit)
        exit_button.grid(column=2, row=5, sticky=N+W+S+E)

    def game_window(self):
        self.clear_frame()
        self.main_window.columnconfigure(0, weight=1)
        self.main_window.rowconfigure(0, weight=1)
        self.draw_space = Canvas(self.main_window, width=1280, height=640)
        self.draw_space.grid(sticky=N+W+S+E)
        self.player1 = Player(320)
        #self.player2 = Player()
        self.game_loop()

    def game_loop(self):
        window_width, window_height = self.window_size()
        
        # move to event for changing window size (if it exists)
        self.calculate_player_size(window_width, window_height)
        self.draw_space.delete(ALL)
        #receive other players position
        print(self.player1.y_pos)
        self.draw_players(window_width)
        self.master.after(16, self.game_loop)

    def inputs(self, event):
        #print(event.char)
        match event.char:
            case 'w':
                print("moving up...")
                self.player1.move(-1)
            case 's':
                print("moving down...")
                self.player1.move(1)

    def draw_players(self, window_width):
        x_pos = window_width * 0.04
        self.draw_space.create_rectangle(x_pos, self.player1.y_pos, x_pos + self.player_width, self.player1.y_pos + self.player_height, fill="#000000")
        #self.draw_space.create_rectangle(window_width - x_pos, y_pos, window_width - x_pos + self.player_width, y_pos + self.player_height, fill="#000000")

    def calculate_player_size(self, window_width, window_height):
        self.player_width = window_width * 0.01
        #print(self.main_window.winfo_height())
        self.player_height = window_height * 0.1
        #print(self.player_height)

    def window_size(self):
        return self.main_window.winfo_width(), self.main_window.winfo_height()



class Player:
    def __init__(self, start_pos):
        self.y_pos = start_pos
        self.speed = 5
    def move(self, inputs):
        self.y_pos += inputs * self.speed
        


class Server:
    def __init__(self):
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


                # todo handle client8btgv G3REF V
                # thread.start_new_thread(self.client_handler, (client, client_address, lock)) 


                self.current_connections += 1
                print(self.current_connections)
                # print(self.LANG['connection_count'].format(current_connections))
        
        

class Client:
    def __init__(self):
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(("localhost", 9000))



def main():
    app = Application(Tk())
    app.main_menu()
    app.master.bind('<KeyPress>', app.inputs)
    app.mainloop()


if __name__ == "__main__":
    main()

