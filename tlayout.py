import pygame
import sys

piecelist = ["wk", "wq", "wr", "wb", "wn", "wp", "bk", "bq", "br", "bb", "bn", "bp", 
             "wkh", "wqh", "wrh", "wbh", "wnh", "wph", "bkh", "bqh", "brh", "bbh", "bnh", "bph"]
Width = 512
Height = 512



class Board:
    def __init__(self, screen):
        self.screen = screen
        self.color = None
        self.board = [[] for _ in range(8)]
        self.board[0] = [Pawn("b",0,0), Pawn("b",1,0), Pawn("b",2,0), Pawn("b",3,0), Pawn("b",4,0), Pawn("b",5,0), Pawn("b",6,0), Pawn("b",7,0)]
        self.board[1] = [Pawn("b",0,1), Pawn("b",1,1), Pawn("b",2,1), Pawn("b",3,1), Pawn("b",4,1), Pawn("b",5,1), Pawn("b",6,1), Pawn("b",7,1)]
        self.board[6] = [Pawn("w",0,6), Pawn("w",1,6), Pawn("w",2,6), Pawn("w",3,6), Pawn("w",4,6), Pawn("w",5,6), Pawn("w",6,6), Pawn("w",7,6)]
        self.board[7] = [Pawn("w",0,7), Pawn("w",1,7), Pawn("w",2,7), Pawn("w",3,7), Pawn("w",4,7), Pawn("w",5,7), Pawn("w",6,7), Pawn("w",7,7)]
        
    
    def get_square(self, pos):
        return self.board[pos[1]][pos[0]]


class Pawn:
    def __init__(self, color, file, rank):
        self.color = color
        self.rank = rank
        self.file = file

    def legalmoves(self, board):
        firstmove = False
        potmoves = []
        if (self.color == "w" and self.rank == 6) or (self.color == "b" and self.rank == 1):
            firstmove = True
        if firstmove == True and board[self.file+2][self.rank] == None:
            potmoves.append((self.file+2, self.rank))
        


        
        


    def check_legalmove(self, pos):
        pass




def main():
    pygame.init()
    pygame.display.init()
    screen = pygame.display.set_mode((Width,Height))
    

main()
