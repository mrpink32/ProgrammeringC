import lib.custom_networking as cn
import math, time, random
import _thread as thread
import threading
from tkinter import *
from socket import *


class Application(Frame):
    def __init__(self, master, frame_target):
        Frame.__init__(self, master)
        self.grid(sticky=N+W+S+E)
        self.screen_width, self.screen_height = 1920/2, 1080/2
        self.frame_time = math.floor(1000 / frame_target)
        self.is_client_connected = False
        self.is_host = False

    def clear_frame(self):
        for widget in self.main_window.winfo_children():
            widget.destroy()
        #https://stackoverflow.com/questions/49313874/how-to-remove-columns-or-rows-while-redrawing-a-grid-in-python3-tkinter
        for i in range(0, 7):
            self.main_window.grid_rowconfigure(i, weight=0)
            self.main_window.grid_columnconfigure(i, weight=0)
    
    def main_menu(self):
        self.main_window = self.winfo_toplevel()
        for i in range(0, 7): self.main_window.rowconfigure(i, weight=1)
        for i in range(0, 5): self.main_window.columnconfigure(i, weight=1)
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
        self.draw_space = Canvas(self.main_window, width=self.screen_width, height=self.screen_height)
        self.draw_space.grid(sticky=N+W+S+E)
        self.ball = Ball(self.screen_width/2, self.screen_height/2, 15)
        self.player1 = Player(self.screen_width * 0.04, self.screen_height/2)
        self.player2 = Player(self.screen_width - self.screen_width * 0.04, self.screen_height/2)
        self.master.bind('<Configure>', self.configure_event)
        self.master.bind('<KeyPress>', self.inputs)
        self.configure_event()
        self.game_loop()

    def game_loop(self):
        self.draw_space.delete(ALL)
        if self.is_client_connected:
            self.ball.move()
            self.detect_collision()
        self.draw_ball()
        self.draw_players()
        self.draw_ui()
        self.master.after(self.frame_time, self.game_loop)

    def draw_ball(self):
        self.draw_space.create_oval(self.ball.x_pos - self.ball.radius, self.ball.y_pos - self.ball.radius, self.ball.x_pos + self.ball.radius, self.ball.y_pos + self.ball.radius, fill="#000000")

    def draw_players(self):
        self.draw_space.create_rectangle(self.player1.x_pos, self.player1.y_pos, self.player1.x_pos + self.player_width, self.player1.y_pos + self.player_height, fill="#0000ff")
        self.draw_space.create_rectangle(self.player2.x_pos - self.player_width, self.player2.y_pos, self.player2.x_pos, self.player2.y_pos + self.player_height, fill="#ff0000")

    def draw_ui(self):
        # point_info = [self.point1_x_pos, self.points_y_pos, self.player1.points, self.point2_x_pos, self.points_y_pos, self.player2.points]
        # for i in range(0, 2):
        #     x_pos, y_pos, points = point_info[0+i*3], point_info[1+i*3],point_info[2+i*3],
        #     self.draw_space.create_text(x_pos, y_pos, text=points)
        self.draw_space.create_text(self.point1_x_pos, self.points_y_pos, text=self.player1.points)
        self.draw_space.create_text(self.point2_x_pos, self.points_y_pos, text=self.player2.points)

    def get_window_size(self):
        return self.main_window.winfo_width(), self.main_window.winfo_height()

    def get_player_size(self):
        return self.window_width * 0.01, self.window_height * 0.1

    def get_ui_size(self):
        self.point1_x_pos = self.window_width / 5
        self.point2_x_pos = self.window_width - self.point1_x_pos
        self.points_y_pos = self.window_height / 10

    def detect_collision(self):
        # for face in self.ball.hitbox:
        #     if face
        if self.ball.x_pos <= self.player1.x_pos and self.player1.y_pos > self.ball.y_pos < self.player1.y_pos + self.player_height:
            angle_out = 360 - self.ball.move_direction
            self.ball.move_direction = angle_out
        if self.ball.y_pos <= 0 or self.ball.y_pos >= self.window_height:
            angle_out = 360 - self.ball.move_direction
            self.ball.move_direction = angle_out
        match self.ball.x_pos:
            case self.ball.x_pos if self.ball.x_pos >= self.window_width:
                self.player1.points += 1
                self.ball.reset(self.window_width/2, self.window_height/2)
            case self.ball.x_pos if self.ball.x_pos <= 0:
                self.player2.points += 1
                self.ball.reset(self.window_width/2, self.window_height/2)
            
    def configure_event(self, event=None):
        self.window_width, self.window_height = self.get_window_size()
        self.player_width, self.player_height = self.get_player_size()
        self.get_ui_size()

    def inputs(self, event):
        match event.char:
            case 'w':
                if self.is_host:
                    if self.player1.y_pos > 0:
                        print("moving up...")
                        self.player1.move(-1)
                else:
                    if self.player2.y_pos > 0:
                        print("moving up...")
                        self.player2.move(-1)
            case 's':
                if self.is_host:
                    if self.player1.y_pos < self.window_height - self.player_height:
                        print("moving down...")
                        self.player1.move(1)
                else:
                    if self.player2.y_pos < self.window_height - self.player_height:
                        print("moving down...")
                        self.player2.move(1)

    def start_server(self):
        self.is_host = True
        self.game_window()
        #thread.start_new_thread(lambda : Server(app=self))
        server_thread = threading.Thread(target=lambda : Server(self))
        server_thread.start()
    
    def start_client(self):
        self.game_window()
        # thread.start_new_thread(lambda : Client(app=self))
        client_thread = threading.Thread(target=lambda : Client(self))
        client_thread.start()
        #thread.start_new_thread(Client, (self))

class Ball:
    def __init__(self, start_width, start_height, ball_radius=15):
        self.x_pos = start_width
        self.y_pos = start_height
        self.radius = ball_radius
        self.speed = 5
        self.direction()

    def move(self):
        move_direction_radian = (self.move_direction * math.pi) / 180        
        self.x_pos += math.cos(move_direction_radian) * self.speed
        self.y_pos += math.sin(move_direction_radian) * self.speed

    def reset(self, start_width, start_height):
        self.x_pos = start_width
        self.y_pos = start_height
        self.direction()

    def direction(self):
        while True: 
            val = random.randint(0, 360)
            if val != 90 or val != 270:
                self.move_direction = val
                print(self.move_direction)
                break

class Player:
    def __init__(self, start_width, start_height):

        self.x_pos = start_width
        self.y_pos = start_height
        self.speed = 5
        self.points = 0

    def move(self, inputs):
        self.y_pos += inputs * self.speed

class Server:
    def __init__(self, app):
        # print(self.LANG['startup_message'].format(self.SERVER_CONFIG['port']))
        print("Starting server!")
        server_socket = socket(AF_INET, SOCK_STREAM)
        server_socket.bind((gethostname(), cn.PORT)) # gethostname()
        server_socket.listen(cn.MAX_QUEUE)
        current_connections = 0
        print("server started!")
        # print(self.LANG['started_message'].format(self.SERVER_CONFIG['host'], self.SERVER_CONFIG['port']))
        while True:
            try: 
                if current_connections < cn.MAX_CONNECTIONS:
                    self.client, _ = server_socket.accept()
                    current_connections += 1
                    app.is_client_connected = True
                    print("Current connections:", current_connections)
                else:
                    print("starting to send and receive")
                    # send coords
                    payload = [app.ball.x_pos, app.ball.y_pos, app.player1.y_pos, app.player1.points, app.player2.points]
                    for item in payload: 
                        cn.send_message(self.client, item)
                        print("send message")
                        time.sleep(0.01)
                    # receive coords
                    app.player2.y_pos = cn.receive_message(self.client, float)
                    print("tasks done")
            except Exception as e:
                print(e)
                current_connections -= 1
                app.is_client_connected = False

class Client:
    def __init__(self, app):
        client_socket = socket(AF_INET, SOCK_STREAM)
        while True:
            try:
                client_socket.connect(("192.168.0.25", cn.PORT)) # 10.156.188.58
                print("Connected")
                while client_socket is not None:
                    try:
                        print("receiving and sending...")
                        # receive coords
                        app.ball.x_pos = cn.receive_message(client_socket, float)
                        print("receiving and sending...")
                        app.ball.y_pos = cn.receive_message(client_socket, float)
                        print("receiving and sending...")
                        app.player1.y_pos = cn.receive_message(client_socket, float)
                        print("receiving and sending...")
                        app.player1.points = cn.receive_message(client_socket, int)
                        print("receiving and sending...")
                        app.player2.points = cn.receive_message(client_socket, int)
                        print("receiving and sending...")
                        # send coords
                        cn.send_message(client_socket, app.player2.y_pos)
                        print("tasks done")
                    except Exception as e:
                        print(e)
            except Exception as e:
                print(e)

def main():
    app = Application(Tk(), 60)
    app.master.title("Pong multiplayer")
    app.main_menu()
    app.mainloop()

if __name__ == "__main__":
    main()