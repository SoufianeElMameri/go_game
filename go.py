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

        # moved to a v box layout to add margins between board and parent go widget
        layout = QVBoxLayout()

        # vertical spacer to add 120 point margin on top
        vertical_spacer = QSpacerItem(0, 120, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        # first add spacer
        layout.addSpacerItem(vertical_spacer)
        # add board itself
        layout.addWidget(self.board)

        # central overall app
        central_widget = QWidget(self)
        # set layout with board
        central_widget.setLayout(layout)

        # make this wiget central
        self.setCentralWidget(central_widget)

        # add a score board
        self.scoreBoard = ScoreBoard(self.board)
        # establish connection with scoreboard
        self.scoreBoard.connect_game_logic(self.board.game_logic) 
        
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.scoreBoard)
        self.scoreBoard.make_connection(self.board)

        # set a size
        self.resize(750, 750)
        # place on center
        self.center()
        # set title
        self.setWindowTitle('Go')
        # show
        self.show()


    def center(self):
        '''Centers the window on the screen'''
        screen = QApplication.primaryScreen().availableGeometry()
        size = self.geometry()
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2
        self.move(x, y)





