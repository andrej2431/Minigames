x_size = 50
y_size = 30

sx = 25
sy = 15

length = 5
speed = 250
spawn_speed = 500
orientation = "right"
iterator = 0
iterator_2 = 0
difficulty = 0
opacne = "a"
import random
###############################
from tkinter import *

window = Tk()

window.title("Snake")
pole = []
window.geometry('800x400')
window.configure(background='midnight blue')
lbl = Label(window, text='Snake', fg='brown', bg='midnight blue', font=('comicsans', 20))
lbl.pack()

canvas = Canvas(window, height=y_size * 10, width=x_size * 10)
canvas.pack()


###############################
def define():
    global sx, sy, orientation, iterator, iterator_2
    sx = 25
    sy = 15
    orientation = "right"
    iterator = 0
    iterator_2 = 0


##############################
# Snake starts
def snake_start(length):
    global iterator
    for x in range(length - 2, -1, -1):
        iterator += 1
        canvas.create_rectangle((sx - x) * 10, sy * 10, (sx - x) * 10 + 10, sy * 10 + 10, fill='black', width=0,
                                tags='n' + str(iterator))


def start():
    snake_start(length)
    canvas.after(1, move)
    canvas.after(spawn_speed, spawn)


# Snake eats
def nom_nom(sx, sy):
    tup = canvas.find_enclosed(sx * 10, sy * 10, sx * 10 + 10, sy * 10 + 10)
    if tup:
        food = canvas.gettags(tup[0])
        if 'food' in food:
            canvas.delete('food')
            spawn()
            return True
    return False


# Snake dies

def prez_hran(sx, sy):
    multiple = canvas.find_overlapping(sx * 10 + 3, sy * 10 + 3, sx * 10 + 6, sy * 10 + 6)
    if sx < 0 or sx >= x_size:
        return False
    if sy < 0 or sy >= y_size:
        return False
    if len(multiple) == 1:
        return False
    return True


# Snake changes directions

def change(event):
    wasd = event.char
    global orientation

    if opacne != wasd:
        if wasd == "w":
            orientation = "up"
        elif wasd == "a":
            orientation = "left"
        elif wasd == "s":
            orientation = "down"
        elif wasd == "d":
            orientation = "right"


def new_direction():
    global sx, sy, orientation
    if orientation == "right":
        sx += 1
    elif orientation == "left":
        sx -= 1
    elif orientation == "up":
        sy -= 1
    elif orientation == "down":
        sy += 1


def opac(orientation):
    global opacne
    if orientation == "right":
        opacne = "a"
    elif orientation == "left":
        opacne = "d"
    elif orientation == "up":
        opacne = "s"
    elif orientation == "down":
        opacne = "w"


# snake move    
def move():
    global iterator, sx, sy, iterator_2
    iterator += 1
    new_direction()

    if nom_nom(sx, sy):
        canvas.create_rectangle(sx * 10, sy * 10, sx * 10 + 10, sy * 10 + 10, fill='black', width=0,
                                tags='n' + str(iterator))
        opac(orientation)
        window.after(speed - int(spin.get()) * 25, move)
    elif prez_hran(sx, sy):
        canvas.create_rectangle(sx * 10, sy * 10, sx * 10 + 10, sy * 10 + 10, fill='black', width=0,
                                tags='n' + str(iterator))
        canvas.delete('n' + str(iterator_2))
        iterator_2 += 1
        opac(orientation)
        window.after(speed - int(spin.get()) * 25, move)

    else:
        print("Game Over")
        btn['state'] = 'normal'


# food spawn

def spawn_pole():
    pole = []
    for x in range(x_size):
        for i in range(y_size):
            if len(canvas.find_overlapping(x * 10 + 3, i * 10 + 3, x * 10 + 6, i * 10 + 6)) == 0:
                pole.append([x * 10, i * 10, x * 10 + 10, i * 10 + 10])
    return pole


def spawn():
    pole = spawn_pole()
    coord = random.randint(0, len(pole) - 1)
    canvas.create_rectangle(pole[coord][0], pole[coord][1], pole[coord][2], pole[coord][3], width=0, fill='red',
                            tags='food')


# reset

def reset():
    canvas.delete("all")


def restart():
    btn['state'] = 'disabled'
    reset()
    define()
    start()


##############################
btn = Button(window, text='New Game', fg='white', bg='brown', font=('comicsans', 12), command=restart, state="disabled")
btn.pack()
canvas.bind_all("<Key>", change)
start()
spin = Spinbox(window, from_=0, to=10)
spin.pack()
window.mainloop()
