import pygame
import sys


piecelist = ["wk", "wq", "wr", "wb", "wn", "wp", "bk", "bq", "br", "bb", "bn", "bp"] # initialization of all the pieces present on a chessboard
piecedic = {}                                                                        # Dictionary of all the pieces (used to make them appear as images on the board later)
squaredic = {}                                                                       # Dictionary of all the squares (used to draw the actual board later)
column = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}                           # Dictionary of the identity of each square according to the rules of chess
Width = 512                                                                          # Initialization of the width and height of the board itself - to be in use later
Height = 512



class Board: # definition of the board class
    def __init__(self, screen): # definition of the initial method
        self.screen = screen
        self.color = None
        self.board = [["--","--","--","--","--","--","--","--"] for _ in range(8)] # Initializing the board as 8 rows of blank spaces to start with
        self.board[0] = ["br","bn","bb","bq","bk","bb","bn","br"] # Assigning the back rank of the board with the non-pawn pieces in their correct order
        self.board[1] = ["bp","bp","bp","bp","bp","bp","bp","bp"] # Assigning all of the black pawns to the second last rank
        self.board[6] = ["wp","wp","wp","wp","wp","wp","wp","wp"] # Assigning all of the white pawns to the second rank
        self.board[7] = ["wr","wn","wb","wq","wk","wb","wn","wr"] # Assigning all of the white non-pawn pieces in the first rank
        print(self.board)
    
    def get_square(self, pos): # definition of the function to return the value of each square (not in chess notation)
        self.col = pos[0] #intialization of the variable that stores the value of the column
        self.row = pos[1] #initialization of the variable that stores the value of the row
        return self.board[self.row][self.col] 
    
    # -- Preserving old code below, in case new code does not function properly. Will delete if all is well. - Dean
    #def moveto(self, pos1, pos2):
        #piece1 = self.board[pos1[1]][pos1[0]]
        #piece2 = self.board[pos2[1]][pos2[0]]
        #if piece1 != "--" and piece2[0] != piece1[0]:
            #self.board[pos1[1]][pos1[0]] = "--"
            #self.board[pos2[1]][pos2[0]] = piece1
        #elif piece2[0] == piece1[0]:
            #print("cannot take your own piece")
        #if piece2[0] != piece1[0] and piece2[0] != "-":
            #print("captured")
    # -- Check comment beginning with "--" above. -Dean
            
    def moveto(self, pos1, pos2):
        piece1 = self.board[pos1[1]][pos1[0]]
        piece2 = self.board[pos2[1]][pos2[0]]
        dx = pos2[0] - pos1[0]
        dy = pos2[1] - pos1[1]
        if piece1 != "--" and piece2[0] != piece1[0]:
            if abs(dx) == abs(dy):  # diagonal move
                # check if there are any pieces in between
                steps = abs(dx) - 1
                x_dir = 1 if dx > 0 else -1
                y_dir = 1 if dy > 0 else -1
                for step in range(steps):
                    x = pos1[0] + x_dir * (step + 1)
                    y = pos1[1] + y_dir * (step + 1)
                    if self.board[y][x] != "--":
                        print("Cannot jump over other pieces.")
                        return
                self.board[pos1[1]][pos1[0]] = "--"
                self.board[pos2[1]][pos2[0]] = piece1
            else:
                print("Invalid move.")
        elif piece2[0] == piece1[0]:
            print("Cannot take your own piece.")
        if piece2[0] != piece1[0] and piece2[0] != "-":
            print("Captured.")
        
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
        if self.sq1[0] == "w":
            if self.pos1[0] == self.pos2[0] and self.sq2[0] != "b":
                if self.pos1[1] > self.pos2[1]:
                    self.boardclass.moveto(self.pos1,self.pos2)
                    print("move white pawn")
            elif self.sq2[0] == "b":
                if self.pos1[1] > self.pos2[1] and (self.pos1[1] == self.pos2[1] + 1):
                    if self.pos1[0] == self.pos2[0] + 1 or self.pos1[0] == self.pos2[0] - 1:
                        self.boardclass.moveto(self.pos1,self.pos2)
                        print("move white pawn")
        if self.sq1[0] == "b":
            if self.pos1[0] == self.pos2[0] and self.sq2[0] != "w":
                if self.pos1[1] < self.pos2[1]:
                    self.boardclass.moveto(self.pos1,self.pos2)
                    print("move black pawn")
            elif self.sq2[0] == "w":
                if self.pos1[1] < self.pos2[1] and (self.pos1[1] == self.pos2[1] - 1):
                    if self.pos1[0] == self.pos2[0] + 1 or self.pos1[0] == self.pos2[0] - 1:
                        self.boardclass.moveto(self.pos1,self.pos2)
                        print("move black pawn")


    def moveN(self):
        if abs(self.pos1[0]-self.pos2[0]) == 2 and abs(self.pos1[1]-self.pos2[1]) == 1: # Checking if the move is valid for a knight: L-shape pattern with 2 squares in one direction and 1 square in the other direction
            if self.sq1[0] == "w" and self.sq2[0] != "w": # Checking if the knight is white, and whether the destination square is not occupied by a white piece
                self.boardclass.moveto(self.pos1,self.pos2) # Moving the queen to the destination square
                print("move white knight") # Printing a message to indicate that the move has been made
            elif self.sq1[0] == "b" and self.sq2[0] != "b": # Checking if the knight is black, and the destination square is not occupied by a black piece
                self.boardclass.moveto(self.pos1,self.pos2) # Moving the knight to the destination square
                print("move black knight") # Printing a message to indicate that the move has been made
        elif abs(self.pos1[0]-self.pos2[0]) == 1 and abs(self.pos1[1]-self.pos2[1]) == 2: # Checking if the move is valid for a knight, which moves in an L-shape pattern with 1 square in one direction and 2 squares in the other direction.
            if self.sq1[0] == "w" and self.sq2[0] != "w": # Checking if the knight is white, and whether the destination square is not occupied by a white piece
                self.boardclass.moveto(self.pos1,self.pos2) # Moving the knight to the destination square
                print("move white knight") # Printing a message to indicate that the move has been made
            elif self.sq1[0] == "b" and self.sq2[0] != "b": # Checking if the knight is black, and the destination square is not occupied by a black piece
                self.boardclass.moveto(self.pos1,self.pos2) # Moving the knight to the destination square
                print("move black knight") # Printing a message to indicate that the move has been made
                
    def moveB(self):
        if self.sq1[0] == "w":
            if abs(self.pos1[0] - self.pos2[0]) == abs(self.pos1[1] - self.pos2[1]) and self.sq2[0] != "w":
                self.boardclass.moveto(self.pos1, self.pos2)
                print("move white bishop")
        if self.sq1[0] == "b":
            if abs(self.pos1[0] - self.pos2[0]) == abs(self.pos1[1] - self.pos2[1]) and self.sq2[0] != "b":
                self.boardclass.moveto(self.pos1, self.pos2)
                print("move black bishop")
                
    def moveR(self):
        print("move rook")
        self.boardclass.moveto(self.pos1,self.pos2)
        
    def moveQ(self):
        if self.pos1[0] == self.pos2[0] or self.pos1[1] == self.pos2[1]: # Checking if the queen is moving horizontally or vertically
            if self.sq1[0] == "w" and self.sq2[0] != "w": # Checking if the queen is white, and whether the destination square is not occupied by a white piece
                self.boardclass.moveto(self.pos1, self.pos2) # Moving the queen to the destination square
                print("move white queen") # Printing a message to indicate that the move has been made
            elif self.sq1[0] == "b" and self.sq2[0] != "b": # Checking if the queen is black, and the destination square is not occupied by a black piece
                self.boardclass.moveto(self.pos1, self.pos2) # Moving the queen to the destination square
                print("move black queen") # Printing a message to indicate that the move has been made
        elif abs(self.pos1[0] - self.pos2[0]) == abs(self.pos1[1] - self.pos2[1]): # Checking if the queen is moving diagonally
            if self.sq1[0] == "w" and self.sq2[0] != "w": # Checking if the queen is white and the destination square is not occupied by a white piece
                self.boardclass.moveto(self.pos1, self.pos2) # Moving the queen to the destination square
                print("move white queen") # Printing a message to indicate that the move has been made
            elif self.sq1[0] == "b" and self.sq2[0] != "b": # Checking if the queen is black, and the destination square is not occupied by a black piece
                self.boardclass.moveto(self.pos1, self.pos2) # Moving the queen to the destination square
                print("move black queen") # Printing a message to indicate that the move has been made

    def moveK(self):
        print("move king")
        self.boardclass.moveto(self.pos1,self.pos2)

        
def main():
    turn = 1
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
                        if piece1 != "--" and turn%2==1 and piece1[0] == "w":
                            move = Movement(screen, board1, board1.board, clicks[0],clicks[1])
                            movedic = {"p":move.moveP,"n":move.moveN,"b":move.moveB, "r":move.moveR, "q":move.moveQ, "k":move.moveK}
                            movedic[piece1[1]]()
                            turn +=1
                        elif piece1 != "--" and turn%2==0 and piece1[0] == "b":
                            move = Movement(screen, board1, board1.board, clicks[0],clicks[1])
                            movedic = {"p":move.moveP,"n":move.moveN,"b":move.moveB, "r":move.moveR, "q":move.moveQ, "k":move.moveK}
                            movedic[piece1[1]]()
                            turn +=1
                        clicks = []
                              
        

        pygame.display.set_caption("Chess")
        boardimage = pygame.image.load("WhiteBackground.jpeg")
        screen.blit(boardimage, (0, 0))
        board1.draw()
        board1.draw_piece()
        pygame.display.update()


main()
