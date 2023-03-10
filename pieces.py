import pygame
import sys
piecevals = {"p": 10, "n": 30, "b": 35, "r": 50, "q": 90, "k": 900}



class Pawn:
    def __init__(self, color):
        self.color = color
        self.value = piecevals["p"]
        self.imagename = self.color + "p"
        self.dir = -1 if self.color == "w" else 1

class Knight:
    def __init__(self, color):
        self.color = color
        self.value = piecevals["n"]
        self.imagename = self.color + "n"
        self.dir = -1 if self.color == "w" else 1

class Bishop:
    def __init__(self, color):
        self.color = color
        self.value = piecevals["b"]
        self.imagename = self.color + "b"
        self.dir = -1 if self.color == "w" else 1

class Rook:
    def __init__(self, color):
        self.color = color
        self.value = piecevals["r"]
        self.imagename = self.color + "r"
        self.dir = -1 if self.color == "w" else 1

class Queen:
    def __init__(self, color):
        self.color = color
        self.value = piecevals["q"]
        self.imagename = self.color + "q"
        self.dir = -1 if self.color == "w" else 1

class King:
    def __init__(self, color):
        self.color = color
        self.value = piecevals["k"]
        self.imagename = self.color + "k"
        self.dir = -1 if self.color == "w" else 1
