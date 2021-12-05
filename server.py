
import socket
from game import OnlineGame
import time
from client import Client

class Server:
    """
    Class for a single server running a game between two Clients
    """

    clients: tuple()
    port: int


    def __init__(self, port, clients):
        self.clients = clients
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('127.0.0.1', int(port)))
        self.socket.listen(50)


    def gather_clients(self):
        """
        Gathers clients connected to this Server's port number.
        """
        
        deadline = time.time() + 30
        while time.time() <= deadline:
            try:
                conn, addr = self.socket.accept()
                self.socket.settimeout(3)
                while True:
                    self.clients.append(Client(username, conn))

            except socket.timeout:
                break

    def get_pair(self):
        
        if len(self.clients) > 1:
            return [self.clients.pop() for _ in range(2)]
        else: 
            return None


    """
    New OnlineGUI
    Make a server and two clients with their IPs and a random port 
    then each client on a players move will be updateds
    """

