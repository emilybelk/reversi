import mysql.connector
import argparse
import os
from datetime import datetime

from tkinter import *
from tkinter import messagebox
from game import Game
from board import Board, Posn, Status


turn = 0

#********* database ***********
# Loads data into the database
# returns connection to the database
def init():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root"
    )  
    mydb.autocommit = True
    mycursor = mydb.cursor()

    load_ddl_str = open("ddl.sql").read()
    load_ddl_data = load_ddl_str.split(';')

    for i in load_ddl_data:
        mycursor.execute(i)

    return mydb

class mainMenu:
    """
    Class for generating main menu UI
    """
    root: Tk


    def __init__(self):
        self.root = Tk()
        self.root.title("WELCOME TO REVERSI")
        signInLabel = Label(self.root, text = "Please Enter your Username and Password").grid(row = 0, column = 0)
        usernameLabel = Label(self.root, text = "Username").grid(row = 0, column = 1)
        username = StringVar()
        usernameEntry = Entry(self.root, textvariable = username).grid(row = 0, column = 2)
        passwordLabel = Label(self.root, text = "Password").grid(row = 1, column = 1)
        password = StringVar()
        passwordEntry = Entry(self.root, textvariable = password, show = '*').grid(row = 1, column = 2)

        #login button
        loginButton = Button(self.root, text="Login", command = lambda: self.validateLogin(username, password)).grid(row=4, column=0) 

    def validateLogin(self,username, password):
        print("username entered :", username.get())
        print("password entered :", password.get())
        self.root.destroy()


    def registerUser(mydb, username, password):
    # credit to https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-execute.html
        mycursor = mydb.cursor()
        mycursor.execute("USE reversi")
        insert_stmt = ("INSERT INTO user (username, password) VALUES (%s, %s)")
        data = (username, password)
        try: 
            mycursor.execute(insert_stmt, data)
            print("Updated table")
            print("{:<15}{:<15}".format("username", "password"))
            mycursor.execute("SELECT * FROM user")
            for x in mycursor:
                print("{:<15}{:<15}".format(x[0],x[1]))
        except mysql.connector.Error as err:
            print("Error: {}".format(err))


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


    def __init__(self, size: int):
        self.root = Tk()
        self.root.title("REVERSI")
        self.boardSize = size
        self.board = Board(self.boardSize)
        self.game = Game(self.board)
        self.whitePhoto = PhotoImage(file = r"C:\Users\jserp\Documents\GitHub\reversi\whiteCircle.png")
        self.blackPhoto = PhotoImage(file = r"C:\Users\jserp\Documents\GitHub\reversi\blackCircle.png")

        self.buttons = {Posn(n, m): Button(self.root, text=" ", font=("Helvetica", 20), \
                                    height=2, width=4, command=lambda n=n, m=m: \
                                    self.buttonClick(self.buttons[Posn(n, m)]))
                        for n in range(size) for m in range(size)}
        {self.buttons[Posn(n, m)].grid(row=n, column=m) for n in range(size) for m in range(size)}
        self.drawButtonValues()

    def drawButtonValues(self):
        for posn in self.board.board.keys():
            b = self.buttons[posn]
            val = self.board.board[posn].value
            if val == "w":
                b["image"] = self.whitePhoto
                b["height"] = 80
                b["width"] = 68
            elif val == "b":
                b["image"] = self.blackPhoto
                b["height"] = 80
                b["width"] = 68
            else:
                b["text"] = val
        self.highlightPossibleMoves()

    def highlightPossibleMoves(self):
        if turn%2 == 0:
            player = self.game.player1
        else:
            player = self.game.player2
        moves = self.game.movesAvail(player)
        for key in self.buttons:
            self.buttons[key]["bg"] = "grey"
        for move in moves:
            b = self.buttons[move]
            b["bg"] = "blue"

    def gameOver(self):
        self.root.withdraw() #this line will make the base window invisible
        go = Tk()
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
    


    def buttonClick(self, b: Button):
        global turn
        """
        Triggered on button click - makeMove(self, player: str, posn: Posn):
        Should first check if move is valid - moveLegal(self, player: str, posn: Posn) -> bool:
        Right now will just change the text
        """
        moveMade = False
        bPosn = [key for key, value in self.buttons.items() if value == b][0]
        if turn%2 == 0:
            moveMade = self.game.makeMove(self.game.player1, bPosn)
        else:
            moveMade = self.game.makeMove(self.game.player2, bPosn)
        if moveMade:
            turn += 1
        
        self.drawButtonValues()
        if self.game.endGame() == True:
            self.gameOver()

    

    def main(self):
        #buttons - will pass in board size
        rows = cols = self.boardSize    # could just pass boardsize for rows/cols, 
                                        # or rewrite generateButtons to accept one int
        self.root.mainloop()

'''
main = mainMenu()
main.main()
'''

gui = GUI(6)
gui.main()
