import pygame
import sys


piecelist = ["wk", "wq", "wr", "wb", "wn", "wp", "bk", "bq", "br", "bb", "bn", "bp", 
             "wkh", "wqh", "wrh", "wbh", "wnh", "wph", "bkh", "bqh", "brh", "bbh", "bnh", "bph"]
piecedic = {}
squaredic = {}
column = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}
Width = 512
Height = 512
turns = []
moves = []
possible_moves = []
direction_grid = [(1,0), (1,1), (0,1), (-1,1), (-1,0), (-1,-1), (0,-1), (1,-1)]

class Board:
    def __init__(self, screen):
        self.screen = screen
        self.color = None
        self.board = [["--","--","--","--","--","--","--","--"] for _ in range(8)]
        self.board[0] = ["br","bn","bb","bq","bk","bb","bn","br"]
        self.board[1] = ["bp","bp","bp","bp","bp","bp","bp","bp"]
        self.board[6] = ["wp","wp","wp","wp","wp","wp","wp","wp"]
        self.board[7] = ["wr","wn","wb","wq","wk","wb","wn","wr"]
    
    def get_square(self, pos):
        return self.board[pos[1]][pos[0]]
    
    def moveto(self, pos1, pos2):
        c = constraints(self.screen)
        piece1 = self.board[pos1[1]][pos1[0]]
        piece2 = self.board[pos2[1]][pos2[0]]
        if piece1 != "--" and piece2[0] != piece1[0]:
            self.board[pos1[1]][pos1[0]] = "--"
            self.board[pos2[1]][pos2[0]] = piece1
            turns.append((pos1,pos2))
        elif c.samecolor(pos1, pos2, self.board):
            print("You cannot take your own piece.")
        if (piece2[0] != piece1[0]) and (piece2[0] != "-"):
            print("Captured!")
        moves.append([pos1,pos2, piece1, piece2])
        #print(moves)

    def makeButton(self, cur, rect):
            if rect.collidepoint(cur):
                pos1 = pygame.mouse.get_pos()[0]//(Width//8)
                pos2 = pygame.mouse.get_pos()[1]//(Height//8)
                return (pos1,pos2)

    def undo(self):
        if len(moves) != 0:
            pos1 = moves[-1][0]
            pos2 = moves[-1][1]
            piece1 = moves[-1][2]
            piece2 = moves[-1][3]
            self.board[pos1[1]][pos1[0]] = piece1
            self.board[pos2[1]][pos2[0]] = piece2
            moves.pop()


    def check_moves(self, pos):
        #we will call this function in a nested for-loop perhaps? where each iteration checks if a square has a piece and then calls this function
        piece = self.board[pos[1]][pos[0]]
        if piece[1] == 'p':
            print("pawn")

        

class drawing(Board):
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
                squaredic[(j,i)] = pygame.Rect((Width//8)*i,(Height//8)*j,Width//8,Height//8) #dont need maybe?

    def draw_piece(self): #checks each square on the board for a piece and draws it if there is one
        for i in range(8):
            for j in range(8):
                piece = self.board[j][i]
                if piece != "--":
                    self.screen.blit(pygame.transform.scale(piecedic[piece],(Width//8,Height//8)), pygame.Rect((Width//8)*i,(Height//8)*j,Width//8,Height//8))
    
    def highlight(self, pos):
        self.board[pos[1]][pos[0]] += "h"
    def unhighlight(self, pos):
        self.board[pos[1]][pos[0]] = self.board[pos[1]][pos[0]][:2]



class constraints:
    def __init__(self, screen):
        self.screen = screen
    def onboard(self,pos):
        return (pos[0] >= 0 and pos[0] <= 7) and (pos[1] >= 0 and pos[1] <= 7)

    def samecolor(self, pos1, pos2, board):
        return board[pos1[1]][pos1[0]][0] == board[pos2[1]][pos2[0]][0]
    
    def blocked(self, pos, board):
        return board[pos[1]][pos[0]] != "--"
    
    def blocked_diag(self, pos1, pos2, board):
        dx = pos2[0] - pos1[0]
        dy = pos2[1] - pos1[1]
        if abs(dx) == abs(dy):  
            blocked = False
            steps = abs(dx) - 1
            x_dir = 1 if dx > 0 else -1
            y_dir = 1 if dy > 0 else -1
            for step in range(steps):
                x = pos1[0] + x_dir * (step +1)
                y = pos1[1] + y_dir * (step +1)
                if board[y][x] != "--":
                    blocked = True
            return blocked
    
    def blocked_straight(self, pos1, pos2, board):
        dx = pos2[0] - pos1[0]
        dy = pos1[1] - pos2[1]
        blocked = False
        if dx == 0:
            y_dir = 1 if dy > 0 else -1
            steps = abs(dy) - 1
            for step in range(steps):
                y = pos2[1] + y_dir * (step + 1)
                x = pos1[0]
                if board[y][x] != "--":
                    blocked = True
        elif dy == 0:
            x_dir = 1 if dx > 0 else -1
            steps = abs(dx) - 1
            for step in range(steps):
                x = pos1[0] + x_dir * (step + 1)
                y = pos1[1]
                if board[y][x] != "--":
                    blocked = True
        return blocked
   


class Movement:
    def __init__(self, screen, boardclass, board, pos1, pos2):
        self.screen = screen
        self.board = board
        self.boardclass = boardclass
        self.pos1 = pos1
        self.pos2 = pos2
        self.sq1 = board[pos1[1]][pos1[0]]
        self.sq2 = board[pos2[1]][pos2[0]]
        self.Pmoves = []
        self.Nmoves = []
        self.Bmoves = []
        self.c = constraints(self.screen)

        
        
    def moveP(self):
        firstmove = False
        

        if self.sq1[0] == "w":
            if self.pos1[1] == 6:
                firstmove = True
            

            if self.pos1[0] == self.pos2[0] and self.sq2[0] != "b":
                if self.pos1[1] > self.pos2[1]:
                    if firstmove and (self.pos1[1] == self.pos2[1] + 2 or self.pos1[1] == self.pos2[1] + 1):
                        self.boardclass.moveto(self.pos1,self.pos2)
                        print("Moved white pawn.")
                    elif self.pos1[1] == self.pos2[1] + 1:
                        self.boardclass.moveto(self.pos1,self.pos2)
                        print("Moved white pawn.")
            elif self.sq2[0] == "b":
                if self.pos1[1] > self.pos2[1] and (self.pos1[1] == self.pos2[1] + 1):
                    if self.pos1[0] == self.pos2[0] + 1 or self.pos1[0] == self.pos2[0] - 1:
                        self.boardclass.moveto(self.pos1,self.pos2)
                        print("Moved white pawn.")

        if self.sq1[0] == "b":
            if self.pos1[1] == 1:
                firstmove = True

            if self.pos1[0] == self.pos2[0] and self.sq2[0] != "w":
                if self.pos1[1] < self.pos2[1]:
                    if firstmove and (self.pos1[1] == self.pos2[1] - 2 or self.pos1[1] == self.pos2[1] - 1):
                        self.boardclass.moveto(self.pos1,self.pos2)
                        print("Moved black pawn.")
                    elif self.pos1[1] == self.pos2[1] - 1:
                        self.boardclass.moveto(self.pos1,self.pos2)
                        print("Moved black pawn.")         
            elif self.sq2[0] == "w":
                if self.pos1[1] < self.pos2[1] and (self.pos1[1] == self.pos2[1] - 1):
                    if self.pos1[0] == self.pos2[0] + 1 or self.pos1[0] == self.pos2[0] - 1:
                        self.boardclass.moveto(self.pos1,self.pos2)
                        print("Moved black pawn.")
                        

    def moveN(self):
        
        
        
        maybemoves = [[x,y] for y in range(8) if abs(self.pos1[1]-y) == 2 for x in range(8) if abs(self.pos1[0]-x) == 1] + [
            [x,y] for y in range(8) if abs(self.pos1[1]-y) == 1 for x in range(8) if abs(self.pos1[0]-x) == 2]
        for move in maybemoves:
            if not self.c.samecolor(self.pos1, move, self.board):
                self.Nmoves.append(move)
                print(self.Nmoves)

        
        if abs(self.pos1[0]-self.pos2[0]) == 2 and abs(self.pos1[1]-self.pos2[1]) == 1:
            self.boardclass.moveto(self.pos1,self.pos2)
        elif abs(self.pos1[0]-self.pos2[0]) == 1 and abs(self.pos1[1]-self.pos2[1]) == 2:
            self.boardclass.moveto(self.pos1,self.pos2)


    def moveB(self):
        #while not blocked:
            #check nearest diagonal space for piece
            #if no piece, append square
            #repeat for each direction
        directions = [(1,1),(1,-1),(-1,-1),(-1,1)]
        for dir in directions:
            blocked = False
            step = 0
            onboard = True
            while not blocked and onboard:
                step +=1
                x = self.pos1[0] + dir[0] * (step)
                y = self.pos1[1] + dir[1] * (step)
                onboard = self.c.onboard((x,y))
                if onboard:
                    if self.board[y][x] != "--":
                        blocked = True
                    else:
                        self.Bmoves.append((x,y))
                    
        
        print(self.Bmoves)
        
        if not self.c.blocked_diag(self.pos1, self.pos2, self.board):
            self.boardclass.moveto(self.pos1,self.pos2)

            
    def moveR(self):
        
        if not self.c.blocked_straight(self.pos1, self.pos2, self.board):
            self.boardclass.moveto(self.pos1,self.pos2)
        

    def moveQ(self):
        if self.pos1[0] == self.pos2[0] or self.pos1[1] == self.pos2[1]:
            self.boardclass.moveto(self.pos1, self.pos2)
        elif abs(self.pos1[0] - self.pos2[0]) == abs(self.pos1[1] - self.pos2[1]):
            self.boardclass.moveto(self.pos1, self.pos2)
        
                
    def moveK(self):
        if abs(self.pos1[0] - self.pos2[0]) <= 1 and abs(self.pos1[1] - self.pos2[1]) <= 1:
            self.boardclass.moveto(self.pos1, self.pos2)

    
        
def main():
    pygame.init()
    pygame.display.init()
    screen = pygame.display.set_mode((Width,Height))
    #screen.fill(pygame.Color("white"))
    board1 = drawing(screen)
    c = constraints(screen)    
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

                    if (len(clicks) == 0 and board1.get_square(selectedsq) == "--"):
                        clicks = []
                    elif sq1 == selectedsq and len(clicks) == 1:
                        board1.unhighlight(clicks[0])
                        clicks = []
                        sq1 = None
                    else:
                        clicks.append(selectedsq)
                        sq1 = selectedsq
                        piece1 = board1.get_square(clicks[0])
                        if len(clicks) == 1:
                            board1.highlight(selectedsq)
                    #print(clicks)
                    
                    if len(clicks) == 2:
                        board1.unhighlight(clicks[0])
                        piece1 = board1.get_square(clicks[0])
                        

                        if piece1 != "--" and len(turns)%2==0 and piece1[0] == "w": #white's move - should probably create a variable for white vs black turns that updates
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
        

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    board1.undo()


        pygame.display.set_caption("Chess")
        boardimage = pygame.image.load("WhiteBackground.jpeg")
        screen.blit(boardimage, (0, 0))
        board1.draw()
        board1.draw_piece()
        pygame.display.update()

main()
