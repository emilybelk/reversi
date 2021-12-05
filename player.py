#from client import Client

class Account:
    username: str
    password: str
    def __init__(self, u: str, p: str):
        username = u
        password = p


# we can determine "accounts" that correspond to guest or AI?

class Player:

    color: str
    score: int
    account: Account # this will probably be assigned from database on login?
    def __init__(self, c: str, a: Account):
        self.color = c
        self.account = a
        self.score = 0
    
    def get_color(self):
        return self.color
    
    def set_score(self, newScore: int):
        self.score = newScore

    def get_score(self):
        return self.score

