from card import Card
import random

class Deck:
    def __init__ (self):
        self.cards = []
        self.populateDeck()

    def populateDeck (self):
        
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        suits = ['H', 'D', 'C', 'S']

        for v in values:
            for s in suits:
                self.cards.append((v,s))

    def shuffleDeck(self):
        random.shuffle(self.cards)

    def drawFromTopByNum(self, num):
        cardsDrawn = []
        for i in range(num):
            cardsDrawn.append(self.cards.pop())
        
        return cardsDrawn
    
    def drawSingleCard(self):
        return self.cards.pop()