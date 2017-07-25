# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

REFRESH_RATE = 60	# refresh rate of draw_handler in simplegui
vel_const = 10		# constant velocity of moving paddle
SCORE1_POS = [WIDTH // 4, HEIGHT // 5]
SCORE2_POS = [WIDTH * 3 // 4, HEIGHT // 5]

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH // 2, HEIGHT // 2]
    if direction == RIGHT:
        ball_vel = [random.randrange(120 // REFRESH_RATE, 240 // REFRESH_RATE),
                    - random.randrange(60 // REFRESH_RATE, 180 // REFRESH_RATE)]
    elif direction == LEFT:
        ball_vel = [- random.randrange(120 // REFRESH_RATE, 240 // REFRESH_RATE),
                    - random.randrange(60 // REFRESH_RATE, 180 // REFRESH_RATE)]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    
    paddle1_pos = HEIGHT // 2
    paddle2_pos = HEIGHT // 2
    paddle1_vel = 0
    paddle2_vel = 0
    
    #reset score
    score1 = 0
    score2 = 0
    
    spawn_ball(RIGHT)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    global paddle1_vel, paddle2_vel
      
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, "White", "White")
    
    # update paddle's vertical position, keep paddle on the screen 
    paddle1_newY = paddle1_pos + paddle1_vel
    paddle2_newY = paddle2_pos + paddle2_vel
    
    if paddle1_newY >= HALF_PAD_HEIGHT and paddle1_newY <= HEIGHT - HALF_PAD_HEIGHT:
            paddle1_pos = paddle1_newY
    
    if paddle2_newY >= HALF_PAD_HEIGHT and paddle2_newY <= HEIGHT - HALF_PAD_HEIGHT:
            paddle2_pos = paddle2_newY
    
    # draw paddles
    x1 = HALF_PAD_WIDTH
    y1 = paddle1_pos
    canvas.draw_polygon([[x1 - HALF_PAD_WIDTH, y1 - HALF_PAD_HEIGHT], 
                         [x1 + HALF_PAD_WIDTH, y1 - HALF_PAD_HEIGHT], 
                         [x1 + HALF_PAD_WIDTH, y1 + HALF_PAD_HEIGHT], 
                         [x1 - HALF_PAD_WIDTH, y1 + HALF_PAD_HEIGHT]], 
                        1, 'White', 'White')
    x2 = WIDTH - HALF_PAD_WIDTH
    y2 = paddle2_pos
    canvas.draw_polygon([[x2 - HALF_PAD_WIDTH, y2 - HALF_PAD_HEIGHT], 
                         [x2 + HALF_PAD_WIDTH, y2 - HALF_PAD_HEIGHT], 
                         [x2 + HALF_PAD_WIDTH, y2 + HALF_PAD_HEIGHT], 
                         [x2 - HALF_PAD_WIDTH, y2 + HALF_PAD_HEIGHT]], 
                        1, 'White', 'White')
    
    # determine whether paddle and ball collide 
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        if ball_pos[1] >= paddle1_pos - HALF_PAD_HEIGHT and ball_pos[1] <= paddle1_pos + HALF_PAD_HEIGHT:
            score1 += 1
            ball_vel[0] = - ball_vel[0]
            # increase velocity of ball by 10% each time it strikes a paddle.
            ball_vel[0] *= 1.1
            ball_vel[1] *= 1.1
        else:
            score2 += 1
            spawn_ball(RIGHT)
    
    if ball_pos[0] >= WIDTH - PAD_WIDTH - BALL_RADIUS:
        if ball_pos[1] >= paddle2_pos - HALF_PAD_HEIGHT and ball_pos[1] <= paddle2_pos + HALF_PAD_HEIGHT:
            score2 += 1
            ball_vel[0] = - ball_vel[0]
            # increase velocity of ball by 10% each time it strikes a paddle.
            ball_vel[0] *= 1.1
            ball_vel[1] *= 1.1
        else:
            score1 += 1
            spawn_ball(LEFT)
    
    # draw scores
    canvas.draw_text(str(score1), SCORE1_POS, 40, "White")
    canvas.draw_text(str(score2), SCORE2_POS, 40, "White")
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    
    # paddle1 movement
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = - vel_const
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = vel_const
    else:
        paddle1_vel	= 0
    
    # paddle2 movement
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel = - vel_const
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = vel_const
    else:
        paddle2_vel	= 0    
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"] or key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    
    if key == simplegui.KEY_MAP["up"] or key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0
        
def restart():
    new_game()
    

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('Restart', restart, 100)


# start frame
new_game()
frame.start()
