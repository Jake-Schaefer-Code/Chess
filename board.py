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

    def movepiece(self, piece):
        pass
    



    
def draw_piece(screen,tile):
    if tile.piece != None:
        image = tile.piece.imagename
        screen.blit(pygame.transform.scale(piecedic[image],(Width//8,Height//8)), pygame.Rect((Width//8)*tile.file,(Height//8)*tile.rank,Width//8,Height//8))



class Movetypes:
    def __init__(self, piece, rank, file, board):
        self.piece = piece
        self.rank = rank
        self.file = file
        self.board = board
    
    def straight_move(self, dir): #this works for diagonals and straight lines
        smoves = [] #temporary list for straight moves - will make a move class or a total moves list in future
        for d in dir:
            rank_dir, file_dir = d
            rank_move = self.rank + rank_dir
            file_move = self.file + file_dir

            while True:
                if inrange(rank_move, file_move):
                    if Tile(rank_move, file_move, self.board[rank_move][file_move]).emptytile: #maybe put this in board class so can just call self.board[rank][file].emptytile
                        smoves.append((file_move,rank_move)) 
                    elif not Tile(rank_move, file_move, self.board[rank_move][file_move]).has_ally:
                        smoves.append((file_move,rank_move)) 
                        break
                    elif Tile(rank_move, file_move, self.board[rank_move][file_move]).has_ally:
                        break
                else:
                    break
                rank_move = rank_move + rank_dir
                file_move = file_move + file_dir






def main():
    pygame.init()
    pygame.display.init()
    screen = pygame.display.set_mode((Width,Height))
    board1 = Board(screen)
    for piece in piecelist:
        piecedic[piece] = pygame.image.load("chess_pieces/"+piece+".PNG")
    square = pygame.Rect((0,0), (512,512))
    sq1 = None
    clicks = []
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    selectedsq = board1.makeButton(event.pos, square)
                    
                    if (len(clicks) == 0 and board1.get_square(selectedsq) == []):
                        clicks = []
                    elif sq1 == selectedsq and len(clicks) == 1:
                        #print("unhighlight")
                        clicks = []
                        sq1 = None
                    else:
                        clicks.append(selectedsq)
                        sq1 = selectedsq
                        piece1 = board1.get_square(clicks[0])
                        if len(clicks) == 1:
                            #print("highlight")
                            pass
                    print(clicks)
                    if len(clicks) == 2:
                        #print("unhighlight")
                        piece1 = board1.get_square(clicks[0])
                        if piece1 == None:
                            clicks = []
                        elif len(turns)%2==0 and piece1.piece.color == "w": #white's move - should probably create a variable for white vs black turns that updates
                            print(clicks[0], clicks[1])
                            board1.moveTo(piece1.piece, clicks[0],clicks[1])

                        
                        elif len(turns)%2==1 and piece1.piece.color == "b":
                            print(clicks[0], clicks[1])

                            
                        clicks = []
                        
                


        
        pygame.display.set_caption("Chess")
        boardimage = pygame.image.load("WhiteBackground.jpeg")
        screen.blit(boardimage, (0, 0))
        board1.draw()
        for rank in board1.board:
            for p in rank:
                draw_piece(screen,p)
        pygame.display.update()



main()
