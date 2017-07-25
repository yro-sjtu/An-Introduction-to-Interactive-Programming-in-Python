# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console
import simplegui
import random
import math

# current range, default: [0,100)
num_range = 100

# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here

    # remove this when you add your code    
    
    global secret_number
    global remain_guess
    secret_number = random.randrange(0,num_range)
    remain_guess = int(math.ceil(math.log(num_range,2)))
    print "======================================="
    print "New game. Range is [0,%d)" % num_range
    print "Number of remaining guesses is %d" % remain_guess
    print ""

# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    
    # remove this when you add your code
    global num_range
    num_range = 100
    new_game()
    

def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global num_range
    num_range = 1000
    new_game()
    
def input_guess(guess):
    # main game logic goes here	
    
    # remove this when you add your code
    global remain_guess
    guess_num = int(guess)
    
    remain_guess -= 1
    
    print "Guess was", guess_num 
    print "Number of remaining guesses is", remain_guess
    
    if guess_num == secret_number:
        print "Correct!"
    elif guess_num < secret_number:
        print "Higher!"
    else:
        print "Lower!"
    print ""
    
    if remain_guess == 0:
        new_game()
        
# create frame
frame = simplegui.create_frame("Guess_the_number", 200, 200)
frame.add_input('guess',input_guess, 100)
frame.add_button('Range is [0,100)', range100, 120)
frame.add_button('Range is [0,1000)', range1000, 120)

# register event handlers for control elements and start frame


# call new_game 
new_game()
frame.start()


# always remember to check your completed program against the grading rubric
