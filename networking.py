import socket
import select
import sys
from _thread import *
import time
from server import GameServer

"""The first argument AF_INET is the address domain of the
socket. This is used when we have an Internet Domain with
any two hosts The second argument is the type of socket.
SOCK_STREAM means that data or characters are read in
a continuous flow."""
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
 

 
"""# checks whether sufficient arguments have been provided
if len(sys.argv) != 3:
    print ("Correct usage: script, IP address, port number")
    exit()
 
# takes the first argument from command prompt as IP address
IP_address = str(sys.argv[1])
 
# takes second argument from command prompt as port number
Port = int(sys.argv[2])"""
 
"""
binds the server to an entered IP address and at the
specified port number.
The client must be aware of these parameters
"""
IP_address = "192.168.0.21"
Port = 45678

server.bind((IP_address, Port))
 
"""
listens for 100 active connections. This number can be
increased as per convenience.
"""
server.listen(100)

list_of_clients = []
 
def clientthread(conn, addr):
 
    idx = list_of_clients.index(conn)
    if idx == 0:
        message = "You are Player 1, port:" + str(Port + 1)
        print(message)
        encodedMessage = bytes(message, 'utf-8')
        conn.sendall(encodedMessage)
    elif idx == 1:
        message = "You are Player 2, port:" + str(Port + 1)
        print(message)
        encodedMessage = bytes(message, 'utf-8')
        conn.sendall(encodedMessage)
    else:
        pass

    while True:
            try:
                message = conn.recv(2048)
                if message:
 
                    """prints the message and address of the
                    user who just sent the message on the server
                    terminal"""
                    print ("<" + addr[0] + "> " + message)
 
                    # Calls broadcast function to send message to all
                    message_to_send = message
                    broadcast(message_to_send, conn)
 
                else:
                    continue
 
            except:
                continue
 
"""Using the below function, we broadcast the message to all
clients who's object is not the same as the one sending
the message """
def broadcast(message, connection):
    for clients in list_of_clients:
        if clients!=connection:
            try:
                clients.send(message)
            except:
                clients.close()
 


start = False
while True:
 
    """Accepts a connection request and stores two parameters,
    conn which is a socket object for that user, and addr
    which contains the IP address of the client that just
    connected"""
    conn, addr = server.accept()
 
    """Maintains a list of clients for ease of broadcasting
    a message to all available people in the chatroom"""
    list_of_clients.append(conn)
 
    # prints the address of the user that just connected
    print (addr[0] + " connected")

    """if len(list_of_clients) > 1 and start is False:
        message = "Connect"
        print(message)
        encodedMessage = bytes(message, 'utf-8')
        for clients in list_of_clients:
            try:
                clients.send(message)
            except:
                clients.close()
        start = True"""
        #game_server = GameServer(Port+1, (self.clients[0], self.clients[1]))'''
 
    # creates and individual thread for every user
    # that connects
    start_new_thread(clientthread,(conn,addr))  

conn.close()
server.close()