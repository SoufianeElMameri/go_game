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

        self.boardArray = [[Piece.NoPiece for _ in range(self.boardWidth)] for _ in range(self.boardHeight)]  # TODO - create a 2d int/Piece array to store the state of the game
        self.printBoardArray()    # TODO - uncomment this method after creating the array above

    def printBoardArray(self):
        '''prints the boardArray in an attractive way'''
        print("boardArray:")
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.boardArray]))

    def mousePosToColRow(self, event):
        '''convert the mouse click event to a row and column'''
        # get mouse click's X-coordinate
        x = event.position().x()
        # get mouse click's Y-coordinate
        y = event.position().y()

        # calculate column and row based on square dimensions
        col = int(x // self.squareWidth())
        row = int(y // self.squareHeight())

        # ensure the values are within bounds
        if 0 <= col < self.boardWidth and 0 <= row < self.boardHeight:
            return row, col
        else:
            return None, None

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
        self.timer.start(self.timerSpeed)  # start the timer with the correct speed
        print("start () - timer is started")

    def timerEvent(self):
        '''this event is automatically called when the timer is updated. based on the timerSpeed variable '''
        # TODO adapt this code to handle your timers
        if Board.counter == 0:
            print("Game over")
        self.counter -= 1
        print('timerEvent()', self.counter)
        self.updateTimerSignal.emit(self.counter)

    def paintEvent(self, event):
        '''paints the board and the pieces of the game'''
        painter = QPainter(self)
        #painter.fillRect(self.contentsRect(), QBrush(QColor(245, 222, 179)))
        self.drawBoardSquares(painter)
        self.drawPieces(painter)

    def mousePressEvent(self, event):
        '''this event is automatically called when the mouse is pressed'''
        # get mouse click's X-coordinate
        x = event.position().x()
        # get mouse click's Y-coordinate
        y = event.position().y()

        # convert pixel coordinates to row and column
        row, col = self.mousePosToColRow(event)

        # check if the click is within the board boundaries
        if row is not None and col is not None:
            # calculate the top-left pixel of the clicked cell
            squareWidth = self.squareWidth()
            squareHeight = self.squareHeight()
            cell_x = col * squareWidth
            cell_y = row * squareHeight
            if self.tryMove(row, col):  # Attempt to make the move
                print(f"Valid move at row {row}, col {col}")
            else:
                print(f"Move failed at row {row}, col {col}")
            # emit signal with pixel coordinates
            clickLoc = f"cell top-left: [{int(cell_x)}, {int(cell_y)}], row: {row}, col: {col}"
            print(f"mousePressEvent() - {clickLoc}")
            self.clickLocationSignal.emit(clickLoc)
        else:
            # handle clicks outside the board
            print(f"mousePressEvent() - click outside the board at [{x}, {y}]")

    def resetGame(self):
        '''clears pieces from the board'''
        # TODO write code to reset game

    def tryMove(self, newX, newY):
        '''tries to move a piece'''
        # validate the move
        if self.boardArray[newX][newY] == Piece.NoPiece:  # Check if the cell is empty
            self.boardArray[newX][newY] = Piece.Black  # Example: Always place a Black piece
            self.update()  # Trigger a repaint to show the new piece
            print(f"Placed Black piece at row {newX}, col {newY}")
            return True
        else:
            print(f"Invalid move: Cell at row {newX}, col {newY} is already occupied")
            return False

    def drawBoardSquares(self, painter):
        '''draw all the square on the board'''
        print("[DEBUG] drawBoardSquares called")
        squareWidth = int(self.squareWidth())
        squareHeight = int(self.squareHeight())
        for row in range(0, Board.boardHeight):
            for col in range(0, Board.boardWidth):
                print(f"[DEBUG] Drawing square at row {row}, col {col}")
                painter.save()
                painter.translate(col * squareWidth, row * squareHeight)
                painter.setBrush(QBrush(QColor(181, 136, 99)))  # Set brush color
                painter.drawRect(0, 0, squareWidth, squareHeight)  # Draw rectangles
                painter.restore()

    def drawPieces(self, painter):
        '''draw the pieces on the board'''
        for row in range(0, len(self.boardArray)):
            for col in range(0, len(self.boardArray[0])):
                piece = self.boardArray[row][col]
                # skip empty squares
                if piece == 0:
                    continue
                painter.save()
                painter.translate(col * self.squareWidth(), row * self.squareHeight())
                # TODO draw some pieces as ellipses
                # TODO choose your color and set the painter brush to the correct color
                if piece == 1:  # Black piece
                    painter.setBrush(QColor(0, 0, 0))
                elif piece == 2:  # White piece
                    painter.setBrush(QColor(255, 255, 255))
                radius = int((self.squareWidth() - 2) / 2)
                center = QPoint(radius, radius)
                painter.drawEllipse(center, radius, radius)
                painter.restore()
