from math import floor

from PyQt6.QtGui import QImage, QPixmap, QIcon
from PyQt6.QtWidgets import QDockWidget, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QPushButton, QDialog, QGridLayout, \
    QFrame
from PyQt6.QtCore import pyqtSlot, Qt, QSize
from board import Board


class ScoreBoard(QDockWidget):
    '''# base the score_board on a QDockWidget'''

    def __init__(self, board: Board, parent=None):
        super().__init__(parent)
        self.board = board
        # removing the title bar to remove the close button
        self.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.initUI()

        # Connect player timerExpiredSignal to the handle_timer_expired slot
        self.board.player1.timerExpiredSignal.connect(lambda name: self.handle_timer_expired(self.board.player2))
        self.board.player2.timerExpiredSignal.connect(lambda name: self.handle_timer_expired(self.board.player1))

        # Connect player turnUpdateSignal to handle turn change
        self.board.player1.turnUpdateSignal.connect(self.update_ui)
        self.board.player2.turnUpdateSignal.connect(self.update_ui)

        # Connect players' signals to update the UI
        self.board.player1.timerUpdateSignal.connect(self.update_timer)
        self.board.player2.timerUpdateSignal.connect(self.update_timer)

        # Connect players' signals to update the UI
        self.board.player1.scoreUpdateSignal.connect(self.update_score)
        self.board.player2.scoreUpdateSignal.connect(self.update_score)

        self.board.player1.territoryUpdateSignal.connect(self.update_terriory)
        self.board.player2.territoryUpdateSignal.connect(self.update_terriory)
        
        self.board.game_logic.passUpdateSignal.connect(self.update_pass)

        self.board.game_logic.UpdateBoardSignal.connect(self.updateBoard)
        #self.board.player1.timerUpdateSignal.connect(self.update_timer)
        #self.board.player2.timerUpdateSignal.connect(self.update_timer)

    def initUI(self):
        '''initiates ScoreBoard UI'''
        self.resize(200, 200)
        self.setWindowTitle('ScoreBoard')

        # create a widget to hold other widgets
        self.mainWidget = QWidget()
        self.mainLayout = QVBoxLayout()

        # horizontal alignment box for info labels
        self.infoSection = QHBoxLayout()

        # vertical alignment box for text
        self.player1_section_widget = QWidget()
        self.player1_section_widget.setFixedHeight(150)
        self.player1_section = QVBoxLayout(self.player1_section_widget)

        # vertical alignment box for text
        self.player2_section_widget = QWidget()
        self.player2_section_widget.setFixedHeight(150)
        self.player2_section = QVBoxLayout(self.player2_section_widget)

        # elements to info section
        self.info_btn = QPushButton()
        self.info_btn.setIcon(QIcon("icons/info_icon.png"))
        self.info_btn.setObjectName("info_btn")

        self.info_btn.setIconSize(QSize(30,30))
        self.info_btn.setCursor(Qt.CursorShape.PointingHandCursor)


        self.how_to_btn = QPushButton()
        self.how_to_btn.setIcon(QIcon("icons/help_icon.png"))
        self.how_to_btn.setObjectName("how_to_btn")

        self.how_to_btn.setIconSize(QSize(30, 30))
        self.how_to_btn.setCursor(Qt.CursorShape.PointingHandCursor)


        # active user label controll
        self.active_player_widget = QWidget()
        self.active_player_label_layout =  QHBoxLayout(self.active_player_widget)
        self.active_player_label = QLabel(f"{self.board.game_logic.getCurrentPlayer().get_name()}")
        self.active_player_label_layout.addWidget(self.active_player_label)
        self.active_player_widget.setFixedHeight(50)


        self.pass_label = QWidget()
        self.pass_label_layout =  QHBoxLayout(self.pass_label)
        self.pass_label_label = QLabel("")
        self.pass_label_layout.addWidget(self.pass_label_label)
        self.pass_label.setFixedHeight(50)


        

        # elements to a score board
        # player 1 section
        # name
        self.player1_name_label = QLabel(f"{self.board.player1.get_name()}")
        self.player1_name_label.setStyleSheet("""
            font-weight: bold;
            font-size: 18px;
        """)
        # type of peaces
        if self.board.player1.get_piece() == 1:
            self.player1_color_label = QLabel(f"Pieces: White")
        else:
            self.player1_color_label = QLabel(f"Pieces: Black")
        # to show or not time left label
        if self.board.game_mode == "timed":
            self.player1_time_label = QLabel(f"Time left: {self.parse_time(self.board.player2.get_time())}")
        # show score
        self.player1_score_label = QLabel(f"Score: {self.board.player1.get_capturedPieces()}")
        # show area captured
        self.player1_territory_label = QLabel(f"Territory: 0")

        # player 1 section
        # name
        self.player2_name_label = QLabel(f"{self.board.player2.get_name()}")
        self.player2_name_label.setStyleSheet("""
            font-weight: bold;
            font-size: 18px;
        """)
        # type of peaces
        if self.board.player2.get_piece() == 1:
            self.player2_color_label = QLabel(f"Pieces: White")
        else:
            self.player2_color_label = QLabel(f"Pieces: Black")
        # to show or not time left label
        if self.board.game_mode == "timed":
            self.player2_time_label = QLabel(f"Time left: {self.parse_time(self.board.player2.get_time())}")
        # show score
        self.player2_score_label = QLabel(f"Score: {self.board.player2.get_capturedPieces()}")
        # show area captured
        self.player2_territory_label = QLabel(f"Territory: 0")

        # add elements to info section
        # stratches to add equal space before and after widgets
        self.infoSection.addStretch()
        self.infoSection.addWidget(self.info_btn)
        self.infoSection.addWidget(self.how_to_btn)
        self.infoSection.addStretch()

        # add elements to player 1 section
        self.player1_section.addWidget(self.player1_name_label)
        if self.board.game_mode == "timed":
            self.player1_section.addWidget(self.player1_time_label)
        self.player1_section.addWidget(self.player1_color_label)
        self.player1_section.addWidget(self.player1_score_label)
        self.player1_section.addWidget(self.player1_territory_label)

        # add elements to player 2 section
        self.player2_section.addWidget(self.player2_name_label)
        if self.board.game_mode == "timed":
            self.player2_section.addWidget(self.player2_time_label)
        self.player2_section.addWidget(self.player2_color_label)
        self.player2_section.addWidget(self.player2_score_label)
        self.player2_section.addWidget(self.player2_territory_label)

        # create control buttons
        self.pass_turn_btn = QPushButton("Pass")
        self.change_mode_btn = QPushButton("Players/Mode")
        self.reset_btn = QPushButton("Restart Game")

        # separator line
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line2 = QFrame()
        line2.setFrameShape(QFrame.Shape.HLine)

        # add all elements to a main layout
        self.mainWidget.setLayout(self.mainLayout)
        self.mainLayout.addLayout(self.infoSection)
        self.mainLayout.addStretch()
        self.mainLayout.addWidget(self.active_player_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addWidget(self.pass_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.mainLayout.addStretch()
        self.mainLayout.addWidget(line)
        self.mainLayout.addWidget(self.player1_section_widget)
        self.mainLayout.addWidget(line2)
        self.mainLayout.addWidget(self.player2_section_widget)
        self.mainLayout.addStretch()

        self.mainLayout.addWidget(self.pass_turn_btn)
        self.mainLayout.addWidget(self.reset_btn)
        self.mainLayout.addWidget(self.change_mode_btn)

        # set everything to a score board widget
        self.setWidget(self.mainWidget)

        # listeners for buttons
        self.info_btn.clicked.connect(lambda: self.show_rules())
        self.how_to_btn.clicked.connect(lambda: self.show_help())
        self.reset_btn.clicked.connect(lambda: self.board.resetGame())
        self.pass_turn_btn.clicked.connect(lambda: self.show_finish_result(-1))
        self.change_mode_btn.clicked.connect(lambda: (self.board.initDialog() , self.board.resetGame()))

        self.update_ui(self.board.game_logic.getCurrentPlayer().get_name(), 1)

        # styles
        self.setStyleSheet("""
            QWidget {
                width: 150px;
                background-color: white;
                font-size: 15px;
            }
            QPushButton {
                background-color: rgb(217, 232, 250);
                padding: 10px 20px;
                border: 1px solid rgb(163, 185, 212);
                font-size: 15px;
                border-radius: 10%;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgb(163, 185, 212);
            }
            QPushButton#info_btn, QPushButton#how_to_btn {
                background-color: white;
                width: auto;
                border: none;
            }
        """)

    def updateBoard(self):
        if self.board.game_mode == "general":
            self.player1_time_label.setText("")
            self.player2_time_label.setText("")
        self.player1_name_label.setText(self.board.player1.get_name())
        self.player2_name_label.setText(self.board.player2.get_name())
        if self.board.player1.get_piece() == 1:
            self.player1_color_label.setText("Pieces: White")
            self.player2_color_label.setText("Pieces: Black")
        else:
            self.player1_color_label.setText("Pieces: Black")
            self.player2_color_label.setText("Pieces: White")
    # function to show window to show rules
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
    # function to show window to show faq
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
        layout.addWidget(QLabel("1. Who starts: The player using black stones always moves first, followed by the player using white stones. Turns alternate between players."))
        layout.addWidget(QLabel("2.How stones can be placed: A stone can be placed on any unoccupied intersection of the board, except in situations where doing so violates the game's rules"))
        layout.addWidget(QLabel("3. What is territory: Territory refers to empty intersections on the board that are surrounded by a player’s stones."))
        layout.addWidget(QLabel("4. What is a pass: You skip your turn when you don't see beneficial move."))
        layout.addWidget(QLabel("5. What is a KO rule: The ko rule removes this possibility of indefinite repetition by forbidding the recapture of the ko."))
        layout.addWidget(QLabel("6. What is a suicide rule: You cannot place a stone which will immediately have no liberties."))
        last_label = QLabel("7. When the game ends: The game ends when both players pass their turn, or in speed go mode - when time is over")
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

    # function to parse raw seconds to a classic time stamp
    def parse_time(self, time):
        # get full minutes
        minutes = time / 60
        # get full seconds
        seconds =  time % 60
        # return
        return str(floor(minutes)) + ":" + str(floor(seconds))

    def make_connection(self, board):
        '''this handles a signal sent from the board class'''
        # when the clickLocationSignal is emitted in board the setClickLocation slot receives it
        board.clickLocationSignal.connect(self.setClickLocation)

    def update_ui(self, player_name, turn):
        # self.active_player_label.setText(self.board.player2.get_name())
        # update turn labels
        if player_name == self.board.player1.get_name():
            if turn == 1:
                self.active_player_label.setText(self.board.player1.get_name() + "'s Turn")
                self.active_player_label.setStyleSheet("""
                    color: orange;
                    font-size: 20px;
                    font-weight: bold;
                """)
                self.pass_turn_btn.setStyleSheet("""
                    QPushButton {
                        background-color: rgb(252, 230, 199);
                        border: 1px solid rgb(219, 199, 171);
                    }
                    QPushButton:hover {
                        background-color: rgb(219, 199, 171);
                    }
                """)
        elif player_name == self.board.player2.get_name():
            if turn == 1:
                self.active_player_label.setText(self.board.player2.get_name()+"'s Turn")
                self.active_player_label.setStyleSheet("""
                    color: green;
                    font-size: 20px;
                    font-weight: bold;
                """)
                self.pass_turn_btn.setStyleSheet("""
                    QPushButton {
                        background-color: rgb(205, 247, 210);
                        border: 1px solid rgb(171, 207, 176);
                    }
                    QPushButton:hover {
                        background-color: rgb(171, 207, 176);
                    }
                """)

        # update timer labels
    def update_timer(self, player_name, time_left):
        # find which player to update his timer
        if self.board.game_mode == "timed":
            if player_name == self.board.player1.get_name():
                self.player1_time_label.setText(f"Time left: {self.parse_time(time_left)}")
            elif player_name == self.board.player2.get_name():
                self.player2_time_label.setText(f"Time left: {self.parse_time(time_left)}")

    def update_score(self, player_name, score):
        # find which player to update his timer
        if player_name == self.board.player1.get_name():
            self.player1_score_label.setText(f"Scores: {score} ")
        elif player_name == self.board.player2.get_name():
            self.player2_score_label.setText(f"Scores: {score}")
    def update_terriory(self, player_name, territory):
        # find which player to update his timer
        if player_name == self.board.player1.get_name():
            self.player1_territory_label.setText(f"Territory: {territory} ")
        elif player_name == self.board.player2.get_name():
            self.player2_territory_label.setText(f"Territory: {territory} ")

    def update_pass(self, player_name , type):
        # find which player to update his timer
        if type == "pass":
            self.pass_label_label.setText(f"{player_name} passed his turn")
        elif type == "clear":
            self.pass_label_label.setText("")
 
    @pyqtSlot(str)  # checks to make sure that the following slot is receiving an argument of the type 'int'
    def setClickLocation(self, clickLoc):
        '''updates the label to show the click location'''
        self.label_clickLocation.setText("Click Location: " + clickLoc)
        #print('slot ' + clickLoc)


    def show_finish_result(self, player):
        # check if both players passed their turns
        if self.board.game_logic.passTurn() or player != -1:

            self.end_game()
            self.board.game_logic.player1.startTimer()
            self.board.game_logic.player2.startTimer()
            dialogWindow = QDialog()
            dialogWindow.setWindowFlags(Qt.WindowType.FramelessWindowHint)
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
            score_player_1 = self.board.player1.get_finalScore()
            score_player_2 = self.board.player2.get_finalScore()
            if player!= -1:
                layout.addWidget(QLabel(player.get_name() + " won"), alignment=Qt.AlignmentFlag.AlignCenter)
                layout.addWidget(QLabel("Score : " + str(player.get_finalScore())), alignment=Qt.AlignmentFlag.AlignCenter)
            else:
                winner = self.board.player1 if score_player_1 > score_player_2 else self.board.player2 if score_player_2 > score_player_1 else 0
                # show corresponding result
                if winner == 0:
                    layout.addWidget(QLabel("Friendship wins"), alignment=Qt.AlignmentFlag.AlignCenter)
                else:
                    layout.addWidget(QLabel(winner.get_name() + " won"), alignment=Qt.AlignmentFlag.AlignCenter)
                    layout.addWidget(QLabel("Score :" + str(winner.get_finalScore())), alignment=Qt.AlignmentFlag.AlignCenter)

            # create buttons and object names for them
            btn_restart = QPushButton("Restart")
            btn_restart.setObjectName("restart_game_btn")

            button = QPushButton("Close")
            button.setObjectName("close_game_btn")

            # group buttons to section
            buttonSection = QHBoxLayout()
            buttonSection.addWidget(btn_restart)
            buttonSection.addWidget(button)

            # add button section to a dialog window
            layout.addLayout(buttonSection)

            # event listeners for buttons
            btn_restart.clicked.connect(lambda: (self.board.resetGame(), dialogWindow.accept()))
            button.clicked.connect(lambda: (self.board.endGame(), dialogWindow.accept()))

            # set layout
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
                    font-weight: bold;
                }
                #close_game_btn {
                    background-color: rgb(245, 188, 188);
                    font-weight: bold;
                }
                #restart_game_btn:hover {
                    background-color: rgb(230, 215, 151);
                }
                #close_game_btn:hover{
                    background-color: rgb(196, 141, 135);
                }
                """
            )
            dialogWindow.exec()

    def end_game(self):
        '''calls the calculate_final_scores method from the GameLogic class'''
        if hasattr(self, 'game_logic'):
            self.game_logic.calculate_final_scores(self.game_logic.getBoard())
        else:
            print("GameLogic instance is not connected to the ScoreBoard.")

    def connect_game_logic(self, game_logic):
        '''Connects the ScoreBoard to the GameLogic instance.'''
        self.game_logic = game_logic

    def handle_timer_expired(self, player):
        print(f"{player.get_name()} ran out of time. Ending game.")
        self.show_finish_result(player)
