import pygame
import sys



class Tile:
    def __init__(self, file, rank, piece = None):
        self.rank = rank
        self.file = file
        self.piece = piece
    
    def samecolor(self,color):
        if self.piece != None:
            return self.piece.color == color
        elif self.piece == None:
            return False        

    def emptytile(self):
        return self.piece == None
    
    def has_piece(self):
        return self.piece != None

    def has_ally(self, color1):
        return self.piece != None and self.piece.color == color1
    
    def has_enemy(self, color1):
        return self.piece != None and self.piece.color != color1
    


def inrange(rank, file):
    return (file >= 0 and file <= 7) and (rank >= 0 and rank <= 7)

