from board import Board, Posn, Status

"""
TODO:
WHILE LOOP:
- end game conditions
    - no spaces on board
    - no active moves for at least one player

GAME:
- score
    - count white pieces
    - count black pieces
- make move
    - check legal
    - update pieces 

- while loop to play game, ideally not in this class

IM THINKING: we dont need players stored in board we can pass them in 

- gui
"""

class Game:
    """
    Class for a single reversi game. 
    A game will have a board. 
    https://stackoverflow.com/questions/40740615/check-moves-in-othello-reversi-python-3
    DIRS stores all the possible directions we could go in. 
    """

    DIRS = [Posn(n, m) for n, m in [(0, -1),  (1, -1), 
                                    (1,  0),  (1,  1),  
                                    (0,  1),  (-1, 1),  
                                    (-1, 0),  (-1, -1)]]

    board: Board


    def __init__(self, board: Board):
        self.board = board


    def playerPieces(self, player: str) -> set():
        """
        Return all the pieces that belong to the current player.
        """

        return {k for k, v in self.board if v.value == player}


    def playerScore(self, player: str) -> int:
        """
        Return the given player's score.
        """

        return len(self.playerPieces())


    def movesAvailHelper(self, piece: Posn) -> set():
        """
        Return a set of all the moves available to be made because of this piece. 
        """

        possible_moves = set()
        for direction in self.DIRS:
            new_posn = piece + direction
            while board[new_posn].value != board[piece].value:
                if board[new_posn].value == ' ':
                    possible_moves.add(new_posn)
                    break
                else:
                    new_posn += direction

        return possible_moves


    def movesAvail(self, player: str) -> set():
        """
        Returns a set of Posn's where the given player could make a move. 
        A move is available if there is a free space that is in some way connected
        (horizontally, vertically, diagonally) to another one of this player's pieces. 
        """

        pieces = self.playerPieces(player)
        moves = set()
        for piece in pieces:
            moves = moves | self.movesAvailHelper(piece)
        return moves


    def availMove(self, player: str) -> bool:
        """
        Return if there are any available moves for this player. 
        """

        return len(movesAvail) > 0

    
    def moveLegal(self, player: str, posn: Posn) -> bool:
        """
        Determine if the given posn is available and legal for the given
        player to take. 
        """

        return self.board[posn].value == ' ' \
               and posn in self.movesAvail(player) 


    def affectedPieces(self, player: str, posn: Posn) -> set():
        """
        TODO
        Return a set containing all the affected pieces this player owns 
        so that we can fill them in. 
        """

        affected = set()
        for direction in self.DIRS:
            new_posns = set()
            new_posn = piece + direction
            while board[new_posn].value != board[posn].value and board[new_posn].value != ' ':
                new_posns.add(new_posn)
                new_posn += direction
                if board[new_posn].value == board[posn].value:
                    new_posns.add(new_posn)
                    affected = affected | new_posns

        return affected


    def makeMove(self, player: str, posn: Posn):
        """
        Occupy the given posn and all affected posn's in the player's favor if allowed. 
        """

        if self.moveLegal(player, posn):
            self.board[posn] = player
            for piece in self.affectedPieces(player, posn):
                self.board[piece] = player


    def noMovesAvail(self) -> bool:
        """
        Return if no moves are available left in the game for either player. 
        """

        return min(len(self.movesAvail('b')) len(self.movesAvail('w'))) == 0


    def boardFull(self) -> bool:
        """
        Return if no spaces left empty on the board. 
        """
        
        for posn, status in self.board.items():
            if status.value == ' ':
                return False
        
        return True


    def endGame(self) -> bool:
        """
        Return if game is over. 
        """

        return self.boardFull() or self.noMovesAvail()
