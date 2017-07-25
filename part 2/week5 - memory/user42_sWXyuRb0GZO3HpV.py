# implementation of card game - Memory

import simplegui
import random

# global variables
cards = [] 		# a list contains the permutation of numbers
exposed = [] 	# a list to determine whether the card is visible or not
state = 0		# reflect the states of unpaired cards
hist = []		# track the previous two clicks, store indice
turn_cnt = 0	# total number of turns

# helper function to initialize globals
def new_game():
    global cards, exposed, state, turn_cnt, hist
    cards = range(8) + range(8)
    random.shuffle(cards)
    exposed = [False for i in range(16)]
    state = 0
    turn_cnt = 0
    hist = []
     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global exposed, state, hist, turn_cnt  
    idx = pos[0] // 50
    if exposed[idx]:
        return None
    
    exposed[idx] = True
    if state == 0:     
        hist.append(idx)
        state = 1
    elif state == 1:
            hist.append(idx)
            state = 2
            turn_cnt += 1
    elif state == 2:
        if cards[hist[0]] != cards[hist[1]]:
            exposed[hist[0]] = False
            exposed[hist[1]] = False
        hist = [idx]
        state = 1
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    label.set_text("Turns: " + str(turn_cnt)) 
    for i in range(len(cards)):
        if exposed[i]:
            bias = frame.get_canvas_textwidth(str(cards[i]), 50) // 2
            text_pos = [i * 50 + bias, 70]
            canvas.draw_text(str(cards[i]), text_pos, 50, "White")
        else:
            rect_points =[[i * 50, 100], [i * 50 + 50, 100],
                          [i * 50 + 50, 0], [i * 50, 0]]
            canvas.draw_polygon(rect_points, 1, "Brown", "Green")

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric