class Spielelement():
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def xGeben(self):
        return self.x

    def yGeben(self):
        return  self.y

    def xSetzen(self, x):
        self.x = x

    def ySetzen(self, y):
        self.y = y

    def posSetzen(self, x, y):
        self.x = x
        self.y = y
class Spieler(Spielelement):

    def __init__(self):
        self.x = 0
        self.y = -280





class Gegner(Spielelement):

    def __init__(self):
        self.x = 400
        self.y = 300


class Geschoss(Spielelement):

    def __init__(self):
        self.x = 400
        self.y = 300
