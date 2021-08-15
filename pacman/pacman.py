x_size = 28
y_size = 31
square = 20
where = 0
mv = 0
obstacles = []
locked = True
positions = [[0, 359], [30, 300], [45, 270]]
mouth = 0
where = 0
# right = 1
# left = -1
# up = 2
# down = -2
colors = ['red', 'gold2', 'pink', 'cyan']
speed = 20
direction = 1
turn = 1
score = 0
lemme = []
lock = False
orientation = {"cyan": 2, "pink": 2, "gold2": 2, "red": 2}
ghost_peace = {"cyan": 0, "red": 0, "gold2": 0, "pink": 0}
#######################
from tkinter import *

window = Tk()
window.title("Pac-Man")
window.geometry('560x620')
window.configure(background='black')
canvas = Canvas(window, height=y_size * square, width=x_size * square, background='black')


# red lines
def siet():
    for x in range(0, 28):
        canvas.create_line(x * 20, 0, x * 20, 620, fill='dark red', tags='line')
    for y in range(0, 31):
        canvas.create_line(0, y * 20, 560, y * 20, fill='dark red', tags='line')


# map outline
def basic_map():
    f = open('mapa.txt', 'r')
    b_map = f.read()
    n_map = b_map.split()
    f.close()

    for x in n_map:
        row = x.split(',')
        canvas.create_rectangle(row[0], row[1], row[2], row[3], fill='cornflower blue', width=0, tags='wall')


# cage map
def cage():
    canvas.create_rectangle(210, 250, 220, 330, fill='dark blue', width=0, tags='obstacle')
    canvas.create_rectangle(210, 320, 350, 330, fill='dark blue', width=0, tags='obstacle')
    canvas.create_rectangle(350, 330, 340, 250, fill='dark blue', width=0, tags='obstacle')
    canvas.create_rectangle(220, 250, 260, 260, fill='dark blue', width=0, tags='obstacle')
    canvas.create_rectangle(300, 250, 340, 260, fill='dark blue', width=0, tags='obstacle')
    canvas.create_rectangle(260, 250, 300, 255, fill='orange', width=0, tags='obstacle')


# obstacle map
def obstacle_map():
    f = open('obstacles.txt', 'r')
    obst_1 = f.read()
    obst_2 = obst_1.replace('[', '').replace(",", "")
    obst_3 = obst_2.split(']')
    for x in obst_3:
        row = x.split()
        if len(row) > 0:
            canvas.create_rectangle(row[0], row[1], row[2], row[3], fill='cornflower blue', width=0, tags='obstacle')


# ghosts
def spawn_ghosts():
    ghost("pink", 0)
    ghost("cyan", 20)
    ghost("red", 40)
    ghost("gold2", 60)
    canvas.after(3000, move_out)
    canvas.after(6000, move_out)
    canvas.after(9000, move_out)
    canvas.after(12000, move_out)


def ghost(color, x, rx=0, ry=0):
    canvas.create_polygon(243 + x, 297, 244 + x, 297, 244 + x, 296, 245 + x, 296, 245 + x, 295, 246 + x, 295, 246 + x,
                          296, 247 + x, 296, 247 + x, 297, 249 + x, 297,
                          249 + x, 295, 251 + x, 295, 251 + x, 297, 253 + x, 297, 253 + x, 296, 254 + x, 296, 254 + x,
                          295, 255 + x, 295, 255 + x, 296, 256 + x, 296,
                          256 + x, 297, 257 + x, 297, 257 + x, 289, 256 + x, 289, 256 + x, 286, 255 + x, 286, 255 + x,
                          285, 254 + x, 285, 254 + x, 284, 252 + x, 284,
                          252 + x, 283, 248 + x, 283, 248 + x, 284, 246 + x, 284, 246 + x, 285, 245 + x, 285, 245 + x,
                          286, 244 + x, 286, 244 + x, 289, 243 + x, 289,
                          fill=color, tags=[color, 'ghost'], width=0)

    canvas.create_polygon(255 + x, 285, 254 + x, 285, 254 + x, 284, 252 + x, 284, 252 + x, 285, 251 + x, 285, 251 + x,
                          288, 252 + x, 288, 252 + x, 289, 254 + x, 289, 254 + x, 288, 255 + x, 288, fill="white",
                          tags=[color, "eyes", 'ghost'], width=0)
    canvas.create_polygon(248 + x, 284, 246 + x, 284, 246 + x, 285, 245 + x, 285, 245 + x, 288, 246 + x, 288, 246 + x,
                          289, 248 + x, 289, 248 + x, 288, 249 + x, 288, 249 + x, 285, 248 + x, 285, fill="white",
                          tags=[color, "eyes", 'ghost'], width=0)
    canvas.create_rectangle(246 + x, 284, 248 + x, 286, fill="blue", tags=[color, "blue-eyes", 'ghost'], width=0)
    canvas.create_rectangle(252 + x, 284, 254 + x, 286, fill="blue", tags=[color, "blue-eyes", 'ghost'], width=0)


def ghost_cyan(cyan):
    pass


def move_out():
    global mv, ghost_peace
    if mv == 0:
        out('red')
        mv += 1
        ghost_peace["red"] = 1

    elif mv == 1:
        out('pink')
        mv += 1
        ghost_peace['pink'] = 1

    elif mv == 2:
        out('cyan')
        mv += 1
        ghost_peace['cyan'] = 1

    else:
        out('gold2')
        ghost_peace['gold2'] = 1


def ghost_move(color):
    global orientation
    direction_1 = orientation[color]
    possible_direction = []
    cords = [canvas.coords(color)[0] - 3, canvas.coords(color)[1] - 17]
    pac_x = canvas.coords(pac)[0]
    pac_y = canvas.coords(pac)[1]
    y_dif = []
    x_dif = []
    abs_dif = []

    ##    canvas.create_polygon (255+x,285, 254+x,285, 254+x,284, 252+x,284, 252+x,285, 251+x,285, 251+x,288, 252+x,288, 252+x,289, 254+x,289, 254+x,288, 255+x,288, fill ="white", tags = [color,"eyes",'ghost'],width = 0)
    ##    canvas.create_polygon (248+x,284, 246+x,284, 246+x,285, 245+x,285, 245+x,288, 246+x,288, 246+x,289, 248+x,289, 248+x,288, 249+x,288, 249+x,285, 248+x,285, fill = "white", tags = [color,"eyes",'ghost'],width = 0)
    ##    canvas.create_rectangle(246+x,284,248+x,286,fill = "blue", tags = [color,"blue-eyes",'ghost'],width = 0)
    ##    canvas.create_rectangle(252+x,284,254+x,286,fill = "blue", tags = [color,"blue-eyes",'ghost'],width = 0)
    if cords[0] % 20 == 0.0 and cords[1] % 20 == 0.0:
        if detect_wall(cords, -1) and 1 != direction_1:
            possible_direction.append([next_square(cords, -1), -1])

        if detect_wall(cords, 1) and -1 != direction_1:
            possible_direction.append([next_square(cords, 1), 1])

        if detect_wall(cords, -2) and 2 != direction_1:
            possible_direction.append([next_square(cords, -2), -2])
        if detect_wall(cords, 2) and -2 != direction_1:
            possible_direction.append([next_square(cords, 2), 2])
        for e in range(len(possible_direction)):
            y_dif.append([abs(pac_y - possible_direction[e][0][1])])
            x_dif.append([abs(pac_x - possible_direction[e][0][0])])
            abs_dif.append([x_dif[e] + y_dif[e]])

        better_choice = abs_dif.index(min(abs_dif))

        direction_1 = possible_direction[better_choice][1]
    ##        for row in canvas.find_withtag('eyes'):
    ##            if color in canvas.gettags(row):
    ##                eyes = canvas.coords(row)
    ##                canvas.move(row,-pac_x +eyes[0],

    if cords[0] >= 560 or cords[0] <= 0:
        direction_1 = orientation[color]

    if cords[0] == 580 and cords[1] == 280:
        canvas.move(color, -600, 0)
    elif cords[0] == -20 and cords[1] == 280:
        canvas.move(color, 600, 0)

    if direction_1 == 1:
        canvas.move(color, 2, 0)
    elif direction_1 == -1:
        canvas.move(color, -2, 0)
    elif direction_1 == 2:
        canvas.move(color, 0, -2)
    elif direction_1 == -2:
        canvas.move(color, 0, 2)

    orientation[color] = direction_1


# blue obstacle
def click(event):
    x = int(event.x / 10) * 10
    y = int(event.y / 10) * 10
    if locked:
        return
    if len(canvas.find_overlapping(x, y, x + 10, y + 10)) == 2:
        canvas.create_rectangle(x, y, x + 10, y + 10, fill='cornflower blue', width=0, tags='obstacle')
        obstacles.append([x, y, x + 10, y + 10])

    elif len(canvas.find_overlapping(x, y, x + 10, y + 10)) == 3:
        canvas.delete(canvas.find_overlapping(x, y, x + 10, y + 10)[2])
        del obstacles[-1]


# pac-man
def pac_man():
    global mouth, where
    mouth += 1
    if direction == -1:
        where = 180
    elif direction == 1:
        where = 0
    elif direction == 2:
        where = 90
    else:
        where = 270

    canvas.itemconfig(pac, start=positions[mouth][0] + where, extent=positions[mouth][1])
    if mouth == 2:
        mouth = -1
    if not lock:
        canvas.after(100, pac_man)


# pac man diretion change
def change(event):
    wasd = event.char
    global turn, lock
    if wasd == 'd':
        turn = 1

    elif wasd == 'w':
        turn = 2

    elif wasd == 's':
        turn = -2

    elif wasd == 'a':
        turn = -1
    elif wasd == 'l':
        lock = not lock
        if not lock:
            canvas.after(60, move)


# pac man moves
def move():
    global direction, lock, ghost_peace, score
    if ghost_peace["cyan"] == 1:
        ghost_move('cyan')
    if ghost_peace["red"] == 1:
        ghost_move('red')
    if ghost_peace["gold2"] == 1:
        ghost_move('gold2')
    if ghost_peace["pink"] == 1:
        ghost_move('pink')

    cords = canvas.coords(pac)
    the_tags = tags_in_square(cords, color=True)
    if 'ghost' in the_tags[0]:
        if 'nomnom' in the_tags[0]:
            canvas.delete(the_tags[1])
            ghost_peace[the_tags[1]] = 0
            score += 200

        else:
            lock = True
            game_over()

    if cords[0] % 20 == 0.0 and cords[1] % 20 == 0.0:

        if detect_wall(cords, turn):
            direction = turn

        if not detect_wall(cords, direction):
            if not lock:
                canvas.after(speed, move)
                return

    if turn == -direction:
        direction = turn

    is_food(cords)
    if not canvas.find_withtag('food'):
        lock = True
        victory()
    if direction == 1:
        canvas.move(pac, 2, 0)
    elif direction == -1:
        canvas.move(pac, -2, 0)
    elif direction == 2:
        canvas.move(pac, 0, -2)
    elif direction == -2:
        canvas.move(pac, 0, 2)

    if cords[0] == 580 and cords[1] == 280:
        canvas.move(pac, -600, 0)
    elif cords[0] == -30 and cords[1] == 280:
        canvas.move(pac, 600, 0)

    if not lock:
        canvas.after(speed, move)


# next square
def next_square(cords, turn, food=0):
    if turn == 1:
        square = [cords[0] + 20, cords[1], cords[0] + 40 - food, cords[1] + 20]
    elif turn == -1:
        square = [cords[0] - 20 + food, cords[1], cords[0], cords[1] + 20]
    elif turn == 2:
        square = [cords[0], cords[1] - 20 + food, cords[0] + 20, cords[1]]
    elif turn == -2:
        square = [cords[0], cords[1] + 20, cords[0] + 20, cords[1] + 40 - food]
    return square


# detect walls
def detect_wall(cords, turn):
    square = next_square(cords, turn)
    tags = tags_in_square(square)
    if 'wall' in tags or 'obstacle' in tags:
        return False
    return True


# what tags are in a square
def tags_in_square(square, color=False):
    tags = {}
    nomnom = []
    for row in canvas.find_overlapping(square[0], square[1], square[2], square[3]):
        for x in canvas.gettags(row):
            if color:
                if x == 'nomnom':
                    nomnom = canvas.gettags(row)[0]
            tags[x] = row
    if color:
        return tags, nomnom
    return tags


# pieces of food
def food():
    n = open('x_clear.txt', 'r')
    m = open('y_clear.txt', 'r')
    x_clear = n.read().split(',')
    y_clear = m.read().split(',')
    for x in range(20, 540, 20):
        for y in range(20, 600, 20):
            if (str(x) not in x_clear or str(y) not in y_clear) and len(
                    canvas.find_overlapping(x, y, x + 20, y + 20)) == 0:
                if (x < 220 or x > 320) or (y < 260 or y > 300):
                    if (x == 20 and (y == 60 or y == 460)) or (x == 520 and (y == 60 or y == 460)):
                        canvas.create_oval(x + 5, y + 5, x + 15, y + 15, fill='orange', width=0, tags=['food', 'big'])
                    else:
                        canvas.create_rectangle(x + 8, y + 8, x + 12, y + 12, fill='orange', width=0, tags='food')


# is there food in front
def is_food(cords):
    global score
    square = next_square(cords, direction, 18)
    if 'food' in tags_in_square(square):
        if 'big' in tags_in_square(square):
            eating_time()
            canvas.delete(tags_in_square(square)['food'])
            score -= 50
            canvas.itemconfigure(T, text=score)
        else:
            canvas.delete(tags_in_square(square)['food'])
            score += 10
            canvas.itemconfigure(T, text=score)


# eating time
def color_change(color):
    ghost = canvas.coords(color)

    canvas.create_polygon(ghost, fill='blue', tags=[color, 'face', 'nomnom'], width=0)
    canvas.create_rectangle(ghost[0] + 4, ghost[1] - 9, ghost[0] + 6, ghost[1] - 7, fill='peach puff',
                            tags=[color, 'good', 'nomnom'], width=0)
    canvas.create_rectangle(ghost[0] + 8, ghost[1] - 9, ghost[0] + 10, ghost[1] - 7, fill='peach puff',
                            tags=[color, 'good', 'nomnom'], width=0)

    canvas.create_rectangle(ghost[0] + 1, ghost[1] - 4, ghost[0] + 2, ghost[1] - 3, fill='peach puff',
                            tags=[color, 'good', 'nomnom'], width=0)

    canvas.create_rectangle(ghost[0] + 2, ghost[1] - 5, ghost[0] + 4, ghost[1] - 4, fill='peach puff',
                            tags=[color, 'good', 'nomnom'], width=0)

    canvas.create_rectangle(ghost[0] + 4, ghost[1] - 4, ghost[0] + 6, ghost[1] - 3, fill='peach puff',
                            tags=[color, 'good', 'nomnom'], width=0)

    canvas.create_rectangle(ghost[0] + 6, ghost[1] - 5, ghost[0] + 8, ghost[1] - 4, fill='peach puff',
                            tags=[color, 'good', 'nomnom'], width=0)

    canvas.create_rectangle(ghost[0] + 8, ghost[1] - 4, ghost[0] + 10, ghost[1] - 3, fill='peach puff',
                            tags=[color, 'good', 'nomnom'], width=0)

    canvas.create_rectangle(ghost[0] + 10, ghost[1] - 5, ghost[0] + 12, ghost[1] - 4, fill='peach puff',
                            tags=[color, 'good', 'nomnom'], width=0)

    canvas.create_rectangle(ghost[0] + 12, ghost[1] - 4, ghost[0] + 13, ghost[1] - 3, fill='peach puff',
                            tags=[color, 'good', 'nomnom'], width=0)


def eating_time():
    for row in colors:
        canvas.addtag_withtag('nomnom', row)
        color_change(row)
    canvas.after(10000, end_eating)

    canvas.after(5000, blink)
    canvas.after(6000, blink)
    canvas.after(7000, blink)
    canvas.after(8000, blink)
    canvas.after(9000, blink)


def blink():
    canvas.itemconfig('face', fill='white')
    canvas.itemconfig('good', fill='red')
    canvas.after(500, blink_back)


def blink_back():
    canvas.itemconfig('face', fill='blue')
    canvas.itemconfig('good', fill='peach puff')


def end_eating():
    global ghost_peace
    canvas.delete('face')
    canvas.dtag('nomnom', 'nomnom')
    if ghost_peace['pink'] == 0:
        ghost("pink", 0)
        out('pink')
        ghost_peace['pink'] = 1

    if ghost_peace["gold2"] == 0:
        ghost("gold2", 60)
        out("gold2")
        ghost_peace['gold2'] = 1

    if ghost_peace["red"] == 0:
        ghost("red", 40)
        out("red")
        ghost_peace['red'] = 1

    if ghost_peace["cyan"] == 0:
        ghost("cyan", 20)
        out("cyan")
        ghost_peace['cyan'] = 1


def out(color):
    canvas.move(color, 0, -60)


# victory
def victory():
    canvas.delete('ghost')
    canvas.delete(pac)
    G = canvas.create_text(275, 300, text="Victory", font=("Comic Sans", 100), fill="gold")


# game over
def game_over():
    canvas.delete('ghost')
    canvas.itemconfig(pac, start=0, extent=359)
    canvas.after(20, close)


rx = 0


def close():
    global rx
    rx += 1
    canvas.itemconfig(pac, start=rx, extent=359 - 2 * rx)
    if rx < 177:
        canvas.after(10, close)
    else:
        canvas.delete(pac)
        G = canvas.create_text(275, 300, text="Game Over", font=("Comic Sans", 70), fill="dim gray")


# start position
def start():
    basic_map()
    obstacle_map()
    cage()
    pac_man()
    food()
    spawn_ghosts()


######################
canvas.bind_all("<Key>", change)
canvas.bind("<Button-1>", click)
# T = Text(window, height=1, width=30,background ='black')
# T.pack()
J = canvas.create_text(50, 220, text="High Score:", font=("Comic Sans", 13), fill="blue")
T = canvas.create_text(50, 240, text=0, font=("Comic Sans", 13), fill="blue")
# siet()
pac = canvas.create_arc(270, 460, 290, 480, start=0, extent=359, fill="yellow", tags='pac-man')
start()
canvas.after(500, move)
canvas.pack()
window.mainloop()
