from tkinter import *
master = Tk()
master.geometry("803x900")
master.resizable(0,0)
w= Canvas(master,width = 800, height = 800 )
turn = 'white'
################### Created Canvas
for x  in [700,500,300,100]:
    for i in range(x,800,100):
        w.create_rectangle(i-x,i,i-x+100,i+100,fill = 'saddle brown')
        w.create_rectangle(i,i-x,i+100,i-x+100,fill = 'saddle brown')
w.create_rectangle(2,2,800,800)
################### Created chessboard



w_p = PhotoImage(file = 'w_p.png')
w_k = PhotoImage(file = 'w_k.png')
w_kt = PhotoImage(file = 'w_kt.png')
w_q = PhotoImage(file = 'w_q.png')
w_r = PhotoImage(file = 'w_r.png')
w_b = PhotoImage(file = 'w_b.png')

b_p = PhotoImage(file = 'b_p.png')
b_k = PhotoImage(file = 'b_k.png')
b_kt = PhotoImage(file = 'b_kt.png')
b_q = PhotoImage(file = 'b_q.png')
b_r = PhotoImage(file = 'b_r.png')
b_b = PhotoImage(file = 'b_b.png')
################### Created piece templates
def w_pawn(x,y):
    return w.create_image(x,y,image = w_p,tags = ['unmoved','piece','pawn','white'])

def b_pawn(x,y):
    return w.create_image(x,y,image = b_p, tags = ['unmoved','piece','pawn','black'])
################### create pawn function
def set_board():
    for x in range (50,800,100):
        w_pawn(x,650)
        b_pawn(x,150)
        ########### Created white/black pawns
    for x in [50,750]: 
        w.create_image(x,750,image = w_r,tags = ['white','piece','rook','unmoved'])
    for x in [150,650]: 
        w.create_image(x,750,image = w_kt,tags = ['white','piece','knight'])
    for x in [250,550]:
        w.create_image(x,750,image = w_b,tags = ['white','piece','bishop'])
    w.create_image(350,750,image = w_q,tags = ['white','piece','queen'])
    w.create_image(450,750,image = w_k,tags = ['white','piece','king','unmoved'])

    for x in [50,750]: 
        w.create_image(x,50,image = b_r,tags = ['black','piece','rook','unmoved'])
    for x in [150,650]: 
        w.create_image(x,50,image = b_kt,tags = ['black','piece','knight'])
    for x in [250,550]:
        w.create_image(x,50,image = b_b,tags = ['black','piece','bishop'])
    w.create_image(350,50,image = b_q,tags = ['black','piece','queen'])
    w.create_image(450,50,image = b_k,tags = ['black','piece','king','unmoved'])
    #############Created the rest of the board

class Coords:
    def __init__(self,x=0,y=0,label = None):
        self.l = label
        self.x = x
        self.y = y
    def where(self,event):
       self.x =  event.x
       self.y = event.y
    def __repr__(self):
        return str(self.l)+'(x = '+str(self.x)+', y = '+ str(self.y)+')'
cords = Coords()

##################### Coords class for storing the coords
last_move = [Coords(label = 'from'),Coords(label = 'to'),('None')]
foll = False
obj = 0
orig = 0
moves = 0
def follow():
    if foll == True:
        x = w.coords(obj)[0]
        y = w.coords(obj)[1]
        w.move(obj,cords.x-x,cords.y-y)
        w.after(10,follow)
#############################piece follows mouse

def click(event):
    global foll,obj,orig
    x = event.x-event.x%100
    y = event.y-event.y%100
    o = list(filter(lambda x: x>33,w.find_overlapping(x,y,x+100,y+100)))
    if o and turn in w.gettags(o[0]):
            obj = o[0]
            foll = True
            orig = w.coords(obj)
            follow()
###################################picks up a piece if possible

def release(event):
    global foll,turn,moves
    if foll:
        foll = False
        x1 = w.coords(obj)[0]
        y1 = w.coords(obj)[1]
        
        x2 = int(cords.x/100)*100+50
        y2 = int(cords.y/100)*100+50

        if valid_move(x2,y2,obj):
            if turn=='black':
                turn = 'white'
            else:
                turn = 'black'
            moves+=1
            print('moves:',moves)
            b2.config(state = NORMAL)
            w.move(obj,x2-x1,y2-y1)
            last_move[0].x = int(orig[0])
            last_move[0].y = int(orig[1])
            last_move[1].x = int(x2)
            last_move[1].y = int(y2)
            
        else:
            w.move(obj,orig[0]-x1,orig[1]-y1)
############################################## release a piece or return it at previous position
w.bind('<Motion>',cords.where)
w.bind('<Button-1>',click)
w.bind('<ButtonRelease-1>',release)
######################################
def new_game():
    global turn
    w.delete('piece')
    w.delete('text')
    set_board()
    turn = 'white'
    
def undo():
    global turn,moves
    w.move(obj,last_move[0].x-last_move[1].x,last_move[0].y-last_move[1].y)
    if turn == 'white':
        turn = 'black'
    else:
        turn = 'white'
    w.addtag_withtag('unmoved', obj)
    moves-=1
    print('moves:',moves)
    b2.config(state = DISABLED)
def resign():
    global turn
    if turn == 'black':
        winner = 'White'
    else:
        winner = 'Black'
    turn = 0
    w.create_text(400,400,text = 'Game Over\n'+winner+' wins!',font = ("Helvetica", 40, "bold italic"),fill = 'dark blue',tag = 'text')
##################################
b1 = Button(text = 'New Game',font =("Helvetica", 12, "bold italic") ,background ='bisque', activebackground = 'tan2',command = new_game,width = 20,height = 3)
b1.place(x =295 ,y = 815)
b2 = Button(text = 'Undo',command =  undo,font =("Helvetica", 12, "bold italic") ,background ='bisque', activebackground = 'tan2',width = 20,height = 3)
b2.place(x=561,y=815)
b3 = Button(text = 'Resign',font =("Helvetica", 12, "bold italic") ,background ='bisque', activebackground = 'tan2',command =  resign,width = 20,height = 3)
b3.place(x=28,y=815)

################### Dragging pieces
def in_square(x,y):
    return list(filter(lambda x: (x>33 and x!=obj),w.find_overlapping(x-10,y-10,x+10,y+10)))

def in_between_straight(x1,y1,x2,y2):
    x_diff = int(x1-x2)
    y_diff =  int(y1-y2)
    if x_diff == 0 :
            n = 1
            if y_diff>0:
                n = -1
            if list(filter(lambda x: x>33,w.find_overlapping(orig[0],orig[1]+100*n,orig[0],y2-100*n))) and abs(y_diff)!= 100:
                return True
            
    elif y_diff == 0:
        n = 1
        if x_diff>0:
            n = -1
        if list(filter(lambda x: x>33,w.find_overlapping(orig[0]+100*n,orig[1],x2-100*n,orig[1]))) and abs(x_diff)!=100:
                return True
    else:
        return True
    return False

def in_between_diagonal(x1,y1,x2,y2):
    x_diff = int(x1-x2)
    y_diff =  int(y1-y2)
    if abs(x_diff) != abs(y_diff):
        return True
    plus_minus =int(x_diff/abs(x_diff))
    plus_diff = x_diff/y_diff
    squares = [(x2+i*100,y2+i*100*plus_diff) for i in range(plus_minus, int(x_diff/100),plus_minus)]
    for square in squares:
        if in_square(square[0],square[1]):
            return True
    return False
    
######################################checks if there are pieces in certain squares    
        
    
def valid_move(x2,y2,obj):
    tags  = w.gettags(obj)
    x_diff = int(orig[0] - x2)
    y_diff = int(orig[1] - y2)
    t = in_square(x2,y2)
    
    if x2==orig[0] and y2 == orig[1]:
        return False
    
    if x2>800 or y2 > 800:
        return False
    
    if 'knight' in tags:
        
        if not ((abs(x_diff) == 200 and abs(y_diff) == 100) or (abs(x_diff) == 100 and abs(y_diff) == 200)):
            return False

        
    elif 'rook' in tags:
        if in_between_straight(orig[0],orig[1],x2,y2):
            return False
        

    elif 'pawn' in tags:
        if 'white' in tags:
            n = 1
        else:
            n= -1
        if y_diff*n<0:
            return False
        
        if abs(x_diff)>100 or (abs(x_diff) == 100 and y_diff!= 100*n):
            return False
        
        elif abs(x_diff) == 100:
            if t:
                if not(('black' in w.gettags(t[0]) and 'white' in tags) or ('white' in w.gettags(t[0]) and 'black' in tags)):
                  return False
            else:
                en_passante = in_square(x2,orig[1])
                if en_passante and ('pawn' in w.gettags(en_passante[0]) and (last_move[1].x == x2 and last_move[1].y == orig[1]) and (last_move[0].x ==x2  and last_move[0].y == orig[1]-200*n)):
                    w.delete(en_passante[0])
                else:
                    return False
        
        elif('unmoved' in tags and abs(y_diff) > 200) or ('unmoved' not in tags and abs(y_diff) > 100):
            return False
            
        elif t:
            return False
        elif abs(y_diff) == 200:
            if list(filter(lambda x: (x>33 and x!=obj),w.find_overlapping(x2-10,y2-10+100*n,x2+10,y2+10+100*n))) :
                return False
        
    elif 'king' in tags:
        
        if x_diff == 200 and y_diff == 0 and'unmoved' in tags:
            nt = in_square(x2-200,y2)
            
            if nt and 'rook' in w.gettags(nt[0]) and 'unmoved' in w.gettags(nt[0]):
                
                if not in_between_straight(orig[0],orig[1],x2-100,y2):
                    
                    return False
                
                else:
                    w.move(nt[0],300,0)
            else:
                return False
            
        elif x_diff == -200 and y_diff == 0 and 'unmoved' in tags:
            nt = in_square(x2+100,y2)
            
            if nt and 'rook' in w.gettags(nt[0]) and 'unmoved' in w.gettags(nt[0]):
                if not in_between_straight(orig[0],orig[1],x2+100,y2):
                    return False
                
                else:
                    w.move(nt[0],-200,0)
            else:
                return False
            
        elif abs(x_diff)>100 or abs(y_diff)>100:
            return False
            


    elif 'bishop' in tags:
        if in_between_diagonal(orig[0],orig[1],x2,y2):
            return False


        
    elif 'queen' in tags:
        if in_between_diagonal(orig[0],orig[1],x2,y2) and in_between_straight(orig[0],orig[1],x2,y2):
            return False

        
    if t:
        if ('white' in tags and 'white' in w.gettags(t[0])) or ('black' in tags and 'black' in w.gettags(t[0])):
            return False
        else:
            last_move[2] = w.gettags(t[0])
            w.delete(t[0])
    else:
        last_move[2] = ('None')
    if 'unmoved' in tags:
        w.dtag(obj,'unmoved')
    
    return True


##############################################checks if move is possible






set_board()  
w.pack()
w.mainloop()    
       
