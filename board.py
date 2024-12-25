from PyQt6.QtWidgets import QFrame
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QPoint
from PyQt6.QtGui import QPainter, QColor, QBrush
from piece import Piece

class Board(QFrame):  # base the board on a QFrame widget
    updateTimerSignal = pyqtSignal(int)  # signal sent when the timer is updated
    clickLocationSignal = pyqtSignal(str)  # signal sent when there is a new click location

    # TODO set the board width and height to be square
    boardWidth = 7  # board is 0 squares wide # TODO this needs updating
    boardHeight = 7  #
    timerSpeed = 1000  # the timer updates every 1 second
    counter = 10  # the number the counter will count down from

    def __init__(self, parent):
        super().__init__(parent)
        self.initBoard()

    def initBoard(self):
        '''initiates board'''
        self.timer = QTimer(self)  # create a timer for the game
        self.timer.timeout.connect(self.timerEvent)  # connect timeout signal to timerEvent method
        self.isStarted = False  # game is not currently started
        self.start()  # start the game which will start the timer

        self.boardArray = [[Piece.NoPiece for _ in range(self.boardWidth+1)] for _ in range(self.boardHeight+1)]  # TODO - create a 2d int/Piece array to store the state of the game
        self.printBoardArray()    # TODO - uncomment this method after creating the array above

    def printBoardArray(self):
        '''prints the boardArray in an attractive way'''
        print("boardArray:")
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.boardArray]))

    def mousePosToColRow(self, event):
        '''convert the mouse click event to a row and column'''
        # get mouse click's X and Y coordinates
        x = event.position().x()
        y = event.position().y()

        # calculate the nearest intersection
        col = round(x / self.squareWidth())
        row = round(y / self.squareHeight())

        # clamp the values to be within the board boundaries
        col = max(0, min(col, self.boardWidth ))
        row = max(0, min(row, self.boardHeight ))
        return row, col

    def squareWidth(self):
        '''returns the width of one square in the board'''
        return self.contentsRect().width() / self.boardWidth

    def squareHeight(self):
        '''returns the height of one square of the board'''
        return self.contentsRect().height() / self.boardHeight

    def start(self):
        '''starts game'''
        self.isStarted = True  # set the boolean which determines if the game has started to TRUE
        self.resetGame()  # reset the game
        #self.timer.start(self.timerSpeed)  # start the timer with the correct speed
        print("start () - timer is started")

    def timerEvent(self):
        '''this event is automatically called when the timer is updated. based on the timerSpeed variable '''
        # TODO adapt this code to handle your timers
        if Board.counter == 0:
            print("Game over")
        self.counter -= 1
        #print('timerEvent()', self.counter)
        self.updateTimerSignal.emit(self.counter)

    def paintEvent(self, event):
        '''paints the board and the pieces of the game'''
        painter = QPainter(self)
        #painter.fillRect(self.contentsRect(), QBrush(QColor(245, 222, 179)))
        self.drawBoardSquares(painter)
        self.drawPieces(painter)

    def mousePressEvent(self, event):
        '''this event is automatically called when the mouse is pressed'''
        # get mouse click's X and Y coordinates
        x = event.position().x()
        y = event.position().y()
        # get the nearest intersection
        newX, newY = self.mousePosToColRow(event)
        # calculate the actual intersection position in pixels
        intersection_x = newY * self.squareWidth()
        intersection_y = newX * self.squareHeight()
        # calculate the distance from the click to the intersection
        distance = ((x - intersection_x) ** 2 + (y - intersection_y) ** 2) ** 0.5
        # check if the click is within the acceptable radius
        tolerance = min(self.squareWidth(), self.squareHeight()) / 2
        if distance <= tolerance:
            # valid click; delegate move logic to tryMove
            if self.tryMove(newX, newY):
                print(f"Valid move at intersection newX {newX}, newY {newY}")
            else:
                print(f"Move failed at intersection newX {newX}, newY {newY}")
        else:
            # invalid click
            print("mousePressEvent() - click too far from any intersection, ignoring")

    def resetGame(self):
        '''clears pieces from the board'''
        # TODO write code to reset game

    def tryMove(self, newX, newY):
        '''tries to move a piece'''
        # check if the position is within the bounds of the board
        if not (0 <= newX <= self.boardHeight and 0 <= newY <= self.boardWidth):
            print(f"Invalid move: Position newX {newX}, newY {newY} is out of bounds")
            return False

        # check if the position is empty
        if self.boardArray[newX][newY] == Piece.NoPiece:
            # place the piece (e.g., Black)
            self.boardArray[newX][newY] = Piece.Black
            self.update()  # Repaint the board
            self.printBoardArray()
            return True
        else:
            # if the position is occupied, reject the move
            print(f"Invalid move: Cell at newX {newX}, newY {newY} is already occupied")
            return False

    def drawBoardSquares(self, painter):
        '''draw all the square on the board'''
        squareWidth = int(self.squareWidth())
        squareHeight = int(self.squareHeight())
        for row in range(0, Board.boardHeight):
            for col in range(0, Board.boardWidth):
                painter.save()
                painter.translate(col * squareWidth, row * squareHeight)
                painter.setBrush(QBrush(QColor(181, 136, 99)))  # Set brush color
                painter.drawRect(0, 0, squareWidth, squareHeight)  # Draw rectangles
                painter.restore()

    def drawPieces(self, painter):
        '''draw the pieces at intersections'''
        for row in range(len(self.boardArray)):
            for col in range(len(self.boardArray[0])):
                piece = self.boardArray[row][col]
                # skip empty intersections
                if piece == Piece.NoPiece:
                    continue

                painter.save()

                # Calculate the center of the intersection
                x = col * self.squareWidth()
                y = row * self.squareHeight()

                # Set brush color based on the piece type
                if piece == Piece.Black:
                    painter.setBrush(QColor(0, 0, 0))  # Black
                elif piece == Piece.White:
                    painter.setBrush(QColor(255, 255, 255))  # White

                # Draw the piece as a circle centered on the intersection
                radius = min(self.squareWidth(), self.squareHeight()) / 3
                painter.drawEllipse(
                    int(x - radius),
                    int(y - radius),
                    int(2 * radius),
                    int(2 * radius)
                )

                painter.restore()
