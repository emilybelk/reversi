import mysql.connector
import argparse
import os
from datetime import datetime

from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from game import Game
from board import Board, Posn, Status
from database import init, registerUser, cleanup 




class mainMenu:
    """
    Class for generating main menu UI
    """
    root: Tk


    def __init__(self):
        self.root = Tk()
        self.root.eval('tk::PlaceWindow . center')
        self.root.configure(bg = 'lightblue')
        self.root.title("WELCOME TO REVERSI")
        self.root.geometry("400x200")
        signInLabel = Label(self.root, bg = 'lightblue', text = "Please Enter your Credentials", font=("Helvetica", 20)).grid(row = 0, column = 0, columnspan=2)
        spacer1 = Label(self.root, bg = 'lightblue', text = " ", font=("Helvetica", 10)).grid(row = 1, column = 0)
        usernameLabel = Label(self.root, bg = 'lightblue',text = "Username: ", font=("Helvetica", 12)).grid(sticky = "w", row = 2, column = 0)
        username = StringVar()
        usernameEntry = Entry(self.root, textvariable = username).grid(sticky = "e",row = 2, column = 0)
        passwordLabel = Label(self.root, bg = 'lightblue', text = "Password: ", font=("Helvetica", 12)).grid(sticky = "w",row = 3, column = 0)
        password = StringVar()
        passwordEntry = Entry(self.root, textvariable = password, show = '*').grid(sticky = "e",row = 3, column = 0)

        spacer2 = Label(self.root, bg = 'lightblue', text = " ", font=("Helvetica", 10)).grid(row = 4, column = 0)

        #Buttons
        loginButton = ttk.Button(self.root, text="Login", command = lambda: self.validateLogin(username, password)).grid(row=5, column=0) 
        registerButton = ttk.Button(self.root, text="Register", command = lambda: print("registered user")).grid(row = 5, column = 1)

        spacer3 = Label(self.root, bg = 'lightblue', text = " ", font=("Helvetica", 10)).grid(row = 6, column = 0)

    def validateLogin(self,username, password):
        print("username entered :", username.get())
        print("password entered :", password.get())
        self.root.destroy()
        sc = SelectGamemode()
        sc.main()

    def main(self):
        self.root.mainloop() 

class SelectGamemode:
    root: Tk
    def __init__(self):
        self.root = Tk()
        self.root.eval('tk::PlaceWindow . center')
        self.root.title("SELECT GAMEMODE")
        self.root.geometry("400x200")
        self.root.configure(bg = 'lightblue')
        choose = Label(self.root, bg = 'lightblue', text = "Choose Gamemode", font=("Helvetica", 20)).grid(sticky = "",row = 0, column = 1)
        spacer1 = Label(self.root, bg = 'lightblue', text = " ", font=("Helvetica", 50)).grid(row = 1, column = 1)
        localButton = ttk.Button(self.root, text="Local", command = lambda: self.launchLocal()).grid(sticky = "e",row=2, column=0) 
        onlineButton = ttk.Button(self.root, text="Online", command = lambda: print("Online Game")).grid(row = 2, column = 1)
        aiButton = ttk.Button(self.root, text="  AI  ", command = lambda: print("AI Game")).grid(sticky = "w",row = 2, column = 2)
        spacer2 = Label(self.root, bg = 'lightblue',text = " ", font=("Helvetica", 10)).grid(row = 3, column = 1)
    def launchLocal(self):
        self.root.destroy()
        local = localSettings()
        local.main()
        
    def main(self):
        self.root.mainloop()

class localSettings:
    root: Tk
    size: int
    def __init__(self):
        self.root = Tk()
        self.root.eval('tk::PlaceWindow . center')
        self.root.title("LOCAL SETTINGS")
        self.root.geometry("400x200")
        self.root.configure(bg = 'lightblue')
        self.size = 6
        hello = Label(self.root, bg = 'lightblue', text = "Choose Game Settings", font=("Helvetica", 20)).grid(sticky = "s",row = 0, column = 0)
        boardSizes = [
        "6",
        "8",
        "10"
        ] 
        boardSize = StringVar(self.root)
        spacer1 = Label(self.root, bg = 'lightblue', text = " ", font=("Helvetica", 50)).grid(row = 1, column = 1)
        sizes = Label(self.root, bg = 'lightblue', text = "Select Board Size: ", font=("Helvetica", 12)).grid(sticky = "w",row = 2, column = 0)
        w = ttk.OptionMenu(self.root, boardSize, boardSizes[0], *boardSizes).grid(sticky = "w", row = 2, column = 1)
        spacer1 = Label(self.root, bg = 'lightblue', text = " ", font=("Helvetica", 10)).grid(row = 3, column = 1)
        confirmButton = ttk.Button(self.root, text="Confirm", command = lambda: self.startGame(boardSize)).grid(sticky = "",row=4, column=1) 
    
    def startGame(self, selectedSize):
        self.root.destroy()
        self.size = int(selectedSize.get())
        gui = GUI(self.size)
        gui.main()

    def main(self):
        self.root.mainloop()


class GUI:
    """
    Class for generating gameplay UI
    """
    root: Tk
    boardSize: int
    board: Board
    game: Game
    buttons: dict()
    whitePhoto: PhotoImage
    blackPhoto: PhotoImage
    scoreLabel: Label
    p1ScoreLabel: Label
    p2ScoreLabel: Label
    moveLabel: Label


    def __init__(self, size: int):
        self.root = Tk()
        self.root.eval('tk::PlaceWindow . center')
        self.root.title("REVERSI")
        self.root.configure(bg = 'lightblue')
        #self.root.geometry("500x500")
        self.boardSize = size
        self.board = Board(self.boardSize)
        self.game = Game(self.board)
        self.whitePhoto = PhotoImage(file = r"C:\Users\jserp\Documents\GitHub\reversi\whiteCircle.png")
        self.blackPhoto = PhotoImage(file = r"C:\Users\jserp\Documents\GitHub\reversi\blackCircle.png")
        self.scoreLabel = Label(self.root, bg = "lightblue", text = "Current Score", font=("Helvetica", 20))
        self.scoreLabel.grid(sticky = "w", row = 0, column = self.boardSize+1)
        self.p1ScoreLabel = Label(self.root, bg = "lightblue", text = str(self.game.player1.getColor())+ ": Player 1: " + str(self.game.playerScore(self.game.player1)), font=("Helvetica", 16))
        self.p1ScoreLabel.grid(sticky = "nw", row = 1, column = self.boardSize+1)
        self.p2ScoreLabel = Label(self.root, bg = "lightblue", text = str(self.game.player2.getColor())+ ": Player 2: " + str(self.game.playerScore(self.game.player2)), font=("Helvetica", 16))
        self.p2ScoreLabel.grid(sticky = "w", row = 1, column = self.boardSize+1)
        self.moveLabel = Label(self.root, bg = "lightblue", text = "Current Move: " + str(self.game.currPlayer.getColor()), font=("Helvetica", 16))
        self.moveLabel.grid(sticky = "sw", row = 2, column = self.boardSize+1)

        self.buttons = {Posn(n, m): Button(self.root, text=" ", font=("Helvetica", 20), \
                                    height=2, width=4, command=lambda n=n, m=m: \
                                    self.buttonClick(self.buttons[Posn(n, m)]))
                        for n in range(size) for m in range(size)}
        {self.buttons[Posn(n, m)].grid(row=n, column=m) for n in range(size) for m in range(size)}
        self.drawButtonValues()
        #self.drawScore()

    def drawButtonValues(self):
        for posn in self.board.board.keys():
            b = self.buttons[posn]
            val = self.board.board[posn].value
            if val == "w":
                b["image"] = self.whitePhoto
                b["height"] = 82
                b["width"] = 68
            elif val == "b":
                b["image"] = self.blackPhoto
                b["height"] = 82
                b["width"] = 68
            else:
                b["text"] = val
        self.highlightPossibleMoves()

    def deactivateBoard(self):
        for posn in self.board.board.keys():
            b = self.buttons[posn]
            b["command"] = 0
            b['relief'] = 'sunken'
            b['bg'] = "grey"
    
    def drawScore(self):
        self.p1ScoreLabel.config(text = str(self.game.player1.getColor())+ ": Player 1: " + str(self.game.playerScore(self.game.player1)))
        self.p2ScoreLabel.config(text = str(self.game.player2.getColor())+ ": Player 2: " + str(self.game.playerScore(self.game.player2)))
        self.moveLabel.config(text = "Current Move: " + str(self.game.currPlayer.getColor()))
        '''
        self.scoreLabel = Label(self.root, bg = "lightblue", text = "Current Score", font=("Helvetica", 20)).grid(sticky = "w", row = 0, column = self.boardSize+1)
        self.p1ScoreLabel = Label(self.root, bg = "lightblue", text = str(self.game.player1.getColor())+ ": Player 1: " + str(self.game.playerScore(self.game.player1)), font=("Helvetica", 16)).grid(sticky = "nw", row = 1, column = self.boardSize+1)
        self.p2ScoreLabel = Label(self.root, bg = "lightblue", text = str(self.game.player2.getColor())+ ": Player 2: " + str(self.game.playerScore(self.game.player2)), font=("Helvetica", 16)).grid(sticky = "w", row = 1, column = self.boardSize+1)
        self.moveLabel = Label(self.root, bg = "lightblue", text = "Current Move: " + str(self.game.currPlayer.getColor()), font=("Helvetica", 16)).grid(sticky = "sw", row = 2, column = self.boardSize+1)
        '''

    def highlightPossibleMoves(self):
        moves = self.game.movesAvail(self.game.currPlayer)
        for key in self.buttons:
            self.buttons[key]["bg"] = "grey"
        for move in moves:
            b = self.buttons[move]
            b["bg"] = "blue"
    
    def gameOver(self):
        self.deactivateBoard()
        self.scoreLabel.config(text = "Final Score   ")
        self.moveLabel.config(text = "")
        #gameOver = Label(self.root, bg = "grey", fg = "red", text = "GAME OVER\n" + self.game.winner(), font=("Helvetica", 20)). \
        #    grid(sticky = "", row = int(self.boardSize/2)-1, column=int(self.boardSize/2)-2, columnspan=4, rowspan = 3)
        gameOver = Label(self.root,borderwidth=1, relief="solid", bg = "lightblue", fg = "black", text = "GAME OVER\n" + self.game.winner(), font=("Helvetica", 30)). \
            place(x = 68*(self.boardSize/2-2)+28, y = 82*self.boardSize/2-35)
        restartButton = ttk.Button(self.root, text="Play Again", command = lambda: self.newGame()).place(x = 68*(self.boardSize/2-1)+35, y = 82*(self.boardSize/2+2)-35) 
        
    def newGame(self):
        self.root.destroy()
        gui = GUI(self.boardSize)
        gui.main()
    '''
    def gameOver(self):
        self.deactivateBoard() #this line will make the base window invisible
        go = Tk()
        go.eval('tk::PlaceWindow . center')
        # following line makes the base window inactive
        go.grab_set()
        go.title("GAME OVER")
        winner = self.game.winner()
        whiteScore = self.game.playerScore(self.game.player1)
        blackScore = self.game.playerScore(self.game.player2)
        gameOver = Label(go, text = "GAME OVER", font=("Helvetica", 50))
        gameOver.pack()
        p1Score = Label(go, text = "Player 1 Score: " + str(whiteScore), font = ("Helvetica", 20))
        p1Score.pack()
        p2Score = Label(go, text = "Player 2 Score: " + str(blackScore), font = ("Helvetica", 20))
        p2Score.pack()
        winLabel = Label(go, text = winner, font = ("Helvetica", 20))
        winLabel.pack()
        go.mainloop()
    ''' 

    def buttonClick(self, b: Button):

        """
        Triggered on button click - makeMove(self, player: str, posn: Posn):
        Should first check if move is valid - moveLegal(self, player: str, posn: Posn) -> bool:
        Right now will just change the text
        """
        moveMade = False
        bPosn = [key for key, value in self.buttons.items() if value == b][0]
        moveMade = self.game.makeMove(self.game.currPlayer, bPosn)
        if moveMade:
            self.game.nextPlayer()
        
        self.drawButtonValues()
        self.drawScore()
        if self.game.endGame() == True:
            self.gameOver()
        else:
            if(self.game.noMovesAvail(self.game.currPlayer) == True):
                self.game.nextPlayer()
                self.drawButtonValues()
                self.drawScore()

    

    def main(self):
        #buttons - will pass in board size
        rows = cols = self.boardSize    # could just pass boardsize for rows/cols, 
                                        # or rewrite generateButtons to accept one int
        self.root.mainloop()


main = mainMenu()
main.main()



