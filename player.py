from piece import Piece  # Ensure this import is correct
from PyQt6.QtCore import QTimer, pyqtSignal, QObject

class Player(QObject):
    # signal updates to connect ui change on change of those variables
    timerExpiredSignal = pyqtSignal(str) 
    timerUpdateSignal = pyqtSignal(str, int)
    scoreUpdateSignal = pyqtSignal(str, int)
    turnUpdateSignal = pyqtSignal(str, int)
    territoryUpdateSignal = pyqtSignal(str, int)
    def __init__(self, name):
        '''Initializes a player with the given name and default values for points, time, turn, and piece'''
        super().__init__()
        self.name = name
        self.capturedPieces = 0  # Default points
        self.finalScore = 0
        self.remaining_time = 2 * 60
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._decrement_time)  # Connect the timeout signal to _decrement_time
        self.turn = 0  
        self.piece = Piece.NoPiece  # Assuming Piece class has a 'noPiece' constant
        self.timer_running = False
        self.territory = 0

    # Getter for name
    def get_territory(self):
        return self.territory
    def set_territory(self, territory):
        self.territory = territory
        self.territoryUpdateSignal.emit(self.name, self.territory)

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
        return self.remaining_time

    # Setter for time
    def set_time(self, time):
        self.remaining_time = time

    # Getter for turn
    def get_turn(self):
        return self.turn

    # Setter for turn
    def set_turn(self, turn):
        self.turn = turn
        self.turnUpdateSignal.emit(self.name, self.turn)
        
    # Getter for piece
    def get_piece(self):
        return self.piece

    # Setter for piece
    def set_piece(self, piece):
        # Ensure the piece is one of the valid types (NoPiece, White, Black)
        if piece in [Piece.NoPiece, Piece.White, Piece.Black]:
            self.piece = piece

    # Getter for finalscore
    def get_finalScore(self):
        return self.finalScore

    # Setter for finalscore
    def set_finalScore(self, score):
        self.finalScore = score

    # method to start the timer for the player if no running
    def startTimer(self):
        if self.timer.isActive():
            return
        print(f"Starting timer for {self.name}") 
        # starting the QTimer with a 1-second interval 
        self.timer.start(1000)  

    # method tto stop he timer for the player if running
    def stopTimer(self):
        if not self.timer.isActive():
            return
        print(f"Stopping timer for {self.name}") 
        # stop the QTimer
        self.timer.stop()  
    #decrementing the player time and emiting signals for UI updates
    def _decrement_time(self):
        
        if self.remaining_time > 0:
            self.remaining_time -= 1
            # emit signal to update the UI
            self.timerUpdateSignal.emit(self.name, self.remaining_time)  
        else:
            # Time ran out; signal expiration
            # stop the QTimer
            self.timer.stop()  
            # emit signal to update the UI
            self.timerExpiredSignal.emit(self.name)  
    def reset(self):
        # reseting captured pieces and updating ui
        self.capturedPieces = 0
        self.scoreUpdateSignal.emit(self.name, self.capturedPieces)

        # reseting remaining time and updating ui
        self.remaining_time = 2 * 60  
        self.timerUpdateSignal.emit(self.name, self.remaining_time)
        self.territory = 0
        # stop the timer 
        self.stopTimer()

        # rest turn
        self.turn = 0

        # reset pieces to no pieces
        self.piece = Piece.NoPiece
        # to debug
        print(f"Player {self.name} reset complete")