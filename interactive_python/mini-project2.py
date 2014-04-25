# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import math
import random

# initialize global variables used in your code

secret_num = 0
ran = 0
guess_num = 0
which_game = ""

# helper function to start and restart the game
def new_game():
    global secret_num
    global ran
    secret_num = random.randint(0, ran)
    if ran == 0:
        print "Please select valid range"
    else:
        print "New game. Range is from 0 to", ran
        print "Number of remaining guesses is", guess_num
    print
    
# define event handlers for control panel
def range100():
    global ran
    global guess_num
    global which_game
    
    which_game = "**"
    guess_num = 7    
    ran = 100
    new_game()

def range1000():
    global ran
    global guess_num
    global which_game
    
    which_game = "***"
    guess_num = 10
    ran = 1000
    new_game()

def refresh_game():
    global which_game
    if which_game == "**":
        range100()
    else:
        range1000()
    
def input_guess(guess): 
    global secret_num
    global guess_num
    
    guess_int = int(guess)    
    guess_num -= 1
    
    print "Guess was", guess
    print "Number of remaining guesses is", guess_num
    
    if secret_num > guess_int:
        print "Higher!"
        print
    elif secret_num < guess_int:
        print "Lower!"
        print
    elif secret_num == guess_int:
        print
        print "Correct! You won!"
        print
        refresh_game()
    else:
        print "Some unexplicable error."
        refresh_game()
        
    if guess_num <= 0:
        print "You have lost. Guess was", secret_num
        print
        refresh_game()
        
# create frame
f = simplegui.create_frame("Guess the number", 200, 200)

# register event handlers for control elements
f.add_button("Range is [0,100]", range100, 200)
f.add_button("Range is [0,1000]", range1000, 200)
f.add_input("Enter a guess", input_guess,  200)

# call new_game and start frame
new_game()

f.start()
