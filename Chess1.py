import matplotlib.pyplot as plt
import numpy as np
from PIL.Image import Image
from PIL import Image
from tkinter import *
from tkinter import ttk

root = Tk()

Im = Image.open("chessboard.png")
Im.show()

class Board:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.tiles = {} #dictionary of the tiles
        self.white_pieces = {} #dictionary of the white pieces
        self.black_pieces = {} #dictionary of the black pieces
    
    
    def select_piece(self):
        
    def setup(self): #sets up the pieces in the startin positions
        
    
    
class Game:
    
