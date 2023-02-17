import pygame
import sys

piecelist = ["wk", "wq", "wr", "wb", "wn", "wp", "bk", "bq", "br", "bb", "bn", "bp"]
piecedic = {}

class Board():
    def __init__(self):
        pass




def main():
    pygame.init()
    pygame.display.init()
    for piece in piecelist:
        piecedic[piece] = pygame.image.load(piece+".PNG")
        boardimage = pygame.image.load("chessboard.png")
        screen = pygame.display.set_mode((boardimage.get_width(), boardimage.get_height()))


    while True:
        pygame.display.update()

main()