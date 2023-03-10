import pygame
import sys
piecevals = {"p": 10, "n": 30, "b": 35, "r": 50, "q": 90, "k": 900} # initialization for the relative values of each piece in order of priority



class Pawn: # intialization of the pawn class
    def __init__(self, color):
        self.color = color # allows a color to be assigned to the pawn
        self.value = piecevals["p"] #accesses the value dictionary written above
        self.imagename = self.color + "p" #accessing the name of the pawn by combining the color with the letter p 
        self.dir = -1 if self.color == "w" else 1 #assigns a direction to the piece

class Knight: # intialization of the knight class
    def __init__(self, color):
        self.color = color # allows a color to be assigned
        self.value = piecevals["n"] #accesses the value dictionary written above
        self.imagename = self.color + "n" #accessing the name of the knight by combining the color with the letter n
        self.dir = -1 if self.color == "w" else 1 #assigns a direction to the piece

class Bishop: # intialization of the bishop class
    def __init__(self, color):
        self.color = color # allows a color to be assigned
        self.value = piecevals["b"] #accesses the value dictionary written above
        self.imagename = self.color + "b" #accessing the name of the bishop by combining the color with the letter b
        self.dir = -1 if self.color == "w" else 1 #assigns a direction to the piece

class Rook: # intialization of the rook class
    def __init__(self, color):
        self.color = color # allows a color to be assigned
        self.value = piecevals["r"] #accesses the value dictionary written above
        self.imagename = self.color + "r" #accessing the name of the rook by combining the color with the letter r
        self.dir = -1 if self.color == "w" else 1 #assigns a direction to the piece

class Queen: # intialization of the queen class
    def __init__(self, color):
        self.color = color # allows a color to be assigned
        self.value = piecevals["q"] #accesses the value dictionary written above
        self.imagename = self.color + "q" #accessing the name of the queen by combining the color with the letter q
        self.dir = -1 if self.color == "w" else 1 #assigns a direction to the piece

class King: # intialization of the king class
    def __init__(self, color):
        self.color = color # allows a color to be assigned
        self.value = piecevals["k"] #accesses the value dictionary written above
        self.imagename = self.color + "k" #accessing the name of the king by combining the color with the letter k
        self.dir = -1 if self.color == "w" else 1 #assigns a direction to the piece
