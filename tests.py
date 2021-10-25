import unittest
from board import Board, Posn, Status

class TestReversi(unittest.TestCase):
    board = Board(8)

    def testBoard(self):
        self.board.printBoard()
        self.board.updatePosnStatus(Posn(2, 2), "w")
        self.board.printBoard()


if __name__ == '__main__':
    unittest.main()