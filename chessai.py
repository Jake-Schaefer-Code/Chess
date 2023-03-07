checkmate = 1000
stalemate = 0

valuedict = {"p": 1, "n": 3, "b": 3.5, "r": 5, "q": 10, "k": 1000}

def greed_ai():
    pass

'''def kings_pawn():
    if white's pawn occupies the square e4 or if the first move is returned as a move to e4:
      move black pawn to e5
      

#def caro_kann():
    if white's pawn occupies the square e4 or if the first move is returned as a move to e4
     move black pawn to c6
     then if white moves to square d4 or if white moves Knight to F3:
        play black pawn to d5 
        then if white captures black pawn on d5

        elif white 

    if white's move != to anything:
    call ai function to continue playing or break and call the function
'''


def teamVal(self, color, board): #gets value of specified team's pieces
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
            return best_move, min_eval
