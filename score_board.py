
from PyQt6.QtGui import QImage, QPixmap, QIcon
from PyQt6.QtWidgets import QDockWidget, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QPushButton, QDialog
from PyQt6.QtCore import pyqtSlot, Qt, QSize
from board import Board


class ScoreBoard(QDockWidget):
    '''# base the score_board on a QDockWidget'''

    def __init__(self, board: Board, parent=None):
        super().__init__(parent)
        self.board = board
        self.initUI()

    def initUI(self):
        '''initiates ScoreBoard UI'''
        self.resize(200, 200)
        self.setWindowTitle('ScoreBoard')

        # create a widget to hold other widgets
        self.mainWidget = QWidget()
        self.mainLayout = QVBoxLayout()

        # horizontal alignment box for info labels
        self.infoSection = QHBoxLayout()

        # horizontal alignment box for text
        self.player1_section = QHBoxLayout()

        # horizontal alignment box for text
        self.player2_section = QHBoxLayout()

        # create two labels which will be updated by signals
        # self.label_clickLocation = QLabel("Click Location: ")
        # self.label_timeRemaining = QLabel("Time remaining: ")

        # elements to info section
        self.info_btn = QPushButton()
        self.info_btn.setIcon(QIcon("icons/info_icon.png"))
        self.info_btn.setObjectName("info_btn")
        self.info_btn.setIconSize(QSize(15,15))

        self.how_to_btn = QPushButton()
        self.how_to_btn.setIcon(QIcon("icons/help_icon.png"))
        self.how_to_btn.setObjectName("how_to_btn")
        self.how_to_btn.setIconSize(QSize(15, 15))

        # elements to a score board
        self.player1_name_label = QLabel(f"{self.board.player1.get_name()}")
        self.player1_time_label = QLabel(f"{self.board.player1.get_time()}")
        self.player1_score_label = QLabel(f"{self.board.player1.get_capturedPieces()}")

        self.player2_name_label = QLabel(f"{self.board.player2.get_name()}")
        self.player2_time_label = QLabel(f"{self.board.player2.get_time()}")
        self.player2_score_label = QLabel(f"{self.board.player2.get_capturedPieces()}")

        self.infoSection.addStretch()
        self.infoSection.addWidget(self.info_btn)
        self.infoSection.addWidget(self.how_to_btn)
        self.infoSection.addStretch()

        self.player1_section.addWidget(self.player1_name_label)
        self.player1_section.addWidget(self.player1_time_label)
        self.player1_section.addWidget(self.player1_score_label)

        self.player2_section.addWidget(self.player2_name_label)
        self.player2_section.addWidget(self.player2_time_label)
        self.player2_section.addWidget(self.player2_score_label)

        self.pass_turn_btn = QPushButton("Pass")
        self.reset_btn = QPushButton("Restart Game")
        self.finish_btn = QPushButton("Finish Game")

        self.mainLayout.addLayout(self.infoSection)
        self.mainWidget.setLayout(self.mainLayout)
        self.mainLayout.addLayout(self.player1_section)
        self.mainLayout.addLayout(self.player2_section)

        # init set up
        # self.mainLayout.addWidget(self.label_clickLocation)
        # self.mainLayout.addWidget(self.label_timeRemaining)

        self.mainLayout.addWidget(self.pass_turn_btn)
        self.mainLayout.addWidget(self.reset_btn)
        self.mainLayout.addWidget(self.finish_btn)

        self.setWidget(self.mainWidget)

        # listeners for buttons
        self.info_btn.clicked.connect(lambda: self.show_rules())
        self.how_to_btn.clicked.connect(lambda: self.show_help())
        self.reset_btn.clicked.connect(lambda: self.board.resetGame())
        self.finish_btn.clicked.connect(lambda: self.show_finish_result())
        self.reset_btn.clicked.connect(lambda: self.pass_turn())

        # styles
        self.setStyleSheet("""
            QWidget {
                width: 150px;
                background-color: white;
            }
            QPushButton {
                padding: 10px 20px;
                border: 1px solid gray;
                font-size: 15px;
                border-radius: 10%;
            }
            QPushButton#info_btn, QPushButton#how_to_btn {
                width: auto;
                border: none;
            }
        """)

    def pass_turn(self):
        # TODO
        pass

    def show_rules(self):
        # set a dialog window
        rules = QDialog()
        # set a title for window
        rules.setWindowTitle("Rules")
        # init layout
        layout = QVBoxLayout()
        # a label for image
        imageLabel = QLabel()
        # path to file
        greatImage = QImage("icons/rules_icon.png")
        # convertion to a pixmap first then to label to display image
        pixmap = QPixmap.fromImage(greatImage)
        pixmap = pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
        imageLabel.setPixmap(pixmap)

        # add QLabel with image to layout with center alignment
        layout.addWidget(imageLabel, alignment=Qt.AlignmentFlag.AlignCenter)
        # adding labels
        logic_label = QLabel("The main game rules:")
        logic_label.setObjectName("logic_label")
        layout.addWidget(logic_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("1. Black plays first, with black and white taking turns."))
        layout.addWidget(QLabel("2. A stone can be placed at any unoccupied intersection of the board with limited exceptions."))
        layout.addWidget(QLabel("3. Stones are captured and removed from the board when surrounded on all four sides by the opponent’s stones."))
        layout.addWidget(QLabel("4. Suicide Rule: A stone cannot be placed in a position where it has no liberties (empty adjacent points), unless it captures opposing stones."))
        layout.addWidget(QLabel("5. Ko Rule: A move that recreates the exact same board position from the previous turn is not allowed."))
        layout.addWidget(QLabel("6. Players aim to surround and control empty intersections to claim territory."))
        layout.addWidget(QLabel("7. The game ends when both players pass consecutively, signaling no more useful moves."))
        layout.addWidget(QLabel("8. Players count controlled empty intersections and captured stones to determine the winner."))
        last_label = QLabel("8. Players count controlled empty intersections and captured stones to determine the winner.")
        # class for last label to add spacing after
        last_label.setObjectName("last_label")
        layout.addWidget(last_label)
        # set layout
        rules.setLayout(layout)
        # add styles
        rules.setStyleSheet(
            """
            QDialog {
                background-color: white;
            }
            #logic_label {
                font-size: 30px;
                font-weight: bold;
                margin-bottom: 20px;
            }
            QLabel {
                font-size: 15px;
                margin-top: 5px;
            }
            #last_label {
                margin-bottom: 20px;
            }
            """
        )
        # execute dialog window
        rules.exec()

    def show_help(self):
        # set a dialog window
        help = QDialog()
        # set a title for window
        help.setWindowTitle("Help")
        # init layout
        layout = QVBoxLayout()
        # a label for image
        imageLabel = QLabel()
        # path to file
        greatImage = QImage("icons/faq_icon.png")
        # convertion to a pixmap first then to label to display image
        pixmap = QPixmap.fromImage(greatImage)
        pixmap = pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
        imageLabel.setPixmap(pixmap)

        # add QLabel with image to layout with center alignment
        layout.addWidget(imageLabel, alignment=Qt.AlignmentFlag.AlignCenter)
        # adding labels
        logic_label = QLabel("Frequently asked questions")
        logic_label.setObjectName("logic_label")
        layout.addWidget(logic_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel("1. Black plays first, with black and white taking turns."))
        layout.addWidget(
            QLabel("2. A stone can be placed at any unoccupied intersection of the board with limited exceptions."))
        layout.addWidget(QLabel(
            "3. Stones are captured and removed from the board when surrounded on all four sides by the opponent’s stones."))
        layout.addWidget(QLabel(
            "4. Suicide Rule: A stone cannot be placed in a position where it has no liberties (empty adjacent points), unless it captures opposing stones."))
        layout.addWidget(QLabel(
            "5. Ko Rule: A move that recreates the exact same board position from the previous turn is not allowed."))
        layout.addWidget(QLabel("6. Players aim to surround and control empty intersections to claim territory."))
        layout.addWidget(
            QLabel("7. The game ends when both players pass consecutively, signaling no more useful moves."))
        layout.addWidget(
            QLabel("8. Players count controlled empty intersections and captured stones to determine the winner."))
        last_label = QLabel(
            "8. Players count controlled empty intersections and captured stones to determine the winner.")
        # class for last label to add spacing after
        last_label.setObjectName("last_label")
        layout.addWidget(last_label)
        # set layout
        help.setLayout(layout)
        # add styles
        help.setStyleSheet(
            """
            QDialog {
                background-color: white;
            }
            #logic_label {
                font-size: 30px;
                font-weight: bold;
                margin-bottom: 20px;
            }
            QLabel {
                font-size: 15px;
                margin-top: 5px;
            }
            #last_label {
                margin-bottom: 20px;
            }
            """
        )
        # execute dialog window
        help.exec()

    def make_connection(self, board):
        '''this handles a signal sent from the board class'''
        # when the clickLocationSignal is emitted in board the setClickLocation slot receives it
        board.clickLocationSignal.connect(self.setClickLocation)
        # when the updateTimerSignal is emitted in the board the setTimeRemaining slot receives it
        board.updateTimerSignal.connect(self.setTimeRemaining)

    def update_ui(self, board):
        # update turn labels
        if self.board.player1.get_turn() == 1:
            self.player1_label.setStyleSheet("""
                color: red;
            """)
            self.player2_label.setStyleSheet("""
                color: blue;
            """)
            print("Changed 1")

        if self.board.player2.get_turn() == 1:
            self.player2_label.setStyleSheet("""
                            color: red;
                        """)
            self.player1_label.setStyleSheet("""
                            color: blue;
                        """)
            print("Changed 2")

        # update timer labels


    @pyqtSlot(str)  # checks to make sure that the following slot is receiving an argument of the type 'int'
    def setClickLocation(self, clickLoc):
        '''updates the label to show the click location'''
        self.label_clickLocation.setText("Click Location: " + clickLoc)
        #print('slot ' + clickLoc)

    @pyqtSlot(int)
    def setTimeRemaining(self, timeRemaining):
        '''updates the time remaining label to show the time remaining'''
        update = "Time Remaining: " + str(timeRemaining)
        self.label_timeRemaining.setText(update)
        print('slot ' + str(timeRemaining))
        # self.redraw()


    def show_finish_result(self):
        dialogWindow = QDialog()
        layout = QVBoxLayout()

        # a label for image
        imageLabel = QLabel()
        # path to file
        greatImage = QImage("icons/finish_icon.png")
        # convertion to a pixmap first then to label to display image
        pixmap = QPixmap.fromImage(greatImage)
        pixmap = pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
        imageLabel.setPixmap(pixmap)
        # add QLabel with image to layout with center alignment
        layout.addWidget(imageLabel, alignment=Qt.AlignmentFlag.AlignCenter)

        game_over_label = QLabel("Game is over")
        game_over_label.setObjectName("game_over_label")
        layout.addWidget(game_over_label, alignment=Qt.AlignmentFlag.AlignCenter)
        # decide who have more scores
        score_player_1 = self.board.player1.get_points()
        score_player_2 = self.board.player2.get_points()
        winer = 1 if score_player_1 > score_player_2 else 2 if score_player_2 > score_player_1 else 0
        # show corresponding result
        if winer == 0:
            layout.addWidget(QLabel("Friendship wins"), alignment=Qt.AlignmentFlag.AlignCenter)
        else:
            layout.addWidget(QLabel("PLayer " + str(winer) + " won"), alignment=Qt.AlignmentFlag.AlignCenter)

        btn_restart = QPushButton("Restart")
        btn_restart.setObjectName("restart_game_btn")

        button = QPushButton("Close")

        buttonSection = QHBoxLayout()
        buttonSection.addWidget(btn_restart)
        buttonSection.addWidget(button)

        layout.addLayout(buttonSection)

        btn_restart.clicked.connect(lambda: self.board.resetGame())
        button.clicked.connect(dialogWindow.accept)

        dialogWindow.setLayout(layout)
        # st styles
        dialogWindow.setStyleSheet(
            """
            QDialog {
                background-color: white;
            }
            QPushButton{
                margin-top: 20px;
                padding: 10px auto;
                background-color: white;
                font-size: 15px;
                border: 1px solid gray;
                border-radius: 10%;
            }
            QLabel {
                font-size:18px;
            }
            #game_over_label {
                font-size:20px;
                margin-bottom: 20px;
                font-weight: bold;
            }
            #restart_game_btn {
                background-color: rgb(250, 241, 202);
            }
            """
        )
        dialogWindow.exec()

        self.close()

    def end_game(self):
        '''calls the calculate_final_scores method from the GameLogic class'''
        if hasattr(self, 'game_logic'):
            self.game_logic.calculate_final_scores(self.game_logic.getBoard())
        else:
            print("GameLogic instance is not connected to the ScoreBoard.")

    def connect_game_logic(self, game_logic):
        '''Connects the ScoreBoard to the GameLogic instance.'''
        self.game_logic = game_logic

