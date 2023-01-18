from tkinter import *
import threading
import random
import time
import math


class Application(Frame):
    # setup of basic necessities
    def __init__(self, master, frame_target: int):
        Frame.__init__(self, master)
        self.grid(sticky=N+W+S+E)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.main_window = self.winfo_toplevel()
        self.screen_width, self.screen_height = self.main_window.winfo_screenwidth(
        ), self.main_window.winfo_screenheight()
        self.window_width, self.window_height = 0, 0
        self.frame_target = int(1000/frame_target)
        self.game_speed = 1.0
        self.real_dt = 0.0
        # empty placeholders
        self.last_update_time = 0
        self.draw_space = None
        self.ball = None

    # prepares the main window for the gameloop
    def setup(self):
        self.main_window.columnconfigure(0, weight=1)
        self.main_window.rowconfigure(0, weight=1)
        self.master.bind('<Configure>', self.configure_event)
        # self.master.bind('<KeyPress>', self.inputs)
        self.draw_space = Canvas(
            self, width=self.screen_width/2, height=self.screen_height/2, background="#deccab")
        self.draw_space.grid(sticky=N+W+S+E)
        self.configure_event()
        # self.update()
        self.ball = Ball(self.window_width/2, self.window_height/2, 10)

        self.last_update_time = time.time()

    # calls draw and delte functions
    # plus moves the ball and checks collisions if client is connected
    def game_loop(self):
        start_time = time.time()
        self.real_dt = start_time - self.last_update_time
        self.last_update_time += self.real_dt
        game_dt = self.real_dt * self.game_speed

        self.draw_space.delete(ALL)
        print(game_dt)
        self.ball.move(game_dt)
        self.draw_space.create_rectangle(
            self.window_width/2 - 20, self.window_height/2, self.window_width/2 + 20, self.window_height, fill="#00ffff")
        self.ball.draw(self.draw_space, self.window_width, self.window_height)
        if self.real_dt > 0:
            self.draw_space.create_text(
                self.window_width/2, 50, text=f"fps{1/self.real_dt}")
        delay = int(self.frame_target - (time.time() - start_time))
        self.master.after(delay, self.game_loop)

    # draws a circle on the canvas
    def draw_circle(self, x: int, y: int, radius: float, color: str = "#000000"):
        return self.draw_space.create_oval(x - radius, y - radius, x + radius, y + radius, fill=color)

    # draws the ball on the canvas
    def draw_ball(self):
        self.draw_space.create_oval(self.ball.x_pos - self.ball.radius, self.ball.y_pos - self.ball.radius,
                                    self.ball.x_pos + self.ball.radius, self.ball.y_pos + self.ball.radius, fill="#000000")

    # returns the size of the window
    def get_window_size(self) -> None:
        self.window_width, self.window_height = self.main_window.winfo_width(
        ), self.main_window.winfo_height()

    # calculates the UI size from the window size
    def get_ui_size(self):
        pass

    def detect_collision(self):
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
        self.get_window_size()
        self.get_ui_size()


class Ball:
    # setup of basic necessities for the ball
    def __init__(self, start_width: int, start_height: int, radius):
        self.x_start = start_width
        self.y_start = start_height
        self.x_pos = start_width
        self.y_pos = start_height
        self.radius = radius
        self.speed = -9.82

    # set the x and y coordinates for the ball
    def set_pos(self, x: int, y: int) -> None:
        self.x_pos = x
        self.y_pos = y

    # moves the ball
    def move(self, delta_time):
        self.y_pos -= self.speed * delta_time  # (1 + delta_time)

    # draw
    def draw(self, canvas, width, height, color: str = "#000000"):
        x_offset = width/2 - self.x_start
        y_offset = height/2 - self.y_start
        # print(x_offset, y_offset)
        canvas.create_oval(x_offset + (self.x_pos - self.radius), y_offset + (self.y_pos - self.radius),
                           x_offset + (self.x_pos + self.radius), y_offset + (self.y_pos + self.radius), fill=color)

    # resets ball to start position
    def reset(self, start_width, start_height):
        self.x_pos = start_width
        self.y_pos = start_height
        self.speed = self.start_speed
        self.direction()


class fluid():
    def __init__(self):
        pass

    def draw(self):
        pass


def main():
    app = Application(Tk(), 120)
    app.master.title("Simulation")
    app.setup()
    app.game_loop()
    app.mainloop()


if __name__ == "__main__":
    main()
