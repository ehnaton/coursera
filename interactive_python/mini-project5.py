# implementation of card game - Memory

import simplegui
import random

WIDTH = 800
HEIGHT = 100
CARDS_COUNT = 16
FIELD_WIDTH = WIDTH / CARDS_COUNT

#create a random deck
def deck():  
    global state, turn
    state = turn = 0
    
    cards = [i%(CARDS_COUNT/2) for i in range(CARDS_COUNT)]
    random.shuffle(cards)
    return cards

# helper function to initialize globals
def new_game():
    global deck_of_cards, exposed
    
    deck_of_cards = deck()
    exposed = [False for i in range(CARDS_COUNT)]
     
# define event handlers
def mouseclick(pos):
    global field_index, state, card1, card2, turn
    
    # add game state logic here
    field_index = pos[0]/FIELD_WIDTH
    
    if not exposed[field_index]:
        if state == 0:
            exposed[field_index] = True
            state = 1
            card1 = field_index
        elif state == 1:
            exposed[field_index] = True
            state = 2
            card2 = field_index
        elif state == 2:
            exposed[field_index] = True
            state = 1            
            if not deck_of_cards[card1] == deck_of_cards[card2]:
                exposed[card1] = exposed[card2] = False  
            else:
                pass
                               
            card1 = field_index
            state = 1
            turn += 1

# cards are logically 50x100 pixels in size    
def draw(canvas):
    global deck_of_cards
    width = 15
    field = 0
    
    for number in deck_of_cards:
        canvas.draw_text(str(number), (width,66), 50, "white")
        if not exposed[field]:
            canvas.draw_polygon([[width-15,0],[width-15,HEIGHT],[width+35,HEIGHT],[width+35,0]], 1, "White", "Green")
        width += FIELD_WIDTH
        field += 1
    
    label.set_text("Turns = " + str(turn))
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", WIDTH, HEIGHT)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()

# Always remember to review the grading rubric
