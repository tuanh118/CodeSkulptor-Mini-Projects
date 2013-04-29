# Mini-project #6 - Blackjack
# created by tuanh118

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png") 

DIST = 30

# initialize some useful global variables
in_play = False
outcome = ""
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

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        result = ""
        for count in range (0, len(self.cards)):
            result += self.cards[count].suit + self.cards[count].rank + " "
        return result

    def add_card(self, card):
        if (card.suit in SUITS) and (card.rank in RANKS):
            self.cards.append(card)

    # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
    def get_value(self):
        value = 0
        ace = False
        for count in range (0, len(self.cards)):
            value += VALUES[self.cards[count].rank]
            if self.cards[count].rank == 'A':
                ace = True
        if ace and value + 10 <= 21:
            value += 10
        return value        

    def busted(self):
        if self.get_value() > 21:
            return True
        else:
            return False
    
    def draw(self, canvas, p):
        for count in range (1, len(self.cards)):
            self.cards[count].draw(canvas, [p[0] + CARD_CENTER[0] + count * (DIST + CARD_SIZE[0]), p[1] + CARD_CENTER[1]])
       
 
        
# define deck class
class Deck:
    def __init__(self):
        self.cards = [Card(SUITS[i], RANKS[j]) for i in range (0, len(SUITS)) for j in range (0, len(RANKS))]
        
        
    # add cards back to deck and shuffle
    def shuffle(self):
        self.__init__()
        random.shuffle(self.cards)        

    def deal_card(self):
        card_dealt = self.cards.pop(0)
        return card_dealt
    
    def __str__(self):
        result = ""
        for count in range (0, len(self.cards)):
            result += self.cards[count].suit + self.cards[count].rank + "\n"
        return result



#define event handlers for buttons
def deal():
    global outcome, in_play, player, dealer, d, score

    d = Deck()
    d.shuffle()
    outcome = ""
    
    player = Hand()
    player.add_card(d.deal_card())
    player.add_card(d.deal_card())
    
    dealer = Hand()
    dealer.add_card(d.deal_card())
    dealer.add_card(d.deal_card())
    
    if in_play:
        outcome = "You lose."
        score -= 1
    
    
    in_play = True

def hit():
    global in_play, player, d, score, outcome
 
    # if the hand is in play, hit the player
    if in_play:
        player.add_card(d.deal_card())
   
    # if busted, assign an message to outcome, update in_play and score
        if player.busted():
            outcome = "You went bust and lose."
            score -= 1
            in_play = False
       
def stand():
    global dealer, player, d, in_play, score, outcome
    
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        while dealer.get_value() < 17:
            dealer.add_card(d.deal_card())

    # assign a message to outcome, update in_play and score
        if player.busted():
            outcome = "You have busted."
        else:
            if dealer.busted():
                outcome = "Dealer went busted and you win."
                score += 1
            elif dealer.get_value() < player.get_value():
                outcome = "You win."
                score += 1
            else:
                outcome = "You lose."
                score -= 1
        in_play = False
    

# draw handler    
def draw(canvas):
    global in_play, dealer, player
    
    canvas.draw_text("Blackjack", [100, 100], 35, "Aqua")
    canvas.draw_text("Score " + str(score), [450, 100], 25, "Black")
    canvas.draw_text("Dealer", [80, 170], 25, "Black")
    canvas.draw_text(outcome, [200, 170], 25, "Black")
    
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [60 + CARD_BACK_SIZE[0], 170 + CARD_BACK_SIZE[1]], CARD_SIZE)
    else:
        dealer.cards[0].draw(canvas, [60 + CARD_CENTER[0], 170 + CARD_CENTER[1]])
    dealer.draw(canvas, [60, 170])
    canvas.draw_text("Player", [80, 370], 25, "Black")
    if in_play:
        canvas.draw_text("Hit or stand?", [200, 370], 25, "Black")
    else:
        canvas.draw_text("New deal?", [200, 370], 25, "Black")
    
    player.cards[0].draw(canvas, [60 + CARD_CENTER[0], 370 + CARD_CENTER[1]])
    player.draw(canvas, [60, 370])


# initialization frame
frame = simplegui.create_frame("Blackjack", 800, 600)
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


# remember to review the gradic rubric