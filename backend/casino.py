from blackjack import Blackjack
from player import Player

def main():

    # Default to blackjack for now
    blackjackTable = Blackjack()
    
    # Create players
    player1 = Player('Papaya')
    player2 = Player('Tommy')

    # Add players
    blackjackTable.addPlayer(player1)
    blackjackTable.addPlayer(player2)

    # Start game
    blackjackTable.startRound()

    # Start Rounds
    blackjackTable.startAllPlayerTurns()
    blackjackTable.startHouseTurn()
    blackjackTable.calculateWinners()

if __name__ == '__main__':
    main()