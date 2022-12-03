import chess


class Move:
    # Takes Board Position and Depth to Search and Returns Best Move
    def getNextMoveDict(self, thisBoard, depth, moveDict):
        legalMoves = list(thisBoard.legal_moves)
        while depth > 0:
            for move in legalMoves:
                thisBoard.push(move)
                
                thisBoard.pop()
        return moveDict



board = chess.Board()
thisMove = Move()
dictM = {}
options = thisMove.getNextMoveDict(board, 1, dictM)
print(options)


