from board import Board, Posn, Status
from player import Player, Account

"""
TODO:
WHILE LOOP:
- end game conditions
    - no spaces on board
    - no active moves for at least one player

GAME:
- score
    - count white pieces
    - count black pieces
- make move
    - check legal
    - update pieces 

- while loop to play game, ideally not in this class

IM THINKING: we dont need players stored in board we can pass them in 

- gui
"""

class Game:
    """
    Class for a single reversi game. 
    A game will have a board. 
    https://stackoverflow.com/questions/40740615/check-moves-in-othello-reversi-python-3
    DIRS stores all the possible directions we could go in. 
    """

    DIRS = [Posn(n, m) for n, m in [(0, -1),  (1, -1), 
                                    (1,  0),  (1,  1),  
                                    (0,  1),  (-1, 1),  
                                    (-1, 0),  (-1, -1)]]

    board: Board
    player1: Player
    player2: Player
    currPlayer: Player


    def __init__(self, board: Board):
        self.board = board
        self.player1 = Player("w", Account("1", "2"))
        self.player2 = Player("b", Account("1", "2"))
        self.currPlayer = self.player1
    
    def nextPlayer(self):
        if self.currPlayer == self.player1:
            self.currPlayer = self.player2
        else:
            self.currPlayer = self.player1

    def getBoardValue(self, space: Posn) ->str:
        """
        Returns board value at given Posn
        """
        return self.board.board[space].value

    def playerPieces(self, player: Player) -> set():
        """
        Return all the pieces that belong to the current player.
        """
        pColor = player.getColor()

        return {k for k, v in self.board.board.items() if v.value == pColor}


    def playerScore(self, player: Player) -> int:
        """
        Return the given player's score.
        """

        return len(self.playerPieces(player))


    def movesAvailHelper(self, piece: Posn) -> set():
        """
        Return a set of all the moves available to be made because of this piece. 
        """
        ### is space legal not working. Edge space moves are resulting in KeyError: <board.Posn object at 0x00000185CA1AE130>
        possible_moves = set()
        for direction in self.DIRS:
            new_posn = piece.add(direction)
            firstJump = True
            while self.board.isSpaceLegal(new_posn) == True and self.getBoardValue(new_posn) != self.getBoardValue(piece):
                if self.getBoardValue(new_posn) == ' ':
                    if firstJump == True:
                        break
                    else:
                        possible_moves.add(new_posn)
                        break
                else:
                    firstJump = False
                    new_posn = new_posn.add(direction)
        return possible_moves


    def movesAvail(self, player: Player) -> set():
        """
        Returns a set of Posn's where the given player could make a move. 
        A move is available if there is a free space that is in some way connected
        (horizontally, vertically, diagonally) to another one of this player's pieces. 
        """

        pieces = self.playerPieces(player)
        moves = set()
        for piece in pieces:
            moves = moves | self.movesAvailHelper(piece)
        return moves


    def availMove(self, player: Player) -> bool:
        """
        Return if there are any available moves for this player. 
        """

        return len(self.movesAvail(player)) > 0

    
    def moveLegal(self, player: Player, posn: Posn) -> bool:
        """
        Determine if the given posn is available and legal for the given
        player to take. 
        """

        return (self.getBoardValue(posn) == ' ') \
               and (posn in self.movesAvail(player)) 


    def affectedPieces(self, player: Player, posn: Posn) -> set():
        """
        TODO
        Return a set containing all the affected pieces this player owns 
        so that we can fill them in. 
        """

        affected = set()
        for direction in self.DIRS:
            new_posns = set()
            new_posn = posn.add(direction)
            while self.board.isSpaceLegal(new_posn) == True and self.getBoardValue(new_posn) != self.getBoardValue(posn) and self.getBoardValue(new_posn) != ' ':
                new_posns.add(new_posn)
                new_posn = new_posn.add(direction)
                if self.board.isSpaceLegal(new_posn) == True and self.getBoardValue(new_posn) == self.getBoardValue(posn):
                    new_posns.add(new_posn)
                    affected = affected | new_posns

        return affected


    def makeMove(self, player: Player, posn: Posn) -> bool:
        """
        Occupy the given posn and all affected posn's in the player's favor if allowed. 
        """
        if self.moveLegal(player, posn):
            self.board.updatePosnStatus(posn, player.getColor())
            for piece in self.affectedPieces(player, posn):
                self.board.updatePosnStatus(piece, player.getColor())
            return True
        else:
            return False


    def noMovesAvail(self, player: Player) -> bool:
        """
        Return if no moves are available left in the game for this player. 
        """

        return len(self.movesAvail(player))  == 0


    def boardFull(self) -> bool:
        """
        Return if no spaces left empty on the board. 
        """
        
        for posn, status in self.board.board.items():
            if status.value == ' ':
                return False
        
        return True


    def endGame(self) -> bool:
        """
        Return if game is over. 
        """

        return self.boardFull() or (self.noMovesAvail(self.player1) and self.noMovesAvail(self.player2))

    def winner(self) -> str:
        whiteScore = self.playerScore(self.player1)
        blackScore = self.playerScore(self.player2)
        # here we would want to update user ELO using account info tied to player
        if(whiteScore>blackScore):
            return "Player 1 Wins!"
        else:
            return "Player 2 Wins!"


class OnlineGame(Game):
    """
    Class to represent an online game where 
    two clients are connected via a shared server.
    """

    game: Game

    def __init__(self, game: Game):
            self.game = game


class AIGame(Game):
    """
    Class to represent AI game
    Player 2 will always be AI
    """
    difficulty: int
    
    def __init__(self, board: Board):
        super().__init__(board)
        self.difficulty = 1
    
    def setDifficulty(self, dif: int):
        self.difficulty = dif

    def playerPiecesTest(self, board: Board, player: Player) -> set():
        """
        Return all the pieces that belong to the current player.
        """
        pColor = player.getColor()

        return {k for k, v in board.board.items() if v.value == pColor}

    def movesAvailHelperTest(self, board: Board, piece: Posn) -> set():
        """
        Return a set of all the moves available to be made because of this piece. 
        """
        ### is space legal not working. Edge space moves are resulting in KeyError: <board.Posn object at 0x00000185CA1AE130>
        possible_moves = set()
        for direction in self.DIRS:
            new_posn = piece.add(direction)
            firstJump = True
            while board.isSpaceLegal(new_posn) == True and self.getTestBoardValue(board, new_posn) != self.getTestBoardValue(board, piece):
                if self.getTestBoardValue(board, new_posn) == ' ':
                    if firstJump == True:
                        break
                    else:
                        possible_moves.add(new_posn)
                        break
                else:
                    firstJump = False
                    new_posn = new_posn.add(direction)
        return possible_moves


    def movesAvailTest(self, board: Board, player: Player) -> set():
        """
        Returns a set of Posn's where the given player could make a move. 
        A move is available if there is a free space that is in some way connected
        (horizontally, vertically, diagonally) to another one of this player's pieces. 
        """
        pieces = self.playerPiecesTest(board, player)
        moves = set()
        for piece in pieces:
            moves = moves | self.movesAvailHelperTest(board, piece)
        return moves

    def getTestBoardValue(self, board: Board, space: Posn) ->str:
        """
        Returns test board value at given Posn
        """
        return board.board[space].value

    def affectedPiecesTest(self, board: Board, player: Player, posn: Posn) -> set():
        """
        affected pieces for test board
        """
        affected = set()
        for direction in self.DIRS:
            new_posns = set()
            new_posn = posn.add(direction)
            while board.isSpaceLegal(new_posn) == True and self.getTestBoardValue(board, new_posn) != self.getTestBoardValue(board, posn) and self.getTestBoardValue(board, new_posn) != ' ':
                new_posns.add(new_posn)
                new_posn = new_posn.add(direction)
                if self.board.isSpaceLegal(new_posn) == True and self.getTestBoardValue(board, new_posn) == self.getTestBoardValue(board, posn):
                    new_posns.add(new_posn)
                    affected = affected | new_posns

        return affected


    def testMove(self, board: Board, posn: Posn, player: Player):
        if self.moveLegal(player, posn):
            board.updatePosnStatus(posn, player.getColor())
            for piece in self.affectedPiecesTest(board, player, posn):
                board.updatePosnStatus(piece, player.getColor())
            return True
        else:
            return False

    def nextBoard(self, currBoard: Board, posn: Posn, player: Player) -> Board:
        """
        This function takes the current board, produces a copy with the possible move
        """
        nextBoard = currBoard.copy()
        #print("Old Board")
        #nextBoard.printBoard()
        madeMove = self.testMove(nextBoard, posn, player)
        #print("New Board")
        #nextBoard.printBoard()
        moves = self.movesAvailTest(nextBoard, player)
        return nextBoard


    def get_move(self, board: Board, player: Player):
        return self.do_minimax_with_alpha_beta(board, player, self.difficulty, -100000, 100000)[1]


    def evaluate(self, board: Board, player: Player):
        oppPlayer = player
        if player == self.player1:
            oppPlayer = self.player2
        else:
            oppPlayer = self.player1
        
        pPieces = self.playerPiecesTest(board, player)
        total = 0
        for piece in pPieces:
            total += piece.getWeight()
        
        oppPieces = self.playerPiecesTest(board, oppPlayer)
        for piece in oppPieces:
            total -= piece.getWeight()
        return total

    #Minimax with alpha-beta, based on lecture slides
    def do_minimax_with_alpha_beta(self, board: Board, player: Player, depth: int, my_best, opp_best):
        #This was for the statistics section. Commented it out now
        #self.node_count += 1

        if depth == 0:
            return (self.evaluate(board, player), None)

        moves = self.movesAvailTest(board, player)
        
        #This was for the statistics section. Commented it out now
        #self.branches.append(len(move_list))

        if len(moves) == 0:
            return (self.evaluate(board, player), None)

        best_score = my_best
        best_move = None

        for move in moves:
            nextBoard = self.nextBoard(board, move, player)
            #new_board = deepcopy(board)
            #new_board.execute_move(move, color)

            nextPlayer = player

            if player == self.player1:
                nextPlayer = self.player2
            else:
                nextPlayer = self.player1

            try_tuple = self.do_minimax_with_alpha_beta(nextBoard, nextPlayer, depth-1, -opp_best, -best_score)
            try_score = -try_tuple[0]

            if try_score > best_score:
                best_score = try_score
                best_move = move

            if best_score > opp_best:
                return (best_score, best_move)

        return (best_score, best_move)