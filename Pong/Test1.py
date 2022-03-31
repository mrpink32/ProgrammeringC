from tkinter import *
import websocket
import threading


class Application(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid(sticky=N+W+S+E)
    
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
        self.draw_space.grid(sticky=N+W+S+E) #, rowspan=10, columnspan=10
        self.player1 = Player(320)
        self.player2 = Player(320)
        self.game_loop()

    def game_loop(self):
        self.draw_space.delete(ALL)
        self.window_size()
        self.calculate_player_size()
        #receive other players position
        #print(self.player1.y_pos)
        self.draw_players()
        self.master.after(16, self.game_loop)

    def draw_players(self):
        self.player1.x_pos = self.window_width * 0.04
        self.player2.x_pos = self.window_width - self.window_width * 0.04 
        self.draw_space.create_rectangle(self.player1.x_pos, self.player1.y_pos, self.player1.x_pos + self.player_width, self.player1.y_pos + self.player_height, fill="#0000ff")
        self.draw_space.create_rectangle(self.player2.x_pos - self.player_width, self.player2.y_pos, self.player2.x_pos, self.player2.y_pos + self.player_height, fill="#ff0000")

    def draw_ball(self,Ball_speed_x, Ball_speed_y):
        Ball_thing = self.create_oval(10,10,50,50,fill = "black")
        #https://youtu.be/XFU7FC-i-_Y til resten af lortet jeg mangler

    def calculate_player_size(self):
        self.player_width = self.window_width * 0.01
        self.player_height = self.window_height * 0.1

    def window_size(self):
        self.window_width, self.window_height = self.main_window.winfo_width(), self.main_window.winfo_height()

    def inputs(self, event):
        match event.char:
            case 'w':
                if self.player1.y_pos > 0:
                    print("moving up...")
                    self.player1.move(-self.window_height*0.01)
            case 's':
                if self.player1.y_pos < self.window_height - self.player_height:
                    print("moving down...")
                    self.player1.move(self.window_height*0.01)

class Ball:
    def __init__(self):
        Ball_speed_x = 3
        Ball_speed_y = 3

    def moveBall(self,Ball_thing):
        self.move(Ball_thing,Ball_speed_x,Ball_speed_y)
        (left_pos,top_pos,right_pos,bottom_pos) = self.coords()
        if left_pos <= 0 or right_pos >= 100:#fjern 100, det er en placeholder
            Ball_speed_x = -Ball_speed_x
        if top_pos <= 0 or bottom_pos >= 100: #--||--
            Ball_speed_y = -Ball_speed_y


class Player:
    def __init__(self, start_pos):
        self.x_pos = 0
        self.y_pos = start_pos
        #self.speed = 5 
    def move(self, inputs):    
        self.y_pos += inputs



class Server:
    def __init__(self):
        # print(self.LANG['startup_message'].format(self.SERVER_CONFIG['port']))
        print("Starting server!")
        server_socket = websocket.WebSocketApp("localhost")
        server_socket_thread = threading.Thread(target=lambda: server_socket.run_forever())
        server_socket_thread.start()
        self.current_connections = 0
        print("server started!")
        # print(self.LANG['started_message'].format(self.SERVER_CONFIG['host'], self.SERVER_CONFIG['port']))
        
        Client()
        server_socket.send(9)
        
        # while True:
        #     if self.current_connections < 1:
        #         client, client_address = self.server_socket.accept()
        #         print("grim")
                # print(self.LANG['connected_message'].format(client_address))


                #self.send_message(client, self.LANG['welcome_message'])


                # todo handle client8btgv G3REF V
                # thread.start_new_thread(self.client_handler, (client, client_address, lock)) 


                #self.current_connections += 1
                #print(self.current_connections)
                # print(self.LANG['connection_count'].format(current_connections))



class Client:
    def __init__(self):
        self.test_socket = websocket.WebSocketApp("localhost", on_message=self.grim)
        test_thread = threading.Thread(target=lambda: self.test_socket.run_forever())
        test_thread.start()
    def grim(self, message):
        print(message)



def main():
    app = Application(Tk())
    app.main_menu()
    app.master.bind('<KeyPress>', app.inputs)
    app.mainloop()


if __name__ == "__main__":
    main()
