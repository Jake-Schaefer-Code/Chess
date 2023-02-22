import pygame
import sys


piecelist = ["wk", "wq", "wr", "wb", "wn", "wp", "bk", "bq", "br", "bb", "bn", "bp"]
piecedic = {}
squaredic = {}
column = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}
Width = 512
Height = 512
turns = []

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
            turns.append((pos1,pos2))
        elif piece2[0] == piece1[0]:
            print("cannot take your own piece")
        if (piece2[0] != piece1[0]) and (piece2[0] != "-"):
            print("captured")
        else:
            print("not captured")
        

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

    def draw_piece(self): #checks each square on the board for a piece and draws it if there is one
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
        firstmove = False

        if self.sq1[0] == "w":
            if self.pos1[1] == 6:
                firstmove = True


            
            if self.pos1[0] == self.pos2[0] and self.sq2[0] != "b":
                if self.pos1[1] > self.pos2[1]:
                    if firstmove and (self.pos1[1] == self.pos2[1] + 2 or self.pos1[1] == self.pos2[1] + 1):
                        self.boardclass.moveto(self.pos1,self.pos2)
                        print("move white pawn")
                    elif self.pos1[1] == self.pos2[1] + 1:
                        self.boardclass.moveto(self.pos1,self.pos2)
                        print("move white pawn")
            elif self.sq2[0] == "b":
                if self.pos1[1] > self.pos2[1] and (self.pos1[1] == self.pos2[1] + 1):
                    if self.pos1[0] == self.pos2[0] + 1 or self.pos1[0] == self.pos2[0] - 1:
                        self.boardclass.moveto(self.pos1,self.pos2)
                        print("move white pawn")


        if self.sq1[0] == "b":
            if self.pos1[1] == 1:
                firstmove = True

            if self.pos1[0] == self.pos2[0] and self.sq2[0] != "w":
                if self.pos1[1] < self.pos2[1]:
                    if firstmove and (self.pos1[1] == self.pos2[1] - 2 or self.pos1[1] == self.pos2[1] - 1):
                        self.boardclass.moveto(self.pos1,self.pos2)
                        print("move black pawn")
                    elif self.pos1[1] == self.pos2[1] - 1:
                        self.boardclass.moveto(self.pos1,self.pos2)
                        print("move black pawn")         
            elif self.sq2[0] == "w":
                if self.pos1[1] < self.pos2[1] and (self.pos1[1] == self.pos2[1] - 1):
                    if self.pos1[0] == self.pos2[0] + 1 or self.pos1[0] == self.pos2[0] - 1:
                        self.boardclass.moveto(self.pos1,self.pos2)
                        print("move black pawn")
                        

    def moveN(self):
        if abs(self.pos1[0]-self.pos2[0]) == 2 and abs(self.pos1[1]-self.pos2[1]) == 1:
            if self.sq1[0] == "w" and self.sq2[0] != "w":
                self.boardclass.moveto(self.pos1,self.pos2)
                print("move white knight")
            elif self.sq1[0] == "b" and self.sq2[0] != "b":
                self.boardclass.moveto(self.pos1,self.pos2)
                print("move black knight")
        elif abs(self.pos1[0]-self.pos2[0]) == 1 and abs(self.pos1[1]-self.pos2[1]) == 2:
            if self.sq1[0] == "w" and self.sq2[0] != "w":
                self.boardclass.moveto(self.pos1,self.pos2)
                print("move white knight")
            elif self.sq1[0] == "b" and self.sq2[0] != "b":
                self.boardclass.moveto(self.pos1,self.pos2)
                print("move black knight")


    def moveB(self):
        dx = self.pos2[0] - self.pos1[0]
        dy = self.pos2[1] - self.pos1[1]
        if abs(dx) == abs(dy):  # diagonal move
                # check if there are any pieces in between
                blocked = False
                steps = abs(dx) - 1
                x_dir = 1 if dx > 0 else -1
                y_dir = 1 if dy > 0 else -1
                for step in range(steps):
                    x = self.pos1[0] + x_dir * (step + 1)
                    y = self.pos1[1] + y_dir * (step + 1)
                    if self.board[y][x] != "--":
                        blocked = True
                if blocked != True:
                    self.boardclass.moveto(self.pos1,self.pos2)

            
    def moveR(self):
        dx = self.pos2[0] - self.pos1[0]
        dy = self.pos1[1] - self.pos2[1]
        blocked = False
        if dx == 0:
            y_dir = 1 if dy > 0 else -1
            steps = abs(dy) - 1
            for step in range(steps):
                y = self.pos2[1] + y_dir * (step + 1)
                x = self.pos1[0]
                if self.board[y][x] != "--":
                    blocked = True
            if blocked != True:
                self.boardclass.moveto(self.pos1,self.pos2)
        elif dy == 0:
            x_dir = 1 if dx > 0 else -1
            steps = abs(dx) - 1
            for step in range(steps):
                x = self.pos1[0] + x_dir * (step + 1)
                y = self.pos1[1]
                if self.board[y][x] != "--":
                    blocked = True
            if blocked != True:
                self.boardclass.moveto(self.pos1,self.pos2)

    def moveQ(self):
        if self.pos1[0] == self.pos2[0] or self.pos1[1] == self.pos2[1]:
            if self.sq1[0] == "w" and self.sq2[0] != "w":
                self.boardclass.moveto(self.pos1, self.pos2)
                print("move white queen")
            elif self.sq1[0] == "b" and self.sq2[0] != "b":
                self.boardclass.moveto(self.pos1, self.pos2)
                print("move black queen")
        elif abs(self.pos1[0] - self.pos2[0]) == abs(self.pos1[1] - self.pos2[1]):
            if self.sq1[0] == "w" and self.sq2[0] != "w":
                self.boardclass.moveto(self.pos1, self.pos2)
                print("move white queen")
            elif self.sq1[0] == "b" and self.sq2[0] != "b":
                self.boardclass.moveto(self.pos1, self.pos2)
                print("move black queen")
                
    def moveK(self):
        print("move king")
        self.boardclass.moveto(self.pos1,self.pos2)

        
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
                    if len(clicks) == 0 and board1.get_square(pos1) == "--":
                        pass
                    else:
                        clicks.append(pos1)
                    if len(clicks) == 2:
                        piece1 = board1.get_square(clicks[0])

                        if piece1 != "--" and len(turns)%2==0 and piece1[0] == "w":
                            move = Movement(screen, board1, board1.board, clicks[0],clicks[1])
                            movedic = {"p":move.moveP,"n":move.moveN,"b":move.moveB, "r":move.moveR, "q":move.moveQ, "k":move.moveK}
                            movedic[piece1[1]]()
                            
                        elif piece1 != "--" and len(turns)%2==1 and piece1[0] == "b":
                            move = Movement(screen, board1, board1.board, clicks[0],clicks[1])
                            movedic = {"p":move.moveP,"n":move.moveN,"b":move.moveB, "r":move.moveR, "q":move.moveQ, "k":move.moveK}
                            movedic[piece1[1]]()
                        
                        elif piece1 == "--":
                            clicks = []
                            
                        clicks = []
                    #elif len(clicks) > 2:
                        #clicks = []


        pygame.display.set_caption("Chess")
        boardimage = pygame.image.load("WhiteBackground.jpeg")
        screen.blit(boardimage, (0, 0))
        board1.draw()
        board1.draw_piece()
        pygame.display.update()

main()
