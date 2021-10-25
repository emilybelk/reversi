from board import Board, Posn, Status

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
    p1: str
    p2: str


    def __init__(self, board: Board):
        self.board = board
        self.p1 = "b"
        self.p2 = "w"


    def playerPieces(self, player: str) -> set():
        """
        Return all the pieces that belong to the current player.
        """

        return {k for k, v in self.board if v.value == player}


    def movesAvailHelper(piece: Posn) -> set():
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


    def movesAvail(player: str) -> set():
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


    def availMove(player: str) -> bool:
        """
        Return if there are any available moves for this player. 
        """

        return len(movesAvail) > 0

