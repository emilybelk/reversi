import socket
from player import Player
import json

class Client:
    """
    Class to represent a single client. 
    A Client has:
    - port int that represents the port that this client is connecting to. 
    - ip str that represents the IP address of this client. (default is 127.0.0.1)
    """

    port: int
    ip: str
    socket: socket


    def __init__(self, player : Player, port: int, ip: str):
        self.port = port
        self.ip = ip
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((ip, int(port)))
        self.socket.sendall(player.name.encode('utf-8'))


    def make_moves(self):
        """
        Do as told. 
        """

        new_move = self.receive_commands()
        if new_move:
            # TODO: make a move 
            json_res = json.dumps(#MADE MOVE)
            self.socket.sendall(json_res.encode('utf-8')))


    def recieve_updates(self):
        """
        Wait to recieve game updates from the server. 
        """

        while True:
            vals = ""
            self.socket.settimeout(3)
            try:
                received = self.socket.recv(99999).rstrip()
                if received:
                    vals += received
                    move = ijson.items(vals, '', multiple_values=True, use_float=True)
                    return move

            except socket.timeout:
                self.socket.close()