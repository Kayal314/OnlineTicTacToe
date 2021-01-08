import tkinter as tk
from client import Client
from functools import partial
from tkinter import messagebox


class Player:
    def __init__(self, pl_no):
        self.window = tk.Tk()
        self.window.geometry('500x500')
        self.window.title('Player' + str(pl_no))
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        cross = tk.PhotoImage(file='Icons\\cross.png')
        circle = tk.PhotoImage(file='Icons\\circle.png')
        self.window.resizable(0, 0)  # to make the window non-resizable
        self.buttons = []
        self.made_moves = [False] * 9
        self.prompt = tk.Label(self.window, text='Welcome!', font=("Times New Roman", 25))
        self.prompt.place(x=100, y=30, width=300, height=50)
        self.my_turn = [False, False, False]  # [it is my turn, I won the game, there are 2 players in the game]
        # player 1 is the cross and player 2 is the circle
        if pl_no == 1:
            self.me = cross
            self.other = circle
            self.my_turn[0] = True
        elif pl_no == 2:
            self.me = circle
            self.other = cross
        for i in range(0, 9):
            self.buttons.append(tk.Button(master=self.window, highlightthickness=1, bd=1))
            pos_x = int(i % 3) * 120 + 70
            pos_y = int(i / 3) * 120 + 80
            self.buttons[i].place(x=pos_x, y=pos_y, width=120, height=120)
        for i in range(0, 9):
            move_cmd = partial(self.__make_move, i)
            self.buttons[i].config(command=move_cmd)

        self.player = Client(pl_no, self.buttons, self.other, self.my_turn, self.prompt, self.made_moves)

        self.window.mainloop()

    def __make_move(self, index):
        if not self.my_turn[2]:
            # there is just one player so game can't start
            messagebox.showinfo('Wait', 'Waiting for Rival')
        elif self.my_turn[0] and not self.my_turn[1]:
            if self.made_moves[index]:
                messagebox.showinfo('Invalid move', "Place already used")
            else:
                self.buttons[index].config(image=self.me)
                self.made_moves[index] = True
                self.player.send_messages(str(index))
                self.my_turn[0] = False
                self.prompt.config(text='Rival\'s Turn')
        else:
            if self.my_turn[1]:
                msg = 'Game Over!'
            else:
                msg = "Wait for your turn"
            messagebox.showinfo("Invalid Move", msg)

    def on_closing(self):
        self.player.disconnect()
        self.window.destroy()
