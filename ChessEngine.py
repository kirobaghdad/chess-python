"""
Determines the valid moves at the current state.
"""

class GameState():
    def __init__(self):
        self.board = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wp","wp","wp","wp","wp","wp","wp","wp"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]
        ]

        self.moveFunctions = {'p' : self.getPawnMoves, 'K': self.getKingMoves, 'Q' : self.getQueenMoves, 'R': self.getRockMoves, 'N': self.getNightMoves, 'B':self.getBishopMoves}

        self.whiteToMove = True
        self.moveLog = []
        self.blackKing = (0, 4)
        self.whiteKing = (7, 4)


    #Takes a move as a parameter and executes it
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        if move.pieceMoved == "wK":
            self.whiteKing = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKing = (move.endRow, move.endCol)
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

    def undoMove(self):
        if(len(self.moveLog)):
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            if move.pieceMoved == "wK":
                self.whiteKing = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKing = (move.startRow, move.startCol)
    

    def getValidMoves(self):
        moves = self.getAllPossibleMoves()

        for i in range(len(moves) - 1, -1, -1):
            self.makeMove(moves[i])
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.pop(i)
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        return self.getAllPossibleMoves()


    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board)):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]

                    self.moveFunctions[piece](r,c, moves)

        return moves

    def addMove(self, r0, c0, r1, c1, moves):
        moves.append(Move((r0, c0), (r1, c1), self.board))


    #Pawn promotion is not implemented
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:
            if r-1 >= 0:
                if  self.board[r-1][c] == "--": #1 Square Pawn Advance 
                    moves.append(Move((r, c), (r-1, c), self.board)) 
                    if r == 6 and self.board[r-2][c] == "--": #2 Square Pawn Advance 
                        moves.append(Move((r, c), (r-2, c), self.board))

                if c-1 >= 0:
                    if self.board[r-1][c-1][0] == 'b':
                        self.addMove(r, c, r-1, c-1, moves)
                
                if c+1 <= 7:
                    if self.board[r-1][c+1][0] == 'b': 
                        self.addMove(r,c, r-1, c+1, moves)


        else:
            if r + 1 < 8:
                if self.board[r+1][c] == "--": #1 Square Pawn Advance 
                    moves.append(Move((r, c), (r+1, c), self.board)) 
                    if r == 1 and self.board[r+2][c] == "--": #2 Square Pawn Advance 
                        moves.append(Move((r, c), (r+2, c), self.board))
                if c-1 >= 0:
                    if self.board[r+1][c-1][0] == 'w':
                        self.addMove(r, c, r+ 1, c-1, moves)
                
                if c+1 <= 7:
                    if self.board[r+1][c+1][0] == 'w': 
                        self.addMove(r,c, r+1, c+1, moves)

    def getMovesOneDirection(self,r,c,moves,down, right):
        col = c + right
        row = r + down
       # while (right == 1 and col < 8) or (right == -1 and col >= 0) or (down == 1 and row < 8) or (down == -1 and row >= 0):
        while col < 8 and col >= 0 and  row < 8 and row >= 0:
            piece = self.board[row][col]
            if piece == "--":
                self.addMove(r,c, row, col, moves)
            elif (piece[0] == 'b'and self.whiteToMove) or (piece[0] == 'w' and not self.whiteToMove):
                self.addMove(r,c,row,col,moves)
                break
            else: break
            
            col = col + right
            row = row + down   



    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKing[0], self.whiteKing[1])
        else: return self.squareUnderAttack(self.blackKing[0], self.blackKing[1])

    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove
        moves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        
        for move in moves:
            if move.endRow == r and move.endCol == c:
                return True
        return False

    def getRockMoves(self, r, c, moves):
        self.getMovesOneDirection(r,c,moves, 0, 1) #Right Moves
        self.getMovesOneDirection(r,c,moves, 0, -1) #Left Moves
        self.getMovesOneDirection(r,c,moves, 1, 0) #Down Moves
        self.getMovesOneDirection(r,c,moves, -1, 0) #Up Moves
                    

        
    def getBishopMoves(self, r, c, moves):
        self.getMovesOneDirection(r, c, moves, 1,1)   #Down, Right Mobes
        self.getMovesOneDirection(r, c, moves, 1,-1)  #Down, Left Moves
        self.getMovesOneDirection(r, c, moves, -1,1)  #Up, Right Moves
        self.getMovesOneDirection(r, c, moves, -1,-1) #Up, Left Moves

    def getNightMoves(self, r, c, moves):
        positions = [[r - 2, c + 1], [r - 1, c + 2], [r + 1,c + 2], [r + 2, c + 1], [r + 2, c - 1], [r + 1, c - 2], [r - 1, c - 2], [r - 2, c - 1]]

        for position in positions:
            if position[0] < 8 and position[0] >= 0 and position[1] < 8 and position[1] >= 0:
                piece = self.board[position[0]][position[1]]
                if (piece == "--") or (self.whiteToMove and piece[0] == 'b') or (not self.whiteToMove and piece[0] == 'w'):
                    self.addMove(r,c, position[0], position[1], moves)


    def getQueenMoves(self, r, c, moves):
        self.getBishopMoves(r,c, moves)
        self.getRockMoves(r,c, moves)

    def getKingMoves(self, r, c, moves):
        positions = [[r - 1, c + 1], [r, c + 1], [r + 1, c + 1], [r + 1, c], [r + 1, c - 1], [r, c - 1], [r - 1, c - 1], [r - 1, c]] 

        for position in positions:
            if position[0] < 8 and position[0] >= 0 and position[1] < 8 and position[1] >= 0:
                piece = self.board[position[0]][position[1]]
                if (piece == "--") or (self.whiteToMove and piece[0] == 'b') or (not self.whiteToMove and piece[1] == 'w'):
                    self.addMove(r,c, position[0], position[1], moves)

class Move():
    ranksToRows = {"1" : 7, "2": 6, "3": 5, "4": 4, "5": 3, "6":2, "7":1, "8":0}
    rowsToRanks = {v:k for k, v in ranksToRows.items()}

    filesToCols = {"a": 0, "b":1, "c":2, "d": 3, "e": 4, "f":5, "g": 6, "h":7}
    colsToFiles = {v: k for k, v in filesToCols.items()}


    def __init__(self, startSQ, endSQ, board):
        self.startRow = startSQ[0]
        self.startCol = startSQ[1]
        
        self.endRow = endSQ[0]
        self.endCol = endSQ[1]

        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol


    def __eq__(self,other):
        if isinstance(other, Move):
            return other.moveID == self.moveID
        return False 

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
    
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

    # @staticmethod
    # def getRowCol(self, s):
    #     return str(self.filesToCols[s[0]]) + str(self.ranksToRows[s[1]]) + str(self.filesToCols[s[2]]) + str(self.ranksToRows[s[3]])