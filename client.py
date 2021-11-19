from os import SEEK_END
import socket

class Client:

    ClientSocket = socket.socket()
    host = '127.0.0.1'
    port = 1233

    def __init__(self):
        self.run()

    def connectToServer(self):
        try:
            self.ClientSocket.connect((self.host, self.port))
        except socket.error as e:
            print(str(e))


    def sendMove(self, move: str):
        Input = input('Say Something: ')
        self.ClientSocket.send(str.encode(Input))

    def waitForMove(self):
        while True:
            Response = self.ClientSocket.recv(1024)
            if not Response:
                break
            else:
                Response = Response.decode('utf-8')
                return Response

    def run(self):
        self.connectToServer()
        resp = self.waitForMove()
        print(resp)
            
        #self.ClientSocket.close()

    def main(self):
        print('Waiting for connection')
        try:
            self.ClientSocket.connect((self.host, self.port))
        except socket.error as e:
            print(str(e))

        Response = self.ClientSocket.recv(1024)

        
        while True:
            Input = input('Say Something: ')
            self.ClientSocket.send(str.encode(Input))
            Response = self.ClientSocket.recv(1024)
            print(Response.decode('utf-8'))

        ClientSocket.close()

#client = Client()
#client.connectToServer()
#client.sendMove("hello")