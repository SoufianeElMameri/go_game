import random
from player import Player
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
        # Randomly assign Black and White pieces
        pieces = [Piece.Black, Piece.White]
        random.shuffle(pieces)  # Shuffle the pieces list to randomize assignment
        
        # Assign pieces to players
        self.player1.set_piece(pieces[0])
        self.player2.set_piece(pieces[1])

        # Print out the assigned pieces for debugging
        if self.player1.get_piece() == Piece.Black:
            print(f"{self.player1.get_name()} is assigned 'Black'")
            print(f"{self.player2.get_name()} is assigned 'White'")
            self.currentPlayer = self.player1
        else:
            print(f"{self.player2.get_name()} is assigned 'Black'")
            print(f"{self.player1.get_name()} is assigned 'White'")
            self.currentPlayer = self.player2
    # methd to return the currentPlayer's turn
    def getCurrentPlayer(self):
        return self.currentPlayer
    
    # method to switch the current player's turn
    def switchTurn(self):
        if self.currentPlayer == self.player1:
            self.currentPlayer = self.player2
        else:
            self.currentPlayer = self.player1
    
    def find_group(self, board, x, y, player_color):
        """Find all connected pieces of the same color using flood-fill."""
        stack = [(x, y)]
        group = []
        visited = set()
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right

        while stack:
            cx, cy = stack.pop()
            if (cx, cy) in visited:
                continue
            visited.add((cx, cy))
            group.append((cx, cy))

            for dx, dy in directions:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < len(board) and 0 <= ny < len(board[0]) and board[nx][ny] == player_color:
                    stack.append((nx, ny))
        return group

    def is_group_surrounded(self, board, group, opponent_color):
        """Check if a group of pieces is completely surrounded."""
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        group_set = set(group)  # Convert group to a set for fast lookups

        for x, y in group:
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                # Check if neighbor is out of bounds
                if not (0 <= nx < len(board) and 0 <= ny < len(board[0])):
                    # If out-of-bounds, treat the border as a valid surrounding
                    continue
                # Skip neighbors that are part of the group
                if (nx, ny) in group_set:
                    continue
                # Check if neighbor is not the opponent's piece
                if board[nx][ny] != opponent_color:
                    return False
        return True

    def group_has_internal_space(self, board, group):
        """Check if the group has any internal empty spaces."""
        visited = set()
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        # Flood-fill around the group to find internal spaces
        for x, y in group:
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(board) and 0 <= ny < len(board[0]) and board[nx][ny] == Piece.NoPiece:
                    # Check if the empty space connects to the outside
                    if self.is_empty_space_open(board, nx, ny):
                        return True  # There's an open space connected to the outside
        return False
    def is_group_fully_surrounded(self, board, group, opponent_color):
        """Check if a group is fully surrounded without internal space."""
        # Verify the group is surrounded
        if not self.is_group_surrounded(board, group, opponent_color):
            return False

        # Check for internal spaces
        if self.group_has_internal_space(board, group):
            return False

        return True
    def is_empty_space_open(self, board, x, y):
        """Flood-fill to determine if an empty space connects to the board boundary."""
        stack = [(x, y)]
        visited = set()
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while stack:
            cx, cy = stack.pop()
            if (cx, cy) in visited:
                continue
            visited.add((cx, cy))

            for dx, dy in directions:
                nx, ny = cx + dx, cy + dy
                if not (0 <= nx < len(board) and 0 <= ny < len(board[0])):  # Reached board boundary
                    return True
                if board[nx][ny] == Piece.NoPiece and (nx, ny) not in visited:
                    stack.append((nx, ny))

        return False  # Empty space is fully enclosed
    def capture_pieces(self, board, last_move_x, last_move_y, player_color):
        """Find and capture all opponent groups surrounded after the last move."""
        opponent_color = Piece.White if player_color == Piece.Black else Piece.Black
        # up, down, left, right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  
        captured_groups = []

        # Check adjacent opponent groups
        for dx, dy in directions:
            nx, ny = last_move_x + dx, last_move_y + dy
            if 0 <= nx < len(board) and 0 <= ny < len(board[0]) and board[nx][ny] == opponent_color:
                group = self.find_group(board, nx, ny, opponent_color)
                #print(f"Debug: Found group: {group}")
                if self.is_group_fully_surrounded(board, group, player_color):
                    #print(f"Debug: Group is fully surrounded: {group}")
                    captured_groups.extend(group)

        # Remove captured pieces
        for x, y in captured_groups:
            if len(captured_groups) == 1:
                print("only one piece was captured added to its color list")
                if board[x][y] == Piece.Black:
                    self.blackLastMoves.append([x,y])
                elif board[x][y] == Piece.White:
                    self.whiteLastMoves.append([x,y])
            #print(f"Debug: Capturing piece at ({x}, {y})")
            board[x][y] = Piece.NoPiece  # Clear the captured pieces
        #print(f"Debug: Total captured groups: {captured_groups}")
        return captured_groups

    def check_selfCapture(self, board, x, y, player_color):
        """
        Check if the newly placed piece completes a larger surround and results in a capture.
        If the piece placed is an opponent's piece in a trapped space, capture it immediately.
        """
        opponent_color = Piece.White if player_color == Piece.Black else Piece.Black

        # Find the larger area connected to the placed piece (can include opponent pieces)
        larger_group = self.find_group(board, x, y, board[x][y])
        #print(f"Debug: Larger group found: {larger_group}")

        # Otherwise, check if the larger group is surrounded by the opponent
        if self.is_group_surrounded(board, larger_group, opponent_color):
            #print(f"Debug: Larger group is surrounded and will be captured: {larger_group}")

            if board[x][y] == player_color:
                #print(f"Debug: Opponent's piece at ({x}, {y}) is in a trap and will be captured immediately.")
                board[x][y] = Piece.NoPiece  # Remove the placed opponent piece immediately
                return -1  # Indicate a self-capture
            # Use the same logic as capture_pieces to clear the board
            for gx, gy in larger_group:
                board[gx][gy] = Piece.NoPiece  # Clear the captured pieces

            return larger_group  # Return the list of captured pieces

        #print(f"Debug: Larger group is not surrounded.")
        return []  # No pieces captured
    
    def same_move_check(self , x , y , color):
        if color == Piece.Black:
            for lastX , lastY in self.blackLastMoves:
                if lastX == x and lastY == y:
                    print("found repeating move for black" , x , y )
                    return True
            print("clearing black" )
            self.blackLastMoves.clear()

        if color == Piece.White:
            for lastX , lastY in self.whiteLastMoves:
                if lastX == x and lastY == y:
                    print("found repeating move for black" , x , y )
                    return True
            print("clearing white" )
            self.whiteLastMoves.clear()
        
        return False
    
    def clearPass(self):
        self.passes == 0
    def clearMoves(self):
        self.blackLastMoves.clear()
        self.whiteLastMoves.clear()
    def passTurn(self):
        self.passes +=1
        if self.passes == 2:
            return True
        return False