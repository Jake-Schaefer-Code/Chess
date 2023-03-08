def p_moves(self):
    firstmove = False
    promoted = False
    
    if promoted is None:
        while True:
            dir = []
            if self.piece.color == "w":
                dir = [(1,-1),(-1,-1)]
            elif self.piece.color == "b":
                dir = [(1,1),(-1,1)]

            if (self.piece.color == "w" and self.rank == 6) or (self.piece.color == "b" and self.rank == 1):
                firstmove = True
            if self.piece.color == "w":
                if self.board[self.rank-1][self.file].piece == None:
                    self.potmoves.append((self.file, self.rank-1))
                if firstmove == True and self.board[self.rank-2][self.file].piece == None:
                    self.potmoves.append((self.file, self.rank-2))
                if self.rank == 0:
                        promoted = True
                        break

            elif self.piece.color == "b":
                if self.board[self.rank+1][self.file].piece == None:
                    self.potmoves.append((self.file, self.rank+1))
                if firstmove == True and self.board[self.rank+2][self.file].piece == None:
                    self.potmoves.append((self.file, self.rank+2))
                if self.rank == 7:
                        promoted = True
                        break

            for d in dir:
                if inrange(self.rank+d[1],self.file+d[0]):
                    if self.board[self.rank+d[1]][self.file+d[0]].piece != None:
                        if not self.board[self.rank][self.file].samecolor(self.board[self.rank+d[1]][self.file+d[0]].piece.color):
                            self.potmoves.append((self.file+d[0],self.rank+d[1]))


        return self.potmoves
    
    else:
        dir = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,1),(-1,-1),(1,-1)]
        self.potmoves += self.straight_move(dir)
        return self.potmoves
