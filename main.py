# Zum Testen
from multiprocessing import Pool
from Spielkonsole import *


def append_spk():
    return Spielkonsole(False, False)


if __name__ == '__main__':
    spk = Spielkonsole("standard", Grafischedarstellung=False, bestehendes_neuronales_Netz_laden=False)

# Options: "Baum","zufällig","standard", "minimal"

# Info: Baum kann noch nicht gespeichert oder geladen werden
