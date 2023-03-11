import pygame
import sys
from Tile import *
from pieces import *
import copy
import time
import random


PIECELIST = ["wk", "wq", "wr", "wb", "wn", "wp", "bk", "bq", "br", "bb", "bn", "bp", 
             "wkh", "wqh", "wrh", "wbh", "wnh", "wph", "bkh", "bqh", "brh", "bbh", "bnh", "bph"] #piecelist defining pieces, by 1. color; 2. piece (n for knight); 3. highlighted/clicked status
piecedic = {}
for piece in PIECELIST:
    piecedic[piece] = pygame.image.load("chess_pieces/"+piece+".PNG") #Loading chess pieces by .png file from chess_pieces folder
WIDTH = 512
HEIGHT = 512
#Below we define the type of directional movements for the pieces later on
DIR = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,1),(-1,-1),(1,-1)] #Both Straight and Diagonal movement
N_DIR = [(-2,-1),(-2,1),(-1,-2),(1,-2),(2,-1),(2,1),(-1,2),(1,2)] #L-shaped Knight movement
STR_DIR = [(1,0),(-1,0),(0,1),(0,-1)] 
DIAG_DIR = [(1,1),(-1,1),(-1,-1),(1,-1)]

#Note: calling a piece on the board acts like board[rank][file] or board[y][x]

class Board:
    def __init__(self, screen):
        self.screen = screen
        self.bool = True
        self.color = None
        self.curteam = "w" #set to white to establish first move and ai movements
        self.moves_dict, self.moves_dictw, self.moves_dictb = {}, {}, {}
        self.board = [[Tile(0,0),Tile(0,0),Tile(0,0),Tile(0,0),Tile(0,0),Tile(0,0),Tile(0,0),Tile(0,0)] for _ in range(8)]
        for rank in range(8):
            for file in range(8):
                self.board[rank][file] = Tile(file, rank)
        #Placing pieces on tiles below
        self.board[0] = [Tile(0,0,Rook("b")), Tile(1,0,Knight("b")), Tile(2,0,Bishop("b")), Tile(3,0,Queen("b")),
                         Tile(4,0,King("b")), Tile(5,0,Bishop("b")), Tile(6,0,Knight("b")), Tile(7,0,Rook("b"))]
        self.board[1] = [Tile(0,1,Pawn("b")), Tile(1,1,Pawn("b")), Tile(2,1,Pawn("b")), Tile(3,1,Pawn("b")),
                         Tile(4,1,Pawn("b")), Tile(5,1,Pawn("b")), Tile(6,1,Pawn("b")), Tile(7,1,Pawn("b"))]        
        self.board[6] = [Tile(0,6,Pawn("w")), Tile(1,6,Pawn("w")), Tile(2,6,Pawn("w")), Tile(3,6,Pawn("w")),
                         Tile(4,6,Pawn("w")), Tile(5,6,Pawn("w")), Tile(6,6,Pawn("w")), Tile(7,6,Pawn("w"))]       
        self.board[7] = [Tile(0,7,Rook("w")), Tile(1,7,Knight("w")), Tile(2,7,Bishop("w")), Tile(3,7,Queen("w")),
                         Tile(4,7,King("w")), Tile(5,7,Bishop("w")), Tile(6,7,Knight("w")), Tile(7,7,Rook("w"))]
        
    def get_square(self, pos): #Determining location– to be used for clicking on square
        return self.board[pos[1]][pos[0]]
    
    def draw(self): #Drawing board
        #Drawing tiles by rank and file below
        for i in range(8): 
            for j in range(8):
                if (i+1)%2 == 1 and (8-j)%2 == 1:
                     self.color = (169,108,69) #Drawing brown tiles
                elif (i+1)%2 == 0 and (8-j)%2 == 0:
                    self.color = (169,108,69)
                else:
                    self.color = (245,198,156) #Drawing peach tiles
                pygame.draw.rect(self.screen, self.color, pygame.Rect((WIDTH//8)*i,(HEIGHT//8)*j,WIDTH//8,HEIGHT//8))

    def makeButton(self, cur, rect): #Clicking function for moving pieces
            if rect.collidepoint(cur):
                #Parameters for what is being clicked on defined below:
                pos1 = pygame.mouse.get_pos()[0]//(WIDTH//8)
                pos2 = pygame.mouse.get_pos()[1]//(HEIGHT//8)
                return (pos1,pos2)
    
    def nextturn(self):
        self.curteam = "b" if self.curteam == "w" else "w" #Checking if current team is white (given white's first move privilege) to determine if AI moves

    def kingLoc(self, board): #Determining location of King for checkmate function
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
        self.board[pos1[1]][pos1[0]] = Tile(pos1[0],pos1[1]) #Current position
        self.board[pos2[1]][pos2[0]] = Tile(pos2[0],pos2[1],piece) #Clicked position to be moved to

    def testmove(self, piece, pos1, pos2, board): #Moves piece as a "test" function, used for checkmate
        board[pos1[1]][pos1[0]] = Tile(pos1[0],pos1[1])
        board[pos2[1]][pos2[0]] = Tile(pos2[0],pos2[1],piece)
        return board

    def untestmove(self, piece1, piece2, pos1, pos2, board): #Unmoves "test" move above
        board[pos1[1]][pos1[0]] = Tile(pos1[0],pos1[1],piece1)
        board[pos2[1]][pos2[0]] = Tile(pos2[0],pos2[1],piece2)
        return board

    def callmove(self, piece, endpos, board, bool = True): #Making the movement based on the type of piece being clicked
        file = endpos[0]
        rank = endpos[1]
        move = Movetypes(piece, rank, file, board, self, bool = bool)
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
    
    def get_all_moves(self, board, bool = True): #Used to iterate over valid moves
        self.all_moves_white = []
        self.all_moves_black = []
        self.moveList = []
        for i in range(8):
            for j in range(8):
                tile = self.board[j][i]
                if tile.piece != None:
                    self.moveList = self.callmove(tile.piece, (i,j), board)
                    if tile.piece.color == "w" and type(self.moveList) is list:
                        self.all_moves_white += self.moveList
                        self.moves_dict[(i,j)] = self.moveList #creates a list of moves for dictionary key at the piece position

                    elif tile.piece.color == "b" and type(self.moveList) is list:
                        self.all_moves_black += self.moveList
                        self.moves_dict[(i,j)] = self.moveList

        return (self.all_moves_white, self.all_moves_black, self.moves_dict) 

class Movetypes:
    def __init__(self, piece, rank, file, board, boardclass, bool = True):
        self.piece = piece
        self.rank = rank
        self.file = file
        self.pos = (file, rank)
        self.color = piece.color
        self.bool = bool
        self.board = board
        self.boardclass = boardclass
        self.potmoves = []
           
    def p_moves(self): #Pawn moveset
        firstmove = False #To be used for pawn's two-tile movement privilege
        i = -1 if self.piece.color == "w" else 1 #Direction as per color of piece, upward (-1) for white
        dir = [(1,1*i),(-1,1*i)]
        if (self.piece.color == "w" and self.rank == 6) or (self.piece.color == "b" and self.rank == 1): #Checking if correct pawn is on correct rank for two-tile privilege
            firstmove = True

        if inrange(self.rank+i, self.file) and self.board[self.rank+i][self.file].piece == None:
            move = (self.file, self.rank+i)
            self.callincheck(move)
            
        #Checking king of entity moving, and going through all of the possible ways it could be attacked
        if firstmove == True and self.board[self.rank+(2*i)][self.file].piece == None:
            move = (self.file, self.rank+(2*i))
            self.callincheck(move)
            
                   
        for d in dir:
            if inrange(self.rank+d[1],self.file+d[0]):
                if self.board[self.rank+d[1]][self.file+d[0]].piece != None: #Checking if there is a piece in the new position
                    if not self.board[self.rank][self.file].samecolor(self.board[self.rank+d[1]][self.file+d[0]].piece.color): #Checking color of piece in new position
                        move = (self.file+d[0],self.rank+d[1])
                        self.callincheck(move)                
        return self.potmoves
    
    def n_moves(self):
        for d in N_DIR: #Using specific L-type movement defined before
            x, y = self.file + d[0], self.rank + d[1]
            if inrange(y, x):
                itertile = Tile(x, y, self.board[y][x].piece)
                if itertile.emptytile() or not itertile.has_ally(self.piece.color): #Checking if the tile is empty or if the piece on the tile is not an ally
                    move = (x,y)
                    self.callincheck(move)
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
                    move = (file_move, rank_move)
                    self.callincheck(move)
        return self.potmoves

    def straight_move(self, dir):
        smoves = [] #Store potential moves
        for d in dir:
            rank_dir, file_dir = d
            rank_move = self.rank + rank_dir
            file_move = self.file + file_dir
            while True:
                if inrange(rank_move, file_move):
                    itertile = Tile(rank_move, file_move, self.board[rank_move][file_move].piece)
                    if itertile.piece == None:
                        move = (file_move, rank_move)
                        self.callincheck(move) #Check if the move puts an entity in check
                    elif not itertile.piece == None:
                        if not itertile.has_ally(self.piece.color):
                            move = (file_move, rank_move) #Note: We can't use self.callincheck(move) here because we need to break loop in some instances
                            if self.bool == True:
                                if not self.incheckmove(move):
                                    self.potmoves.append(move)
                                    break #Breaking out of the loop given the piece can't move further in this direction
                            else:
                                self.potmoves.append(move)
                                break
                        elif itertile.has_ally(self.piece.color):
                            break
                else:
                    break
                rank_move = rank_move + rank_dir
                file_move = file_move + file_dir
        return smoves

    def incheckmove(self, move): #Implementing this over each piece, checking if this move puts the king in check
        piece = self.piece #Piece that we are checking the result of its potential moves
        pos = self.pos #Start position of the piece we are checking
        testboard = copy.deepcopy(self.board)
        testboard = self.testmovepiece(piece, pos, move, testboard)
        for rank in range(8):
            for file in range(8):
                if testboard[rank][file].has_enemy(piece.color): #If square on the board has an enemy
                    enemy_piece = testboard[rank][file].piece #Get which piece is on that square
                    enemy_moves = self.boardclass.callmove(enemy_piece, (file, rank), testboard, bool = False) #get the moves of that piece with bool = False, so it doesnt call this function again
                    for m in enemy_moves:
                        if isinstance(testboard[m[1]][m[0]].piece, King):
                            return True
        return False

    def testmovepiece(self, piece, pos1, pos2, board): 
        board[pos1[1]][pos1[0]] = Tile(pos1[0],pos1[1])
        board[pos2[1]][pos2[0]] = Tile(pos2[0],pos2[1],piece)
        return board

    def callincheck(self, move): 
        if self.bool == True:
            if not self.incheckmove(move):
                self.potmoves.append(move)
        else:
            self.potmoves.append(move)

def draw_piece(screen,tile): #Drawing pieces through piece dictionary (piecedic)
    if tile.piece != None:
        image = tile.piece.imagename
        screen.blit(pygame.transform.scale(piecedic[image],(WIDTH//8,HEIGHT//8)), pygame.Rect((WIDTH//8)*tile.file,(HEIGHT//8)*tile.rank,WIDTH//8,HEIGHT//8))

def play_click(): #Clicking sound effect
    click_effect = pygame.mixer.Sound("piecenoise.mp3")
    pygame.mixer.Sound.set_volume(click_effect, 0.1)
    pygame.mixer.Sound.play(click_effect)

def play_music(): #Background music
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.load("Kaissa.mp3")
    pygame.mixer.music.play()

def main():
    pygame.init()
    pygame.display.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
    board1 = Board(screen)
    square = pygame.Rect((0,0), (512,512)) #Creating board, defining dimensions 
    startsq, piece1, piecemoves = None, None, None
    clicks = [] #List for tracking mouse clicks
    play_music()
    firstmove = True
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    if board1.curteam == "w":
                        selectedsq = board1.makeButton(event.pos, square)
                        selectedpiece = board1.get_square(selectedsq).piece
                        if selectedpiece != None:
                            if len(clicks) == 0 and selectedpiece.color == board1.curteam: #Checking if this is the first click and if the selected piece is on the current team
                                clicks.append(selectedsq)
                                startsq = selectedsq #Saving selected square
                                play_click()
                            elif len(clicks) == 1 and startsq == selectedsq:
                                selectedpiece.imagename = selectedpiece.imagename[:2] #Revert the piece's image to its original form
                                clicks = []
                                startsq = None #Clearing selected square
                                play_click()
                            elif len(clicks) == 1 and selectedpiece.color != board1.curteam:
                                clicks.append(selectedsq)
                                play_click()
                            elif len(clicks) == 1 and selectedpiece.color == board1.curteam and piece1 != None: #Checking if there is already a piece selected and if the new piece is on the current team
                                piece1.imagename = piece1.imagename[:2]
                                selectedpiece.imagename = selectedpiece.imagename[:2]
                                clicks = []
                                play_click()
                            if len(clicks) == 1 and selectedpiece.color == board1.curteam:
                                piece1 = selectedpiece #Saving selected piece
                                selectedpiece.imagename = selectedpiece.imagename + "h"
                                piecemoves = board1.callmove(piece1, clicks[0], board1.board)
                                play_click()
                        elif selectedpiece == None and len(clicks)==0:
                            clicks = [] #Resetting clicks should nothing be selected
                        else:
                            clicks.append(selectedsq)
                            startsq = selectedsq
                        if len(clicks) == 2 and piece1 != None:
                            piece1.imagename = piece1.imagename[:2]
                            moves = board1.get_all_moves(board1.board)[0] if board1.curteam == "w" else board1.get_all_moves(board1.board)[1]
                            if piece1.color == board1.curteam and clicks[1] in piecemoves: #Checking if the selected move is legal
                                board1.moveTo(piece1, clicks[0],clicks[1])
                                play_click()
                                board1.nextturn()
                            elif moves == []:
                                print("Checkmate!") 
                            else:
                                print("Not a legal move!")
                            clicks = []
            
            if board1.curteam == "b": #Making AI moves here, should it be black's turn

                if firstmove == True:
                    board1.moveTo(board1.board[1][4].piece, (4,1), (4,3)) #AI makes predetermined first move, e2 to e4
                    firstmove = False
                    board1.nextturn()
                elif board1.get_all_moves(board1.board)[1] == []:
                    print("Checkmate! White wins!")
                else:
                    moves = board1.get_all_moves(board1.board)[2]
                    starttile = random.choice(list(moves.keys())) #Choosing a random piece to move
                    while True:
                        if board1.board[starttile[1]][starttile[0]].piece != None and board1.board[starttile[1]][starttile[0]].piece.color == "b":
                            if moves[starttile] != []:
                                move = random.choice(moves[starttile]) #Choosing a random move for the selected piece
                                break
                            else:
                                starttile = random.choice(list(moves.keys()))
                        else:
                            starttile = random.choice(list(moves.keys()))
                    
                    best_piece = -10 #To be used to determine greed-based behavior– which piece should be captured
                    
                    for key in moves:
                        if board1.board[key[1]][key[0]].piece != None and board1.board[key[1]][key[0]].piece.color == "b":
                            for tile in moves[key]:
                                if board1.board[tile[1]][tile[0]].piece != None and board1.board[tile[1]][tile[0]].piece.color == "w":
                                    cur_piece = board1.board[tile[1]][tile[0]].piece.value #Retrieves value of the white piece
                                    if cur_piece > best_piece: #Choose whether the cur_piece is worth pursuing
                                        best_piece = cur_piece
                                        move = tile
                                        starttile = key
                                              
                    board1.moveTo(board1.board[starttile[1]][starttile[0]].piece, (starttile[0],starttile[1]), (move[0],move[1]))
                    play_click()
                    board1.nextturn()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p: #Press key p to unpause music
                    pygame.mixer.music.unpause()
                    print("Unpaused music. Press S to pause music.")
                if event.key == pygame.K_s:
                    pygame.mixer.music.pause() #Press key s to pause music
                    print("Paused music. Press P to unpause music.")

        pygame.display.set_caption("Chess")
        boardimage = pygame.image.load("WhiteBackground.jpeg") #Background image to be drawn on, just white
        screen.blit(boardimage, (0, 0))
        board1.draw()
        for rank in board1.board:
            for p in rank:
                draw_piece(screen,p)
        pygame.display.update()

main()
