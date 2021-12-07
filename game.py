from board import Board, Posn, Status
from player import Player, Account
from client import Client
import socket

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
    
    def next_player(self):
        if self.currPlayer == self.player1:
            self.currPlayer = self.player2
        else:
            self.currPlayer = self.player1

    def get_board_value(self, space: Posn) ->str:
        """
        Returns board value at given Posn
        """
        return self.board.board[space].value

    def player_pieces(self, player: Player) -> set():
        """
        Return all the pieces that belong to the current player.
        """
        pColor = player.get_color()

        return {k for k, v in self.board.board.items() if v.value == pColor}


    def player_score(self, player: Player) -> int:
        """
        Return the given player's score.
        """

        return len(self.player_pieces(player))


    def moves_avail_helper(self, piece: Posn) -> set():
        """
        Return a set of all the moves available to be made because of this piece. 
        """
        ### is space legal not working. Edge space moves are resulting in KeyError: <board.Posn object at 0x00000185CA1AE130>
        possible_moves = set()
        for direction in self.DIRS:
            new_posn = piece.add(direction)
            firstJump = True
            while self.board.is_space_legal(new_posn) == True and self.get_board_value(new_posn) != self.get_board_value(piece):
                if self.get_board_value(new_posn) == ' ':
                    if firstJump == True:
                        break
                    else:
                        possible_moves.add(new_posn)
                        break
                else:
                    firstJump = False
                    new_posn = new_posn.add(direction)
        return possible_moves


    def moves_avail(self, player: Player) -> set():
        """
        Returns a set of Posn's where the given player could make a move. 
        A move is available if there is a free space that is in some way connected
        (horizontally, vertically, diagonally) to another one of this player's pieces. 
        """

        pieces = self.player_pieces(player)
        moves = set()
        for piece in pieces:
            moves = moves | self.moves_avail_helper(piece)
        return moves


    def avail_move(self, player: Player) -> bool:
        """
        Return if there are any available moves for this player. 
        """

        return len(self.moves_avail(player)) > 0

    
    def move_legal(self, player: Player, posn: Posn) -> bool:
        """
        Determine if the given posn is available and legal for the given
        player to take. 
        """

        return (self.get_board_value(posn) == ' ') \
               and (posn in self.moves_avail(player)) 


    def affected_pieces(self, player: Player, posn: Posn) -> set():
        """
        TODO
        Return a set containing all the affected pieces this player owns 
        so that we can fill them in. 
        """

        affected = set()
        for direction in self.DIRS:
            new_posns = set()
            new_posn = posn.add(direction)
            while self.board.is_space_legal(new_posn) == True and self.get_board_value(new_posn) != self.get_board_value(posn) and self.get_board_value(new_posn) != ' ':
                new_posns.add(new_posn)
                new_posn = new_posn.add(direction)
                if self.board.is_space_legal(new_posn) == True and self.get_board_value(new_posn) == self.get_board_value(posn):
                    new_posns.add(new_posn)
                    affected = affected | new_posns

        return affected


    def make_move(self, player: Player, posn: Posn) -> bool:
        """
        Occupy the given posn and all affected posn's in the player's favor if allowed. 
        """
        if self.move_legal(player, posn):
            self.board.update_posn_status(posn, player.get_color())
            for piece in self.affected_pieces(player, posn):
                self.board.update_posn_status(piece, player.get_color())
            return True
        else:
            return False


    def no_moves_avail(self, player: Player) -> bool:
        """
        Return if no moves are available left in the game for this player. 
        """

        return len(self.moves_avail(player))  == 0


    def board_full(self) -> bool:
        """
        Return if no spaces left empty on the board. 
        """
        
        for posn, status in self.board.board.items():
            if status.value == ' ':
                return False
        
        return True


    def end_game(self) -> bool:
        """
        Return if game is over. 
        """

        return self.board_full() or (self.no_moves_avail(self.player1) and self.no_moves_avail(self.player2))

    def winner(self) -> str:
        whiteScore = self.player_score(self.player1)
        blackScore = self.player_score(self.player2)
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
    client: Client
    socket: socket
    localPlayer: Player

    def __init__(self, board: Board, c1: Client, playerNum: int):
        super().__init__(board)
        self.client = c1
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostname()
        self.socket.connect(("192.168.0.21", self.client.port))
        if playerNum == 1:
            self.localPlayer = self.player1
        else:
            self.localPlayer = self.player2

    def send_move(self, pos: str):
        """
        send "row, col" 
        call s.split() -> list(row, col)
        """
        
        self.socket.send(pos.encode('utf-8'))

    def recieve_move(self):
        while True:
            self.socket.settimeout(120)
            try:
                received = self.socket.recv(99999).rstrip()
                if received:
                    return (received.decode('utf-8')).split() # list(row, col)

            except socket.timeout:
                self.socket.close()
                return None

    def make_move_online(self, player: Player, posn: Posn) -> bool:
        """
        Occupy the given posn and all affected posn's in the player's favor if allowed. 
        """
        moveMade = self.make_move(player, posn) #"row, colf"
        if moveMade:
            self.send_move(f"{posn.n}, {posn.m}")
        else:
            return False

    def wait_for_move(self) -> Posn:
        posn = self.recieve_move()
        return Posn(posn[0], posn[1]) if posn else False


class AIGame(Game):
    """
    Class to represent AI game
    Player 2 will always be AI
    """
    difficulty: int
    
    def __init__(self, board: Board):
        super().__init__(board)
        self.difficulty = 1
    
    def set_difficulty(self, dif: int):
        self.difficulty = dif

    def player_pieces_test(self, board: Board, player: Player) -> set():
        """
        Return all the pieces that belong to the current player.
        """
        pColor = player.get_color()

        return {k for k, v in board.board.items() if v.value == pColor}

    def moves_avail_helper_test(self, board: Board, piece: Posn) -> set():
        """
        Return a set of all the moves available to be made because of this piece. 
        """
        ### is space legal not working. Edge space moves are resulting in KeyError: <board.Posn object at 0x00000185CA1AE130>
        possible_moves = set()
        for direction in self.DIRS:
            new_posn = piece.add(direction)
            firstJump = True
            while board.is_space_legal(new_posn) == True and self.get_test_board_value(board, new_posn) != self.get_test_board_value(board, piece):
                if self.get_test_board_value(board, new_posn) == ' ':
                    if firstJump == True:
                        break
                    else:
                        possible_moves.add(new_posn)
                        break
                else:
                    firstJump = False
                    new_posn = new_posn.add(direction)
        return possible_moves


    def moves_avail_test(self, board: Board, player: Player) -> set():
        """
        Returns a set of Posn's where the given player could make a move. 
        A move is available if there is a free space that is in some way connected
        (horizontally, vertically, diagonally) to another one of this player's pieces. 
        """
        pieces = self.player_pieces_test(board, player)
        moves = set()
        for piece in pieces:
            moves = moves | self.moves_avail_helper_test(board, piece)
        return moves

    def get_test_board_value(self, board: Board, space: Posn) ->str:
        """
        Returns test board value at given Posn
        """
        return board.board[space].value

    def affected_pieces_test(self, board: Board, player: Player, posn: Posn) -> set():
        """
        affected pieces for test board
        """
        affected = set()
        for direction in self.DIRS:
            new_posns = set()
            new_posn = posn.add(direction)
            while board.is_space_legal(new_posn) == True and self.get_test_board_value(board, new_posn) != self.get_test_board_value(board, posn) and self.get_test_board_value(board, new_posn) != ' ':
                new_posns.add(new_posn)
                new_posn = new_posn.add(direction)
                if self.board.is_space_legal(new_posn) == True and self.get_test_board_value(board, new_posn) == self.get_test_board_value(board, posn):
                    new_posns.add(new_posn)
                    affected = affected | new_posns

        return affected


    def test_moves(self, board: Board, posn: Posn, player: Player):
        if self.move_legal(player, posn):
            board.update_posn_status(posn, player.get_color())
            for piece in self.affected_pieces_test(board, player, posn):
                board.update_posn_status(piece, player.get_color())
            return True
        else:
            return False

    def next_board(self, currBoard: Board, posn: Posn, player: Player) -> Board:
        """
        This function takes the current board, produces a copy with the possible move
        """
        nextBoard = currBoard.copy()
        #print("Old Board")
        #nextBoard.printBoard()
        madeMove = self.test_moves(nextBoard, posn, player)
        #print("New Board")
        #nextBoard.printBoard()
        moves = self.moves_avail_test(nextBoard, player)
        return nextBoard


    def get_move(self, board: Board, player: Player):
        return self.do_minimax_with_alpha_beta(board, player, self.difficulty, -100000, 100000)[1]


    def evaluate(self, board: Board, player: Player):
        oppPlayer = player
        if player == self.player1:
            oppPlayer = self.player2
        else:
            oppPlayer = self.player1
        
        pPieces = self.player_pieces_test(board, player)
        total = 0
        for piece in pPieces:
            total += piece.get_weight()
        
        oppPieces = self.player_pieces_test(board, oppPlayer)
        for piece in oppPieces:
            total -= piece.get_weight()
        return total

    #Minimax with alpha-beta, based on lecture slides
    def do_minimax_with_alpha_beta(self, board: Board, player: Player, depth: int, my_best, opp_best):
        #This was for the statistics section. Commented it out now
        #self.node_count += 1

        if depth == 0:
            return (self.evaluate(board, player), None)

        moves = self.moves_avail_test(board, player)
        
        #This was for the statistics section. Commented it out now
        #self.branches.append(len(move_list))

        if len(moves) == 0:
            return (self.evaluate(board, player), None)

        best_score = my_best
        best_move = None

        for move in moves:
            nextBoard = self.next_board(board, move, player)
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