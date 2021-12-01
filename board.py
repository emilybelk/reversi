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
    - weight: used for AI, weighted value for the specific posn on the board
    """

    n: int
    m: int
    weight: int

    def __init__(self, n: int, m: int):
        self.n = n
        self.m = m
        self.weight = 0

    def __eq__(self, obj) -> bool:
        return isinstance(obj, Posn) \
            and self.n == obj.n \
            and self.m == obj.m

    def __hash__(self):
        return hash((self.n, self.m))

    def add(self, posn):
        return Posn(self.n + posn.n, self.m + posn.m)

    def setWeight(self, w):
        self.weight = w

    def getWeight(self):
        return self.weight


class Board:
    """
    Class for our game board. 
    - board: dict(Posn: Status) representing each position on the board and it's current status
    - size: nat that is one of 6, 8, 10 representing the size of the board 
    """

    DIRS = [Posn(n, m) for n, m in [(0, -1),  (1, -1), 
                                    (1,  0),  (1,  1),  
                                    (0,  1),  (-1, 1),  
                                    (-1, 0),  (-1, -1)]]

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

        self.setWeights()


    def printBoard(self):
        print('\n'.join(''.join(self.board[Posn(n, m)].value for n in range(self.size)) for m in range(self.size)))

    def printBoardWeights(self):
        for n in range(self.size):
            for m in range(self.size):
                for posn in self.board.keys():
                    if (posn.n == n and posn.m == m):
                        print(posn.getWeight(), end=' ')
            print('')

    def updatePosnStatus(self, posn: Posn, status: str):
        self.board[posn] = Status(status)

    def isSpaceLegal(self, posn: Posn):
        if posn in self.board.keys():
            return True
        else:
            return False

    def isCornerSpace(self, posn: Posn):
        """
        Funtion to determine whether a space is a corner, used for weighting for AI algorithm
        Return true if coordinate n is 0 or max, and m is 0 or max
        """
        if (posn.n == 0 or posn.n==self.size-1) and (posn.m ==0 or posn.m==self.size-1):
            return True
        else:
            return False

    def isCornerAdjacent(self, posn: Posn):
        """
        Function to determine whether a space is corner adjacent, used for weighting in AI algo
        """
        for direction in self.DIRS:
            new_posn = posn.add(direction)
            if(self.isSpaceLegal(new_posn)):
                if(self.isCornerSpace(new_posn)):
                    return True
                else:
                    continue
            else:
                continue
        return False
    
    def isCornerAdjacentAdjacent(self, posn: Posn):
        """
        Funciton to determine if a space is next to the corner adjacent spaces, but not corners
        These will have higher weights than others
        """
        for direction in self.DIRS:
            new_posn = posn.add(direction)
            if(self.isSpaceLegal(new_posn)):
                if(self.isCornerSpace(new_posn)):
                    return False
                else:
                    if(self.isCornerAdjacent(new_posn)):
                        return True
                    else:
                        continue
            else:
                continue
        return False

    def isEdge(self, posn:Posn):
        """
        Function to deterimine whether a space is an edge, but not a corner, or corner adjacent
        These will have higher weights than others
        """
        if(self.isCornerSpace(posn) or self.isCornerAdjacent(posn)):
            return False
        else:
            for direction in self.DIRS:
                new_posn = posn.add(direction)
                if(self.isSpaceLegal(new_posn)): # need to make sure the adjacent space is outside the grid
                    continue
                else:
                    return True
            return False



    def setWeights(self):
        for posn in self.board.keys():
            if self.isCornerSpace(posn):
                posn.setWeight(120)
            elif(self.isCornerAdjacent(posn)):
                posn.setWeight(-50)
            elif(self.isCornerAdjacentAdjacent(posn) and self.isEdge(posn)):
                posn.setWeight(20)
            elif(self.isEdge(posn)):
                posn.setWeight(10)
            else:
                posn.setWeight(-5)
            