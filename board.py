import pygame
import sys
from Tile import *
from pieces import *

piecelist = ["wk", "wq", "wr", "wb", "wn", "wp", "bk", "bq", "br", "bb", "bn", "bp", 
             "wkh", "wqh", "wrh", "wbh", "wnh", "wph", "bkh", "bqh", "brh", "bbh", "bnh", "bph"]
piecedic = {}
squaredic = {}
Width = 512
Height = 512
turns = []

#IMPORTANT: calling a piece on the board acts like board[rank][file] or board[y][x]

class Board:
    def __init__(self, screen):
        self.screen = screen
        self.color = None
        self.curteam = "w"
        self.board = [[Tile(0,0),Tile(0,0),Tile(0,0),Tile(0,0),Tile(0,0),Tile(0,0),Tile(0,0),Tile(0,0)] for _ in range(8)]
        for rank in range(8):
            for file in range(8):
                self.board[rank][file] = Tile(file, rank)
        self.board[0] = [Tile(0,0,Rook("b")), Tile(1,0,Knight("b")), Tile(2,0,Bishop("b")), Tile(3,0,Queen("b")),
                         Tile(4,0,King("b")), Tile(5,0,Bishop("b")), Tile(6,0,Knight("b")), Tile(7,0,Rook("b"))]
        self.board[1] = [Tile(0,1,Pawn("b")), Tile(1,1,Pawn("b")), Tile(2,1,Pawn("b")), Tile(3,1,Pawn("b")),
                         Tile(4,1,Pawn("b")), Tile(5,1,Pawn("b")), Tile(6,1,Pawn("b")), Tile(7,1,Pawn("b"))]        
        self.board[6] = [Tile(0,6,Pawn("w")), Tile(1,6,Pawn("w")), Tile(2,6,Pawn("w")), Tile(3,6,Pawn("w")),
                         Tile(4,6,Pawn("w")), Tile(5,6,Pawn("w")), Tile(6,6,Pawn("w")), Tile(7,6,Pawn("w"))]       
        self.board[7] = [Tile(0,7,Rook("w")), Tile(1,7,Knight("w")), Tile(2,7,Bishop("w")), Tile(3,7,Queen("w")),
                         Tile(4,7,King("w")), Tile(5,7,Bishop("w")), Tile(6,7,Knight("w")), Tile(7,7,Rook("w"))]
        

    def get_square(self, pos):
        return self.board[pos[1]][pos[0]]
    
    def draw(self):
        for i in range(8):
            for j in range(8):
                if (i+1)%2 == 1 and (8-j)%2 == 1:
                     self.color = (169,108,69)
                elif (i+1)%2 == 0 and (8-j)%2 == 0:
                    self.color = (169,108,69)
                else:
                    self.color = (245,198,156)
                pygame.draw.rect(self.screen, self.color, pygame.Rect((Width//8)*i,(Height//8)*j,Width//8,Height//8))
                squaredic[(j,i)] = pygame.Rect((Width//8)*i,(Height//8)*j,Width//8,Height//8)

    def makeButton(self, cur, rect):
            if rect.collidepoint(cur):
                pos1 = pygame.mouse.get_pos()[0]//(Width//8)
                pos2 = pygame.mouse.get_pos()[1]//(Height//8)
                return (pos1,pos2)
    
    def moveTo(self, piece, pos1, pos2):
        self.board[pos1[1]][pos1[0]] = Tile(pos1[0],pos1[1])
        self.board[pos2[1]][pos2[0]] = Tile(pos2[0],pos2[1],piece)
        turns.append((pos1,pos2))

    def callmove(self, piece, rank, file):
        move = Movetypes(piece, rank, file, self.board)
        if isinstance(piece, Pawn):
            return move.p_moves()
        if isinstance(piece, Knight):
            return move.n_moves()
        if isinstance(piece, Bishop):
            return move.b_moves()
        if isinstance(piece, Rook):
            return move.r_moves()
        if isinstance(piece, Queen):
            return move.q_moves()
        if isinstance(piece, King):
            return move.k_moves()
    
    def get_all_moves(self):
        self.all_moves_white = []
        self.all_moves_black = []
        self.list1 = []
        for rank in self.board:
            for file in rank:
                if file.piece != None:
                    if file.piece.color == self.curteam:
                        self.list1 = self.callmove(file.piece, file.rank, file.file)
                        if type(self.list1) is list:
                            self.all_moves_white += self.list1
                    if file.piece.color != self.curteam:
                        self.list1 = self.callmove(file.piece, file.rank, file.file)
                        if type(self.list1) is list:
                            self.all_moves_black += self.list1

                        
        return(self.all_moves_white, self.all_moves_black)
    
    def incheck(self, king, kingpos):
        king_moves = self.callmove(king, kingpos[1],kingpos[0])
        moves = []
        if self.curteam == "w":
            moves = self.get_all_moves()[1]
        elif self.curteam == "b":
            moves = self.get_all_moves()[0]
        if kingpos in moves:
            print("in check")
        if type(king_moves) is list:
            while True:
                for m in king_moves:
                    if m not in moves:
                        break
                    elif m == king_moves[-1] and m in moves:
                        print("checkmate")
                        break


        
        
        


    def nextturn(self):
        self.curteam = "b" if self.curteam == "w" else "w"




    
def draw_piece(screen,tile):
    if tile.piece != None:
        image = tile.piece.imagename
        screen.blit(pygame.transform.scale(piecedic[image],(Width//8,Height//8)), pygame.Rect((Width//8)*tile.file,(Height//8)*tile.rank,Width//8,Height//8))



class Movetypes: #maybe put these in the board class? this may not be optimal
    def __init__(self, piece, rank, file, board):
        self.piece = piece
        self.rank = rank
        self.file = file
        self.board = board
        self.potmoves = []
    
    def p_moves(self):
        firstmove = False
        
        dir = []
        if self.piece.color == "w":
            dir = [(1,-1),(-1,-1)]
        elif self.piece.color == "b":
            dir = [(1,1),(-1,1)]
        
        if (self.piece.color == "w" and self.rank == 6) or (self.piece.color == "b" and self.rank == 1):
            firstmove = True
        if self.piece.color == "w":
            if self.board[self.rank-1][self.file].piece == None:
                self.potmoves.append((self.file, self.rank-1))
            if firstmove == True and self.board[self.rank-2][self.file].piece == None:
                self.potmoves.append((self.file, self.rank-2))
                   
        elif self.piece.color == "b":
            if firstmove == True and self.board[self.file][self.rank-2].piece == None:
                self.potmoves.append((self.file, self.rank+2))
            if self.board[self.file][self.rank-1].piece == None:
                self.potmoves.append((self.file, self.rank+1))
        
        for d in dir:
            if inrange(self.rank+d[1],self.file+d[0]):
                if self.board[self.rank+d[1]][self.file+d[0]].piece != None:
                    if not self.board[self.rank][self.file].samecolor(self.board[self.rank+d[1]][self.file+d[0]].piece.color):
                        self.potmoves.append((self.file+d[0],self.rank+d[1]))
                

        return self.potmoves
    
    def n_moves(self):
        moves = [(x,y) for y in range(8) if abs(self.rank-y) == 2 for x in range(8) if abs(self.file-x) == 1] + [
            (x,y) for y in range(8) if abs(self.rank-y) == 1 for x in range(8) if abs(self.file-x) == 2]
        for x,y in moves:
            itertile = Tile(x, y, self.board[y][x].piece)
            if itertile.emptytile() or not itertile.has_ally(self.piece.color):
                self.potmoves.append((x,y))
        return self.potmoves
    
    def b_moves(self):
        dir = [(1,1),(-1,1),(-1,-1),(1,-1)]
        self.potmoves+=self.straight_move(dir)
        return self.potmoves
    
    def r_moves(self):
        dir = [(1,0),(-1,0),(0,1),(0,-1)]
        self.potmoves+=self.straight_move(dir)
        return self.potmoves
    
    def q_moves(self):
        dir = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,1),(-1,-1),(1,-1)]
        self.potmoves+=self.straight_move(dir)
        return self.potmoves
    
    def k_moves(self):
        #self.potmoves = []
        #return self.potmoves
        return []

    def straight_move(self, dir): #this works for diagonals and straight lines
        smoves = [] #temporary list for straight moves - will make a move class or a total moves list in future
        for d in dir:
            rank_dir, file_dir = d
            rank_move = self.rank + rank_dir
            file_move = self.file + file_dir

            while True:
                if inrange(rank_move, file_move):
                    itertile = Tile(rank_move, file_move, self.board[rank_move][file_move].piece)

                    if itertile.emptytile(): #maybe put this in board class so can just call self.board[rank][file].emptytile
                        smoves.append((file_move,rank_move)) 
                    elif not itertile.emptytile():
                        if not itertile.has_ally(self.piece.color):
                            smoves.append((file_move,rank_move)) 
                            break
                        elif itertile.has_ally(self.piece.color):
                            break
                else:
                    break
                rank_move = rank_move + rank_dir
                file_move = file_move + file_dir
        return smoves
        






def main():
    
    pygame.init()
    pygame.display.init()
    screen = pygame.display.set_mode((Width,Height))
    board1 = Board(screen)
    for piece in piecelist:
        piecedic[piece] = pygame.image.load("chess_pieces/"+piece+".PNG")
    square = pygame.Rect((0,0), (512,512))
    startsq, piece1, piecemoves = None, None, None
    clicks = []
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                   
                    #We should probably go over this again we might be able to simplify
                    
                    selectedsq = board1.makeButton(event.pos, square)
                    selectedpiece = board1.get_square(selectedsq).piece
                    if selectedpiece != None:
                        if len(clicks) == 0 and selectedpiece.color == board1.curteam:
                            clicks.append(selectedsq)
                            startsq = selectedsq
                        elif len(clicks) == 1 and startsq == selectedsq:
                            selectedpiece.imagename = selectedpiece.imagename[:2]
                            clicks = []
                            startsq = None
                        elif len(clicks) == 1 and selectedpiece.color != board1.curteam:
                            clicks.append(selectedsq)

                        if len(clicks) == 1 and selectedpiece.color == board1.curteam:
                            piece1 = selectedpiece
                            selectedpiece.imagename = selectedpiece.imagename + "h"
                            piecemoves = board1.callmove(piece1, clicks[0][1], clicks[0][0])
                            allmoves = board1.get_all_moves()
                            print(allmoves)
                            print(piecemoves)

                    elif selectedpiece == None and len(clicks)==0:
                        clicks = []
                    
                    else:
                        clicks.append(selectedsq)
                        startsq = selectedsq
                    
                    if len(clicks) == 2 and piece1 != None:
                        piece1.imagename = piece1.imagename[:2]
                        if piece1.color == board1.curteam and clicks[1] in piecemoves:
                            board1.moveTo(piece1, clicks[0],clicks[1])
                            board1.nextturn()
                            
                        clicks = []
                    #print(clicks)
        
        pygame.display.set_caption("Chess")
        boardimage = pygame.image.load("WhiteBackground.jpeg")
        screen.blit(boardimage, (0, 0))
        board1.draw()
        for rank in board1.board:
            for p in rank:
                draw_piece(screen,p)
        pygame.display.update()

main()
