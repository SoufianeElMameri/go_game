from PyQt6.QtWidgets import QFrame, QDialog, QVBoxLayout, QHBoxLayout, QTextEdit, QLabel, QPushButton, QApplication
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QPoint
from PyQt6.QtGui import QPainter, QColor, QBrush, QImage, QPixmap
from piece import Piece
from player import Player
from game_logic import GameLogic

class Board(QFrame):  # base the board on a QFrame widget
    updateTimerSignal = pyqtSignal(int)  # signal sent when the timer is updated
    clickLocationSignal = pyqtSignal(str)  # signal sent when there is a new click location
    
    boardWidth = 6  # setting the board to 6 squares = 7 intersection
    boardHeight = 6 # setting the board to 6 squares = 7 intersection

    timerSpeed = 1000  # the timer updates every 1 second
    counter = 10  # the number the counter will count down from


    def __init__(self, parent):
        super().__init__(parent)

        # player info set up
        self.player1 = Player("Player 1")
        self.player2 = Player("Player 2")

        # game mode
        self.game_mode = "timed"

        # greating, set names and set game mode dialog
        self.initDialog()

        # init score board widget
        self.initBoard()

    def initDialog(self):
        # set up a dialog window
        dialogWindow = QDialog()
        dialogWindow.setWindowTitle("Go Game - Project")
        # set layout
        layout = QVBoxLayout()
        layout.setSpacing(15)  # Add spacing between rows

        # horizontal alignment box for text names inputs
        namesSection = QHBoxLayout()

        # buttons and their class names
        name1 = QTextEdit("")
        # set a place holder as expected user names
        name1.setPlaceholderText("Player 1")
        # set a size
        name1.setFixedSize(150, 38)
        # set object name
        name1.setObjectName("name_input")

        names_separator = QLabel("vs")

        name2 = QTextEdit("")
        # set a place holder as expected user names
        name2.setPlaceholderText("Player 2")
        # set object name
        name2.setObjectName("name_input")
        # set a size
        name2.setFixedSize(150, 38)

        # add to names box layout
        namesSection.addWidget(name1)
        namesSection.addWidget(names_separator, alignment=Qt.AlignmentFlag.AlignCenter)
        namesSection.addWidget(name2)

        # a label for image
        imageLabel = QLabel()
        # path to file
        greatImage = QImage("icons/game_icon.png")
        # conversion to a pixmap first then to label to display image
        pixmap = QPixmap.fromImage(greatImage)
        pixmap = pixmap.scaled(130, 130, Qt.AspectRatioMode.KeepAspectRatio)
        imageLabel.setPixmap(pixmap)

        # add QLabel with image to layout with center alignment
        layout.addWidget(imageLabel, alignment=Qt.AlignmentFlag.AlignCenter)

        # welcome center alignment
        welcome_text_label = QLabel("Welcome")
        welcome_text_label.setObjectName("welcome_text_label")
        layout.addWidget(welcome_text_label, alignment=Qt.AlignmentFlag.AlignCenter)

        desc_label = QLabel("to Go Game")
        desc_label.setObjectName("desc_label")
        layout.addWidget(desc_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # selection of game mode section
        layout.addWidget(QLabel("Let's get acquainted:"), alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(namesSection)

        # levels button section
        layout.addWidget(QLabel("Game Mode"), alignment=Qt.AlignmentFlag.AlignCenter)
        timed_level_btn = QPushButton("Speed GO")
        timed_level_btn.setObjectName("timed_level_btn")

        general_level_btn = QPushButton("Normal Go")
        general_level_btn.setObjectName("general_level_btn")
        # horizontal alignment box for buttons
        levels_buttonLayout = QHBoxLayout()
        levels_buttonLayout.addWidget(timed_level_btn)
        levels_buttonLayout.addWidget(general_level_btn)
        layout.addLayout(levels_buttonLayout)

        # button section
        start_btn = QPushButton("Start Game")
        start_btn.setObjectName("start_btn")

        # change the cursor o pointer for tthe buttons
        start_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        timed_level_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        general_level_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        # horizontal alignment box for buttons
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(start_btn)
        layout.addLayout(buttonLayout)

        dialogWindow.setLayout(layout)

        # buttons press events
        timed_level_btn.clicked.connect(lambda: self.select_level_processing(timed_level_btn, general_level_btn))
        general_level_btn.clicked.connect(lambda: self.select_level_processing(timed_level_btn, general_level_btn))
        start_btn.clicked.connect(lambda: self.on_start_button_clicked(dialogWindow, name1, name2))

        # styles for init widget window
        dialogWindow.setStyleSheet(
            """
            QDialog {
                background-color: white;
            }
            QLabel#welcome_text_label {
                font-size: 40px;
                font-weight: 700;
                margin: 20px auto;
                margin-bottom : -5px;
            }
            QPushButton#start_btn{
                padding: 10px auto;
                background-color: green;
                font-size: 15px;
                font-weight: 600;
                border-radius: 10%;
                background-color: rgb(194, 229, 196 );
                border: 1px solid rgb(179, 211, 180 );
            }
            QLabel {
                font-size:18px;
            }
            QLabel#modeWarning {
                font-size: 10px;
                font-style: italic;
                color: rgb(193, 92, 65);
            }
            #name_input {
                font-size: 15px;
                font-weight: bold;
                border: 1px solid black;
                border-radius: 10px;
                padding: 5px;
            }
            #desc_label {
                margin-top: 0px;
                margin-bottom: 20px;
                font-size: 15px;
            }
            #timed_level_btn, #general_level_btn {
                padding: 10px auto;
                background-color: white;
                font-size: 15px;
                font-weight: 600;
                border-radius: 10%;
                border: 1px solid rgb(212, 212, 212);
            }
            #timed_level_btn {
                background-color: rgb(220, 239, 252);
                border: 1px solid rgb(160, 197, 222);
            }
            #timed_level_btn:hover, #general_level_btn:hover {
                background-color: rgb(180, 220, 250);
            }
            #start_btn:hover{
                background-color: rgb(174, 209, 176);
            }
            """
        )
        dialogWindow.exec()

    def on_start_button_clicked(self, dialog, name1, name2):
        # convert user inputs and set names for players objects
        if name1.toPlainText() :
            self.player1.set_name(name1.toPlainText())

        if name2.toPlainText() :
            self.player2.set_name(name2.toPlainText())

        # print game info to console
        print(self.player1.get_name() + " vs " + self.player2.get_name())
        print("game mode: " + str(self.game_mode))
        # close dialog
        dialog.accept()

    def select_level_processing(self, timed_level_btn, general_level_btn):
        # process game mode selection and view of buttons to accomodate selection change
        active_btn = self.sender()
        # timed mode
        if active_btn == timed_level_btn:
            # set game mode
            self.game_mode = "timed"
            # print("timed level")
            # choose not active button
            not_active_btn = general_level_btn
            # set styles
            active_btn.setStyleSheet("""
                background-color: rgb(220, 239, 252);
                border: 1px solid rgb(160, 197, 222);
            """)
            not_active_btn.setStyleSheet("""
                background-color: white;
                border: 1px solid rgb(212, 212, 212);
            """)
        elif active_btn == general_level_btn:
            # print("no timer level")
            # set game mode
            self.game_mode = "general"
            # choose not active button
            not_active_btn = timed_level_btn
            # set styles
            active_btn.setStyleSheet("""
                background-color: rgb(220, 239, 252);
                border: 1px solid rgb(160, 197, 222);
            """)
            not_active_btn.setStyleSheet("""
                background-color: white;
                border: 1px solid rgb(212, 212, 212);
            """)

    def initBoard(self):
        '''initiates board'''
        print(self.player1)
        self.timer = QTimer(self)  # create a timer for the game
        self.timer.timeout.connect(self.timerEvent)  # connect timeout signal to timerEvent method
        self.isStarted = False  # game is not currently started
        self.start()  # start the game which will start the timer
        
        self.game_logic = GameLogic(self.player1 , self.player2)
        self.game_logic.assign_pieces()
        self.boardArray = [[Piece.NoPiece for _ in range(self.boardWidth+1)] for _ in range(self.boardHeight+1)]
        self.printBoardArray()
        # starting timer if the game mode is timed
        self.startTimeForPlayer()
        

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
        #self.timer.start(self.timerSpeed)  # start the timer with the correct speed
        print("start () - timer is started")

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
            # valid click call try move to validate the move
            if self.tryMove(newX, newY):
                # self.game_logic.currentPlayer.set_turn(0)
                self.game_logic.currentPlayer.stopTimer()
                # since a move has been made clear the previous pass 
                print("player playerd clearing passes")
                self.game_logic.clearPass()
                # check normal piece capture
                captured_pieces = self.game_logic.capture_pieces(self.boardArray, newX, newY, self.game_logic.getCurrentPlayer().get_piece())
                # check self capture
                selfCaptured = self.game_logic.check_selfCapture(self.boardArray,newX, newY, self.game_logic.currentPlayer.get_piece())
                # if self capture return -1 it mean it was a suicided 
                if selfCaptured == -1:
                    # reject the move
                    print("Self-capture detected. Move is invalid, no points awarded.")
                    self.boardArray[newX][newY] = Piece.NoPiece  # Undo the move
                    return 
                print("Pieces captured:", captured_pieces)
                # update the player's score
                self.game_logic.getCurrentPlayer().set_capturedPieces(len(captured_pieces))
                print("Pieces captured ", selfCaptured , selfCaptured)
                self.game_logic.getCurrentPlayer().set_territory(self.game_logic.calculate_territory(self.boardArray , self.game_logic.getCurrentPlayer().get_piece()))
                # switch the turns
                self.game_logic.switchTurn()
                self.game_logic.setBoard(self.boardArray)
                self.game_logic.getCurrentPlayer().set_territory(self.game_logic.calculate_territory(self.boardArray , self.game_logic.getCurrentPlayer().get_piece()))
                # self.game_logic.currentPlayer.set_turn(1)
                self.startTimeForPlayer()
                # printing scores for debug
                print("Current scores: \nPlayer 1 captured" , self.player1.get_capturedPieces() , "\nPlayer 2 captured" , self.player2.get_capturedPieces()  )
            else:
                print(f"Move failed at intersection newX {newX}, newY {newY}")
        else:
            # invalid click
            print("mousePressEvent() - click too far from any intersection, ignoring")

    def resetGame(self):
        '''clears pieces from the board'''
        self.boardArray = [[Piece.NoPiece for _ in range(self.boardWidth+1)] for _ in range(self.boardHeight+1)]
        self.player1.reset()
        self.player2.reset()
        self.game_logic.assign_pieces()
        self.game_logic.clearMoves()
        self.update()
        self.game_logic.clearPass()
        print("game restarted")
        self.game_logic.playersModeChanged()
        self.startTimeForPlayer()
        
    def tryMove(self, newX, newY):
        '''tries to move a piece'''
        
        # check if the position is within the bounds of the board
        if not (0 <= newX <= self.boardHeight and 0 <= newY <= self.boardWidth):
            print(f"Invalid move: Position newX {newX}, newY {newY} is out of bounds")
            return False

        # check if the position is empty and make sure its not a repeating move
        if self.boardArray[newX][newY] == Piece.NoPiece and not self.game_logic.same_move_check(newX, newY , self.game_logic.getCurrentPlayer().get_piece()):
            self.boardArray[newX][newY] = self.game_logic.getCurrentPlayer().get_piece()
            self.update()  # Repaint the board
            self.printBoardArray()
            return True
        else:
            # if the position is occupied, or repeating move reject it
            print(f"Invalid move:")
            return False

    def drawBoardSquares(self, painter):
        '''draw all the square on the board'''
        self.resize(510, 510)
        squareWidth = int(self.squareWidth())
        squareHeight = int(self.squareHeight())
        for row in range(0, Board.boardHeight):
            for col in range(0, Board.boardWidth):
                painter.save()
                painter.translate(col * squareWidth, row * squareHeight)
                painter.setBrush(QBrush(QColor(189, 140, 100)))  # Set brush color
                painter.drawRect(0, 0, squareWidth - 1, squareHeight - 1)  # Draw rectangles
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
    def endGame(self):
        QApplication.quit()

    def startTimeForPlayer(self):
        if self.game_mode == "timed":
            self.game_logic.currentPlayer.startTimer()

