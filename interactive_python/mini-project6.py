# Mini-project #6 - Blackjack
import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
msg = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, x, y, faceDown):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [x + CARD_CENTER[0], y + CARD_CENTER[1]], CARD_SIZE)
        
        if faceDown:
            card_loc = (CARD_BACK_CENTER[0], CARD_BACK_CENTER[1])
            canvas.draw_image(card_back, card_loc, CARD_BACK_SIZE, [x + CARD_BACK_CENTER[0], y + CARD_BACK_CENTER[1]], CARD_SIZE)
              
# define hand class
class Hand:
    def __init__(self):
        self.hand = []

    def __str__(self):
        return " ".join([str(c) for c in self.hand])

    def add_card(self, card):
        self.hand.append(card)

    def get_value(self):
        val = 0
        ace = False
       
        for card in self.hand:
            if card.get_rank() == 'A':
                ace = True
            val += VALUES[card.get_rank()]
        if ace and val <= 10:
            return val + 10
        else:
            return val
    
    def busted(self):
        val = self.get_value()
        if val > 21:
            return True
    
    def draw(self, canvas, pos):
        for card in self.hand:
            card.draw(canvas, 30+80*self.hand.index(card), pos, False)
            
# define deck class
class Deck:
    def __init__(self):
        self.deck = [Card(suit, rank) for suit in SUITS for rank in RANKS]   
        self.shuffle()

    # add cards back to deck and shuffle
    def shuffle(self):
        random.shuffle(self.deck)

    def deal_card(self):
        return self.deck.pop()
    
    def __str__(self):
        return " ".join([str(c) for c in self.deck])

#define event handlers for buttons
def deal():
    global msg, current, in_play, dealer, player, deck, score

    if in_play:
        score -= 1
    
    player = Hand()
    dealer = Hand()
    deck = Deck()
    deck.shuffle()
    
    msg = ""
    current = "Hit or Stand?"
    in_play = True
    
    player.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
 
def hit():
    global in_play, msg, score, current
    
    if in_play:
        player.add_card(deck.deal_card())
        if player.busted():
            msg = 'You went bust!'
            current = 'New deal?'
            in_play = False
            score -= 1
        if player.get_value() == 21:            
            msg = 'Black jack! You win!'
            current = 'New deal?'
            in_play = False
            score += 1
        
def stand():
    global msg, in_play, score, current
    
    if in_play:
        while dealer.get_value() < 17:
            dealer.add_card(deck.deal_card())
            if dealer.busted():
                msg = "Dealer busted. You won! New deal?"
                score += 1
        if not dealer.busted():            
            if dealer.get_value() > player.get_value():
                msg = "Dealer wins! New deal?"
                score -= 1            
            elif dealer.get_value() == player.get_value():
                msg = "It's a tie, unfortunately you lost"
                score -= 1
            else:
                msg = "You won! New deal?"
                score += 1
            
    in_play = False
    current = "New deal?"
        
# draw handler     
def draw(canvas):
    dealer.draw(canvas, 200)
    player.draw(canvas, 400)
    
    canvas.draw_text("Score: " + str(score), (450, 95), 20, "Red")
    canvas.draw_text("Blackjack", (170,100), 40, "Black")
    canvas.draw_text("Dealer", (70, 180), 26, "Black")
    canvas.draw_text("Player", (70, 380), 26, "Black")
    canvas.draw_text(msg, (220, 180), 20, "Black")    
    canvas.draw_text(current, (400, 380), 20, "Black")     
    
    card = Card("S", "A")
    if in_play:
        card.draw(canvas, 30, 200, faceDown = True)

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# deal an initial hand
deal()
# get things rolling
frame.start()
