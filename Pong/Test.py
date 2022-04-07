import lib.custom_networking as cn
import math, time, random, cmath
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
            self.main_window.grid_rowconfigure(i, weight=0)
            self.main_window.grid_columnconfigure(i, weight=0)
    
    def main_menu(self):
        self.main_window = self.winfo_toplevel()
        for i in range(0, 7): self.main_window.rowconfigure(i, weight=1)
        for i in range(0, 5): self.main_window.columnconfigure(i, weight=1)
        host_button = Button(self.main_window, text="Host", command=self.start_as_server)
        host_button.grid(column=2, row=1, sticky=N+W+S+E)
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
        self.player1 = Player(self.screen_height/2, self)
        self.player2 = Player(self.screen_height/2, self)
        self.ball = Ball(self.screen_width/2, self.screen_height/2, self)
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

    def draw_players(self):
        self.draw_space.create_rectangle(self.player1x_pos, self.player1.y_pos, self.player1x_pos + self.player_width, self.player1.y_pos + self.player_height, fill="#0000ff")
        self.draw_space.create_rectangle(self.player2x_pos - self.player_width, self.player2.y_pos, self.player2x_pos, self.player2.y_pos + self.player_height, fill="#ff0000")
    
    def draw_ball(self):
        self.draw_space.create_oval(self.ball.x_pos - self.ball_size, self.ball.y_pos - self.ball_size, self.ball.x_pos + self.ball_size, self.ball.y_pos + self.ball_size ,fill="#000000")

    def draw_ui(self):
        # point_info = [self.point1_x_pos, self.points_y_pos, self.player1.points, self.point2_x_pos, self.points_y_pos, self.player2.points]
        # for i in range(0, 2):
        #     x_pos, y_pos, points = point_info[0+i*3], point_info[1+i*3],point_info[2+i*3],
        #     self.draw_space.create_text(x_pos, y_pos, text=points)
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
                cn.send_message(-1)
            case 's':
                print("moving down...")
                cn.send_message(1)

    def start_as_server(self):
        self.server = Server(self)
        self.game_window()
    
    def start_as_client(self):
        self.game_window()


class Ball:
    def __init__(self, start_width, start_height, hitbox):
        self.x_pos = start_width
        self.y_pos = start_height
        self.speed = 5
        self.hitbox = hitbox
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
    def __init__(self, start_height, hitbox):
        self.y_pos = start_height
        self.speed = 5
        self.hitbox = hitbox
        self.points = 0
    def move(self, inputs):
        self.y_pos += inputs * self.speed


class Server:
    def __init__(self, app):
        print("Starting server!")
        server_socket = socket(AF_INET, SOCK_STREAM)
        server_socket.bind(("localhost", cn.PORT)) # gethostname()
        server_socket.listen(cn.MAX_QUEUE)
        self.clients = []
        self.current_connections = 0
        print("server started!")
        while True:
            try:
                if current_connections < self.SERVER_CONFIG['max_connections']:
                    client, _ = server_socket.accept()
                    self.clients.append(client)
                    thread.start_new_thread(self.client_handler, (client, client_address, lock))
                    current_connections += 1
                    print("Current connections:", current_connections)
                else:
                    break
            except Exception as e:
                print(e)
    def client_handler(self, client, client_address, lock):
        while True:
            try:
                message = cn.receive_message(client)
            except Exception as e:
                print(e)
                client.close()
                break
        with lock:
            global current_connections
            current_connections -= 1
            


def main():
    app = Application(Tk(), 60)
    app.master.title("Pong multiplayer")
    app.main_menu()
    app.master.bind('<KeyPress>', app.inputs)
    app.master.bind('<Configure>', app.configure_event)
    app.mainloop()


if __name__ == "__main__":
    main()
