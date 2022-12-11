import math
import pickle
import random
import time

#from keyboard import is_pressed
from NeuronalesNetz import NeuronalesNetz
from Baum import Baum

from Spielausgabe import Spielausgabe
from Spielelement import *
import xlsxwriter

class Spielkonsole:

    def __init__(self, Art: str, Grafischedarstellung: bool = True, bestehendes_neuronales_Netz_laden: bool = True):
        self.grafik = Grafischedarstellung
        self.score = 0
        self.spieler = Spieler()
        self.gegnerliste = []
        self.geschoss = Geschoss()
        self.alive = True
        self.Monsteranzahl = 16
        self.Spielergeschwindigkeit = 15
        self.Kugelgeschwindigkeit = 15
        self.Gegnergeschwindigkeit = 2
        self.AbstandMonsterx = 20
        self.AbstandMonstery = 20
        self.Generation = 0
        if Art == "standard":
            self.NeuronalesNetz = NeuronalesNetz(Art)
        elif Art == "zufällig":
            self.NeuronaleNetze = []
            for i in range(0, 99):
                self.NeuronaleNetze.append(NeuronalesNetz(Art))
        if bestehendes_neuronales_Netz_laden:
            self.LoadNeuronaleNetz()
        if self.grafik:
            self.spa = Spielausgabe(self.spieler.x, self.spieler.y)
        self.Gegnerhinzufuegen(False)
        self.geschosssstatus = "Schussbereit"
        print(1)
        if Art == "standard":
            self.maingameLoop()
        elif Art == "zufällig":
            self.maingameloopzufaellig()
        elif Art == "Baum":
            self.Baum = Baum()
            self.gen = 100
            self.maingameloopbaum(False)
        elif Art == "minimal":
            self.maingameLoopmin()

    def Gegnerhinzufuegen(self, random: bool = False):

        for i in range(len(self.gegnerliste), self.Monsteranzahl):
            gegner = Gegner()
            self.gegnerliste.append(gegner)
        if random:
            self.Gegnersetzen_random()
        else:
            self.Gegnersetzen()

        if self.grafik:
            for e in self.gegnerliste:
                self.spa.gegnererzeugen(e.xGeben(), e.yGeben())

    def Gegnersetzen_random(self):
        for g in self.gegnerliste:
            x = random.randint(-200, 200)

            y = random.randint(100, 250)
            g.xSetzen(x)
            g.ySetzen(y)

    def Gegnersetzen(self):

        x = -200
        y = 250
        for e in self.gegnerliste:
            e.xSetzen(x)
            if x < 200:
                x += 30
            else:
                x = -200
            e.ySetzen(y)
            if y > 100:
                y -= 50
            else:
                y = 250

    def scoregeben(self):
        return self.score

    def moveLeft(self):
        x = self.spieler.xGeben()
        x -= self.Spielergeschwindigkeit
        if x < -280:
            x = -280
        self.spieler.xSetzen(x)

    def moveRight(self):
        x = self.spieler.xGeben()
        x += self.Spielergeschwindigkeit
        if x > 280:
            x = 280
        self.spieler.xSetzen(x)

    def isCollision(self, t1, t2):
        distance = math.sqrt(math.pow(t1.xGeben() - t2.xGeben(), 2) + math.pow(t1.yGeben() - t2.yGeben(), 2))
        if distance < 15:
            return True
        else:
            return False

    def shoot(self):
        if self.geschosssstatus == "Schussbereit":
            self.geschoss.xSetzen(self.spieler.xGeben())
            self.geschoss.ySetzen(self.spieler.yGeben() + 10)
            self.geschosssstatus = "abgefeuert"

    def Uebergabewerte_ermitteln(self):
        uebergabewerte = []
        for i in self.gegnerliste:
            uebergabewerte.append(i.xGeben())
            uebergabewerte.append(i.yGeben())
        uebergabewerte.append(self.spieler.xGeben())
        uebergabewerte.append(self.geschoss.yGeben())
        uebergabewerte.append(self.geschoss.xGeben())
        return uebergabewerte

    def maingameLoop(self):  # standard
        ch = 30
        while True:
            if not self.alive:
                self.reset()
            # if is_pressed("Left"):
            # self.moveLeft()

            # if is_pressed("Right"):
            # self.moveRight()

            # if is_pressed("Up"):
            # self.shoot()
            k = random.randint(0, ch)
            if k == 10:
                nB = self.NeuronalesNetz.evaluieren(self.score)
            if self.score == self.Monsteranzahl:
                print("Generation:" + str(self.Generation+1))
                print("Score:" + str(self.score))
                print("Gewonnen")
                self.saveNeuronalesNetz()
                break
            for gegner in self.gegnerliste:
                # Move the enemy
                x = gegner.xGeben()
                x += self.Gegnergeschwindigkeit
                gegner.xSetzen(x)
                if x > 280:
                    for e in self.gegnerliste:
                        y = e.yGeben() - 40
                        e.ySetzen(y)
                    self.Gegnergeschwindigkeit *= -1
                if x < -280:
                    self.Gegnergeschwindigkeit *= -1
                    for e in self.gegnerliste:
                        y = e.yGeben() - 40
                        e.ySetzen(y)

                    # Check for collision between bullet and enemy

                if self.isCollision(self.geschoss, gegner):
                    # x = random.randint(-200, 200)
                    # y = random.randint(100, 250)
                    # gegner.xSetzen(x)
                    # gegner.ySetzen(y)
                    self.gegnerliste.remove(gegner)
                    self.geschoss.xSetzen(500)
                    self.geschoss.ySetzen(500)
                    self.geschosssstatus = "Schussbereit"
                    self.score += 1

                    # Check for collision between enemy and player
                if gegner.yGeben() < self.spieler.yGeben():
                    # print("Game Over")
                    self.alive = False

            # Move the bullet
            if self.geschosssstatus == "abgefeuert":
                if self.geschoss.yGeben() < 280:

                    y = self.geschoss.yGeben()
                    y += self.Kugelgeschwindigkeit
                    self.geschoss.ySetzen(y)
                else:
                    self.geschosssstatus = "Schussbereit"
            uebergabewerte = self.Uebergabewerte_ermitteln()
            g = self.NeuronalesNetz.update(uebergabewerte)
            if g == 0:
                self.moveRight()
                # print("Rechts")
            elif g == 1:
                self.moveLeft()
                # print("Links")
            elif g == 2:
                # print("Schuss")
                self.shoot()

            if self.grafik == True:
                self.spa.aktualisiern(self.geschoss.xGeben(), self.geschoss.yGeben(), self.score, self.gegnerliste,
                                      self.spieler.xGeben(), self.geschosssstatus, self.Generation)
    def maingameLoopmin(self):  # standard

        while True:
            if not self.alive:
                self.reset()
            # if is_pressed("Left"):
            # self.moveLeft()

            # if is_pressed("Right"):
            # self.moveRight()

            # if is_pressed("Up"):
            # self.shoot()
            if self.score == self.Monsteranzahl:
                print("Gewonnen")
                break
            for gegner in self.gegnerliste:
                # Move the enemy
                x = gegner.xGeben()
                x += self.Gegnergeschwindigkeit
                gegner.xSetzen(x)
                if x > 280:
                    for e in self.gegnerliste:
                        y = e.yGeben() - 40
                        e.ySetzen(y)
                    self.Gegnergeschwindigkeit *= -1
                if x < -280:
                    self.Gegnergeschwindigkeit *= -1
                    for e in self.gegnerliste:
                        y = e.yGeben() - 40
                        e.ySetzen(y)

                    # Check for collision between bullet and enemy

                if self.isCollision(self.geschoss, gegner):
                    # x = random.randint(-200, 200)
                    # y = random.randint(100, 250)
                    # gegner.xSetzen(x)
                    # gegner.ySetzen(y)
                    self.gegnerliste.remove(gegner)
                    self.geschoss.xSetzen(500)
                    self.geschoss.ySetzen(500)
                    self.geschosssstatus = "Schussbereit"
                    self.score += 1

                    # Check for collision between enemy and player
                if gegner.yGeben() < self.spieler.yGeben():
                    # print("Game Over")
                    self.alive = False

            # Move the bullet
            if self.geschosssstatus == "abgefeuert":
                if self.geschoss.yGeben() < 280:

                    y = self.geschoss.yGeben()
                    y += self.Kugelgeschwindigkeit
                    self.geschoss.ySetzen(y)
                else:
                    self.geschosssstatus = "Schussbereit"
            if self.spieler.xGeben() > -180:
                self.moveLeft()
            else:
                self.shoot()
            if self.grafik == True:
                self.spa.aktualisiern(self.geschoss.xGeben(), self.geschoss.yGeben(), self.score, self.gegnerliste,
                                      self.spieler.xGeben(), self.geschosssstatus, self.Generation)

    def maingameloopzufaellig(self):
        while True:
            for AnzahlIndiviuals in range(0, 99):
                while True:
                    # if is_pressed("Left"):
                    # self.moveLeft()

                    # if is_pressed("Right"):
                    # self.moveRight()

                    # if is_pressed("Up"):
                    # self.shoot()
                    for gegner in self.gegnerliste:
                        # Move the enemy
                        x = gegner.xGeben()
                        x += self.Gegnergeschwindigkeit
                        gegner.xSetzen(x)
                        if x > 280:
                            for e in self.gegnerliste:
                                y = e.yGeben() - 40
                                e.ySetzen(y)
                            self.Gegnergeschwindigkeit *= -1
                        if x < -280:
                            self.Gegnergeschwindigkeit *= -1
                            for e in self.gegnerliste:
                                y = e.yGeben() - 40
                                e.ySetzen(y)

                            # Check for collision between bullet and enemy

                        if self.isCollision(self.geschoss, gegner):
                            # x = random.randint(-200, 200)
                            # y = random.randint(100, 250)
                            # gegner.xSetzen(x)
                            # gegner.ySetzen(y)
                            self.gegnerliste.remove(gegner)
                            self.geschoss.xSetzen(500)
                            self.geschoss.ySetzen(500)
                            self.geschosssstatus = "Schussbereit"
                            self.score += 1

                            # Check for collision between enemy and player
                        if gegner.yGeben() < self.spieler.yGeben():
                            # print("Game Over")
                            self.alive = False
                            self.resetz(AnzahlIndiviuals)
                            break
                    # Move the bullet
                    if self.geschosssstatus == "abgefeuert":
                        if self.geschoss.yGeben() < 280:

                            y = self.geschoss.yGeben()
                            y += self.Kugelgeschwindigkeit
                            self.geschoss.ySetzen(y)
                        else:
                            self.geschosssstatus = "Schussbereit"
                    uebergabewerte = self.Uebergabewerte_ermitteln()
                    g = self.NeuronaleNetze[AnzahlIndiviuals].update(uebergabewerte)
                    if g == 0:
                        self.moveRight()
                        # print("Rechts")
                    elif g == 1:
                        self.moveLeft()
                        # print("Links")
                    elif g == 2:
                        # print("Schuss")
                        self.shoot()

                    if self.grafik == True:
                        self.spa.aktualisiern(self.geschoss.xGeben(), self.geschoss.yGeben(), self.score,
                                              self.gegnerliste,
                                              self.spieler.xGeben(), self.geschosssstatus, self.Generation)

    def maingameloopbaum(self, zufall):  # Baum

            simscore = 0
            while True:
                timeb = time.time()
                if not self.alive:
                    self.resetbaum(zufall)
                # if is_pressed("Left"):
                # self.moveLeft()

                # if is_pressed("Right"):
                # self.moveRight()

                # if is_pressed("Up"):
                # self.shoot()
                if self.score == self.Monsteranzahl:
                    print("Gewonnen")
                    break
                for gegner in self.gegnerliste:
                    # Move the enemy
                    x = gegner.xGeben()
                    x += self.Gegnergeschwindigkeit
                    gegner.xSetzen(x)
                    if x > 280:
                        for e in self.gegnerliste:
                            y = e.yGeben() - 40
                            e.ySetzen(y)
                        self.Gegnergeschwindigkeit *= -1
                    if x < -280:
                        self.Gegnergeschwindigkeit *= -1
                        for e in self.gegnerliste:
                            y = e.yGeben() - 40
                            e.ySetzen(y)

                        # Check for collision between bullet and enemy

                    if self.isCollision(self.geschoss, gegner):
                        # x = random.randint(-200, 200)
                        # y = random.randint(100, 250)
                        # gegner.xSetzen(x)
                        # gegner.ySetzen(y)
                        self.gegnerliste.remove(gegner)
                        self.geschoss.xSetzen(500)
                        self.geschoss.ySetzen(500)
                        self.geschosssstatus = "Schussbereit"
                        self.score += 1
                        simscore = self.score * ((time.time()-timeb)/10)

                        # Check for collision between enemy and player
                    if gegner.yGeben() < self.spieler.yGeben():
                        # print("Game Over")
                        self.alive = False

                # Move the bullet
                if self.geschosssstatus == "abgefeuert":
                    if self.geschoss.yGeben() < 280:

                        y = self.geschoss.yGeben()
                        y += self.Kugelgeschwindigkeit
                        self.geschoss.ySetzen(y)
                    else:
                        self.geschosssstatus = "Schussbereit"
                # Move the player
                g = self.Baum.moveGeben(simscore)
                if g == "r":
                    self.moveRight()
                    # print("Rechts")
                elif g == "l":
                    self.moveLeft()
                    # print("Links")
                elif g == "s":
                    # print("Schuss")
                    self.shoot()


                if self.grafik == True:
                    self.spa.aktualisiern(self.geschoss.xGeben(), self.geschoss.yGeben(), self.score, self.gegnerliste,
                                          self.spieler.xGeben(), self.geschosssstatus, self.Generation)

    def reset(self):  # für standard
        random = True
        # Save Neuronales Netz to disc
        if self.NeuronalesNetz.score_to_beat < self.score:
            try:
                self.saveNeuronalesNetz()
                print("Neuronales Netz gespeichert")
            except:
                print("Neuronales Netz konnte nicht gespeichert werden")
        self.Generation += 1

        print("Generation: " + str(self.Generation))
        # self.show_change()
        # Gegner zurücksetzen
        self.Gegnerhinzufuegen()
        if random == False:
            self.Gegnersetzen_random()
        else:
            self.Gegnersetzen()
        # Spieler zurücksetzen
        self.spieler.xSetzen(0)
        # Score zurücksetzen
        print("Score: " + str(self.score))
        self.score = 0
        # Geschoss zurücksetzen
        self.geschoss.xSetzen(5000)
        # MainGameLoop neu starten
        self.alive = True

    def resetz(self, AnzahlNN):  # für zufall
        for i in range(0, AnzahlNN):
            # Save Neuronales Netz to disc
            if self.NeuronaleNetze[i].score_to_beat < self.score:
                try:
                    with open("NeuronalesNetz.pickle", "wb") as NN:
                        pickle.dump(self.NeuronaleNetze[i], NN)
                except Exception as ex:
                    print("Neuronales Netz konnte nicht gespeichert werden!")
            self.Generation = self.NeuronaleNetze[i].evaluieren(self.score)
        print("Generation: " + str(self.Generation))
        # self.show_change()
        # Gegner zurücksetzen
        self.Gegnerhinzufuegen()
        if random:
            self.Gegnersetzen_random()
        else:
            self.Gegnersetzen()
        # Spieler zurücksetzen
        self.spieler.xSetzen(0)
        # Score zurücksetzen
        print("Score: " + str(self.score))
        self.score = 0
        # Geschoss zurücksetzen
        self.geschoss.xSetzen(5000)
        # MainGameLoop neu starten
        self.alive = True

    def resetbaum(self, zufall: bool):
        # Baum zurücksetzen
        self.Baum.aktuellerKnoten = self.Baum.wurzel
        if self.Generation == self.gen:
            print("Hihscore: " + str(self.Baum.highscore))
            self.gen +=100
        self.Generation += 1
        #self.scoreueberzeit()
        print("Generation: " + str(self.Generation))
        # self.show_change()
        # Gegner zurücksetzen
        self.Gegnerhinzufuegen()
        if zufall:
            self.Gegnersetzen_random()
        else:
            self.Gegnersetzen()
        # Spieler zurücksetzen
        self.spieler.xSetzen(0)
        # Score zurücksetzen
        print("Score: " + str(self.score))
        self.score = 0
        # Geschoss zurücksetzen
        self.geschoss.xSetzen(5000)
        # MainGameLoop neu starten
        self.alive = True

    def saveNeuronalesNetz(self):
        try:
            with open("NeuronalesNetz.pickle", "wb") as NN:
                pickle.dump(self.NeuronalesNetz, NN)
        except Exception as ex:
            print("Neuronales Netz konnte nicht gespeichert werden!")

    def LoadNeuronaleNetz(self):
        try:
            with open("NeuronalesNetz.pickle", "rb") as NN:
                self.NeuronalesNetz = pickle.load(NN)

        except:
            print("Neuronales Netz konnte nicht geladen werden")

    def show_change(self):
        with open("NeuronalesNetz.pickle", "rb") as NN:
            NeuronalesN = pickle.load(NN)
        # Layer auswählen
        for i in range(1, len(NeuronalesN.layers) - 1):
            # Neuron
            for e in range(len(NeuronalesN.layers[i])):
                for k in range(0, len(NeuronalesN.layers[i][e].gewichte)):
                    ZP1 = NeuronalesN.layers[i][e].gewichte[k]
                    ZP2 = self.NeuronalesNetz.layers[i][e].gewichte[k]
                    print("An Stelle: Layer " + str(i) + "   Neuron " + str(e) + "   Gewicht " + str(
                        k) + "   change: " + str(ZP2 - ZP1))

    def scoreueberzeit(self):
        a = "=AVERAGE(B2:B" + str(self.Generation + 1) + ")"
        b = "=Sheet1!$C$2:$C$" + str(self.Generation + 1) + ")"
        workbook = xlsxwriter.Workbook("Diagramm.xlsx")
        chart = workbook.add_chart({"type": "line"})
        worksheet = workbook.add_worksheet()
        worksheet.write(self.Generation + 1, 0, self.Generation)
        worksheet.write(self.Generation + 1, 1, self.score)
        worksheet.write(self.Generation + 1, 2, a)
        chart.add_series(({
            "values": b
        }))
        worksheet.insert_chart("D5", chart)
        workbook.close()
