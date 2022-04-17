import lib.custom_networking as cn
from tkinter import *
from socket import *
import threading
import math
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
            self.main_window.grid_rowconfigure(i, weight=0)
            self.main_window.grid_columnconfigure(i, weight=0)
    
    def main_menu(self):
        self.main_window = self.winfo_toplevel()
        for i in range(0, 7): self.main_window.rowconfigure(i, weight=1)
        for i in range(0, 5): self.main_window.columnconfigure(i, weight=1)
        join_button = Button(self.main_window, text="Join", command=self.start_as_client)
        join_button.grid(column=2, row=3, sticky=N+W+S+E)
        exit_button = Button(self.main_window, text="Exit", command=exit)
        exit_button.grid(column=2, row=5, sticky=N+W+S+E)

    def game_window(self):
        self.clear_frame()
        self.main_window.columnconfigure(0, weight=1)
        self.main_window.rowconfigure(0, weight=1)
        self.draw_space = Canvas(self.main_window, width=self.screen_width, height=self.screen_height)
        self.draw_space.grid(sticky=N+W+S+E)
        self.player1 = Player(self.screen_height/2)
        self.player2 = Player(self.screen_height/2)
        self.ball = Ball(self.screen_width/2, self.screen_height/2)
        self.game_loop()

    def game_loop(self):
        self.draw_space.delete(ALL)
        self.draw_ball()
        self.draw_players()
        self.draw_ui()
        self.master.after(self.frame_time, self.game_loop)

    def draw_players(self):
        self.draw_space.create_rectangle(self.player1x_pos, self.player1.y_pos, self.player1x_pos + self.player_width, self.player1.y_pos + self.player_height, fill="#0000ff")
        self.draw_space.create_rectangle(self.player2x_pos - self.player_width, self.player2.y_pos, self.player2x_pos, self.player2.y_pos + self.player_height, fill="#ff0000")
    
    def draw_ball(self):
        self.draw_space.create_oval(self.ball.x_pos - self.ball_size, self.ball.y_pos - self.ball_size, self.ball.x_pos + self.ball_size, self.ball.y_pos + self.ball_size ,fill="#000000")

    def draw_ui(self):
        self.draw_space.create_text(self.point1_x_pos, self.points_y_pos, text=self.player1.points)
        self.draw_space.create_text(self.point2_x_pos, self.points_y_pos, text=self.player2.points)

    def calculate_player_size(self):
        self.player_width = self.window_width * 0.01
        self.player_height = self.window_height * 0.1
        self.ball_size = 20
        self.player1x_pos = self.window_width * 0.04
        self.player2x_pos = self.window_width - self.player1x_pos

    def calculate_ui_size(self):
        self.point1_x_pos = self.window_width / 5
        self.point2_x_pos = self.window_width - self.point1_x_pos
        self.points_y_pos = self.window_height / 10

    def detect_collision(self):
        # for face in self.ball.hitbox:
        #     if face
        if self.ball.y_pos <= 0 or self.ball.y_pos >= self.window_height:
            # print((cmath.acos(self.ball.move_direction) * 180) / math.pi)
            angle_out = (math.acos(180 - self.ball.move_direction) * 180) / math.pi
            print(angle_out)
            #self.ball.move_direction = (cmath.acos(self.ball.move_direction) * 180) / math.pi * 2
        # turn into match statement
        if self.ball.x_pos >= self.window_width:
            self.player1.points += 1
            self.ball.reset(self.window_width/2, self.window_height/2)
        if self.ball.x_pos <= 0:
            self.player2.points += 1
            self.ball.reset(self.window_width/2, self.window_height/2)
            
    def configure_event(self, event):
        self.window_width, self.window_height = event.width, event.height
        self.calculate_player_size()
        self.calculate_ui_size()

    def inputs(self, event):
        match event.char:
            case 'w':
                print("moving up...")
                cn.send_message(self.client.client_socket, -1)
            case 's':
                print("moving down...")
                cn.send_message(self.client.client_socket, 1)

    def start_as_client(self):
        self.client = Client(self)
        self.game_window()
        

class Ball:
    def __init__(self, start_width, start_height):
        self.x_pos = start_width
        self.y_pos = start_height


class Player:
    def __init__(self, start_height):
        self.y_pos = start_height
        self.points = 0


class Client:
    def __init__(self, app):
        self.app = app
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        while True:
            try:
                self.client_socket.connect(("localhost", cn.PORT))
                threading.Thread(target=self.connection_handler)
                break
            except Exception as e:
                print(e)
    def connection_handler(self):
        while self.client_socket is not None:
            try:
                # receive coords
                print("receive")
                self.app.ball.x_pos = cn.receive_message(self.client_socket, float)
                self.app.ball.y_pos = cn.receive_message(self.client_socket, float)
                self.app.player1.y_pos = cn.receive_message(self.client_socket, float)
                self.app.player2.y_pos = cn.receive_message(self.client_socket, float)
                self.app.player1.points = cn.receive_message(self.client_socket, int)
                self.app.player2.points = cn.receive_message(self.client_socket, int)
            except Exception as e:
                print(e)
                self.client_socket.close()
                break
        

def main():
    app = Application(Tk(), 60)
    app.master.title("Pong multiplayer")
    app.main_menu()
    app.master.bind('<KeyPress>', app.inputs)
    app.master.bind('<Configure>', app.configure_event)
    app.mainloop()


if __name__ == "__main__":
    main()
