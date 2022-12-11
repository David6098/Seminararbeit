import  random
from operator import index


class Baum:
    def __init__(self):
        self.wurzel = Blatt(0, Abschlusss(), None)
        self.aktuellerKnoten = self.wurzel
        self.highscore = 0
        # moeglmoves = ["r", "l", "s", None]

    def moveGeben(self, score):
        if self.highscore < score:
            self.highscore = score
        try:
            if self.highscore > 5:
                move, knoten = self.aktuellerKnoten.moveGeben(score, 40)
            else:
                move, knoten = self.aktuellerKnoten.moveGeben(score, 20)
            self.aktuellerKnoten = knoten
            return move
        except MemoryError:
            print("Memory Error")
            self.getsize()
    def getsize(self):
        a = self.wurzel.getsize(0)
        print("Baum ist " +str(a) + " Elemente groß.")

class Abschlusss:
    def __init__(self):
        self.score = 0
    def vorgaengeraktualisieren(self):
        pass


class Blatt:
    def __init__(self, score, vor, mov):
        self.move = mov
        self.score = score
        self.Kinder = []
        self.vorgaenger = vor


    def moveGeben(self, score, k):
        r = random.randint(0, k)

        self.score = 0
        if self.Kinder == []:
            self.Kinder.append(Blatt(self.score, self, "r"))
            self.Kinder.append(Blatt(self.score, self, "l"))
            self.Kinder.append(Blatt(self.score, self, "s"))
            self.Kinder.append(Blatt(self.score, self, None))
        if r != 20:
            self.score = score
            f = 0
            a = 0
            for i in range(0, len(self.Kinder)):
                if self.Kinder[i].score >= self.score:
                    f = a
                    self.score = self.Kinder[i].score
                a = a + 1

        else:

            f = random.randint(0, 3)
        self.vorgaengeraktualisieren()
        return self.move, self.Kinder[f]
    def vorgaengeraktualisieren(self):
        if self.score > self.vorgaenger.score:
            self.vorgaenger.score = self.score

    def getsize(self, a):
        a += 1
        try:
            for i in self.Kinder:
                i.getsize(a)
        except:
            print("Baum ist mindestens " + str(a) + " Elemente groß.")
        return a


