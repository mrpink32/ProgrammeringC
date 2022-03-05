from tkinter import *
import socket
import math


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
        host_button = Button(self.main_window, text="Host", command=self.game_window)
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
        # move to game loop or handler of event for changing window size (if it exists)
        self.calculate_player_size()
        self.game_loop(0)

    def game_loop(self, i):
        self.draw_space.delete(ALL)
        #receive other players position
        v = 320 + (math.sin((i * math.pi) / 180) * 256)
        print(v, i)
        self.draw_player(v)
        i += 1
        self.master.after(16, self.game_loop, i)

    def draw_player(self, y_pos):
        # make dependent on window width
        x_pos = 50
        self.draw_space.create_rectangle(x_pos, y_pos, x_pos + self.player_width, y_pos + self.player_height, fill="#000000")

    def calculate_player_size(self):
        self.player_width = self.main_window.winfo_width() * 0.1 #0.01
        #print(self.main_window.winfo_height())
        self.player_height = self.main_window.winfo_height() * 0.5 #0.10
        #print(self.player_height)


class Server():
    def __init__(self):
        #self.server = 
        pass
        


class Client():
    pass


def main():
    app = Application(Tk())
    app.main_menu()
    app.mainloop()


if __name__ == "__main__":
    main()
