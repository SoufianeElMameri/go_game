import random
from piece import Piece

class GameLogic:
    def __init__(self, player1 , player2):
        '''Initializes the GameLogic object'''
        print("Game Logic Object Created")
        self.currentPlayer = None
        self.player1 = player1
        self.player2 = player2
        self.blackLastMoves = []
        self.whiteLastMoves = []
        self.passes = 0

    # method to assign pieces to players randomly
    def assign_pieces(self):
        '''Randomly assign pieces to two players (one Black, one White)'''
        pieces = [Piece.Black, Piece.White]
        # shuffle the pieces list to randomize assignment
        random.shuffle(pieces)  
        
        # assign pieces to players
        self.player1.set_piece(pieces[0])
        self.player2.set_piece(pieces[1])

        # print out the assigned pieces for debugging
        if self.player1.get_piece() == Piece.Black:
            print(f"{self.player1.get_name()} is assigned 'Black'")
            print(f"{self.player2.get_name()} is assigned 'White'")
            self.currentPlayer = self.player1
        else:
            print(f"{self.player2.get_name()} is assigned 'Black'")
            print(f"{self.player1.get_name()} is assigned 'White'")
            self.currentPlayer = self.player2
    # methd to return the currentPlayer
    def getCurrentPlayer(self):
        return self.currentPlayer
    
    # method to switch the current player
    def switchTurn(self):
        if self.currentPlayer == self.player1:
            self.currentPlayer = self.player2
        else:
            self.currentPlayer = self.player1
    
    # method to search for group of connected pieces using flood-fill algo
    def find_group(self, board, x, y, player_color):

        stack = [(x, y)]
        group = []
        # to track visted points
        visited = set()
        # up, down, left, right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] 

        # loop until there are no more points to explore
        while stack:
            # get the current point from the stack
            cx, cy = stack.pop()
            # check if the points where already visited
            if (cx, cy) in visited:
                continue
            # if not visted add them 
            visited.add((cx, cy))
            # add the new point to the group
            group.append((cx, cy))


            for dx, dy in directions:
                nx, ny = cx + dx, cy + dy
                # checking if the neighboring point is in the bounds and matches the player color
                if 0 <= nx < len(board) and 0 <= ny < len(board[0]) and board[nx][ny] == player_color:
                    stack.append((nx, ny))
        return group

    # check if a gorup of pieces are surrounded by opponent pieces
    def is_group_surrounded(self, board, group, opponent_color):

        # up, down, left, right directions
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        # convert the group to a set to search faster
        group_set = set(group) 

        for x, y in group:
            # check all neighboring points
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                # check if the neighboring point is out of bounds
                if not (0 <= nx < len(board) and 0 <= ny < len(board[0])):
                    continue
                #skip the neighboring point if it is part of the group
                if (nx, ny) in group_set:
                    continue
                # check if the neighboring point is not the opponent's piece
                if board[nx][ny] != opponent_color:
                    return False
        return True

    # check if a group of pieces has internal space
    def group_has_internal_space(self, board, group):
        # directions
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        # checking each piece in the group
        for x, y in group:
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                # check if the neighboring point is within bounds and is empty
                if 0 <= nx < len(board) and 0 <= ny < len(board[0]) and board[nx][ny] == Piece.NoPiece:
                    # check if the empty space connects to the outside
                    if self.is_empty_space_open(board, nx, ny):
                        # if there is an empty space return true
                        return True  
        # return false no internal space
        return False
    # check that the group is fully surrounded
    def is_group_fully_surrounded(self, board, group, opponent_color):
        # checking if the group is surrounded
        if not self.is_group_surrounded(board, group, opponent_color):
            return False

        # if the group is surrounded check if it has internal space
        if self.group_has_internal_space(board, group):
            return False

        return True
    
    # check if an empty space connects to the board boundary
    def is_empty_space_open(self, board, x, y):
        
        stack = [(x, y)]
        visited = set()
        # directions up, down left right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        # loop until there are no more points to explore
        while stack:
            cx, cy = stack.pop()
            # check if the point was already visited
            if (cx, cy) in visited:
                continue
            # mark the point as visited
            visited.add((cx, cy))
            # explore all neighboring points
            for dx, dy in directions:
                nx, ny = cx + dx, cy + dy
                # check if the neighboring point is out of bounds
                if not (0 <= nx < len(board) and 0 <= ny < len(board[0])):  # Reached board boundary
                    # out-of-bounds means the empty space is open
                    return True
                if board[nx][ny] == Piece.NoPiece and (nx, ny) not in visited:
                    # add the neighboring point to the stack for further exploration
                    stack.append((nx, ny))
        # all empty spaces are fully enclosed
        return False  
    
    # method to capture pieces if possible
    def capture_pieces(self, board, last_move_x, last_move_y, player_color):
        # determen the opponent's pieces
        opponent_color = Piece.White if player_color == Piece.Black else Piece.Black
        # directions up, down, left, right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  

        # list to save all the captured pieces
        captured_groups = []

        # check adjacent opponent groups
        for dx, dy in directions:
            nx, ny = last_move_x + dx, last_move_y + dy
            if 0 <= nx < len(board) and 0 <= ny < len(board[0]) and board[nx][ny] == opponent_color:
                group = self.find_group(board, nx, ny, opponent_color)
                #print("Found group:" ,group)
                if self.is_group_fully_surrounded(board, group, player_color):
                    #print("Group is fully surrounded:" ,group)
                    captured_groups.extend(group)

        # Remove captured pieces
        for x, y in captured_groups:
            # check if there was only one piece captured
            if len(captured_groups) == 1:
                # check which color was the piece
                print("only one piece was captured added to its color list")
                if board[x][y] == Piece.Black:
                    # add the locations of the piece to the last moves
                    # to stop repeating moves
                    self.blackLastMoves.append([x,y])
                elif board[x][y] == Piece.White:
                    # add the locations of the piece to the last moves
                    # to stop repeating moves
                    self.whiteLastMoves.append([x,y])
            #remove the captured pieces from the board
            board[x][y] = Piece.NoPiece 
        # return the captured pieces 
        return captured_groups

    # method to check if the placed pieces causes a self capture
    def check_selfCapture(self, board, x, y, player_color):
        # determen the opponent's pieces color
        opponent_color = Piece.White if player_color == Piece.Black else Piece.Black

        # find the larger area connected to the placed piece (can include opponent pieces)
        larger_group = self.find_group(board, x, y, board[x][y])
        #print("Larger group found:",  larger_group)

        # check if the larger group is surrounded by the opponent
        if self.is_group_surrounded(board, larger_group, opponent_color):
            # check if the piece to capture is 
            if board[x][y] == player_color:
                #print(f"Debug: Opponent's piece at ({x}, {y}) is in a trap and will be captured immediately.")
                board[x][y] = Piece.NoPiece  # Remove the placed opponent piece immediately
                return -1  # Indicate a self-capture
            # Use the same logic as capture_pieces to clear the board
            for gx, gy in larger_group:
                board[gx][gy] = Piece.NoPiece  

            return larger_group 

        return []  # no pieces captured
    
    # method to check if a repeating move is made
    def same_move_check(self , x , y , color):
        # check which color 
        if color == Piece.Black:
            # check if the current move exist in the last capture of the same color
            for lastX , lastY in self.blackLastMoves:
                if lastX == x and lastY == y:
                    print("found repeating move for black" , x , y )
                    # repeating
                    return True
            print("clearing black" )
            #if not repeating clear the last move
            self.blackLastMoves.clear()

        if color == Piece.White:
            # check if the current move exist in the last capture of the same color
            for lastX , lastY in self.whiteLastMoves:
                if lastX == x and lastY == y:
                    print("found repeating move for black" , x , y )
                    # repeating
                    return True
            print("clearing white" )
            #if not repeating clear the last move
            self.whiteLastMoves.clear()
        # no reaptition 
        return False
    
    # method to clear the passes
    def clearPass(self):
        self.passes == 0

    # method to clear the past moves
    def clearMoves(self):
        self.blackLastMoves.clear()
        self.whiteLastMoves.clear()
    # method to pass the current turn
    def passTurn(self):
        self.passes +=1
        # if two passes has been made return true to end the game
        if self.passes == 2:
            return True
        # only one pass has been made continue the game
        return False