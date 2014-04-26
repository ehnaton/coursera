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
SPEED_FACTOR = 1.1

ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [0, 0]

score1 = 0
score2 = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    
    # start ball on the left side or on the right side
    if direction == RIGHT:
        ball_vel = [random.randrange(120, 240) / 90, -random.randrange(60, 180) / 90]
    else:
        ball_vel = [-random.randrange(120, 240) / 90, -random.randrange(60, 180) / 90]
    
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel # these are floats
    global score1, score2 # these are ints
    
    score1 = 0
    score2 = 0
    
    paddle1_pos = HEIGHT / 2.0
    paddle2_pos = HEIGHT / 2.0
    paddle1_vel = 0.0
    paddle2_vel = 0.0
    
    if random.randrange(2) == 0:
        spawn_ball(RIGHT)
    else:
        spawn_ball(LEFT)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel 
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    #touching bottom margin
    if ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
        
    #touching top margin
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
    
    #striking with right gutter
    if ball_pos[0] >= (WIDTH - 1) - PAD_WIDTH - BALL_RADIUS:
        if ball_pos[1] > paddle2_pos - HALF_PAD_HEIGHT and ball_pos[1] < paddle2_pos + HALF_PAD_HEIGHT:
            ball_vel[0] = -ball_vel[0] * SPEED_FACTOR   
            ball_vel[1] = ball_vel[1] * SPEED_FACTOR
        else:      
            score1 += 1
            spawn_ball(LEFT)
    
    #striking left gutter
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        if ball_pos[1] > paddle1_pos - HALF_PAD_HEIGHT and ball_pos[1] < paddle1_pos + HALF_PAD_HEIGHT:
            ball_vel[0] = -ball_vel[0] * SPEED_FACTOR   
            ball_vel[1] = ball_vel[1] * SPEED_FACTOR
        else:
            score2 += 1
            spawn_ball(RIGHT)
    
    # update paddle's vertical position
    paddle1_pos += paddle1_vel
    paddle2_pos += paddle2_vel
    
    #keep paddle on the screen    
    if paddle1_pos - HALF_PAD_HEIGHT < 0:
        paddle1_pos = HALF_PAD_HEIGHT
    if paddle1_pos + HALF_PAD_HEIGHT > HEIGHT - 1:
        paddle1_pos = HEIGHT - 1 - HALF_PAD_HEIGHT
    
    if paddle2_pos - HALF_PAD_HEIGHT < 0:
        paddle2_pos = HALF_PAD_HEIGHT
    if paddle2_pos + HALF_PAD_HEIGHT > HEIGHT - 1:
        paddle2_pos = HEIGHT - 1 - HALF_PAD_HEIGHT
    
    # draw paddles
    canvas.draw_polygon([(0, paddle1_pos - HALF_PAD_HEIGHT), (PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT),
                    (PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT), (0, paddle1_pos + HALF_PAD_HEIGHT)],
                   1, "White", "White")
    canvas.draw_polygon([(WIDTH - PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT), (WIDTH, paddle2_pos - HALF_PAD_HEIGHT),
                    (WIDTH, paddle2_pos + HALF_PAD_HEIGHT), (WIDTH - PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT)],
                   1, "White", "White")
    
    # draw ball and scores
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, "White", "White")    
    canvas.draw_text(str(score1), ((WIDTH / 4) - 10, 40), 40, "Green")
    canvas.draw_text(str(score2), ((WIDTH / 4 * 3) - 10, 40), 40, "Green")
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    acc = 10
    
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = -acc
    
    if key == simplegui.KEY_MAP['s']:
        paddle1_vel = acc
    
    if key == simplegui.KEY_MAP['up']:
        paddle2_vel = -acc
    
    if key == simplegui.KEY_MAP['down']:
        paddle2_vel = acc

def keyup(key):
    global paddle1_vel, paddle2_vel
    
    if key == simplegui.KEY_MAP['w'] or key == simplegui.KEY_MAP['s']:
        paddle1_vel = 0
    
    if key == simplegui.KEY_MAP['up'] or key == simplegui.KEY_MAP['down']:
        paddle2_vel = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

frame.add_button("Restart game", new_game, WIDTH/3)

# start frame
frame.start()
new_game()
