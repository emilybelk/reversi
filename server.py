'''
import socket
import os
from _thread import *

ServerSocket = socket.socket()
host = '127.0.0.1'
port = 1233
ThreadCount = 0
try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waitiing for a Connection..')
ServerSocket.listen(5)


def threaded_client(connection):
    connection.send(str.encode('Welcome to the Servern'))
    while True:
        data = connection.recv(2048)
        reply = 'Server Says: ' + data.decode('utf-8')
        if not data:
            break
        connection.sendall(str.encode(reply))
    connection.close()


while True:
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
ServerSocket.close()

'''
import socket
import os
from threading import Thread
from threading import Lock

# from https://stackoverflow.com/questions/55496858/how-to-send-and-receive-message-from-client-to-client-with-python-socket

clients = [] # The clients we have connected to
clients_lock = Lock()

def listener(client, address):
    print ("Accepted connection from: ", address)
    with clients_lock:
        clients.append(client) # Add a client to our list
    try:    
        while True:
            data = client.recv(1024)
            if not data:
                break
            else:
                print (repr(data))
                # Here you need to read your data
                # and figure out who you want to send it to
                for idx, c in clients:
                    if c == client:
                        break
                    else:
                        client_to_send_to = idx
                        # Send this data to other client
                        with clients_lock:
                            if client_to_send_to < len(clients):
                                clients[client_to_send_to].sendall(data)
    finally:
        with clients_lock:
            clients.remove(client)
            client.close()
host = '127.0.0.1'
port = 1233

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host,port))
s.listen(3)
th = []

while True:
    print ("Server is listening for connections...")
    client, address = s.accept()
    th.append(Thread(target=listener, args = (client,address)).start())

s.close()