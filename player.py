class Account:
    username: str
    password: str
    def __init__(self, u: str, p: str):
        username = u
        password = p


# we can determine "accounts" that correspond to guest or AI?

class Player:

    color: str
    account: Account # this will probably be assigned from database on login?
    def __init__(self, c: str, a: Account):
        self.color = c
        self.account = a
    
    def getColor(self):
        return self.color

