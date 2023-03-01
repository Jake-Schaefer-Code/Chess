import pygame
import sys

class Pawn:
    def __init__(self, color):
        self.color = color
        self.imagename = self.color + "p"
        self.dir = -1 if self.color == "w" else 1

class Knight:
    def __init__(self, color):
        self.color = color
        self.imagename = self.color + "n"
        self.dir = -1 if self.color == "w" else 1

class Bishop:
    def __init__(self, color):
        self.color = color
        self.imagename = self.color + "b"
        self.dir = -1 if self.color == "w" else 1

class Rook:
    def __init__(self, color):
        self.color = color
        self.imagename = self.color + "r"
        self.dir = -1 if self.color == "w" else 1

class Queen:
    def __init__(self, color):
        self.color = color
        self.imagename = self.color + "q"
        self.dir = -1 if self.color == "w" else 1

class King:
    def __init__(self, color):
        self.color = color
        self.imagename = self.color + "k"
        self.dir = -1 if self.color == "w" else 1