# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
nextstep = ""

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
        # return a string representation of a hand
        ans = 'Hand contains '
        for card in self.cards:
            ans += str(card) + ' '
        return ans

    def add_card(self, card):
        self.cards.append(card)	# add a card object to a hand

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        value, cnt_aces = 0, 0
        for card in self.cards:
            value += VALUES[card.get_rank()]
            if card.get_rank() == 'A':
                cnt_aces += 1
        if cnt_aces == 0:
            return value
        else:
            if value + 10 <= 21:
                return value + 10
            else:
                return value
   
    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        card_pos = pos
        for card in self.cards:
            card.draw(canvas, card_pos)
            card_pos[0] += 1.5 * CARD_SIZE[0]
        
# define deck class 
class Deck:
    def __init__(self):
        # create a Deck object
        self.cards = []
        for s in SUITS:
            for r in RANKS:
                self.cards.append(Card(s, r))

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.cards)

    def deal_card(self):
        # deal a card object from the deck
        return self.cards.pop()
    
    def __str__(self):
        # return a string representing the deck
        ans ='Deck contains '
        for card in self.cards:
            ans += str(card) + ' '
        return ans

#define event handlers for buttons
def deal():
    global outcome, in_play, score
    global deck, player, dealer, nextstep
    if in_play:
        outcome = "You lose"
        score -= 1
    
    nextstep = "Hit or stand?"
    deck = Deck()
    deck.shuffle()
    player, dealer = Hand(), Hand()
    for i in range(2):
        player.add_card(deck.deal_card())
        dealer.add_card(deck.deal_card())
    
    if not in_play:
        outcome = ""
        in_play = True
    
#    print "player_hands: " + str(player) + ", value: " + str(player.get_value())
#    print "dealer_hands: " + str(dealer) + ", value: " + str(dealer.get_value())

def hit():
    # if the hand is in play, hit the player
    global in_play, outcome, score, nextstep 
    if not in_play:
        return None
    outcome = ""
    player.add_card(deck.deal_card())

    # if busted, assign a message to outcome, update in_play and score
    if player.get_value() > 21:
        outcome = 'You have busted and lose'
        score -= 1
        in_play = False
        nextstep = "New deal?"

def stand():
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    global in_play, outcome, score, nextstep
    if not in_play:
        return None
    outcome = ""
    if player.get_value() > 21:
        outcome = 'You have busted and lose'
        in_play = False       
    else:
        while dealer.get_value() < 17:
            dealer.add_card(deck.deal_card())

    # assign a message to outcome, update in_play and score
    dealer_value = dealer.get_value()
    if dealer_value > 21:
        outcome = 'Dealer bust and you win'
        score += 1
        in_play = False
    else:
        if dealer_value < player.get_value():
            outcome = 'You win'
            score += 1
            in_play = False
        else:
            outcome = 'You lose'
            score -= 1
            in_play = False
    
    nextstep = "New deal?"

# draw handler    
def draw(canvas):
    canvas.draw_text("Blackjack", [100, 100], 50, 'Aqua')
    canvas.draw_text("Score: " + str(score), [400, 100], 40, "Black")
    canvas.draw_text("Dealer", [72, 170], 30, "Black")
    canvas.draw_text("Player", [72, 370], 30, "Black")
    canvas.draw_text(outcome, [200, 170], 30, "Red")
    canvas.draw_text(nextstep, [200, 370], 30, "Black")
    player.draw(canvas, [72, 400])
    dealer.draw(canvas, [72, 200])
    if in_play:
        canvas.draw_image(card_back, [CARD_CENTER[0], CARD_CENTER[1]], CARD_SIZE, [72 + CARD_CENTER[0], 200 + CARD_CENTER[1]], CARD_SIZE)

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric