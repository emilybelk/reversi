import mysql.connector
import argparse
import os
from datetime import datetime

from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from game import AIGame, Game
from board import Board, Posn, Status
import database as db
import threading
import time
import PIL.Image
import PIL.ImageTk
import hashlib
from server import *
from client import Client
from elo import elo_display

class LoginScreen:
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
        loginButton = ttk.Button(self.root, text="Login", command = lambda: self.validate_login(username, password)).grid(sticky = 's', row=5, column=0) 
        registerButton = ttk.Button(self.root, text="Register", command = lambda: self.register_user(username, password)).grid(sticky = 's', row = 5, column = 1)

        guestButton = ttk.Button(self.root, text="Continue as Guest", command = lambda: self.play_as_guest()).grid(sticky = 's', row = 6, column = 0)


        spacer3 = Label(self.root, bg = 'lightblue', text = " ", font=("Helvetica", 10)).grid(row = 7, column = 0)

    def validate_login(self,username, password):
        username = username.get()
        print("username entered: " +  username)       
        password = password.get()
        print("password entered: " + password)
        # Hash and encode the password entered by the user
        userPasswordHashed = hashlib.sha256(password.encode())
        password = userPasswordHashed.hexdigest()
        val = db.login_user(username, password)
        if val:
            self.root.destroy()
            sc = SelectGamemode()
            sc.main()
        else:
            errorLabel = Label(self.root, bg = 'lightblue', fg = 'red', text = "Login Failed: Check Credentials ", font=("Helvetica", 10)).grid(sticky = "w",row = 4, column = 0, columnspan = 2)

    def register_user(self, username, password):
        username = username.get()
        print("username entered: " + username)       
        password = password.get()
        print("password entered: " + password)
        # Hash and encode the password entered by the user
        userPasswordHashed = hashlib.sha256(password.encode())
        password = userPasswordHashed.hexdigest()
        val = db.register_user(username, password)
        if val:
            self.root.destroy()
            sc = SelectGamemode()
            sc.main()
        else:
            errorLabel = Label(self.root, bg = 'lightblue', fg = 'red', text = "Account already exists.", font=("Helvetica", 10)).grid(sticky = "w",row = 4, column = 0, columnspan = 2)

    def play_as_guest(self):
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
        localButton = ttk.Button(self.root, text="Local", command = lambda: self.launch_local()).grid(sticky = "e",row=2, column=0) 
        onlineButton = ttk.Button(self.root, text="Online", command = lambda: self.launch_online()).grid(row = 2, column = 1)
        aiButton = ttk.Button(self.root, text="  AI  ", command = lambda: self.launch_AI()).grid(sticky = "w",row = 2, column = 2)
        lbButton = ttk.Button(self.root, text="Leaderboard", command = lambda: self.launch_leaderboard()).grid(sticky = "w",row = 1, column = 0)
        spacer2 = Label(self.root, bg = 'lightblue',text = " ", font=("Helvetica", 10)).grid(row = 3, column = 1)
    def launch_local(self):
        self.root.destroy()
        local = localSettings()
        local.main()
    def launch_AI(self):
        self.root.destroy()
        AI = AISettings()
        AI.main()    
    def launch_online(self):
        self.root.destroy()
        OL = onlineLobby()
        OL.main()
    def launch_leaderboard(self):
        LB = Leaderboard()
        LB.main()
        
    def main(self):
        self.root.mainloop()

class Leaderboard:
    root:Tk
    
    def __init__(self):
        self.root = Tk()
        self.root.eval('tk::PlaceWindow . center')
        self.root.title("LEADERBOARD")

        self.root.configure(bg = 'lightblue')
        hello = Label(self.root, bg = 'lightblue', text = "Leaderboard", font=("Helvetica", 20)).grid(sticky = "s",row = 0, column = 0)
        list = elo_display()
        table = Label(self.root, text = "Position     User     ELO").grid(sticky = "w",row = 1, column = 0)
        r1= Label(self.root, text="1:      " + str(list[0][0]) + "    " + str(list[0][1])).grid(sticky = "w",row = 2, column = 0)
        r2= Label(self.root, text="2:      " + str(list[1][0]) + "    " + str(list[1][1])).grid(sticky = "w",row = 3, column = 0)
        r3= Label(self.root, text="3:      " + str(list[2][0]) + "    " + str(list[2][1])).grid(sticky = "w",row = 4, column = 0)
        r4= Label(self.root, text="4:      " + str(list[3][0]) + "    " + str(list[3][1])).grid(sticky = "w",row = 5, column = 0)
        r5= Label(self.root, text="5:      " + str(list[4][0]) + "    " + str(list[4][1])).grid(sticky = "w",row = 6, column = 0)
        r6= Label(self.root, text="6:      " + str(list[5][0]) + "    " + str(list[5][1])).grid(sticky = "w",row = 7, column = 0)
        r7= Label(self.root, text="7:      " + str(list[6][0]) + "    " + str(list[6][1])).grid(sticky = "w",row = 8, column = 0)
        r8= Label(self.root, text="8:      " + str(list[7][0]) + "    " + str(list[7][1])).grid(sticky = "w",row = 9, column = 0)
        r9= Label(self.root, text="9:      " + str(list[8][0]) + "    " + str(list[8][1])).grid(sticky = "w",row = 10, column = 0)
        r10= Label(self.root,text="10:     " + str(list[9][0]) + "    " + str(list[9][1])).grid(sticky = "w",row = 11, column = 0)


    def main(self):
        self.root.mainloop()

class onlineLobby:
    root: Tk
    client: Client
    start_port: int
    def __init__(self):
        self.root = Tk()
        self.root.eval('tk::PlaceWindow . center')
        self.root.title("LOCAL SETTINGS")
        self.root.geometry("400x200")
        self.root.configure(bg = 'lightblue')
        hello = Label(self.root, bg = 'lightblue', text = "Joining Game", font=("Helvetica", 20)).grid(sticky = "s",row = 0, column = 0)
        self.client = Client(45678, '127.0.0.1')
        self.start_port = 45678
        #self.checkForGame()
        

    def checkForGame(self):
        playerNum, new_port = self.client.wait_for_game()
        #start = self.client.wait_for_start(new_port)
        self.root.destroy()
        gui = OnlineGUI(self.client, playerNum)
        gui.main()

    

    def main(self):
        self.root.after(20, self.checkForGame)
        self.root.mainloop()
        

class localSettings:
    root: Tk
    size: int
    colors: str
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
        boardColors = [
        "white/black",
        "blue/orange",
        "red/green"
        ]
        boardSize = StringVar(self.root)
        color = StringVar(self.root)
        spacer1 = Label(self.root, bg = 'lightblue', text = " ", font=("Helvetica", 50)).grid(row = 1, column = 1)
        sizes = Label(self.root, bg = 'lightblue', text = "Select Board Size: ", font=("Helvetica", 12)).grid(sticky = "w",row = 2, column = 0)
        w = ttk.OptionMenu(self.root, boardSize, boardSizes[0], *boardSizes).grid(sticky = "w", row = 2, column = 1)
        #spacer1 = Label(self.root, bg = 'lightblue', text = " ", font=("Helvetica", 10)).grid(row = 3, column = 1)
        colors = Label(self.root, bg = 'lightblue', text = "Select Board Colors: ", font=("Helvetica", 12)).grid(sticky = "w",row = 3, column = 0)
        c = ttk.OptionMenu(self.root, color, boardColors[0], *boardColors).grid(sticky = "w", row = 3, column = 1)
        confirmButton = ttk.Button(self.root, text="Confirm", command = lambda: self.start_game(boardSize, color)).grid(sticky = "",row=4, column=1)

    def start_game(self, selectedSize, selectedColors):
            self.root.destroy()
            self.size = int(selectedSize.get())
            self.colors = selectedColors.get()
            gui = GUI(self.size, self.colors)
            gui.main()

    def main(self):
        self.root.mainloop()

class AISettings:
    root: Tk
    size: int
    difficulty: int
    colors: str
    def __init__(self):
        self.root = Tk()
        self.root.eval('tk::PlaceWindow . center')
        self.root.title("AI SETTINGS")
        self.root.geometry("400x200")
        self.root.configure(bg = 'lightblue')
        self.size = 6
        hello = Label(self.root, bg = 'lightblue', text = "Choose Game Settings", font=("Helvetica", 20)).grid(sticky = "s",row = 0, column = 0)
        boardSizes = [
        "6",
        "8",
        "10"
        ]
        dif = [
        "Easy",
        "Medium",
        "Hard"
        ]  
        boardColors = [
        "white/black",
        "blue/orange",
        "red/green"
        ]
        
        boardSize = StringVar(self.root)
        DiffLevel = StringVar(self.root)
        color = StringVar(self.root)
        spacer1 = Label(self.root, bg = 'lightblue', text = " ", font=("Helvetica", 20)).grid(row = 1, column = 1)
        sizes = Label(self.root, bg = 'lightblue', text = "Select Board Size: ", font=("Helvetica", 12)).grid(sticky = "w",row = 2, column = 0)
        w = ttk.OptionMenu(self.root, boardSize, boardSizes[0], *boardSizes).grid(sticky = "w", row = 2, column = 1)
        levels = Label(self.root, bg = 'lightblue', text = "Select AI difficulty: ", font=("Helvetica", 12)).grid(sticky = "w",row = 3, column = 0)
        y = ttk.OptionMenu(self.root, DiffLevel, dif[0], *dif).grid(sticky = "w", row = 3, column = 1)
        colors = Label(self.root, bg = 'lightblue', text = "Select Board Colors: ", font=("Helvetica", 12)).grid(sticky = "w",row = 4, column = 0)
        c = ttk.OptionMenu(self.root, color, boardColors[0], *boardColors).grid(sticky = "w", row = 4, column = 1)
        #spacer2 = Label(self.root, bg = 'lightblue', text = " ", font=("Helvetica", 10)).grid(row = 4, column = 1)
        confirmButton = ttk.Button(self.root, text="Confirm", command = lambda: self.start_AI_game(boardSize, DiffLevel, color)).grid(sticky = "",row=5, column=1)
    

    def start_AI_game(self, selectedSize, selectedDiff, selectedColors):
        self.root.destroy()
        self.size = int(selectedSize.get())
        diff = selectedDiff.get()
        self.colors = selectedColors.get()
        switcher = {
        "Easy": 1,
        "Medium": 2,
        "Hard": 3,
        }
        self.difficulty = switcher.get(diff) 
        AIgui = AIGUI(self.size, self.difficulty, self.colors)
        AIgui.main()

    def main(self):
        self.root.mainloop()


### need to make board smaller for size 10 games

class GUI:
    """
    Class for generating gameplay UI
    """
    root: Tk
    boardSize: int
    board: Board
    game: Game
    buttons: dict()
    p1Photo: PhotoImage
    p2Photo: PhotoImage
    scoreLabel: Label
    p1ScoreLabel: Label
    p2ScoreLabel: Label
    moveLabel: Label
    colors: str


    def __init__(self, size: int, col: str):
        self.root = Tk()
        self.root.eval('tk::PlaceWindow . center')
        self.root.title("REVERSI")
        self.root.configure(bg = 'lightblue')
        #self.root.geometry("500x500")
        self.boardSize = size
        self.colors = col
        self.board = Board(self.boardSize)
        self.game = Game(self.board)
        #self.whitePhoto = PhotoImage(file = r"C:\Users\jserp\Documents\GitHub\reversi\whiteCircle.png")
        #self.blackPhoto = PhotoImage(file = r"C:\Users\jserp\Documents\GitHub\reversi\blackCircle.png")
        boardColors = [
        "white/black",
        "blue/orange",
        "red/green"
        ]
        if self.colors == "white/black":
            self.p1Photo = PIL.ImageTk.PhotoImage(PIL.Image.open('whiteCircle.png').convert('RGBA'))
            self.p2Photo = PIL.ImageTk.PhotoImage(PIL.Image.open('blackCircle.png').convert('RGBA'))
        elif self.colors == "blue/orange":
            self.p1Photo = PIL.ImageTk.PhotoImage(PIL.Image.open('blueCircle.png').convert('RGBA'))
            self.p2Photo = PIL.ImageTk.PhotoImage(PIL.Image.open('orangeCircle.png').convert('RGBA'))
        else:
            self.p1Photo = PIL.ImageTk.PhotoImage(PIL.Image.open('redCircle.png').convert('RGBA'))
            self.p2Photo = PIL.ImageTk.PhotoImage(PIL.Image.open('greenCircle.png').convert('RGBA'))
        self.scoreLabel = Label(self.root, bg = "lightblue", text = "Current Score", font=("Helvetica", 20))
        self.scoreLabel.grid(sticky = "w", row = 0, column = self.boardSize+1)
        self.p1ScoreLabel = Label(self.root, bg = "lightblue", text = str(self.game.player1.get_color())+ ": Player 1: " + str(self.game.player_score(self.game.player1)), font=("Helvetica", 16))
        self.p1ScoreLabel.grid(sticky = "nw", row = 1, column = self.boardSize+1)
        self.p2ScoreLabel = Label(self.root, bg = "lightblue", text = str(self.game.player2.get_color())+ ": Player 2: " + str(self.game.player_score(self.game.player2)), font=("Helvetica", 16))
        self.p2ScoreLabel.grid(sticky = "w", row = 1, column = self.boardSize+1)
        self.moveLabel = Label(self.root, bg = "lightblue", text = "Current Move: " + str(self.game.currPlayer.get_color()), font=("Helvetica", 16))
        self.moveLabel.grid(sticky = "sw", row = 2, column = self.boardSize+1)

        self.buttons = {Posn(n, m): Button(self.root, text=" ", font=("Helvetica", 20), \
                                    height=2, width=4, command=lambda n=n, m=m: \
                                    self.button_click(self.buttons[Posn(n, m)]))
                        for n in range(size) for m in range(size)}
        {self.buttons[Posn(n, m)].grid(row=n, column=m) for n in range(size) for m in range(size)}
        self.draw_button_values()
        #self.drawScore()

    def draw_button_values(self):
        for posn in self.board.board.keys():
            b = self.buttons[posn]
            val = self.board.board[posn].value
            if val == "w":
                b["image"] = self.p1Photo
                b["height"] = 82
                b["width"] = 68
            elif val == "b":
                b["image"] = self.p2Photo
                b["height"] = 82
                b["width"] = 68
            else:
                b["text"] = val
        self.highlight_possible_moves()

    def deactivate_board(self):
        for posn in self.board.board.keys():
            b = self.buttons[posn]
            b["command"] = 0
            b['relief'] = 'sunken'
            b['bg'] = "grey"
    
    def draw_score(self):
        self.p1ScoreLabel.config(text = str(self.game.player1.get_color())+ ": Player 1: " + str(self.game.player_score(self.game.player1)))
        self.p2ScoreLabel.config(text = str(self.game.player2.get_color())+ ": Player 2: " + str(self.game.player_score(self.game.player2)))
        self.moveLabel.config(text = "Current Move: " + str(self.game.currPlayer.get_color()))
        '''
        self.scoreLabel = Label(self.root, bg = "lightblue", text = "Current Score", font=("Helvetica", 20)).grid(sticky = "w", row = 0, column = self.boardSize+1)
        self.p1ScoreLabel = Label(self.root, bg = "lightblue", text = str(self.game.player1.getColor())+ ": Player 1: " + str(self.game.playerScore(self.game.player1)), font=("Helvetica", 16)).grid(sticky = "nw", row = 1, column = self.boardSize+1)
        self.p2ScoreLabel = Label(self.root, bg = "lightblue", text = str(self.game.player2.getColor())+ ": Player 2: " + str(self.game.playerScore(self.game.player2)), font=("Helvetica", 16)).grid(sticky = "w", row = 1, column = self.boardSize+1)
        self.moveLabel = Label(self.root, bg = "lightblue", text = "Current Move: " + str(self.game.currPlayer.getColor()), font=("Helvetica", 16)).grid(sticky = "sw", row = 2, column = self.boardSize+1)
        '''

    def highlight_possible_moves(self):
        moves = self.game.moves_avail(self.game.currPlayer)
        for key in self.buttons:
            self.buttons[key]["bg"] = "grey"
        for move in moves:
            b = self.buttons[move]
            b["bg"] = "blue"
    
    def game_over(self):
        self.deactivate_board()
        self.scoreLabel.config(text = "Final Score   ")
        self.moveLabel.config(text = "")
        #gameOver = Label(self.root, bg = "grey", fg = "red", text = "GAME OVER\n" + self.game.winner(), font=("Helvetica", 20)). \
        #    grid(sticky = "", row = int(self.boardSize/2)-1, column=int(self.boardSize/2)-2, columnspan=4, rowspan = 3)
        gameOver = Label(self.root,borderwidth=1, relief="solid", bg = "lightblue", fg = "black", text = "GAME OVER\n" + self.game.winner(), font=("Helvetica", 30)). \
            place(x = 68*(self.boardSize/2-2)+28, y = 82*self.boardSize/2-35)
        restartButton = ttk.Button(self.root, text="Play Again", command = lambda: self.new_game()).place(x = 68*(self.boardSize/2-1)+35, y = 82*(self.boardSize/2+2)-35) 
        
    def new_game(self):
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

    def button_click(self, b: Button):

        """
        Triggered on button click - makeMove(self, player: str, posn: Posn):
        Should first check if move is valid - moveLegal(self, player: str, posn: Posn) -> bool:
        Right now will just change the text
        """
        moveMade = False
        bPosn = [key for key, value in self.buttons.items() if value == b][0]
        moveMade = self.game.make_move(self.game.currPlayer, bPosn)
        if moveMade:
            self.game.next_player()
        
        self.draw_button_values()
        self.draw_score()
        if self.game.end_game() == True:
            self.game_over()
        else:
            if(self.game.no_moves_avail(self.game.currPlayer) == True):
                self.game.next_player()
                self.draw_button_values()
                self.draw_score()

  

    def main(self):
        #buttons - will pass in board size
        rows = cols = self.boardSize    # could just pass boardsize for rows/cols, 
                                        # or rewrite generateButtons to accept one int
        self.root.mainloop()

class AIGUI(GUI):

    difficulty: int

    def __init__(self, size: int, diff: int, col: str):
        super().__init__(size, col)
        self.game = AIGame(self.board)
        self.difficulty = diff
        self.game.set_difficulty(self.difficulty)

    """
    Maybe add commands similar to these to stop user input while AI is thinking

    def pauseBoard(self):
        for posn in self.board.board.keys():
            b = self.buttons[posn]
            b["command"] = 0
    
    def resumeBoard(self):
        for posn in self.board.board.keys():
            b = self.buttons[posn]
            b["command"] = self.buttonClick(b)
    """

    def button_click(self, b: Button):
        """
        Triggered on button click - makeMove(self, player: str, posn: Posn):
        Should first check if move is valid - moveLegal(self, player: str, posn: Posn) -> bool:
        Right now will just change the text
        """
        if (self.game.currPlayer != self.game.player2):
            def click():
                moveMade = False
                bPosn = [key for key, value in self.buttons.items() if value == b][0]
                moveMade = self.game.make_move(self.game.currPlayer, bPosn)
                if moveMade:
                    self.game.next_player()
                    self.draw_button_values()
                    self.draw_score()
                    bestPosn = self.game.get_move(self.board.copy(),self.game.currPlayer)
                    moveMade = self.game.make_move(self.game.currPlayer, bestPosn)
                    if moveMade:
                        #if self.boardSize < 7 or self.game.difficulty < 3:
                        time.sleep(2)
                        self.game.next_player()
                        self.draw_button_values()
                        self.draw_score()
                    if self.game.end_game() == True:
                        self.game_over()
                    else:
                        if(self.game.no_moves_avail(self.game.currPlayer) == True):
                            self.game.next_player()
                            
                self.draw_button_values()
                self.draw_score()
                if self.game.end_game() == True:
                    self.game_over()
                else:
                    if(self.game.no_moves_avail(self.game.currPlayer) == True):
                        self.game.next_player()
                        moveMade = self.game.make_move(self.game.currPlayer, self.game.get_move(self.board.copy(),self.game.currPlayer))
                        if moveMade:
                            #if self.boardSize < 7 or self.game.difficulty < 3:
                            time.sleep(2)
                            self.game.next_player()
                            self.draw_button_values()
                            self.draw_score()
                        if self.game.end_game() == True:
                            self.game_over()
                        else:
                            if(self.game.no_moves_avail(self.game.currPlayer) == True):
                                self.game.next_player()
                        self.draw_button_values()
                        self.draw_score()
            threading.Thread(target = click).start()

    def new_game(self): 
        self.root.destroy()
        gui = AIGUI(self.boardSize, self.difficulty)
        gui.main() 


class OnlineGUI(GUI):  
    """
    Class for an online game
    When a user requests to join an online game 
    add them to a waiting queue of clients. As enough clients
    populate pair them off and start games. 
    """
    game: OnlineGame
    def __init__(self, client: Client, playerNum: int):
        size = 8
        super().__init__(size)
        self.game = OnlineGame(self.board, client, playerNum)
        if playerNum == 2:
            oppMove = self.game.wait_for_move()
            self.game.make_move(self.game.currPlayer, oppMove)

    def button_click(self, b: Button):
        def click():
            moveMade = False
            bPosn = [key for key, value in self.buttons.items() if value == b][0]
            moveMade = self.game.make_move_online(self.game.currPlayer, bPosn)
            if moveMade:
                self.game.next_player()
                self.draw_button_values()
                self.draw_score()
                oppMove = self.game.wait_for_move()
                self.game.make_move(self.game.currPlayer, oppMove)
            self.draw_button_values()
            self.draw_score()
            if self.game.end_game() == True:
                self.game_over()
            else:
                if(self.game.no_moves_avail(self.game.currPlayer) == True):
                    self.game.next_player()
                    oppMove = self.game.wait_for_move()
                    self.game.make_move(self.game.currPlayer, oppMove)
                    self.draw_button_values()
                    self.draw_score()
        threading.Thread(target = click).start()

main = LoginScreen()
main.main()