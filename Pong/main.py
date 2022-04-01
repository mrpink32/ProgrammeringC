from cmath import pi
import lib.custom_networking as cn
import math, time, random
import _thread as thread
from tkinter import *
from socket import *

#import screeninfo


class Application(Frame):
    def __init__(self, master, frame_target):
        Frame.__init__(self, master)
        self.grid(sticky=N+W+S+E)
        self.screen_width, self.screen_height = 1920, 1080 #screeninfo.get_monitors()[0].width, screeninfo.get_monitors()[0].height
        self.frame_time = math.floor(1000 / frame_target)

    
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
        self.player1 = Player(self.screen_height/2)
        self.player2 = Player(self.screen_height/2)
        self.ball = Ball(self.screen_width/2, self.screen_height/2)
        self.draw_space = Canvas(self.main_window, width=self.screen_width, height=self.screen_height)
        self.draw_space.grid(sticky=N+W+S+E)
        self.is_game_running = True
        self.game_loop()

    def game_loop(self):
        self.draw_space.delete(ALL)
        self.ball.move()
        self.draw_ball()
        self.draw_players()
        self.master.after(self.frame_time, self.game_loop)

    def draw_players(self):
        self.draw_space.create_rectangle(self.player1x_pos, self.player1.y_pos, self.player1x_pos + self.player_width, self.player1.y_pos + self.player_height, fill="#0000ff")
        self.draw_space.create_rectangle(self.player2x_pos - self.player_width, self.player2.y_pos, self.player2x_pos, self.player2.y_pos + self.player_height, fill="#ff0000")

    def draw_ball(self):
        self.draw_space.create_oval(self.ball.x_pos - self.ball_size, self.ball.y_pos - self.ball_size, self.ball.x_pos + self.ball_size, self.ball.y_pos + self.ball_size ,fill="#000000")
        #https://youtu.be/XFU7FC-i-_Y til resten af lortet jeg mangler

    def calculate_player_size(self):
        self.player_width = self.window_width * 0.01
        self.player_height = self.window_height * 0.1
        self.ball_size = 15
        self.player1x_pos = self.window_width * 0.04
        self.player2x_pos = self.window_width - self.player1x_pos

    def window_size(self):
        self.window_width, self.window_height = self.main_window.winfo_width(), self.main_window.winfo_height()

    def configure_event(self, event):
        self.window_width, self.window_height = event.width, event.height
        #self.window_size()
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
        self.game_window()
        thread.start_new_thread(lambda:Server(app=self))
    
    def start_client(self):
        self.game_window()
        #threading.Thread(target=lambda : Client(self)).start()
        thread.start_new_thread(lambda:Client(app=self))



class Ball:
    def __init__(self, start_width, start_height):
        self.x_pos = start_width
        self.y_pos = start_height
        self.speed = 5
        self.move_direction = random.randint(1, 359)
    def move(self):
        move_direction_radian = (self.move_direction * math.pi)/180        
        self.x_pos += math.sin(move_direction_radian) * self.speed
        self.y_pos += math.cos(move_direction_radian) * self.speed



class Player:
    def __init__(self, start_height):
        self.y_pos = start_height
        self.speed = 5
    def move(self, inputs):
        self.y_pos += inputs * self.speed



class Server:
    def __init__(self, app):
        # print(self.LANG['startup_message'].format(self.SERVER_CONFIG['port']))
        print("Starting server!")
        server_socket=socket(AF_INET, SOCK_STREAM)
        server_socket.bind((cn.HOST, cn.PORT))
        server_socket.listen(cn.MAX_QUEUE)
        current_connections=0
        print("server started!")
        # print(self.LANG['started_message'].format(self.SERVER_CONFIG['host'], self.SERVER_CONFIG['port']))
        while True:
            try:
                if current_connections<cn.MAX_CONNECTIONS:
                    self.client, client_address=server_socket.accept()
                    # print(self.LANG['connected_message'].format(client_address))
                    #self.send_message(client, self.LANG['welcome_message'])
                    # thread.start_new_thread(self.client_handler, (client, client_address, lock)) 
                    current_connections+=1
                    print("Current connections:", current_connections)
                    # print(self.LANG['connection_count'].format(current_connections))
                else:
                    # send coords
                    cn.send_message(self.client, app.player1.y_pos)
                    #print("Coords sent:", result)
                    # receive coords
                    package=float(cn.receive_message(self.client))
                    app.player2.y_pos=package
                    time.sleep(0.005)
            except Exception as e:
                print(e)
                current_connections-=1
        


class Client:
    def __init__(self, app):
        client_socket=socket(AF_INET, SOCK_STREAM)
        while True:
            try:
                client_socket.connect((cn.HOST, cn.PORT))
                while client_socket is not None:
                    try:
                        # receive coords
                        package=float(cn.receive_message(client_socket))
                        app.player2.y_pos=package
                        # send coords
                        cn.send_message(client_socket, app.player1.y_pos)
                    except Exception as e:
                        print(e)
                        break
            except Exception as e:
                print(e)


def main():
    app = Application(Tk(), 60)
    app.master.title("Pong multiplayer")
    app.main_menu()
    app.master.bind('<KeyPress>', app.inputs)
    app.master.bind('<Configure>', app.configure_event)
    app.mainloop()


if __name__ == "__main__":
    main()
