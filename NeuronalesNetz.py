import json
import random
import math


class NeuronalesNetz:
    def __init__(self, art: str, expected_inputs: int = 20):
        self.Art = art
        self.layers = []
        self.score_to_beat = 0
        self.averagescore = 0
        self.max_score = expected_inputs
        self.generation = 0
        self.Lernfaktor = 3
        self.InputLayer(expected_inputs)
        self.HiddenLayers(8)
        self.OutputLayer()


    def InputLayer(self, Inputs: int):
        Layer = []
        for i in range(0, Inputs*2+3):
            neuron = Inputneuron(0)
            Layer.append(neuron)
        self.layers.append(Layer)

    def HiddenLayers(self, AnzahlHiddenLayers: int):
        for i in range(0, AnzahlHiddenLayers):
            Layer = []
            for e in range(0, 8):
                neuron = Neuron(len(self.layers[i]))
                Layer.append(neuron)
            self.layers.append(Layer)

    def OutputLayer(self):
        Layer = []
        liste = []
        for q in range(len(self.layers[-1])):
            liste.append(self.layers[-1][q].output())
        for i in range(0, 4):
            neuron = Outputneuron(liste)
            Layer.append(neuron)
        self.layers.append(Layer)

    def update(self, liste: list):
        # Inputs aktualisieren
        for i in range(0, len(liste)):
            self.layers[0][i].changeinput(liste[i])

        return self.HiddenLayers_aktualisieren()

    def HiddenLayers_aktualisieren(self):
        # Layer auswählen
        for i in range(len(self.layers) - 2):
            # Neuron Output geben lassen
            for e in range(len(self.layers[i])):
                k = self.layers[i][e].output()
                # Output in nächste Layer übergeben
                for f in self.layers[i + 1]:
                    f.inputs[e] = k

        return self.OutputLayers_aktualisieren()

    def OutputLayers_aktualisieren(self):


        l =[self.layers[-1][0].output(),self.layers[-1][1].output(),self.layers[-1][2].output(),self.layers[-1][3].output()]
        k = l
        k.sort()
        return l.index(k[-1])


    def evaluieren(self, score: int):

        if self.score_to_beat != 0 or score != 0:
            if self.Art == "standard":
                self.baseline(score)

                for i in self.layers[1:-2]:
                    for e in i:
                        e.bias = e.bias + random.randint(-10,10)
                        for t in range(0, len(e.gewichte)):
                            try:
                                e.gewichte[t] = e.gewichte[t] - self.Lernfaktor * (score - self.max_score) * (
                                        math.log(e.Ausgabe) / e.gewichte[t])
                            except:
                                e.gewichte[t] = 0

                            #print(str(t) + str(e.gewichte[t]))

            elif self.Art == "zufällig":
                for i in self.layers[1:-2]:
                    for e in i:
                        if random.choice([True,False]):
                            e.bias = e.bias + random.randint(-10,10)
                        for t in range(0, len(e.gewichte)):
                            if random.choice([True, False]):
                                e.gewichte[t] = e.gewichte[t] - random.uniform(-1,1)
            if score > self.score_to_beat:
                self.score_to_beat = score
            self.generation += 1
            return self.generation
        else:
            Anfangslayer = self.layers[0]
            self.layers = [Anfangslayer]
            self.HiddenLayers(6)
            self.OutputLayer()

    def baseline(self, score):

        self.averagescore = ((self.averagescore * self.generation) + score) / (self.generation + 1)



class AbstractNeuron:
    def __init__(self):
        raise NotImplementedError()

    def output(self):
        raise NotImplementedError()

    def changeinput(self):
        raise NotImplementedError()


class Neuron(AbstractNeuron):
    def __init__(self, Anzahl_Inputs: int):
        self.inputs = []
        self.gewichte = []
        self.bias = random.randint(1, 50)
        for i in range(0, Anzahl_Inputs):
            self.inputs.append(0)
            self.gewichte.append(random.randint(1, 10))
        self.Ausgabe = 0

    def changeinput(self, index, neuerInput):
        self.inputs[index] = neuerInput

    def changebias(self, neuesbias):
        self.bias = neuesbias

    def changegewicht(self, i, neuesGewicht: int):
        self.gewichte[i] = neuesGewicht

    def output(self):
        x = 0

        for i in range(0, len(self.gewichte)):
            x = x + self.inputs[i] * self.gewichte[i]
        x = x + self.bias
        # print("x=" + str(x) + "   self.inputs[i]=" + str(self.inputs[i]) + "   self.gewichte[i]" + str(self.gewichte[i]))
        try:
            self.Ausgabe = 1 / (1 + math.exp(-x))
        except OverflowError:
            if x > 0:
                self.Ausgabe =  1
            elif x < 0:
                self.Ausgabe = 0

        #Step function
        #if x >= 0:
        #    self.Ausgabe=1
        #else:
        #    self.Ausgabe = 0
        return self.Ausgabe


class Inputneuron(AbstractNeuron):
    def __init__(self, input):
        self.inputs = [input]
        self.Preprocessingalgorithmus()

    def Preprocessingalgorithmus(self):
        self.inputs[0] = self.inputs[0] / 280

    def output(self):
        # print(str(self.input) + " Inputoutput")
        return self.inputs[0]

    def changeinput(self, neuerInput):
        self.inputs[0] = neuerInput
        self.Preprocessingalgorithmus()


class Outputneuron(Neuron):
    def __init__(self, liste: list):
        self.inputs = liste
        self.gewichte = []
        for i in range(len(self.inputs)):
            self.gewichte.append(random.randint(1, 10))
        self.bias = random.randint(0, 100)

