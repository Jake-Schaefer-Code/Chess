import pygame
import sys
from Tile import *
from pieces import *
import copy
import time


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
        self.moves_dict, self.moves_dictw, self.moves_dictb = {}, {}, {}
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
    
    def nextturn(self):
        self.curteam = "b" if self.curteam == "w" else "w"

    def kingLoc(self, board):
        wKingLoc, bKingLoc = (int,int), (int,int)
        for rank in board:
            for tile in rank:
                if isinstance(tile.piece, King):
                    if tile.piece.color == "w":
                        wKingLoc = (tile.file,tile.rank)
                    if tile.piece.color == "b":
                        bKingLoc = (tile.file,tile.rank)
        return [wKingLoc, bKingLoc]

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
    
    def get_all_moves(self, board, bool = True):
        self.all_moves_white = []
        self.all_moves_black = []
        self.moveList = []
        for rank in board:
            for tile in rank:
                if tile.piece != None:
                    
                    if tile.piece.color == "w":
                        self.moveList = self.callmove(tile.piece, tile.rank, tile.file, board)
                        if type(self.moveList) is list:
                            if bool == True:
                                for move in self.moveList:
                                    if not self.inchecktest(tile.piece, (tile.file,tile.rank),move):
                                        self.all_moves_white.append(move) 
                            else:
                                self.all_moves_white += self.moveList


                    elif tile.piece.color == "b":
                        self.moveList = self.callmove(tile.piece, tile.rank, tile.file, board)
                        if type(self.moveList) is list:
                            if bool == True:
                                for move in self.moveList:
                                    if not self.inchecktest(tile.piece, (tile.file,tile.rank),move):
                                        self.all_moves_black.append(move)
                            else:
                                self.all_moves_black += self.moveList
                            #self.moves_dict[self.board[tile.rank][tile.file]] = self.moveList

                        
        return (self.all_moves_white, self.all_moves_black) 

    def checkForPinsAndChecks(self):
        pins = []
        checks = []
        inCheck = False
        if self.curteam == "w":
            startRank = self.kingLoc(self.board)[0][1]
            startFile = self.kingLoc(self.board)[0][0]
        else:
            startRank = self.kingLoc(self.board)[1][1]
            startFile = self.kingLoc(self.board)[1][0]
        
        for d in DIR:
            possiblePin = ()
            for i in range(1,8):
                iterRank = startRank + d[0] * i
                iterFile = startFile + d[1] * i
                #print(iterFile, iterRank)
                if inrange(iterRank, iterFile):
                    iterTile = self.board[iterRank][iterFile]
                    iterPiece = iterTile.piece
                    if iterPiece != None:
                        if iterTile.has_ally(self.curteam):
                            if possiblePin == ():
                                possiblePin = (iterFile, iterRank, d[0], d[1])
                            elif len(possiblePin) == 1:
                                possiblePin = ()
                                break

                        elif iterPiece.color != self.color:
                            if (isinstance(iterPiece, Rook) and (d in STR_DIR)) or (isinstance(iterPiece, Bishop) and (d in DIAG_DIR)) or \
                                (isinstance(iterPiece, Pawn) and i==1 and ((self.curteam == "b" and (d in DIAG_DIR[2:])) or(self.curteam == "w"  and (d in DIAG_DIR[:2])))) or \
                                (isinstance(iterPiece, Queen)) or (i==1 and isinstance(iterPiece, King)):
                                if possiblePin == (): #there are no possible pins and there is an enemy piece in this line
                                    inCheck = True
                                    checks.append((iterFile, iterRank, d[0], d[1]))
                                    break
                                elif len(possiblePin) == 1: #there is a possible pin and an an enemy piece in this line
                                    pins.append(possiblePin)
                                    break
                            else:
                                break
                else: #out of range
                    break
        for d in N_DIR:
            iterRank = startRank + d[0]
            iterFile = startFile + d[1]
            if inrange(iterRank, iterFile):
                iterTile = self.board[iterRank][iterFile]
                iterPiece = iterTile.piece
                if iterTile.has_enemy(self.curteam) and isinstance(iterPiece, Knight):
                    inCheck = True
                    checks.append((iterFile, iterRank, d[0], d[1]))
        return inCheck, pins, checks

    def inchecktest(self, piece, pos1, pos2, bool = True):
        #print(pos1, pos2)
        test = False
        testboard = copy.deepcopy(self.board)
        piece2 = testboard[pos2[1]][pos2[0]].piece
        testboard = self.testmove(piece, pos1, pos2, testboard)
        
        moves = self.get_all_moves(testboard, bool = False)[1] if piece.color == "w" else self.get_all_moves(testboard, bool = False)[0]
        for m in moves:
            iterTile = testboard[m[1]][m[0]]
            if isinstance(iterTile.piece, King):
                test = True
                break
            
        testboard = self.untestmove(piece, piece2, pos1, pos2, testboard)
        return test

    def valid_moves(self):
        self.inCheck, self.pins, self.checks = self.checkForPinsAndChecks()
        moves = self.get_all_moves(self.board)
        kingLocs = self.kingLoc(self.board)
        legalTiles = []
        if self.curteam == "w":
            kingRank = kingLocs[0][1]
            kingFile = kingLocs[0][0]
        else:
            kingRank = kingLocs[1][1]
            kingFile = kingLocs[1][0]
            #print((kingRank, kingFile))  

        if self.inCheck:
            if len(self.checks) == 1:
                check = self.checks[0]
                checkingRank = check[1]
                checkingFile = check[0]
                pieceChecking = self.board[checkingRank][checkingFile].piece
                legalTiles = []

                if isinstance(pieceChecking, Knight):
                    legalTiles = [(checkingFile, checkingRank)] #must take the knight
                else:
                    for i in range(1, 8):
                        legalTile = (kingFile + check[2] * i, kingRank + check[3] * i)
                        if inrange(legalTile[1], legalTile[0]):
                            if legalTile not in legalTiles:
                                piece = self.board[kingRank][kingFile].piece
                                print(legalTile)
                                if not self.inchecktest(piece, (kingFile, kingRank), legalTile):
                                    print("not in check if moved")
                                    legalTiles.append(legalTile)
                            if legalTile[0] == checkingFile and legalTile[1] == checkingRank:
                                break
                
            else:
                kingTile = self.board[kingRank][kingFile]
                legalTiles = self.callmove(kingTile.piece, kingRank, kingFile, self.board)
                
        else:
            if self.curteam == "w":
                legalTiles = moves[0]
            else:
                legalTiles = moves[1]
            
        return legalTiles




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
        i = -1 if self.piece.color == "w" else 1
        dir = [(1,1*i),(-1,1*i)]
        if (self.piece.color == "w" and self.rank == 6) or (self.piece.color == "b" and self.rank == 1):
            firstmove = True

        if self.board[self.rank+i][self.file].piece == None:
            self.potmoves.append((self.file, self.rank+i))
            #look at the king of the person who is moving and go through all of the possible ways it could be attacked
        if firstmove == True and self.board[self.rank+(2*i)][self.file].piece == None:
            self.potmoves.append((self.file, self.rank+(2*i)))
                   
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
        self.potmoves += self.straight_move(DIAG_DIR)
        return self.potmoves
    
    def r_moves(self):
        self.potmoves += self.straight_move(STR_DIR)
        return self.potmoves
    
    def q_moves(self):
        self.potmoves += self.straight_move(DIR)
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
                    self.potmoves.append((file_move, rank_move))
                        
        
        return self.potmoves

    def straight_move(self, dir):
        smoves = [] #temporary list for straight moves - will make a move class or a total moves list in future
        for d in dir:
            rank_dir, file_dir = d
            rank_move = self.rank + rank_dir
            file_move = self.file + file_dir

            while True:
                if inrange(rank_move, file_move):
                    itertile = Tile(rank_move, file_move, self.board[rank_move][file_move].piece)
                    if itertile.emptytile(): #maybe put this in board class so can just call self.board[rank][file].emptytile
                        self.potmoves.append((file_move,rank_move))
                    elif not itertile.emptytile():
                        if not itertile.has_ally(self.piece.color):
                            self.potmoves.append((file_move,rank_move))
                            break
                        elif itertile.has_ally(self.piece.color):
                            break
                else:
                    break
                rank_move = rank_move + rank_dir
                file_move = file_move + file_dir
        return smoves



def play_click():
    click_effect = pygame.mixer.Sound("Vine_Boom.mp3")
    pygame.mixer.Sound.set_volume(click_effect, 0.1)
    pygame.mixer.Sound.play(click_effect)

def play_music():
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.load("Memories.mp3")
    pygame.mixer.music.play()

def draw_piece(screen,tile):
    if tile.piece != None:
        image = tile.piece.imagename
        screen.blit(pygame.transform.scale(piecedic[image],(WIDTH//8,HEIGHT//8)), pygame.Rect((WIDTH//8)*tile.file,(HEIGHT//8)*tile.rank,WIDTH//8,HEIGHT//8))

def main():
    pygame.init()
    pygame.display.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    board1 = Board(screen)
    square = pygame.Rect((0,0), (512,512))
    startsq, piece1, piecemoves = None, None, None
    clicks = []
    play_music()
    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    #if board1.curteam == "w":
                        selectedsq = board1.makeButton(event.pos, square)
                        selectedpiece = board1.get_square(selectedsq).piece
                        if selectedpiece != None:
                            if len(clicks) == 0 and selectedpiece.color == board1.curteam:
                                clicks.append(selectedsq)
                                startsq = selectedsq
                                play_click()
                            elif len(clicks) == 1 and startsq == selectedsq:
                                selectedpiece.imagename = selectedpiece.imagename[:2]
                                clicks = []
                                startsq = None
                                play_click()
                            elif len(clicks) == 1 and selectedpiece.color != board1.curteam:
                                clicks.append(selectedsq)
                                play_click()
                            elif len(clicks) == 1 and selectedpiece.color == board1.curteam and piece1 != None:
                                piece1.imagename = piece1.imagename[:2]
                                selectedpiece.imagename = selectedpiece.imagename[:2]
                                clicks = []
                                play_click()
                            if len(clicks) == 1 and selectedpiece.color == board1.curteam:
                                piece1 = selectedpiece
                                selectedpiece.imagename = selectedpiece.imagename + "h"
                                piecemoves = board1.callmove(piece1, clicks[0][1], clicks[0][0], board1.board)
                                play_click()
                        elif selectedpiece == None and len(clicks)==0:
                            clicks = []
                        else:
                            clicks.append(selectedsq)
                            startsq = selectedsq
                        if len(clicks) == 2 and piece1 != None:
                            piece1.imagename = piece1.imagename[:2]
                            legal_moves = board1.valid_moves()
                            if piece1.color == board1.curteam and clicks[1] in piecemoves:
                                #print(legal_moves)
                                if clicks[1] in legal_moves:
                                    board1.moveTo(piece1, clicks[0],clicks[1])
                                    #board1.check_promotion(piece1, clicks[1][1], clicks[1][0])
                                    board1.nextturn()
                                    play_click()
                                elif legal_moves == []:
                                    print("checkmate")
                                    for _ in range(10):
                                        play_click()
                                        time.sleep(0.1)
                                else:
                                    print("not a legal move")
                            clicks = []
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pygame.mixer.music.unpause()
                    print("unpaused music")
                if event.key == pygame.K_s:
                    pygame.mixer.music.pause()
                    print("paused music")
                
            
        

            #if board1.curteam == "b": #make AI moves here
            #EX: board1.moveTo(piece, startpos, endpos)
            
        
        pygame.display.set_caption("Chess")
        boardimage = pygame.image.load("WhiteBackground.jpeg")
        screen.blit(boardimage, (0, 0))
        board1.draw()
        for rank in board1.board:
            for p in rank:
                draw_piece(screen,p)
        pygame.display.update()

main()
