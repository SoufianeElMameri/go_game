from PyQt6.QtWidgets import QApplication, QMainWindow, QDockWidget, QVBoxLayout, QSpacerItem, QSizePolicy, QWidget, \
    QHBoxLayout
from PyQt6.QtCore import Qt

from board import Board
from score_board import ScoreBoard


class Go(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def getBoard(self):
        return self.board

    def getScoreBoard(self):
        return self.scoreBoard

    def initUI(self):
        '''Initiates application UI'''
        # self.board = Board(self)
        # self.setCentralWidget(self.board)
        self.board = Board(self)

        layout = QVBoxLayout()

        vertical_spacer = QSpacerItem(0, 120, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        layout.addSpacerItem(vertical_spacer)
        layout.addWidget(self.board)

        central_widget = QWidget(self)
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

        self.scoreBoard = ScoreBoard(self.board)
        self.scoreBoard.connect_game_logic(self.board.game_logic) 
        
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.scoreBoard)
        self.scoreBoard.make_connection(self.board)

        self.resize(750, 750)
        self.center()
        self.setWindowTitle('Go')
        self.show()


    def center(self):
        '''Centers the window on the screen'''
        screen = QApplication.primaryScreen().availableGeometry()
        size = self.geometry()
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2
        self.move(x, y)





