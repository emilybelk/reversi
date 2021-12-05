import unittest
from board import Board, Posn, Status

class TestReversi(unittest.TestCase):
    board = Board(8)

    def testBoard(self):
        self.board.print_board()
        self.board.update_posn_status(Posn(2, 2), "w")
        self.board.print_board()


if __name__ == '__main__':
    unittest.main()