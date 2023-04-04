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

    def get_card_value(self, card):
            if card['rank'] in ['Jack', 'Queen', 'King']:
                return 10
            elif card['rank'] == 'Ace':
                return 11
            else:
                return int(card['rank'])

    def calculate_hand_value(self, hand):
        value = sum([self.get_card_value(card) for card in hand])
        aces = sum([1 for card in hand if card['rank'] == 'Ace'])

        while value > 21 and aces:
            value -=  10
        aces -= 1

        return value