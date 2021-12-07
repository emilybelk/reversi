import socket
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


    def __init__(self, port: int, ip: str):
        self.port = port
        self.ip = ip
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostname()
        self.socket.connect(("192.168.0.21", int(port)))


    def send_move(self, pos: str):
        """
        send "row, col" 
        call s.split() -> list(row, col)
        """
        
        self.socket.send(pos.encode('utf-8'))

    def set_socket(self, conn: socket.socket(socket.AF_INET, socket.SOCK_STREAM)):
        self.socket = conn


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

    def wait_for_game(self):
        playerNum = 0
        new_port = 0
        while True:
            self.socket.settimeout(120)
            try:
                #print("waiting")
                received = self.socket.recv(99999).rstrip()
                if received:
                    received = received.decode('utf-8').split(":")
                    print(received)
                    new_port = int(received[1])
                    #self.new_connect(new_port)
                    print(received[0])
                    if "Player 1" in received[0]:
                        #return 1, Client(received[1], '127.0.0.1')
                        playerNum = 1              
                    else:
                        #return 2, Client(received[1], '127.0.0.1')
                        playerNum = 2 
                    return playerNum, new_port
                    
    
            except socket.timeout:
                self.socket.close()
                return None

    def wait_for_start(self, new_port):
            while True:
                self.socket.settimeout(120)
                try:
                    #print("waiting")
                    received = self.socket.recv(99999).rstrip()
                    if received:
                        received = received.decode('utf-8')
                        print(received)
                
                        if "Connect" in received:
                            return True
                except socket.timeout:
                    self.socket.close()
                    return None

    def new_connect(self, port: int):
        """
        Thinking this could be used to place the client on the game server, rather than the lobby server
        """
        self.socket.close()
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ip, int(port)))

    # def recieve_updates(self):
    #     """
    #     Wait to recieve game updates from the server. 
    #     """

    #     while True:
    #         vals = ""
    #         self.socket.settimeout(3)
    #         try:
    #             received = self.socket.recv(99999).rstrip()
    #             if received:
    #                 vals += received
    #                 move = ijson.items(vals, '', multiple_values=True, use_float=True)
    #                 return move

    #         except socket.timeout:
    #             self.socket.close()