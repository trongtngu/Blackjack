from table import Table
from deck import Deck
from card import Card
from player import Player

class Blackjack(Table):
    def __init__(self):
        super().__init__()
        self.cardsPlayed = []
        self.deck = Deck()
        self.deck.shuffleDeck()

        self.house = Player('House')
        self.houseHand = {}
        self.houseTotal = [0, 0]
        
        self.playerHands = {}
        self.playerTotals = {}

        self.options = ['Hit', 'Stand']
    
    def startRound(self):
        if len(self.deck.cards) < (len(self.players) + 1)*2: # Not enough cards left
            self.deck = Deck()
            self.deck.shuffleDeck()
        
        # Deal players cards and calculate score

        # TODO: Clear hands every time new round starts, can use same deck
        for p in self.players:
            hand = self.deck.drawFromTopByNum(2)
            self.playerHands[p.name] = hand
            self.playerTotals[p.name] = [0,0]
            self.calculatePlayerScoreAtFirstHand(p.name)
        
        # Deal house cards and calculate score
        hand = self.deck.drawFromTopByNum(2)
        self.houseHand[self.house.name] = hand
        self.calculateHouseScoreAtFirstHand()

    def startAllPlayerTurns(self):
        for p in self.players:
            self.startPlayerTurn(p)
    
    def startPlayerTurn(self, player):
        print(f"[{player.name}] - Cards: {self.playerHands[player.name]} - Score: {self.playerTotals[player.name]}")
        print(f"[HOUSE] - Cards: {self.houseHand[self.house.name]} - Score: {self.houseTotal}")
        while self.playerTotals[player.name][0] < 21 or self.playerTotals[player.name][1] < 21:
            action = input("-- Hit or Stand? ")
            if action == 'Hit':
                card = self.deck.drawSingleCard()
                print(f"-- Card Drawn: {card}")
                self.playerHands[player.name].append(card)
                self.playerTotals[player.name] = self.addCardToPlayerScore(self.playerTotals[player.name], card)
                print(f"[{player.name}] - Cards: {self.playerHands[player.name]} - Score: {self.playerTotals[player.name]}")
            elif action == 'Stand':
                # Do nothing
                break;
        
        if self.playerTotals[player.name][0] == 21 or self.playerTotals[player.name][1] == 21:
            print("[FINAL] YOU GOT 21")
        
        elif min(self.playerTotals[player.name][0], self.playerTotals[player.name][1]) > 21:
            print("[FINAL] BUST")
        else:
            finalScore = self.playerTotals[player.name][0]
            if self.playerTotals[player.name][1] > self.playerTotals[player.name][0] and self.playerTotals[player.name][1] <= 21:
                finalScore = self.playerTotals[player.name][1]
            
            print(f"[FINAL SCORE] {finalScore}")

        print("================================================================================")

    def startHouseTurn(self):
        print(f"[HOUSE] - Cards: {self.houseHand} - Score: {self.houseTotal}")
        while self.houseTotal[0] < 17:
            card = self.deck.drawSingleCard()
            print(f"Card Drawn: {card}")
            self.houseHand[self.house.name].append(card)
            self.houseTotal = self.addCardToPlayerScore(self.houseTotal, card)
            print(f"[{self.house.name}] || Cards: {self.houseHand} || Score: {self.houseTotal}")
        
        if self.houseTotal[0] == 21 or self.houseTotal[1] == 21:
            print("[FINAL] 21")
        
        elif min(self.houseTotal[0], self.houseTotal[1]) > 21:
            print("[FINAL] BUST")
        else:
            finalScore = self.houseTotal[0]
            if self.houseTotal[1] > self.houseTotal[0] and self.houseTotal[1] <= 21:
                finalScore = self.houseTotal[1]
            
            print(f"[FINAL SCORE] {finalScore}")
        
        print("================================================================================")

    def calculatePlayerScoreAtFirstHand(self, name):
        for c in self.playerHands[name]:
            if c[0] == 'A':
                stdValue = self.playerTotals[name][0] + 1
                acedValue = self.playerTotals[name][1] + 11
                self.playerTotals[name] = [stdValue, acedValue]
            elif c[0] == 'J' or c[0] == 'Q' or c[0] == 'K':
                stdValue = self.playerTotals[name][0] + 10
                acedValue = self.playerTotals[name][1] + 10
                self.playerTotals[name] = [stdValue, acedValue]
            else:
                stdValue = self.playerTotals[name][0] + int(c[0])
                acedValue = self.playerTotals[name][1] + int(c[0])
                self.playerTotals[name] = [stdValue, acedValue]

    def calculateHouseScoreAtFirstHand(self):
        for c in self.houseHand[self.house.name]:
            if c[0] == 'A':
                stdValue = self.houseTotal[0] + 1
                acedValue = self.houseTotal[1] + 11
                self.houseTotal = [stdValue, acedValue]
            elif c[0] == 'J' or c[0] == 'Q' or c[0] == 'K':
                stdValue = self.houseTotal[0] + 10
                acedValue = self.houseTotal[1] + 10
                self.houseTotal = [stdValue, acedValue]
            else:
                stdValue = self.houseTotal[0] + int(c[0])
                acedValue = self.houseTotal[1] + int(c[0])
                self.houseTotal = [stdValue, acedValue]

    def addCardToPlayerScore(self, handTotal, card):
        if card[0] == 'A':
            stdValue = handTotal[0] + 1
            acedValue = handTotal[1] + 11
            handTotal = [stdValue, acedValue]
        elif card[0] == 'J' or card[0] == 'Q' or card[0] == 'K':
            stdValue = handTotal[0] + 10
            acedValue = handTotal[1] + 10
            handTotal = [stdValue, acedValue]
        else:
            stdValue = handTotal[0] + int(card[0])
            acedValue = handTotal[1] + int(card[0])
            handTotal = [stdValue, acedValue]
        
        return handTotal
    
    def calculateWinners(self):
        print("")
        houseFinalScore = self.houseTotal[0]
        if self.houseTotal[1] > self.houseTotal[0] and self.houseTotal[1] <= 21:
            houseFinalScore = self.houseTotal[1]

        for player in self.players:
            finalScore = self.playerTotals[player.name][0]
            if self.playerTotals[player.name][1] > self.playerTotals[player.name][0] and self.playerTotals[player.name][1] <= 21:
                finalScore = self.playerTotals[player.name][1]
            
            if finalScore > 21:
                print(f"[{player.name}] BUSTED")
            elif houseFinalScore > 21 or finalScore > houseFinalScore:
                print(f"[{player.name}] WIN")
            elif houseFinalScore > finalScore:
                print(f"[HOUSE] WIN")
            else:
                print(f"[{player.name}] PUSHES")
        