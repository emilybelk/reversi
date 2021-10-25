from enum import Enum

class Status(Enum):

    BLACK = 'b'
    WHITE = 'w'
    EMPTY = ' '


class Posn:
    """
    Class for a Position on the game board. 
    A Posn will be represented with nat n, nat m
    with both n and m being in the range(0, boardSize)
    - n: row value
    - m: col value
    """

    n: int
    m: int

    def __init__(self, n: int, m: int):
        self.n = n
        self.m = m

    def __eq__(self, obj) -> bool:
        return isinstance(obj, Posn) \
            and self.n == obj.n \
            and self.m == obj.m

    def __hash__(self):
        return hash((self.n, self.m))

    def add(self, posn: Posn) -> Posn:
        return Posn(self.n + posn.n, self.m + posn.m)


class Board:
    """
    Class for our game board. 
    - board: dict(Posn: Status) representing each position on the board and it's current status
    - size: nat that is one of 6, 8, 10 representing the size of the board 
    """

    board: dict()
    size: int

    def __init__(self, size):
        if size not in range(6, 11) or size % 2 != 0:
            raise ValueError("Board size must be either 6, 8, or 10")

        self.size = size

        self.board = {Posn(n, m): Status.EMPTY for n in range(size) for m in range(size)}
        mid_index = (size / 2) - 1
        self.board[Posn(mid_index, mid_index)] = Status.WHITE
        self.board[Posn(mid_index + 1, mid_index + 1)] = Status.WHITE
        self.board[Posn(mid_index, mid_index + 1)] = Status.BLACK
        self.board[Posn(mid_index + 1, mid_index)] = Status.BLACK


    def printBoard(self):
        print('\n'.join(''.join(self.board[Posn(n, m)].value for n in range(self.size)) for m in range(self.size)))


    def updatePosnStatus(self, posn: Posn, status: str):
        self.board[posn] = Status(status)
