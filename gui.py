from tkinter import *
from tkinter import messagebox


turn = 0
def buttonClick(b):
    global turn
    """
    Triggered on button click - makeMove(self, player: str, posn: Posn):
    Should first check if move is valid - moveLegal(self, player: str, posn: Posn) -> bool:
    Right now will just change the text
    """
    if turn%2 == 0:
        b["text"] = "w"
    else:
        b["text"] = "b"
    turn += 1

def main():
    root = Tk()
    root.title('REVERSI')

    #buttons - will pass in board size 
    rows = 8
    cols = 8
    buttons = [[0 for x in range(rows)] for x in range(cols)]
    for row in range(rows):
        for col in range (cols):
            buttons[row][col] = Button(root, text=" ", font=("Helvetica", 20), height=2, width=4, command=lambda row=row, col=col: buttonClick(buttons[row][col]))
            buttons[row][col].grid(row = row, column = col)


    root.mainloop()

main()