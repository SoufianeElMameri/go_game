from piece import Piece  # Ensure this import is correct

class Player:
    def __init__(self, name):
        '''Initializes a player with the given name and default values for points, time, turn, and piece'''
        self.name = name
        self.capturedPieces = 0  # Default points
        self.finalScore = 0
        self.time = 2 # 2 minutes
        self.turn = 0  
        self.piece = Piece.NoPiece  # Assuming Piece class has a 'noPiece' constant

    def get_turn(self):
        return self.turn
    def set_turn(self, turn):
        self.turn = turn
    # Getter for name
    def get_name(self):
        return self.name

    # Setter for name
    def set_name(self, name):
        self.name = name

    # Getter for points
    def get_capturedPieces(self):
        return self.capturedPieces

    # Setter for points
    def set_capturedPieces(self, points):
        self.capturedPieces+=points

    # Getter for time
    def get_time(self):
        return self.time

    # Setter for time
    def set_time(self, time):
        self.time = time

    # Getter for turn
    def get_turn(self):
        return self.turn

    # Setter for turn
    def set_turn(self, turn):
        self.turn = turn
        
    # Getter for piece
    def get_piece(self):
        return self.piece

    # Setter for piece
    def set_piece(self, piece):
        # Ensure the piece is one of the valid types (NoPiece, White, Black)
        if piece in [Piece.NoPiece, Piece.White, Piece.Black]:
            self.piece = piece
        else:
            print(f"Invalid piece value: {piece}. Must be one of: NoPiece, White, Black.")

    # Getter for finalscore
    def get_finalScore(self):
        return self.finalScore

    # Setter for finalscore
    def set_finalScore(self, score):
        self.finalScore = score