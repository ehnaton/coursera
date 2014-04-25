# template for "Stopwatch: The Game"
import simplegui

# define global variables
sec = 0
score = 0 
tries = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    A = str((t / 10) / 60) 
    B = str(((t / 10) % 60) / 10)
    C = str(((t / 10) % 60) % 10)
    D = str(t % 10)
    
    return A + ':' + B + C + '.' + D
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    timer.start()

def stop():
    global tries, sec, score    
    
    stopped_at = format(sec)
    
    if timer.is_running():
        tries += 1
    #if the last char of time string is "0", we have even num
    if stopped_at[-1] == '0' and timer.is_running():
        score += 1
        
    timer.stop()
    
#set global vars to zero, stop timer
def reset():
    global sec, tries, score
    tries = 0
    score = 0
    sec = 0
    
    timer.stop()

# define event handler for timer 
def timer_handler():
    global sec
    sec += 1    

# define draw handler
def draw(canvas):
    canvas.draw_text(format(sec), [100,100], 40, "white")
    canvas.draw_text(str(score), [250,30], 30, "green")
    canvas.draw_text("/", [265,30], 25, "green")
    canvas.draw_text(str(tries), [272,30], 30, "green")
    
# create frame
frame = simplegui.create_frame("Stopwatch - The Game!", 300, 200)

# register event handlers
timer = simplegui.create_timer(100, timer_handler) #for 100 ms interval
frame.set_draw_handler(draw)

#add controls
start = frame.add_button("Start", start, 100)
stop = frame.add_button("Stop", stop, 100)
reset = frame.add_button("Reset", reset, 100)

# start frame
frame.start()

# Please remember to review the grading rubric
