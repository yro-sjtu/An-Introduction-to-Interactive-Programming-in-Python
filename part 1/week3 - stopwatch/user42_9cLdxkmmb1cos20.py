# template for "Stopwatch: The Game"
import simplegui

# define global variables
button_width = 100	# width of button
width = 300 		# width of canvas
height = 200 		# height of canvas
interval = 100		# time interval of timer
tick_cnt = 0		# number of ticks
font_size = 60		# text size of time digits
score_size = 30		# text size of scores
total_stops = 0		# number of stops(total)
succ_stops = 0		# number of successful stops at whole number
isrunning = False	# boolean tag = True if stopwatch is running

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    tenth = t % 10
    t = t // 10
    sec = t % 60
    t = t // 60
    min = t % 10
    return str(min) + ":" + str(sec // 10) + str(sec % 10) + "." + str(tenth) 
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start_button():
    global isrunning
    
    timer.start()
    isrunning = True
    return None

def stop_button():
    global total_stops
    global succ_stops
    global isrunning
    
    if not isrunning:
        return None
    
    timer.stop()
    isrunning = False
    total_stops += 1
    if tick_cnt % 10 == 0:
        succ_stops += 1
    return None

def reset_button():
    global tick_cnt
    global succ_steps
    global total_stops
    
    timer.stop()
    tick_cnt = 0
    succ_stops = 0
    total_stops = 0
    return None

# define event handler for timer with 0.1 sec interval
def tick():
    global tick_cnt
    tick_cnt += 1
    return None

# define draw handler
def draw(canvas):
    curr_time = format(tick_cnt)
    time_width = frame.get_canvas_textwidth(curr_time, font_size)
    canvas.draw_text(curr_time,[(width -  time_width) // 2, 
                                height // 2], font_size, 'White')
    score = str(succ_stops) + "/" + str(total_stops)
    score_width = frame.get_canvas_textwidth(score, 
                                              score_size)
    canvas.draw_text(score, [width - score_width * 1.5, 
                                   score_size ], 
                     score_size, 'Green')
    
# create frame
frame = simplegui.create_frame('Stopwatch',width,height)

# create timer
timer = simplegui.create_timer(interval,tick)

# register event handlers
frame.set_draw_handler(draw)
frame.add_button('Start',start_button,button_width)
frame.add_button('Stop',stop_button,button_width)
frame.add_button('Reset',reset_button,button_width)

# start frame
frame.start()

# Please remember to review the grading rubric
