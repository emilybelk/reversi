from tkinter import *
from tkinter import messagebox

root = TK()
root.title('REVERSI')

turn = 0

def buttonClick(b):
    """
    Triggered on button click - makeMove(self, player: str, posn: Posn):
    Should first check if move is valid - moveLegal(self, player: str, posn: Posn) -> bool:
    Right now will just change the text
    """
    if turn%2 = 0:
        b.text = "w"
    else:
        b.text = "b"



#buttons - will pass in board size 
buttons=dict()
rows = 8
cols = 8
for row in range(rows):
    for col in range (cols):
        buttons[row][col] = Button(root, text=" ", font=("Helvetica", 20), height=3, width=6, command=lambda: buttonClick(buttons[row][col]))
        buttons[row][col].grid(row = row, column = col)


root.mainloop()