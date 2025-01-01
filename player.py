from piece import Piece  # Ensure this import is correct
from PyQt6.QtCore import QTimer, pyqtSignal, QObject

class Player(QObject):
    timerExpiredSignal = pyqtSignal(str) 
    timerUpdateSignal = pyqtSignal(str, int)
    scoreUpdateSignal = pyqtSignal(str, int)
    def __init__(self, name):
        '''Initializes a player with the given name and default values for points, time, turn, and piece'''
        super().__init__()
        self.name = name
        self.capturedPieces = 0  # Default points
        self.finalScore = 0
        self.remaining_time = 2 * 60
        self.time = QTimer(self)
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
        self.scoreUpdateSignal.emit(self.name, self.capturedPieces)

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

    # method to start the player's timer
    def startTimer(self):
        '''Starts the player's timer if not already running'''
        if self.timer_running:
            print(f"Timer for {self.name} is already running!")  # Debugging log
            return
        print(f"Starting timer for {self.name}")  # Debugging log
        self.timer_running = True
        self.timer.start()  # Start the QTimer

    # method to stop the player's timer
    def stopTimer(self):
        '''Stops the player's timer'''
        if not self.timer_running:
            print(f"Timer for {self.name} is not running!")  # Debugging log
            return
        print(f"Stopping timer for {self.name}")  # Debugging log
        self.timer_running = False
        self.timer.stop()  # Stop the QTimer

    # method to decrement the timer and signal UI update
    def _decrement_time(self):
        '''Decrements the player's time and emits signals for UI updates'''
        if self.remaining_time > 0:
            self.remaining_time -= 1  # Decrease remaining time by 1 second
            print(f"{self.name}'s remaining time: {self.remaining_time} seconds")  # Debugging log
            self.timerUpdateSignal.emit(self.name, self.remaining_time)  # Emit signal to update the UI
        else:
            # Time ran out; signal expiration
            print(f"{self.name}'s time is up!")  # Debugging log
            self.timer_running = False
            self.timer.stop()  # Stop the QTimer
            self.timerExpiredSignal.emit(self.name)  # Emit signal for timer expiration