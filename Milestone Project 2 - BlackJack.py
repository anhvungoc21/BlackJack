#!/usr/bin/env python
# coding: utf-8

# Computer:
#     - 1 card faced up, 1 card faced down
#     - Draw after Player Stay
# 
# Player:
#     - Draw until Stay or Bust
#     - Ace is either 1 or 11
#     - Jack Queen King = 10
#     - Has a bank of chips, deposit every game
#     - Can choose to play again/stop
#     
# Possible Outcomes:
# 1. Player Busts, Computer hasn't played -> Player lose
# 2. Player Stays, Computer > Player -> Player lose
# 3. Player Stays, Computer draws then Busts -> Player win

# In[1]:


# Global Values
import random
from IPython.display import clear_output
card_ranks = ('Ace', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King')
card_values = {'Ace':None, 'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, "Eight": 8, 'Nine': 9, 'Ten': 10,
              'Jack':10, 'Queen':10, 'King':10}
card_suits = ('Diamonds', "Hearts", "Clubs", "Spades")


# In[2]:


class Card():
    '''
    ATTRIBUTES: rank, suit, value
    METHODS: print
    '''
    def __init__(self,suit,rank):
        self.rank = rank
        self.suit = suit
        self.value = card_values[rank]
    
    def __str__(self):
        return self.rank + ' of ' + self.suit


# In[3]:


class Deck():
    '''
    ATTRIBUTES: all_cards
    METHODS: shuffle, deal_card
    '''
    def __init__(self):
        self.all_cards = []
        
        for suit in card_suits:
            for rank in card_ranks:
                created_card = Card(suit,rank)
                self.all_cards.append(created_card)
                
    def shuffle(self):
        random.shuffle(self.all_cards)
                
    def deal_card(self):
        return self.all_cards.pop(0)


# In[4]:


class Player():
    '''
    ATTRIBUTES: hand, balance
    METHODS: bet, draw, clear_hand, count_points
    '''
    def __init__(self,balance):
        self.hand = []
        # Can create a separate chip class instead.
        self.balance = balance
    
    def bet(self):    
        while True:
            try:
                amount = int(input('How much do you want to bet? '))                    
            except:
                print('Invalid bet.')
            else:
                if amount <= self.balance:
                    return amount
                else:
                    print(f'Insufficient funds! You only have ${self.balance}')
    
    def draw(self,card):
        self.hand.append(card)
        self.value += 
        
    # Instead, can create an attribute self.points. 
    # Whenever a card is drawn, add to self.points.
    
    # Also, can create an attribute self.aces 
    # Whenever a card is drawn, add 1 to self.aces()
    def count_points(self):
        total = 0
        ace_list = []
        for card in self.hand:
            if card.rank == 'Ace':
                ace_list.append(card)
                pass
            else:
                total += card.value
                
        for ace in ace_list:
            if 11 + total <= 21:
                ace.value = 11
                total += ace.value
            else:
                ace.value = 1
                total += ace.value

        return total


# In[ ]:


#### LOGIC
while True:
    ### Set up:
    print('Welcome to BlackJack!')
    clear_output()
    
    ## Player:
    # Player starts with $1000
    MyPlayer = Player(1000)
    
    ## Dealer:
    MyDealer = Player(0)
    
    ### Game begins:
    game_on = True
    
    while game_on:
        # New Deck:
        GameDeck = Deck()
        GameDeck.shuffle()
        
        # Clear hands
        MyPlayer.hand.clear()
        MyDealer.hand.clear()
        
        # Bet
        bet = MyPlayer.bet()
        
        # Deal 2 cards:
        for i in range(2):    
            MyPlayer.draw(GameDeck.deal_card())
            MyDealer.draw(GameDeck.deal_card())
        
        # Dealer's face-up card:
        dealer_card = random.choice(MyDealer.hand)
        
        turn = 'player'
        
        # Player's turn:
        if turn == 'player':
            clear_output()
            print(f'You have deposited ${bet}!')
            print(f'Dealer has {dealer_card}')
            
            print('Your cards are: ')            
            for card in MyPlayer.hand:
                print(f'- {card}')
            
            draw = False
        
            choice = input('Do you want to draw? (Y or N): ').upper()
            if choice == 'Y':
                draw = True
            else:
                turn = 'dealer'
                
            while draw == True:
                clear_output()
                
                MyPlayer.draw(GameDeck.deal_card())
                
                print(f'Dealer has {dealer_card}')
                
                print('Your cards are: ')
                for card in MyPlayer.hand:
                    print(f'- {card}')

                if MyPlayer.count_points() > 21:
                    print(f'Player BUST!')
                    print(f'Dealer: {MyDealer.count_points()}, Player: {MyPlayer.count_points()}')
                    MyPlayer.balance -= bet
                    print(f'Player now has ${MyPlayer.balance}')
                    turn = 'None'
                    break
                else:
                    continue_draw = input('Do you want to continue drawing? (Y or N): ').upper()
                    if continue_draw == 'N':
                        draw = False
                        turn = 'dealer'
                        
        # Dealer's turn:
        if turn == 'dealer':
            clear_output()
             
            round_over = False
            
            while round_over == False:
                if 21 >= MyDealer.count_points() > MyPlayer.count_points():

                    print('Dealer\'s cards are: ')
                    for card in MyDealer.hand:
                        print(f'- {card}')
                    print(f'Dealer wins! Player lost ${bet}!')
                    print(f'Dealer: {MyDealer.count_points()}, Player: {MyPlayer.count_points()}')
                    MyPlayer.balance -= bet
                    print(f'Player now has ${MyPlayer.balance}')
                    round_over = True
                    turn = False

                elif MyDealer.count_points() > 21:
                    print('Dealer\'s cards are: ')
                    for card in MyDealer.hand:
                        print(f'- {card}')
                    print(f'Dealer BUSTS! Player won ${bet}!')
                    print(f'Dealer: {MyDealer.count_points()}, Player: {MyPlayer.count_points()}')
                    MyPlayer.balance += bet
                    print(f'Player now has ${MyPlayer.balance}')
                    round_over = True
                    turn = False
                    
                else:
                    MyDealer.draw(GameDeck.deal_card())
        
        # Continue playing:
        if MyPlayer.balance <= 0:
            print('Game Over! Player has lost all money!')
            game_on = False
        else:
            continue_play = 'false'
            while continue_play not in ['Y', 'N']:
                continue_play = input('Continue playing? (Y or N): ').upper()
                
                if continue_play == 'N':
                    game_on = False
        
    if input('Do you want to play again? (Y or N): ') == 'N':
        print('Thanks for playing!')
        break


# # 
