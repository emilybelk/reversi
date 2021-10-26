from tkinter import *
from tkinter import messagebox
from game import Game
from board import Board, Posn, Status

turn = 0
class GUI:
    """
    Class for generating User Interface 
    """
    root: Tk
    boardSize: int
    board: Board
    game: Game
    buttons: dict()


    def __init__(self, size:int):
        self.root = Tk()
        self.root.title("REVERSI")
        self.boardSize = size
        self.board = Board(self.boardSize)
        self.game = Game(self.board)
        self.buttons = {Posn(n, m): Button(self.root, text=" ", font=("Helvetica", 20), \
                                    height=2, width=4, command=lambda n=n, m=m: \
                                    self.buttonClick(self.buttons[Posn(n, m)]))
                        for n in range(size) for m in range(size)}
        {self.buttons[Posn(n, m)].grid(row=n, column=m) for n in range(size) for m in range(size)}
        self.drawButtonValues()

    def drawButtonValues(self):
        for posn in self.board.board.keys():
            b = self.buttons[posn]
            b["text"] = self.board.board[posn].value
        #[lambda posn=(self.buttons[posn])["text"]:(self.board.board[posn]).value for posn in (self.board).board.keys()]

    def buttonClick(self, b: Button):
        global turn
        """
        Triggered on button click - makeMove(self, player: str, posn: Posn):
        Should first check if move is valid - moveLegal(self, player: str, posn: Posn) -> bool:
        Right now will just change the text
        
        if turn%2 == 0:
            b["text"] = "w"
        else:
            b["text"] = "b"
        turn += 1
        """
        self.drawButtonValues()
    

    def main(self):
        #buttons - will pass in board size
        rows = cols = self.boardSize    # could just pass boardsize for rows/cols, 
                                        # or rewrite generateButtons to accept one int
        self.root.mainloop()

gui = GUI(8)
gui.main()