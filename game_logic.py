import random
from player import Player
from piece import Piece

class GameLogic:
    def __init__(self, player1 , player2):
        '''Initializes the GameLogic object'''
        print("Game Logic Object Created")
        self.currentPlayer = None
        self.player1 = player1
        self.player2 = player2

    # method to assign pieces to players randomly
    def assign_pieces(self):
        '''Randomly assign pieces to two players (one Black, one White)'''
        # Randomly assign Black and White pieces
        pieces = [Piece.Black, Piece.White]
        random.shuffle(pieces)  # Shuffle the pieces list to randomize assignment
        
        # Assign pieces to players
        self.player1.set_piece(pieces[0])
        self.player2.set_piece(pieces[1])

        # Print out the assigned pieces for debugging
        if self.player1.get_piece() == Piece.Black:
            print(f"{self.player1.get_name()} is assigned 'Black'")
            print(f"{self.player2.get_name()} is assigned 'White'")
            self.currentPlayer = self.player1
        else:
            print(f"{self.player2.get_name()} is assigned 'Black'")
            print(f"{self.player1.get_name()} is assigned 'White'")
            self.currentPlayer = self.player2
    # methd to return the currentPlayer's turn
    def getCurrentPlayer(self):
        return self.currentPlayer
    
    # method to switch the current player's turn
    def switchTurn(self):
        if self.currentPlayer == self.player1:
            self.currentPlayer = self.player2
        else:
            self.currentPlayer = self.player1