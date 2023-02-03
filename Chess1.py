import matplotlib.pyplot as plt
import numpy as np
from PIL.Image import Image
from PIL import Image

Im = Image.open("chessboard.png")
Im.show()

class Board:
    def __init__(self, screen, x, y, coin_image):
        self.screen = screen
        self.x = x
        self.y = y
    ImBoard = Image.open("chessboard.png")
    ImBoard.show()
class Game:
    
