import random


class Neuron:
    def __init__(self):
        self.bias = random.randint(-100, 100)

n = Neuron()
print(n.bias)