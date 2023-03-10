import pygame
import sys



class Tile: #intialization of the Tile class
    def __init__(self, file, rank, piece = None):
        self.rank = rank #assigning rows
        self.file = file #assigning columns
        self.piece = piece #assigning piece or no piece to each square
    
    def samecolor(self,color): #checks to see which side a certain piece belongs to
        if self.piece != None:
            return self.piece.color == color
        elif self.piece == None:
            return False        

    def emptytile(self): #checks to see if a tile is empty
        return self.piece == None 
    
    def has_piece(self): #checks to see if a tile has a piece
        return self.piece != None

    def has_ally(self, color1): #checks to see if a tile has an allied piece for either side
        return self.piece != None and self.piece.color == color1
    
    def has_enemy(self, color1): #checks to see if a tile has an enemy piece for either side
        return self.piece != None and self.piece.color != color1
    


def inrange(rank, file): #defines the boundaries of the 8x8 board with 64 individual squares
    return (file >= 0 and file <= 7) and (rank >= 0 and rank <= 7)

