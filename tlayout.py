import pygame
import sys

piecelist = ["wk", "wq", "wr", "wb", "wn", "wp", "bk", "bq", "br", "bb", "bn", "bp", 
             "wkh", "wqh", "wrh", "wbh", "wnh", "wph", "bkh", "bqh", "brh", "bbh", "bnh", "bph"]
piecedic = {}
squaredic = {}
Width = 512
Height = 512
turns = []


class Board:
    def __init__(self, screen):
        self.screen = screen
        self.color = None
        self.board = [[[],[],[],[],[],[],[],[]] for _ in range(8)]
        self.board[0] = [[Pawn("b",0,0)], [Pawn("b",1,0)], [Pawn("b",2,0)], [Pawn("b",3,0)], [Pawn("b",4,0)], [Pawn("b",5,0)], [Pawn("b",6,0)], [Pawn("b",7,0)]]
        self.board[1] = [[Pawn("b",0,1)], [Pawn("b",1,1)], [Pawn("b",2,1)], [Pawn("b",3,1)], [Pawn("b",4,1)], [Pawn("b",5,1)], [Pawn("b",6,1)], [Pawn("b",7,1)]]
        self.board[6] = [[Pawn("w",0,6)], [Pawn("w",1,6)], [Pawn("w",2,6)], [Pawn("w",3,6)], [Pawn("w",4,6)], [Pawn("w",5,6)], [Pawn("w",6,6)], [Pawn("w",7,6)]]
        self.board[7] = [[Pawn("w",0,7)], [Pawn("w",1,7)], [Pawn("w",2,7)], [Pawn("w",3,7)], [Pawn("w",4,7)], [Pawn("w",5,7)], [Pawn("w",6,7)], [Pawn("w",7,7)]]

        
    
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
        self.board[pos1[0]][pos1[1]] = []
        self.board[pos2[0]][pos2[1]] = [piece]
        print(self.board)
        turns.append((pos1,pos2))






class Pawn:
    def __init__(self, color, file, rank):
        self.color = color
        self.rank = rank
        self.file = file
        self.imagename = self.color + "p"

    def legalmoves(self, board):
        firstmove = False
        self.potmoves = []
        dir = [(1,-1),(-1,-1)]
        if (self.color == "w" and self.rank == 6) or (self.color == "b" and self.rank == 1):
            firstmove = True
    
        if firstmove == True and board[self.file][self.rank-2] == []:
            self.potmoves.append((self.file, self.rank-2))
        if board[self.file][self.rank-1] == []:
            self.potmoves.append((self.file, self.rank-1))
        for d in dir:
            if board[self.file+d[0]][self.rank+d[1]] != []:
                print(board[self.file+d[0]][self.rank+d[1]])
                if not samecolor(self.file,self.rank,self.file+d[0],self.rank+d[1],board):
                    self.potmoves.append((self.file+d[0],self.rank+d[1]))
        #print(self.potmoves)

    def check_legalmoves(self, pos1, pos2, boardclass):
        if pos2 in self.potmoves:
            self = Pawn(self.color, pos2[0], pos2[1])
            boardclass.moveTo(self, pos1, pos2)
            #print(self)

    def draw(self,screen):
        self.screen = screen
        self.screen.blit(pygame.transform.scale(piecedic[self.imagename],(Width//8,Height//8)), pygame.Rect((Width//8)*self.file,(Height//8)*self.rank,Width//8,Height//8))



#maybe create a module called "constraints" so we can import these functions
def inrange(file,rank):
    return (file >= 0 and file <= 7) and (rank >= 0 and rank <= 7)
        
def samecolor(file1,rank1,file2,rank2,board):
    return board[file1][rank1][0].color == board[file2][rank2][0].color



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
                    if (len(clicks) == 0 and board1.get_square(selectedsq) == None):
                        clicks = []
                    elif sq1 == selectedsq and len(clicks) == 1:
                        print("unhighlight")
                        clicks = []
                        sq1 = None
                    else:
                        clicks.append(selectedsq)
                        sq1 = selectedsq
                        piece1 = board1.get_square(clicks[0])[0]
                        if len(clicks) == 1:
                            print("highlight")
                    
                    if len(clicks) == 2:
                        print("unhighlight")
                        piece1 = board1.get_square(clicks[0])[0]
                        if piece1 == None:
                            clicks = []
                        elif len(turns)%2==0 and piece1.color == "w": #white's move - should probably create a variable for white vs black turns that updates
                            piece1.legalmoves(board1.board)
                            piece1.check_legalmoves(clicks[0], clicks[1], board1)
                            print(board1.board)
                        elif len(turns)%2==1 and piece1.color == "b":
                            pass
                        
                


        
        pygame.display.set_caption("Chess")
        boardimage = pygame.image.load("WhiteBackground.jpeg")
        screen.blit(boardimage, (0, 0))
        board1.draw()
        for rank in board1.board:
            for p in rank:
                if p != []:
                    p[0].draw(screen)
        pygame.display.update()



main()
