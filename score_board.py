from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QDockWidget, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QPushButton, QDialog
from PyQt6.QtCore import pyqtSlot, Qt
from board import Board

class ScoreBoard(QDockWidget):
    '''# base the score_board on a QDockWidget'''

    def __init__(self, board: Board, parent=None):
        super().__init__(parent)
        self.board = board
        self.player1_state = self.board.player1.get_turn()
        self.player2_state = self.board.player2.get_turn()
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
        self.info_btn = QPushButton("Rules")
        self.how_to_btn = QPushButton("Help")

        # elements to a score board
        self.player1_name_label = QLabel(f"{self.board.player1.get_name()}")
        self.player1_time_label = QLabel(f"{self.board.player1.get_time()}")
        self.player1_score_label = QLabel(f"{self.board.player1.get_points()}")

        self.player2_name_label = QLabel(f"{self.board.player2.get_name()}")
        self.player2_time_label = QLabel(f"{self.board.player2.get_time()}")
        self.player2_score_label = QLabel(f"{self.board.player2.get_points()}")

        self.infoSection.addWidget(self.info_btn)
        self.infoSection.addWidget(self.how_to_btn)

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
        self.reset_btn.clicked.connect(lambda: self.board.resetGame())
        self.finish_btn.clicked.connect(lambda: self.show_finish_result())
        self.reset_btn.clicked.connect(lambda: self.pass_turn())

    def pass_turn(self):
        # TODO
        pass

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