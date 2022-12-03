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

        self.whiteToMove = True
        self.moveLog = []
    

    #Takes a move as a parameter and executes it
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved 
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove

    def undoMove(self):
        if(len(self.moveLog)):
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
    

    def getValidMoves(self):
        return self.getAllPossibleMoves()


    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board)):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    if piece == 'p':
                        self.getPawnMoves(r,c, moves)
                    elif piece == 'R':
                        self.getRockMoves(r, c, moves)
                    elif piece == 'N':
                        self.getNightMoves(r, c, moves)
                    elif piece == "B":
                        self.getBishopMoves(r, c, moves)
                    elif piece == 'Q':
                        self.getQueenMoves(r, c, moves)
                    elif piece == "K":
                        self.getKingMoves(r, c, moves)
        return moves

    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:
            if self.board[r-1][c] == "--": #1 Square Pawn Advance 
                moves.append(Move((r, c), (r-1, c), self.board)) 
                if r == 6 and self.board[r-2][c] == "--": #2 Square Pawn Advance 
                    moves.append(Move((r, c), (r-2, c), self.board))
        
        else:
            if self.board[r+1][c] == "--": #1 Square Pawn Advance 
                moves.append(Move((r, c), (r+1, c), self.board)) 
                if r == 1 and self.board[r+2][c] == "--": #2 Square Pawn Advance 
                    moves.append(Move((r, c), (r+2, c), self.board))


    def getRockMoves(self, r, c, moves):
        pass
        
    def getNightMoves(self, r, c, moves):
        pass

    def getBishopMoves(self, r, c, moves):
        pass

    def getQueenMoves(self, r, c, moves):
        pass

    def getKingMoves(self, r, c, moves):
        pass    

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