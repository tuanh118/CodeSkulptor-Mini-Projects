# implementation of card game - Memory
# created by tuanh118

import simplegui
import random

WIDTH = 1200
HEIGHT = 150

# helper function to initialize globals
def init():
    global cards, exposed, correct, state, pre_card, moves
    cards = [(i % 8) for i in range(16)]
    random.shuffle(cards)
    exposed = [False for i in range(16)]
    correct = [False for i in range(8)]
    state = 0
    pre_card = -1
    moves = 0
    l.set_text("Moves = " + str(moves))
    
def change_state(current_card):
    global state, exposed, pre_card, moves
    if state == 0:
        moves += 1
        state = 1
    elif state == 1:
        if pre_card == cards[current_card]:
            correct[cards[current_card]] = True            
        state = 2
    else:
        for i in range(16):
            if not correct[cards[i]]:
                exposed[i] = False
        moves += 1
        state = 1
    l.set_text("Moves = " + str(moves))
    
    
# define event handlers
def mouseclick(pos):
    global state, exposed, pre_card
    rec_width = WIDTH / 16
    for i in range(16):
        if pos[0] >= rec_width * i and pos[0] < rec_width * (i + 1) and not exposed[i]:
            change_state(i)
            pre_card = cards[i]
            exposed[i] = True
                
    
# cards are logically 50x100 pixels in size    
def draw(canvas):
    for i in range(16):
        if exposed[i]:
            canvas.draw_text(str(cards[i]), [WIDTH / 16 * i + WIDTH / 64, HEIGHT / 2 + 20], 60, "White")
        else:
            canvas.draw_text(" ", [WIDTH / 16 * i + WIDTH / 64, 60], 30, "White")
        canvas.draw_line([WIDTH / 16 * (i + 1), 0], [WIDTH / 16 * (i + 1), HEIGHT], 2, "White")
        
        
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", WIDTH, HEIGHT)
frame.add_button("Restart", init)
l1 = frame.add_label("")
l = frame.add_label("Moves = 0")
l2 = frame.add_label("")
credit = frame.add_label("The Polar Bear")

# initialize global variables
init()

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
frame.start()


# Always remember to review the grading rubric