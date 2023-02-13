import matplotlib.pyplot as plt
import numpy as np
from PIL.Image import Image
from PIL import Image
from tkinter import *

root = Tk()
frm = ttk.Frame(root, padding=10) #testing stuff from the tkinter python interface

Im = Image.open("chessboard.png")
Im.show()

coordsx = {}
coordsy = {}

class Board:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.square_color = ""
        self.white_pieces = {} #dictionary of the white pieces
        self.black_pieces = {} #dictionary of the black pieces
        
        #define coordinates of the chess board system
    
    def coordinates(self, screen):
        for i in range(8):
            for j in range(8):
                coordsx[(i+1)] = ((i)*(width/8),(i+1)*(width/8)) #defines each square to be 1/8 of the board
                coordsy[(j+1)] = ((j)*(width/8),(j+1)*(width/8))
                if (i+1)%2 == 1:
                    self.square_color = "black"
                elif (i+1)%2 == 0:
                    self.square_color = "white"
                #draw each square now
                
        
    
    
    def select_piece(self):
        #define where the mouse clicks
        #make sure it is your piece that is clicked
        #check the type of the piece
        #make sure that it is your turn
        #highlight the space where clicked (potentially highlight the potential paths when click arrow keys)
        
        
    def setup(self): #sets up the pieces in the startin positions
        #sets up 16 blank pieces on each side and defines each of those pieces with an image and a type based on their coordinate postion
        
    
    
class Game:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        
class Movement:
    def __init__(self, screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y
    
