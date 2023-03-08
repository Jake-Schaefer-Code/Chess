import pygame
import sys
from Tile import *
from pieces import *
import copy


PIECELIST = ["wk", "wq", "wr", "wb", "wn", "wp", "bk", "bq", "br", "bb", "bn", "bp", 
             "wkh", "wqh", "wrh", "wbh", "wnh", "wph", "bkh", "bqh", "brh", "bbh", "bnh", "bph"]
piecedic = {}
for piece in PIECELIST:
    piecedic[piece] = pygame.image.load("chess_pieces/"+piece+".PNG")
WIDTH = 512
HEIGHT = 512
DIR = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,1),(-1,-1),(1,-1)]
N_DIR = [(-2,-1),(-2,1),(-1,-2),(1,-2),(2,-1),(2,1),(-1,2),(1,2)]
STR_DIR = [(1,0),(-1,0),(0,1),(0,-1)]
DIAG_DIR = [(1,1),(-1,1),(-1,-1),(1,-1)]

#IMPORTANT: calling a piece on the board acts like board[rank][file] or board[y][x]

class Board:
    def __init__(self, screen):
        self.screen = screen
        self.bool = True
        self.color = None
        self.curteam = "w"
        self.moves_dictw, self.moves_dictb = {}, {}
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
                pygame.draw.rect(self.screen, self.color, pygame.Rect((WIDTH//8)*i,(HEIGHT//8)*j,WIDTH//8,HEIGHT//8))

    def makeButton(self, cur, rect):
            if rect.collidepoint(cur):
                pos1 = pygame.mouse.get_pos()[0]//(WIDTH//8)
                pos2 = pygame.mouse.get_pos()[1]//(HEIGHT//8)
                return (pos1,pos2)
    
    def moveTo(self, piece, pos1, pos2):
        self.board[pos1[1]][pos1[0]] = Tile(pos1[0],pos1[1])
        self.board[pos2[1]][pos2[0]] = Tile(pos2[0],pos2[1],piece)

    def testmove(self, piece, pos1, pos2, board):
        board[pos1[1]][pos1[0]] = Tile(pos1[0],pos1[1])
        board[pos2[1]][pos2[0]] = Tile(pos2[0],pos2[1],piece)
        return board

    def untestmove(self, piece1, piece2, pos1, pos2, board):
        board[pos1[1]][pos1[0]] = Tile(pos1[0],pos1[1],piece1)
        board[pos2[1]][pos2[0]] = Tile(pos2[0],pos2[1],piece2)
        return board

    def callmove(self, piece, rank, file, board):
        move = Movetypes(piece, rank, file, board, self, bool = self.bool)
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
    
    def get_all_moves(self, board):
        self.all_moves_white = []
        self.all_moves_black = []
        self.list1 = []
        for rank in board:
            for tile in rank:
                if tile.piece != None:
                    if tile.piece.color == "w":
                        self.list1 = self.callmove(tile.piece, tile.rank, tile.file, board)
                        if type(self.list1) is list:
                            self.all_moves_white += self.list1
                            self.moves_dictw[(tile.file, tile.rank)] = self.list1
                    if tile.piece.color == "b":
                        self.list1 = self.callmove(tile.piece, tile.rank, tile.file, board)
                        if type(self.list1) is list:
                            self.all_moves_black += self.list1
                            self.moves_dictb[(tile.file, tile.rank)] = self.list1

                        
        return(self.all_moves_white, self.all_moves_black)
    
    def legal_moves(self):
        self.all_moves_white = []
        self.all_moves_black = []
        if self.curteam == "w":
            enemyColor = "b"
            allyColor = "w"
            startrank = self.kingLoc(self.board)[0][1]
            startfile = self.kingLoc(self.board)[0][0]
        else:
            enemyColor = "w"
            allyColor = "b"
            startrank = self.kingLoc(self.board)[1][1]
            startfile = self.kingLoc(self.board)[1][0]

        
    def inchecktest(self, piece, pos1, pos2):
        test = False
        self.bool = False
        testboard = copy.deepcopy(self.board)
        piece2 = testboard[pos2[1]][pos2[0]].piece
        testboard = self.testmove(piece, pos1, pos2, testboard)
        moves = self.get_all_moves(testboard)[1] if piece.color == "w" else self.get_all_moves(testboard)[0]
        self.bool = True
        while True:
            for m in moves:
                iterTile = testboard[m[1]][m[0]]
                if isinstance(iterTile.piece, King):
                    test = True
                    break
            break
        testboard = self.untestmove(piece, piece2, pos1, pos2, testboard)
        return test

    def stalemate(self):
        test = False
        testboard = copy.deepcopy(self.board)
        moves = self.get_all_moves(testboard)[1] if self.curteam == "w" else self.get_all_moves(testboard)[0]
        if moves == []:
            test = True
        return test
    
    def checkmate(self):
        test = False
        testboard = copy.deepcopy(self.board)
        moves = self.get_all_moves(testboard)[0] if self.curteam == "w" else self.get_all_moves(testboard)[1]
        print(moves)
        if moves == []:
            test = True
        return test
    
    def nextturn(self):
        self.curteam = "b" if self.curteam == "w" else "w"

    '''def incheck(self):
        print("incheck fn")
        moves = self.get_all_moves()[1] if self.curteam == "w" else self.get_all_moves()[0]
        for m in moves:
            itertile = self.board[m[1]][m[0]]
            if isinstance(itertile.piece, King):
                print("in check")
                return True

        #create a copy of the board, mkae the move, and have some function that evaluates the board 
        #function calls evaluate board anf a pos number indicates win for white and win for black
        #if white has won then like add 1000 points or something and if black has won add -1000
        #recursively minimax algorithm LOOK UP RAHIM'''

    '''def teamVal(self, color, board): #gets value of specified team's pieces
        teamvalue = 0
        for rank in board:
            for file in rank:
                if file.piece != None:
                    if file.piece.color == color:
                        teamvalue += file.piece.value
        return teamvalue

    def evalBoard(self, board): #checks if winning and by how much
        whiteVal = self.teamVal("w", board)
        blackVal = self.teamVal("b", board)
        totVal = whiteVal - blackVal 
        mult = 1 if self.curteam == "w" else -1 #if it is w's turn and b>w, then it returns a neg number - if it is b's turn and b>w, then it returns a pos number
        return totVal * mult

    def searchBoard(self, depth, board): #depth will be how far in advance the game will think
        testboard = copy.deepcopy(board) #copies the input board
        self.get_all_moves_test(testboard) #this will create dictionaries of the possible moves of each piece on the input board

        if depth == 0: #base case
            return self.evalBoard(testboard)
            #create new function - search all captures and return that instead

        for key in self.moves_dictw.keys(): #for each piece on white
            for move in self.moves_dictw[key]: #for each move for each piece on white
                testboard2 = copy.deepcopy(testboard) #copies the input board
                piece = testboard2[key[1]][key[0]].piece
                testboard = self.testmove(piece, key, move, testboard2) #moves the piece on the input board
                self.eval = int(self.searchBoard(depth - 1, testboard)) #recursively calls this function again with the new board
                self.bestEval = max(self.eval, self.bestEval)
        
        return self.bestEval

    def minimax(self, depth, maximizer, board):
        testboard = copy.deepcopy(board)
        self.get_all_moves_test(testboard)
        best_move = [(0,0), (1,1)] #change this to a random move
        if depth == 0: #base case
            return self.evalBoard(testboard)
        
        if maximizer: #maximizer is black - black wants the most points
            max_eval = -10000
            for key in self.moves_dictb.keys(): 
                for move in self.moves_dictb[key]:
                    piece1, piece2 = testboard[key[1]][key[0]].piece, testboard[move[1]][move[0]].piece
                    testboard = self.testmove(piece1, key, move, testboard)        
                    cur_eval = self.minimax(depth - 1, False, testboard)[1]
                    testboard = self.untestmove(piece1, piece2, key, move, testboard)
                    if cur_eval > max_eval:
                        max_eval = cur_eval
                        best_move = [key, move]
            return best_move, max_eval

        elif not maximizer: #minimizer is white
            min_eval = 10000
            for key in self.moves_dictw.keys(): 
                for move in self.moves_dictw[key]:
                    piece1, piece2 = testboard[key[1]][key[0]].piece, testboard[move[1]][move[0]].piece
                    testboard = self.testmove(piece1, key, move, testboard)
                    cur_eval = self.minimax(depth - 1, True, testboard)[1]
                    testboard = self.untestmove(piece1, piece2, key, move, testboard)
                    if cur_eval < min_eval:
                        min_eval = cur_eval
                        best_move = [key, move]
            return best_move, min_eval'''
    
    def kingLoc(self, board):
        wKingLoc, bKingLoc = (int,int), (int,int)
        for rank in board:
            for tile in rank:
                if isinstance(tile.piece, King):
                    if tile.piece.color == "w":
                        wKingLoc = (tile.file,tile.rank)
                    if tile.piece.color == "b":
                        bKingLoc = (tile.file,tile.rank)
        return wKingLoc, bKingLoc

    def checkForPinsAndChecks(self):
        pins = []
        checks = []
        inCheck = False
        if self.curteam == "w":
            enemyColor = "b"
            startRank = self.kingLoc(self.board)[0][1]
            startFile = self.kingLoc(self.board)[0][0]
        else:
            enemyColor = "w"
            startRank = self.kingLoc(self.board)[1][1]
            startFile = self.kingLoc(self.board)[1][0]
        
        for d in DIR:
            possiblePin = ()
            for i in range(8):
                iterRank = startRank + d[0] * i
                iterFile = startFile + d[1] * i
                if inrange(iterRank, iterFile):
                    iterTile = self.board[iterRank][iterFile]
                    iterPiece = iterTile.piece
                    if iterPiece != None:
                        if iterTile.has_ally(self.curteam):
                            if possiblePin == ():
                                possiblePin = (iterRank, iterFile, d[0], d[1])
                            else:
                                break

                        elif iterTile.has_enemy(self.curteam):
                            if (isinstance(iterPiece, Rook) and (d in STR_DIR)) or (isinstance(iterPiece, Bishop) and (d in DIAG_DIR)) or \
                                (isinstance(iterPiece, Pawn) and i==1 and ((self.curteam == "b" and (d in DIAG_DIR[2:])) or(self.curteam == "w"  and (d in DIAG_DIR[:2])))) or \
                                (isinstance(iterPiece, Queen)) or (i==1 and isinstance(iterPiece, King)):
                                if possiblePin == (): 
                                    inCheck = True
                                    checks.append((iterRank, iterFile, d[0], d[1]))
                                    break
                                else:
                                    pins.append(possiblePin)
                                    break
                            else:
                                break
        for d in N_DIR:
            iterRank = startRank + d[0]
            iterFile = startFile + d[1]
            if inrange(iterRank, iterFile):
                iterTile = self.board[iterRank][iterFile]
                iterPiece = iterTile.piece
                if iterTile.has_enemy(self.curteam) and isinstance(iterPiece, Knight):
                    inCheck = True
                    checks.append((iterRank, iterFile, d[0], d[1]))
        
        return inCheck, pins, checks




def draw_piece(screen,tile):
    if tile.piece != None:
        image = tile.piece.imagename
        screen.blit(pygame.transform.scale(piecedic[image],(WIDTH//8,HEIGHT//8)), pygame.Rect((WIDTH//8)*tile.file,(HEIGHT//8)*tile.rank,WIDTH//8,HEIGHT//8))

class Movetypes:
    def __init__(self, piece, rank, file, board, boardclass, bool = True):
        self.piece = piece
        self.rank = rank
        self.file = file
        self.bool = bool
        self.board = board
        self.boardclass = boardclass
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
                if self.bool:
                    if not self.boardclass.inchecktest(self.piece, (self.file,self.rank) ,(self.file, self.rank-1)):
                        self.potmoves.append((self.file, self.rank-1))

                else:
                    self.potmoves.append((self.file, self.rank-1))
            if firstmove == True and self.board[self.rank-2][self.file].piece == None:
                if self.bool:
                    if not self.boardclass.inchecktest(self.piece, (self.file,self.rank) ,(self.file, self.rank-1)):
                        self.potmoves.append((self.file, self.rank-2))
                else:
                    self.potmoves.append((self.file, self.rank-2))
                   
        elif self.piece.color == "b":
            if self.board[self.rank+1][self.file].piece == None:
                if self.bool:
                    if not self.boardclass.inchecktest(self.piece, (self.file,self.rank) ,(self.file, self.rank-1)):
                        self.potmoves.append((self.file, self.rank+1))
                else:
                    self.potmoves.append((self.file, self.rank+1))
            if firstmove == True and self.board[self.rank+2][self.file].piece == None:
                if self.bool:
                    if not self.boardclass.inchecktest(self.piece, (self.file,self.rank) ,(self.file, self.rank-1)):
                        self.potmoves.append((self.file, self.rank+2))
                else:
                    self.potmoves.append((self.file, self.rank+2))
        
        for d in dir:
            if inrange(self.rank+d[1],self.file+d[0]):
                if self.board[self.rank+d[1]][self.file+d[0]].piece != None:
                    if not self.board[self.rank][self.file].samecolor(self.board[self.rank+d[1]][self.file+d[0]].piece.color):
                        if self.bool:
                            if not self.boardclass.inchecktest(self.piece, (self.file,self.rank) ,(self.file+d[0],self.rank+d[1])):
                                self.potmoves.append((self.file+d[0],self.rank+d[1]))
                        else:
                            self.potmoves.append((self.file+d[0],self.rank+d[1]))
                

        return self.potmoves
    
    def n_moves(self):
        moves = [(x,y) for y in range(8) if abs(self.rank-y) == 2 for x in range(8) if abs(self.file-x) == 1] + [
            (x,y) for y in range(8) if abs(self.rank-y) == 1 for x in range(8) if abs(self.file-x) == 2]
        for x,y in moves:
            itertile = Tile(x, y, self.board[y][x].piece)
            if itertile.emptytile() or not itertile.has_ally(self.piece.color):
                if self.bool:
                    if not self.boardclass.inchecktest(self.piece, (self.file,self.rank), (x,y)):
                        self.potmoves.append((x,y))
                else:
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
        dir = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,1),(-1,-1),(1,-1)]
        for d in dir:
            rank_dir, file_dir = d
            rank_move = self.rank + rank_dir
            file_move = self.file + file_dir
            if inrange(rank_move, file_move):
                itertile = Tile(rank_move, file_move, self.board[rank_move][file_move].piece)
                if itertile.emptytile() or not itertile.has_ally(self.piece.color):
                    if self.bool:
                        if not self.boardclass.inchecktest(self.piece, (self.file,self.rank), (file_move,rank_move)):
                            self.potmoves.append((file_move,rank_move))
                            print("not in check")
                        else:
                            print("in check")
                    else:
                        self.potmoves.append((file_move, rank_move))
                        
        
        return self.potmoves

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
                        if self.bool:
                            if not self.boardclass.inchecktest(self.piece, (self.file,self.rank), (file_move,rank_move)):
                                self.potmoves.append((file_move,rank_move))
                        else:
                            self.potmoves.append((file_move,rank_move))
                    elif not itertile.emptytile():
                        if not itertile.has_ally(self.piece.color):
                            if self.bool:
                                if not self.boardclass.inchecktest(self.piece, (self.file,self.rank), (file_move,rank_move)):
                                    self.potmoves.append((file_move,rank_move))
                            else:
                                self.potmoves.append((file_move,rank_move))
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
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    board1 = Board(screen)
    square = pygame.Rect((0,0), (512,512))
    startsq, piece1, piecemoves = None, None, None
    clicks = []
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    if board1.get_all_moves(board1.board)[0] != []:
                        #print(board1.get_all_moves(board1.board)[1])
                        
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
                            elif len(clicks) == 1 and selectedpiece.color == board1.curteam and piece1 != None:
                                piece1.imagename = piece1.imagename[:2]
                                selectedpiece.imagename = selectedpiece.imagename[:2]
                                clicks = []
                            if len(clicks) == 1 and selectedpiece.color == board1.curteam:
                                piece1 = selectedpiece
                                selectedpiece.imagename = selectedpiece.imagename + "h"
                                piecemoves = board1.callmove(piece1, clicks[0][1], clicks[0][0], board1.board)
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
                    #else:
                        #print("checkmate: game over")    
                        #print(clicks)
        '''if board1.curteam == "b": #make AI moves here
            #EX: board1.moveTo(piece, startpos, endpos)
            pass''' 


        pygame.display.set_caption("Chess")
        boardimage = pygame.image.load("WhiteBackground.jpeg")
        screen.blit(boardimage, (0, 0))
        board1.draw()
        for rank in board1.board:
            for p in rank:
                draw_piece(screen,p)
        pygame.display.update()

main()
