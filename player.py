from piece import Piece  # Ensure this import is correct

class Player:
    def __init__(self, name):
        '''Initializes a player with the given name and default values for points, time, turn, and piece'''
        self.name = name
        self.points = 0  # Default points
        self.time = 0  # Default time
        self.turn = False  # Default turn (False means it's not the player's turn)
        self.piece = Piece.NoPiece  # Assuming Piece class has a 'noPiece' constant

    # Getter for name
    def get_name(self):
        return self.name

    # Setter for name
    def set_name(self, name):
        self.name = name

    # Getter for points
    def get_points(self):
        return self.points

    # Setter for points
    def set_points(self, points):
        self.points = points

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
