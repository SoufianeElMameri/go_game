from piece import Piece  # Ensure this import is correct
from PyQt6.QtCore import QTimer, pyqtSignal, QObject

class Player(QObject):
    timerExpiredSignal = pyqtSignal(str) 
    def __init__(self, name):
        '''Initializes a player with the given name and default values for points, time, turn, and piece'''
        super().__init__()
        self.name = name
        self.capturedPieces = 0  # Default points
        self.finalScore = 0
        self.time = 2 * 60 # 2 minutes
        self.turn = 0  
        self.piece = Piece.NoPiece  # Assuming Piece class has a 'noPiece' constant
        self.timer_running = False

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

    def startTimer(self):
        '''Starts the timer to decrement time every second.'''
        print(f"{self.name}'s timer started with {self.time} seconds remaining.")
        if not self.timer_running:
            self.timer_running = True
            self._decrement_time()

    def stopTimer(self):
        '''Stops the timer for the player.'''
        print(f"{self.name}'s timer stopped.")
        self.timer_running = False

    def _decrement_time(self):
        '''Decrements the player's time and re-triggers itself every second.'''
        if not self.timer_running:
            return  # If the timer is stopped, exit the function

        if self.time > 0:
            self.time -= 1
            print(f"{self.name}'s remaining time: {self.time} seconds")
            QTimer.singleShot(1000, self._decrement_time)  # Re-call this function after 1 second
        else:
            print(f"{self.name}'s time is up!")
            self.timer_running = False
            self.timerExpiredSignal.emit(self.name)  # Notify that the player's time has expired
