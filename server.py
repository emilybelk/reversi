
import socket
from game import OnlineGame
import time
from client import Client
from collections import deque
import threading

ACK_TEXT = 'text_received'

class sock:
    conn: socket
    def __init__(self, c: socket):
        self.conn = c
    def set_conn(self, c: socket):
        self.conn = c

class MainServer:
    """
    Class for master server holding all waiting clients. 
    """

    clients: deque()
    socket: socket
    current_port: int
    p1: bool

    def __init__(self):
        self.clients = deque()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = socket.gethostname() 
        self.current_port = 45678
        self.socket.bind(('localhost', int(self.current_port)))
        self.current_port += 1
        self.socket.listen(50)
        self.p1 = True


    def gather_clients(self):
        """
        Gathers clients connected to this Server's port number.
        """
        
        deadline = time.time() + 30
        while time.time() <= deadline:
            if len(self.clients) > 1:
                break
            try:
                
                conn, addr = self.socket.accept()

                self.socket.settimeout(3)
                with conn:
                    client = sock(conn)
                    self.clients.append(client)

            except socket.timeout:
                break
    
    def gather_clients2(self):
        """
        Gathers clients connected to this Server's port number.
        """
        
        deadline = time.time() + 30
        
        while time.time() <= deadline:
            if len(self.clients) > 1:
                break
            try:
                
                conn, addr = self.socket.accept()

                self.socket.settimeout(3)
                with conn:
                    if self.p1:
                        message = "You are Player 1, port:" + str(self.current_port)
                        print(message)
                        encodedMessage = bytes(message, 'utf-8')
                        conn.sendall(encodedMessage)
                        self.p1 = False
                    else:
                        message = "You are Player 2, port:" + str(self.current_port)
                        print(message)
                        encodedMessage = bytes(message, 'utf-8')
                        conn.sendall(encodedMessage)
                    client = sock(conn)
                    self.clients.append(client)
                    if len(self.clients) > 1:
                        time.sleep(10)
                        message = "Connect"
                        print(message)
                        encodedMessage = bytes(message, 'utf-8')
                        conn.sendall(encodedMessage)
                        game_server = GameServer(self.current_port, (self.clients[0], self.clients[1]))


            except socket.timeout:
                break
        
                

    def get_pair(self):       
        if len(self.clients) > 1:
            print("hello")
            return [self.clients.pop() for _ in range(2)]
        else: 
            return None

    def sendTextViaSocket(message, sock):
        # encode the text message
        encodedMessage = bytes(message, 'utf-8')

        # send the data via the socket to the server
        sock.sendall(encodedMessage)

        # receive acknowledgment from the server
        encodedAckText = sock.recv(1024)
        ackText = encodedAckText.decode('utf-8')

        # log if acknowledgment was successful
        if ackText == ACK_TEXT:
            print('server acknowledged reception of text')
        else:
            print('error: server has sent back ' + ackText)
        # end if
    # end function
    
    def make_match(self):
        """
        Used to launch game server for client pair
        """
        p1 = True
        for i in range(2):
            conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conn.connect()
            curr_client = self.clients[i]
            curr_client.set_conn(conn)
            message = ""
            if p1:
                message = "You are Player 1, port:" + str(self.current_port)
                print(message)
            else:
                message = "You are Player 2, port:" + str(self.current_port)
                print(message)
            encodedMessage = bytes(message, 'utf-8')
            # send the data via the socket to the server
            #print(type(client))
            curr_client.conn.sendall(encodedMessage)
            
        game_server = GameServer(self.current_port, (self.clients[0], self.clients[1]))
        self.current_port += 1
        return game_server
            
        return None


    def main(self):
        while True:     
            self.gather_clients2()
            #game = self.make_match()
            #if game:
             #   threading.Thread(target = run_game, kwargs={'game': game}).start()


class GameServer:
    """
    Class for a single server running a game between two Clients
    """

    clients: tuple()
    port: int



    def __init__(self, port, clients):
        self.clients = clients
        self.port = port
        self.next_port = port + 1
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('localhost', int(port)))
        self.socket.listen(50)

    #def start(self):


    def shutdown(self):
        self.socket.close()
    
    

    """
    New OnlineGUI
    Make a server and two clients with their IPs and a random port 
    then each client on a players move will be updateds
    """

