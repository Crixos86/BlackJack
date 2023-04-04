import random

class BlackJackGame:
    def __init__(self):
        self.deck = self.create_deck()
        random.shuffle(self.deck)

    def create_deck(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        deck = [{'suit': suit, 'rank': rank} for suit in suits for rank in ranks]
        return deck

    def deal_card(self):
        return self.deck.pop()

    # Weitere Spiellogik und Methoden können hier hinzugefügt werden.
