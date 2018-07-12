
#PONG pygame
import random
import socket
import pygame, sys
import Tkinter as tk
from pygame.locals import *
# -*- coding: utf-8 -*-

pygame.init()
fps = pygame.time.Clock()

#colors
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0,0,0)

#globals
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
ball_pos = [0,0]
ball_vel = [0,0]
paddle1_vel = 0
paddle2_vel = 0
l_score = 0
r_score = 0

#canvas declaration
window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('Hello World')

# helper function that spawns a ball, returns a position vector and a velocity vector
# if right is True, spawn to the right, else spawn to the left
def ball_init(right):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH/2,HEIGHT/2]
    horz = random.randrange(2,4)
    vert = random.randrange(1,3)
    
    if right == False:
        horz = - horz
        
    ball_vel = [horz,-vert]

# define event handlers
def init():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel,l_score,r_score  # these are floats
    global score1, score2  # these are ints
    paddle1_pos = [HALF_PAD_WIDTH - 1,HEIGHT/2]
    paddle2_pos = [WIDTH +1 - HALF_PAD_WIDTH,HEIGHT/2]
    l_score = 0
    r_score = 0
    if random.randrange(0,2) == 0:
        ball_init(True)
    else:
        ball_init(False)


#draw function of canvas
def draw(canvas):
    global paddle1_pos, paddle2_pos, ball_pos, ball_vel, l_score, r_score
           
    canvas.fill(BLACK)
    pygame.draw.line(canvas, WHITE, [WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1)
    pygame.draw.line(canvas, WHITE, [PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1)
    pygame.draw.line(canvas, WHITE, [WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1)
    pygame.draw.circle(canvas, WHITE, [WIDTH//2, HEIGHT//2], 70, 1)

    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos[1] > HALF_PAD_HEIGHT and paddle1_pos[1] < HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos[1] += paddle1_vel
    elif paddle1_pos[1] == HALF_PAD_HEIGHT and paddle1_vel > 0:
        paddle1_pos[1] += paddle1_vel
    elif paddle1_pos[1] == HEIGHT - HALF_PAD_HEIGHT and paddle1_vel < 0:
        paddle1_pos[1] += paddle1_vel
    
    if paddle2_pos[1] > HALF_PAD_HEIGHT and paddle2_pos[1] < HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos[1] += paddle2_vel
    elif paddle2_pos[1] == HALF_PAD_HEIGHT and paddle2_vel > 0:
        paddle2_pos[1] += paddle2_vel
    elif paddle2_pos[1] == HEIGHT - HALF_PAD_HEIGHT and paddle2_vel < 0:
        paddle2_pos[1] += paddle2_vel

    #update ball
    ball_pos[0] += int(ball_vel[0])
    ball_pos[1] += int(ball_vel[1])

    #draw paddles and ball
    pygame.draw.circle(canvas, RED, ball_pos, 20, 0)
    pygame.draw.polygon(canvas, GREEN, [[paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT], [paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT], [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT], [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT]], 0)
    pygame.draw.polygon(canvas, GREEN, [[paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT], [paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT], [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT], [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT]], 0)

    #ball collision check on top and bottom walls
    if int(ball_pos[1]) <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    if int(ball_pos[1]) >= HEIGHT + 1 - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
    
    #ball collison check on gutters or paddles
    if int(ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH and int(ball_pos[1]) in range(paddle1_pos[1] - HALF_PAD_HEIGHT,paddle1_pos[1] + HALF_PAD_HEIGHT,1):
        ball_vel[0] = -ball_vel[0]
        ball_vel[0] *= 1.1
        ball_vel[1] *= 1.1
    elif int(ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH:
        r_score += 1
        ball_init(True)
        
    if int(ball_pos[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH and int(ball_pos[1]) in range(paddle2_pos[1] - HALF_PAD_HEIGHT,paddle2_pos[1] + HALF_PAD_HEIGHT,1):
        ball_vel[0] = -ball_vel[0]
        ball_vel[0] *= 1.1
        ball_vel[1] *= 1.1
    elif int(ball_pos[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH:
        l_score += 1
        ball_init(False)

    #update scores
    myfont1 = pygame.font.SysFont("Comic Sans MS", 20)
    label1 = myfont1.render("Score "+str(l_score), 1, (255,255,0))
    canvas.blit(label1, (50,20))

    myfont2 = pygame.font.SysFont("Comic Sans MS", 20)
    label2 = myfont2.render("Score "+str(r_score), 1, (255,255,0))
    canvas.blit(label2, (470, 20))  
    
    
#keydown handler
def server_keydown(event):
    global paddle1_vel
    
    if event.key == K_UP:
        paddle1_vel = -8
        #conn.send('u')
    elif event.key == K_DOWN:
        paddle1_vel = 8
        #conn.send('d')
    elif event.key == K_w:
        paddle1_vel = -8
        #conn.send('u')
    elif event.key == K_s:
        paddle1_vel = 8
        #conn.send('d')

#keyup handler
def server_keyup(event):
    global paddle1_vel
    
    if event.key in (K_w, K_s):
        paddle1_vel = 0
    elif event.key in (K_UP, K_DOWN):
        paddle1_vel = 0

def client_down():
    global paddle2_vel
    paddle2_vel = 8
def client_up():
    global paddle2_vel
    paddle2_vel = -8
def client_keyup():
    global paddle2_vel
    paddle2_vel = 0
init()


def create_game():
    print("creating game")
    sock = socket.socket()
    sock.bind(('', 9090))
    sock.listen(1)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                print "quit"
                pygame.quit()
                sys.exit()
        try:
            conn, addr = sock.accept()
            print 'connected:', addr
        except:
            continue
        break
    while True:
        data = conn.recv(1)

        draw(window)

        for event in pygame.event.get():
            if data == 'u': #up
                client_up()
            if data == 'd': #down
                client_down()
            if data == 'n': #nothing
                client_keyup()
            if data == 'q': #quit
                conn.close()

            break
            if event.type == KEYDOWN:
                server_keydown(event)
                if event.key in (K_UP, K_w):
                    conn.send('u')
                if event.key in (K_DOWN, K_s):
                    conn.send('d')
            elif event.type == KEYUP:
                server_keyup(event)
                conn.send('n')
            elif event.type == QUIT:
                conn.send('q')
                pygame.quit()
                sys.exit()
            
        pygame.display.update()
    fps.tick(60)

    conn.close()

def connect_game(localIP):
    sock = socket.socket()
    sock.connect((localIP, 9090))

    while True:
        data = sock.recv(1)

        draw(window)

        if data == 'u': #up
            client_up()
        elif data == 'd': #down
            client_down()
        elif data == 'n': #nothing
            client_keyup()
        elif data == 'q': #quit
            conn.close()
            break

        if event.type == KEYDOWN:
            server_keydown(event)
            if event.key in (K_UP, K_w):
                sock.send('u')
            if event.key in (K_DOWN, K_s):
                sock.send('d')
        elif event.type == KEYUP:
            server_keyup(event)
            sock.send('n')
        elif event.type == QUIT:
            sock.send('q')
            pygame.quit()
            sys.exit()
            
        pygame.display.update()
    fps.tick(60)

    sock.close()

    #print data
#Starting window of online game
root = tk.Tk()
entry =tk.Entry(root)
entry.pack()
btn1 = tk.Button(root,                  
             text="Create game",       
             width=30,height=5,     
             bg="white",fg="black") 
btn1.bind("<Button-1>", create_game())       
btn1.pack()  
btn2 = Button(root,                  
             text="Create game",       
             width=30,height=5,     
             bg="white",fg="black") 
btn2.bind("<Button-2>", connect_game(entry.get()))       
btn2.pack() 
root.mainloop()


'''if sys.argv[1] == 'cr':
    create_game()
elif sys.argv[1] == 'con':
    connect_game(sys.argv[2])
else:
    print ('Error! No input arguments')'''

#game loop


'''while True:

    draw(window)

    for event in pygame.event.get():

        if event.type == KEYDOWN:
            keydown(event)
        elif event.type == KEYUP:
            keyup(event)
        elif event.type == QUIT:
            pygame.quit()
            sys.exit()
            
    pygame.display.update()'''


#Press h to open a hovercard with more details.
