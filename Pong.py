# Implementation of classic arcade game Pong
# Created by tuanh118

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
VEL_CONST = 8

# helper function that spawns a ball, returns a position vector and a velocity vector
# if right is True, spawn to the right, else spawn to the left
def ball_init(right):
    global ball_pos, ball_vel, score1, score2 # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    x = - random.randrange(3, 5)
    y = - random.randrange(1, 3)
    if right:
        x = - x
    ball_vel = [x, y]
    

# define event handlers
def init():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, ball_pos, ball_vel  # these are floats
    global score1, score2  # these are ints
    paddle1_pos = (HEIGHT - PAD_HEIGHT) / 2
    paddle2_pos = (HEIGHT - PAD_HEIGHT) / 2
    paddle1_vel = 0
    paddle2_vel = 0
    score1 = 0
    score2 = 0
    
    dice = 0
    dice = random.randrange(0, 2)
    if dice == 0:
        right = True
    else:
        right = False
    ball_init(right)
    

def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, paddle1_vel, paddle2_vel
 
    # update paddle's vertical position, keep paddle on the screen
    if (paddle1_vel < 0 and paddle1_pos <= 0) or (paddle1_vel > 0 and paddle1_pos >= HEIGHT - 1 - PAD_HEIGHT):
        paddle1_vel = 0
    if (paddle2_vel < 0 and paddle2_pos <= 0) or (paddle2_vel > 0 and paddle2_pos >= HEIGHT - 1 - PAD_HEIGHT):
        paddle2_vel = 0
    paddle1_pos += paddle1_vel
    paddle2_pos += paddle2_vel
        
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
    # draw paddles
    c.draw_line([PAD_WIDTH / 2, paddle1_pos], [PAD_WIDTH / 2, paddle1_pos + PAD_HEIGHT], PAD_WIDTH, "White")
    c.draw_line([WIDTH - 1 - PAD_WIDTH / 2, paddle2_pos], [WIDTH - 1 - PAD_WIDTH / 2, paddle2_pos + PAD_HEIGHT], PAD_WIDTH, "White")
     
    # update ball
    saved = False
    if ball_pos[0] <= PAD_WIDTH + BALL_RADIUS or ball_pos[0] >= (WIDTH - 1 - PAD_WIDTH) - BALL_RADIUS:
        if ball_pos[0] <= PAD_WIDTH + BALL_RADIUS:
            if ball_pos[1] >= paddle1_pos and ball_pos[1] <= paddle1_pos + PAD_HEIGHT:
                saved = True
                ball_vel[0] = - ball_vel[0]
            else:
                right = True
        elif ball_pos[0] >= WIDTH - 1 - PAD_WIDTH - BALL_RADIUS:
            if ball_pos[1] >= paddle2_pos and ball_pos[1] <= paddle2_pos + PAD_HEIGHT:
                saved = True
                ball_vel[0] = - ball_vel[0]
            else:
                right = False
        if saved:
            ball_vel[0] *= 1.1
            ball_vel[1] *= 1.1
        else:
            ball_init(right)
            if right:
                score2 += 1
            else:
                score1 += 1
    
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= (HEIGHT - 1 ) - BALL_RADIUS:
        ball_vel[1] = -1 * ball_vel[1]
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]    
            
    # draw ball and scores
    c.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")
    c.draw_text(str(score1), [WIDTH / 4, HEIGHT / 4], 40, "White")
    c.draw_text(str(score2), [WIDTH * 3 / 4 - 30, HEIGHT / 4], 40, "White")
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == 87:
        paddle1_vel = - VEL_CONST
    elif key == 83:
        paddle1_vel = VEL_CONST
    elif key == 38:
        paddle2_vel = - VEL_CONST
    elif key == 40:
        paddle2_vel = VEL_CONST
        
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == 87 or key == 83:
        paddle1_vel = 0
    if key == 38 or key == 40:
        paddle2_vel = 0


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", init, 100)

# start frame
init()
frame.start()