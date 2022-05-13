import lib.custom_networking as cn
from tkinter import *
from socket import *
import math, random
import threading

class Application(Frame):
    # setup of basic necessities
    def __init__(self, master, frame_target):
        Frame.__init__(self, master)
        self.grid(sticky=N+W+S+E)
        self.screen_width, self.screen_height = 1920/2, 1080/2
        self.frame_time = math.floor(1000 / frame_target)
        self.is_client_connected = False
        self.is_host = False
    # clears main windopw and resets grid configurations
    def clear_frame(self):
        for widget in self.main_window.winfo_children():
            widget.destroy()
        #https://stackoverflow.com/questions/49313874/how-to-remove-columns-or-rows-while-redrawing-a-grid-in-python3-tkinter
        for i in range(0, 5):
            self.main_window.grid_rowconfigure(i, weight=0)
            self.main_window.grid_columnconfigure(i, weight=0)
    # creates the main menu
    def main_menu(self):
        self.main_window = self.winfo_toplevel()
        for i in range(0, 3): self.main_window.rowconfigure(i, weight=1)
        self.main_window.columnconfigure(0, weight=1)
        host_button = Button(self.main_window, text="Host", command=self.start_server)
        host_button.grid(column=0, row=0, sticky=N+W+S+E)
        join_button = Button(self.main_window, text="Join", command=self.start_client)
        join_button.grid(column=0, row=1, sticky=N+W+S+E)
        exit_button = Button(self.main_window, text="Exit", command=exit)
        exit_button.grid(column=0, row=2, sticky=N+W+S+E)
    # prepares the main window for the gameloop
    def game_window(self):
        self.clear_frame()
        self.main_window.columnconfigure(0, weight=1)
        self.main_window.rowconfigure(0, weight=1)
        self.draw_space = Canvas(self.main_window, width=self.screen_width, height=self.screen_height)
        self.draw_space.grid(sticky=N+W+S+E)
        self.ball = Ball(self.screen_width/2, self.screen_height/2)
        self.player1 = Player(self.screen_width * 0.04, self.screen_height/2)
        self.player2 = Player(self.screen_width - self.screen_width * 0.04, self.screen_height/2)
        self.master.bind('<Configure>', self.configure_event)
        self.master.bind('<KeyPress>', self.inputs)
        self.players = [self.player1, self.player2]
        self.configure_event()
        self.game_loop()
    # calls draw and delte functions 
    # plus moves the ball and checks collisions if client is connected
    def game_loop(self):
        self.draw_space.delete(ALL)
        if self.is_client_connected:
            self.ball.move()
            self.detect_collision()
        self.draw_ball()
        self.draw_players()
        self.draw_ui()
        self.master.after(self.frame_time, self.game_loop)
    # draws the ball on the ccanvas
    def draw_ball(self):
        self.draw_space.create_oval(self.ball.x_pos - self.ball.radius, self.ball.y_pos - self.ball.radius, self.ball.x_pos + self.ball.radius, self.ball.y_pos + self.ball.radius, fill="#000000")
    # draws players on the canvas
    def draw_players(self):
        for player in self.players:
            self.draw_space.create_rectangle(player.x_pos - self.player_width, player.y_pos - self.player_height, player.x_pos + self.player_width, player.y_pos + self.player_height, fill="#000000")
    # draws the points at the top of the screen
    def draw_ui(self):
        self.draw_space.create_text(self.point1_x_pos, self.points_y_pos, text=self.player1.points)
        self.draw_space.create_text(self.point2_x_pos, self.points_y_pos, text=self.player2.points)
    # returns the size of the window
    def get_window_size(self):
        return self.main_window.winfo_width(), self.main_window.winfo_height()
    # calculates the size of the payers from the window size and returns it
    def get_player_size(self):
        return self.window_width * 0.005, self.window_height * 0.05
    # calculates the UI size from the window size
    def get_ui_size(self):
        self.point1_x_pos = self.window_width / 5
        self.point2_x_pos = self.window_width - self.point1_x_pos
        self.points_y_pos = self.window_height / 10
    # handles collisions
    def detect_collision(self):
        # bounce ball away from player if midle of ball hits player
        for player in self.players:
            if (player.x_pos - self.player_width) < self.ball.x_pos < (player.x_pos + self.player_width) and (player.y_pos - self.player_height) < self.ball.y_pos < (player.y_pos + self.player_height): #self.ball.x_pos
                angle_out = 180 - self.ball.move_direction
                self.ball.move_direction = angle_out
                self.ball.speed += 0.25
        # bounce from top and bottom
        if self.ball.y_pos <= 0 or self.ball.y_pos >= self.window_height:
            angle_out = 360 - self.ball.move_direction
            self.ball.move_direction = angle_out
        # check for goals
        match self.ball.x_pos:
            case self.ball.x_pos if self.ball.x_pos >= self.window_width:
                self.player1.points += 1
                self.ball.reset(self.window_width/2, self.window_height/2)
            case self.ball.x_pos if self.ball.x_pos <= 0:
                self.player2.points += 1
                self.ball.reset(self.window_width/2, self.window_height/2)
    # recalculates player size and UI size from new window size
    def configure_event(self, event=None):
        self.window_width, self.window_height = self.get_window_size()
        self.player_width, self.player_height = self.get_player_size()
        self.get_ui_size()
    # gets input via the keypress event and moves the player
    def inputs(self, event):
        match event.char:
            case 'w':
                if self.is_host:
                    if self.player1.y_pos > 0 + self.player_height:
                        self.player1.move(-1)
                else:
                    if self.player2.y_pos > 0 + self.player_height:
                        self.player2.move(-1)
            case 's':
                if self.is_host:
                    if self.player1.y_pos < self.window_height - self.player_height:
                        self.player1.move(1)
                else:
                    if self.player2.y_pos < self.window_height - self.player_height:
                        self.player2.move(1)
            # case '\x1b':
                # exit()
    # starts the game as a host
    def start_server(self):
        self.is_host = True
        server_thread = threading.Thread(target=lambda : Server(self))
        server_thread.start()
        self.game_window()
    # starts the game as a client
    def start_client(self):
        client_thread = threading.Thread(target=lambda : Client(self))
        client_thread.start()
        self.game_window()

class Ball:
    # setup of basic necessities for the ball
    def __init__(self, start_width, start_height, start_speed=2, ball_radius=10):
        self.x_pos = start_width
        self.y_pos = start_height
        self.radius = ball_radius
        self.start_speed = start_speed
        self.speed = start_speed
        self.direction()
    # moves the ball
    def move(self):
        move_direction_radian = (self.move_direction * math.pi) / 180        
        self.x_pos += math.cos(move_direction_radian) * self.speed
        self.y_pos += math.sin(move_direction_radian) * self.speed
    # resets ball to start position
    def reset(self, start_width, start_height):
        self.x_pos = start_width
        self.y_pos = start_height
        self.speed = self.start_speed
        self.direction()
    # generates a move direction for the ball
    def direction(self):
        while True: 
            val = random.randint(1, 359)
            if val in range(80, 100) or val in range(260, 280) or val != 180:
                self.move_direction = val
                print(self.move_direction)
                break

class Player:
    # setup of basic necessities for the player
    def __init__(self, start_width, start_height):
        self.x_pos = start_width
        self.y_pos = start_height
        self.speed = 10
        self.points = 0
    # moves the player
    def move(self, inputs):
        self.y_pos += inputs * self.speed

class Server:
    # starts the server and waits for a client to connect
    # if client is connected sends and receives data
    def __init__(self, app):
        print("Starting server!")
        server_socket = socket(AF_INET, SOCK_STREAM)
        server_socket.bind(("localhost", cn.PORT)) #gethostname()
        server_socket.listen(cn.MAX_QUEUE)
        current_connections = 0
        print("server started!")
        while True:
            try: 
                if current_connections < cn.MAX_CONNECTIONS:
                    self.client, _ = server_socket.accept()
                    current_connections += 1
                    app.is_client_connected = True
                    print("Current connections:", current_connections)
                else:
                    # send coords
                    payload = f"{app.ball.x_pos},{app.ball.y_pos},{app.player1.y_pos},{app.player1.points},{app.player2.points}"
                    cn.send_message(self.client, payload)
                    # receive coords
                    app.player2.y_pos = cn.receive_message(self.client, float)
            except Exception as e:
                print(e)
                current_connections -= 1
                app.is_client_connected = False

class Client:
    # setup of basic necessities for the ball
    def __init__(self, app):
        client_socket = socket(AF_INET, SOCK_STREAM)
        # enters a loop of trying to connect to the server
        while True:
            try:
                client_socket.connect((cn.HOST, cn.PORT))
                print("Connected")
                # enters a loop acountable for receiving and sending data to the server
                while client_socket is not None:
                    try:
                        # receive data from server
                        packet = cn.receive_message(client_socket).split(',')
                        app.ball.x_pos = float(packet[0])
                        app.ball.y_pos = float(packet[1])
                        app.player1.y_pos = float(packet[2])
                        app.player1.points = int(packet[3])
                        app.player2.points = int(packet[4])
                        # send coords to server
                        cn.send_message(client_socket, app.player2.y_pos)
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