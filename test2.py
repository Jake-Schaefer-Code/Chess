import pygame
import sys


piecelist = ["wk", "wq", "wr", "wb", "wn", "wp", "bk", "bq", "br", "bb", "bn", "bp"]
piecedic = {}
squaredic = {}
column = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}
Width = 512
Height = 512




class Board:
    def __init__(self, screen):
        self.screen = screen
        self.color = None
        self.board = [["--","--","--","--","--","--","--","--"] for _ in range(8)]
        self.board[0] = ["br","bn","bb","bq","bk","bb","bn","br"]
        self.board[1] = ["bp","bp","bp","bp","bp","bp","bp","bp"]
        self.board[6] = ["wp","wp","wp","wp","wp","wp","wp","wp"]
        self.board[7] = ["wr","wn","wb","wq","wk","wb","wn","wr"]
        print(self.board)
    
    def get_square(self, pos):
        self.col = pos[0]
        self.row = pos[1]
        return self.board[self.row][self.col]
    
    def moveto(self, pos1, pos2):
        piece1 = self.board[pos1[1]][pos1[0]]
        piece2 = self.board[pos2[1]][pos2[0]]
        if piece1 != "--" and piece2[0] != piece1[0]:
            self.board[pos1[1]][pos1[0]] = "--"
            self.board[pos2[1]][pos2[0]] = piece1
        elif piece2[0] == piece1[0]:
            print("cannot take your own piece")
        if piece2[0] != piece1[0] and piece2[0] != "-":
            print("captured")
        

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

    def draw_piece(self):
        for i in range(8):
            for j in range(8):
                
                piece = self.board[j][i]
                if piece != "--":
                    self.screen.blit(pygame.transform.scale(piecedic[piece],(Width//8,Height//8)), pygame.Rect((Width//8)*i,(Height//8)*j,Width//8,Height//8))

class Movement:
    def __init__(self, screen, boardclass, board, pos1, pos2):
        self.screen = screen
        self.board = board
        self.boardclass = boardclass
        self.pos1 = pos1
        self.pos2 = pos2
        self.sq1 = board[pos1[1]][pos1[0]]
        self.sq2 = board[pos2[1]][pos2[0]]
        
    def moveP(self):
        if self.pos1[0] == self.pos2[0]:
            self.boardclass.moveto(self.pos1,self.pos2)

    def moveN(self):
        print("move knight")
    def moveB(self):
        print("move bishop")
    def moveR(self):
        print("move rook")
    def moveQ(self):
        print("move queen")
    def moveK(self):
        print("move king")

        
def main():
    pygame.init()
    pygame.display.init()
    screen = pygame.display.set_mode((Width,Height))
    screen.fill(pygame.Color("white"))
    board1 = Board(screen)
    for piece in piecelist:
        piecedic[piece] = pygame.image.load("chess_pieces/"+piece+".PNG")
    square = pygame.Rect((0,0), (512,512))
    
   
    
    

    
    

    
    clicks = []
    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # left mouse button?
                    pos1 = board1.makeButton(event.pos, square)
                    print(pos1)
                    clicks.append(pos1)
                    if len(clicks) == 2:
                        piece1 = board1.get_square(clicks[0])
                        if piece1 != "":
                            move = Movement(screen, board1, board1.board, clicks[0],clicks[1])
                            movedic = {"p":move.moveP,"n":move.moveN,"b":move.moveB, "r":move.moveR, "q":move.moveQ, "k":move.moveK}
                            movedic[piece1[1]]()
                            #board1.moveto(clicks[0],clicks[1])
                            
                        clicks = []
                              
        

        pygame.display.set_caption("Chess")
        boardimage = pygame.image.load("WhiteBackground.jpeg")
        screen.blit(boardimage, (0, 0))
        board1.draw()
        board1.draw_piece()
        pygame.display.update()


main()
