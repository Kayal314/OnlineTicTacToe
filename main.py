from frontEnd import Player


import tkinter as tk

window = tk.Tk()
window.geometry('380x250')
window.resizable(0, 0)
cross = tk.PhotoImage(file='Icons\\cross.png')
circle = tk.PhotoImage(file='Icons\\circle.png')


def player1():
    window.destroy()
    Player(1)


def player2():
    window.destroy()
    Player(2)


x_btn = tk.Button(master=window, highlightthickness=1, bd=1, image=cross, command=player1)
o_btn = tk.Button(master=window, highlightthickness=1, bd=1, image=circle, command=player2)
x_btn.place(x=50, y=100, width=120, height=120)
o_btn.place(x=210, y=100, width=120, height=120)
label = tk.Label(master=window, font=("Times New Roman", 20), text='Make your choice!')
label.place(x=87, y=30)
window.mainloop()
