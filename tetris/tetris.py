x_size = 10
y_size = 20

colors = ["cyan", "blue", "orange", "yellow", "lawn green", "purple", "red"]
shape = ""
stop = 1
lock = False
speed = 300
game = False
score = 0
import random
###############################
from tkinter import *

window = Tk()

window.title("Snake")
pole = []
window.geometry('800x500')

window.configure(background='midnight blue')
lbl = Label(window, text='Tetris', fg='brown', bg='midnight blue', font=('comicsans', 20))
lbl.pack()

canvas = Canvas(window, height=y_size * 20, width=x_size * 20)
canvas.pack()
control = 1


###############################

##############################
# create pieces
def block(color, x, y):
    canvas.create_rectangle(x, y, x + 20, y + 20, fill=color, tags=('moving', "block"))


def piece(color):
    if color == "cyan":
        block(color, 60, 0)
        block(color, 80, 0)
        block(color, 100, 0)
        block(color, 120, 0)

    elif color == "blue":
        block(color, 60, 20)
        block(color, 40, 0)
        block(color, 40, 20)
        block(color, 80, 20)

    elif color == "orange":
        block(color, 60, 20)
        block(color, 80, 0)
        block(color, 40, 20)
        block(color, 80, 20)

    elif color == "yellow":
        block(color, 80, 0)
        block(color, 100, 0)
        block(color, 100, 20)
        block(color, 80, 20)


    elif color == "lawn green":
        block(color, 80, 20)
        block(color, 80, 0)
        block(color, 100, 0)
        block(color, 60, 20)


    elif color == "purple":
        block(color, 80, 20)
        block(color, 80, 0)
        block(color, 60, 20)
        block(color, 100, 20)


    elif color == "red":
        block(color, 80, 20)
        block(color, 80, 0)
        block(color, 60, 0)
        block(color, 100, 20)


# keyboard

def change(event):
    wasd = event.char
    global orientation, control, stop, lock, speed
    if not lock:
        if wasd == "k":
            counter_clock_turn()

        elif wasd == "a":
            if on_left():
                canvas.move('moving', -20, 0)

        elif wasd == "l":
            clock_turn()

        elif wasd == "d":
            if on_right():
                canvas.move('moving', 20, 0)
        elif wasd == "v":
            stop = stop * -1
            if stop == 1:
                canvas.after(150, fall)
        elif wasd == "f":
            speed = 30

            lock = True
        elif wasd == "h":
            speed = 0
            lock = True


# random piece
def rand(colors):
    global shape
    shape = random.choice(colors)
    piece(shape)


# last rank
def last_rank():
    ids = canvas.find_overlapping(0, 390, 200, 400)
    if ids:
        for row in ids:
            if 'moving' in canvas.gettags(row):
                return True
    return False


# taken
def taken(number):
    cords_1 = canvas.coords('moving')
    for row in canvas.find_withtag('moving'):
        cords_2 = canvas.coords(row)
        x_dif = cords_1[0] - cords_2[0]
        y_dif = cords_1[1] - cords_2[1]
        there = canvas.find_enclosed(cords_1[0] - number * y_dif - 1, cords_1[1] + number * x_dif - 1,
                                     cords_1[0] - number * y_dif + 21, cords_1[1] + number * x_dif + 21)
        if cords_1[0] - y_dif < 0 or cords_1[0] - y_dif > 180 or cords_1[1] + x_dif > 400:
            return True
        if there:
            if len(there) == 1 and not canvas.gettags(there[0]):
                return True
    return False


# game over
def game_over():
    if canvas.find_overlapping(39, 0, 119, 19):
        return True
    return False


# turn
def clock_turn():
    if shape != 'yellow' and shape != 'cyan':
        if taken(-1):
            return
        cords_1 = canvas.coords('moving')
        for row in canvas.find_withtag('moving'):
            cords_2 = canvas.coords(row)
            x_dif = cords_1[0] - cords_2[0]
            y_dif = cords_1[1] - cords_2[1]

            canvas.move(row, x_dif + y_dif, y_dif - x_dif)

    elif shape == 'cyan':
        cords_1 = canvas.coords('moving')
        for row in canvas.find_withtag('moving'):
            cords_2 = canvas.coords(row)
            x_dif = cords_1[0] - cords_2[0]
            y_dif = cords_1[1] - cords_2[1]

            if x_dif == 20:
                if len(canvas.find_enclosed(cords_1[0] - 20, cords_1[1] - 20, cords_1[0], cords_1[1] + 60)) > 1 or \
                        cords_1[1] > 360:
                    return

            if x_dif == -20:
                if len(canvas.find_enclosed(cords_1[0] + 20, cords_1[1] - 40, cords_1[0] + 40, cords_1[1] + 40)) > 1 or \
                        cords_1[1] > 380:
                    return

            if y_dif == 20:
                if len(canvas.find_enclosed(cords_1[0] - 40, cords_1[1] - 20, cords_1[0] + 40, cords_1[1])) > 1 or \
                        cords_1[0] > 160 or cords_1[0] < 40:
                    return

            if y_dif == -20:
                if len(canvas.find_enclosed(cords_1[0] - 20, cords_1[1] + 20, cords_1[0] + 60, cords_1[1] + 40)) > 1 or \
                        cords_1[0] > 140 or cords_1[0] < 20:
                    return

            if x_dif != 0:
                canvas.move(row, x_dif, -x_dif)

            if y_dif != 0:
                canvas.move(row, y_dif, y_dif)
        if x_dif != 0:
            canvas.move("moving", -x_dif / 3, x_dif / 3 * 2)
        if y_dif != 0:
            canvas.move("moving", -y_dif / 3 * 2, -y_dif / 3)


def counter_clock_turn():
    if shape != 'yellow' and shape != 'cyan':
        if taken(1):
            return
        cords_1 = canvas.coords('moving')
        for row in canvas.find_withtag('moving'):
            cords_2 = canvas.coords(row)
            x_dif = cords_1[0] - cords_2[0]
            y_dif = cords_1[1] - cords_2[1]

            canvas.move(row, x_dif - y_dif, y_dif + x_dif)

    elif shape == 'cyan':
        cords_1 = canvas.coords('moving')
        for row in canvas.find_withtag('moving'):
            cords_2 = canvas.coords(row)
            x_dif = cords_1[0] - cords_2[0]
            y_dif = cords_1[1] - cords_2[1]

            if x_dif == 20:
                if len(canvas.find_enclosed(cords_1[0] - 40, cords_1[1] - 20, cords_1[0] - 20, cords_1[1] + 60)) > 1 or \
                        cords_1[1] > 360:
                    return

            if x_dif == -20:
                if len(canvas.find_enclosed(cords_1[0] + 40, cords_1[1] - 40, cords_1[0] + 60, cords_1[1] + 40)) > 1 or \
                        cords_1[1] > 380:
                    return

            if y_dif == 20:
                print(cords_1[0])
                if len(canvas.find_enclosed(cords_1[0] - 40, cords_1[1] - 40, cords_1[0] + 40, cords_1[1] - 20)) > 1 or \
                        cords_1[0] > 160 or cords_1[0] < 40:
                    return

            if y_dif == -20:
                if len(canvas.find_enclosed(cords_1[0] - 20, cords_1[1] + 40, cords_1[0] + 60, cords_1[1] + 60)) > 1 or \
                        cords_1[0] > 140 or cords_1[0] < 20:
                    return

            if x_dif != 0:
                canvas.move(row, x_dif, x_dif)

            if y_dif != 0:
                canvas.move(row, -y_dif, y_dif)
        if x_dif != 0:
            canvas.move("moving", -x_dif / 3 * 2, -x_dif / 3)
        if y_dif != 0:
            canvas.move("moving", y_dif / 3, -y_dif / 3 * 2)

        # around


def on_left():
    ids = canvas.find_withtag('moving')
    for row in ids:
        cords = canvas.coords(row)
        left_of = canvas.find_overlapping(cords[0] - 5, cords[1] + 5, cords[0] - 10, cords[1] + 10)
        if cords[0] == 0.0:
            return False
        if left_of:
            if 'moving' not in canvas.gettags(left_of):
                return False
    return True


def on_right():
    ids = canvas.find_withtag('moving')
    for row in ids:
        cords = canvas.coords(row)
        right_of = canvas.find_overlapping(cords[2] + 5, cords[1] + 5, cords[2] + 10, cords[1] + 10)
        if cords[2] == 200.0:
            return False
        if right_of:
            if 'moving' not in canvas.gettags(right_of):
                return False
    return True


def under():
    ids = canvas.find_withtag('moving')
    for row in ids:
        cords = canvas.coords(row)
        under_it = canvas.find_overlapping(cords[0] + 5, cords[3] + 5, cords[0] + 10, cords[3] + 10)
        if under_it:
            if 'moving' not in canvas.gettags(under_it):
                return True
    return False


def all_in_line():
    global lock, speed, score
    for y in range(0, 400, 20):
        if len(canvas.find_overlapping(0, y + 5, 200, y + 15)) == 10:
            score = score + 100
            for row in canvas.find_overlapping(0, y + 5, 200, y + 15):
                canvas.delete(row)
            canvas.addtag_overlapping("down", 0, 0, 200, y)
            canvas.move("down", 0, 20)
            canvas.dtag("down", "down")
    lock = False
    speed = 300


# fall

def fall():
    global game
    if game:
        return

    if last_rank() or under():
        canvas.dtag('moving', 'moving')
        game = game_over()
        if not game:
            all_in_line()
            rand(colors)
        else:
            print("Game Over")
            print("Score = ", score)
            return

    else:
        canvas.move('moving', 0, 20)

    if stop != -1 and not game:
        canvas.after(speed, fall)


# reset
def reset():
    global speed, game
    speed = 300
    game = False
    canvas.delete("block")
    rand(colors)


def restart():
    global game
    game = True
    canvas.after(speed + 100, reset())


##############################
btn = Button(window, text='New Game', fg='white', bg='brown', font=('comicsans', 12), command=restart)
btn.pack()
canvas.bind_all("<Key>", change)
rand(colors)
canvas.after(500, fall)
window.mainloop()
