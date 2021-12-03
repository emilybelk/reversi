import socket
from game import OnlineGame

class Server:
    """
    Class for a single server running a game between two Clients
    """

    clients: tuple()


    def run_server(self):
        self.gather_clients()
        if len(self.clients) == 2:
            # TODO: run_game()
        
        # TODO: Return result of game


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