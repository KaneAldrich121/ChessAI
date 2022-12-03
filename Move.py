import chess


class Move:
    # Takes Board Position and Depth to Search and Returns Best Move
    def getNextMoveDict(self, thisBoard, moveList, thisDepth, thisChain):
        legalMoves = list(thisBoard.legal_moves)
        while thisDepth != 0:
            for move in legalMoves:
                thisChain.append(move)
                thisBoard.push(move)
                self.getNextMoveDict(thisBoard, moveList, thisDepth - 1, thisChain)
                thisBoard.pop()
                moveList.append(thisChain)
                print(moveList)
                thisChain.pop()
        if thisDepth == 0:
            return thisChain

        return moveList

    def calculateMoveTotal(self, thisBoard, move):
        pieceVals = {"P": 1, "N": 3, "B": 3, "R": 5, "Q": 8, "K": 10,
                     "p": 1, "n": 3, "b": 3, "r": 5, "q": 8, "k": 10}
        capture = thisBoard.is_capture(move)
        gain = 0
        if capture:
            moveString = str(move)
            attackerSquare = moveString[:2]
            attackedSquare = moveString[2:]
            attackingPiece = board.piece_at(chess.parse_square(attackerSquare))
            attackedPiece = board.piece_at(chess.parse_square(attackedSquare))
            gain = pieceVals[attackedPiece]
        if not thisBoard.turn:
            gain = -gain
        return gain




board = chess.Board()
thisMove = Move()
mList = []
chain = []
depth = 2
options = thisMove.getNextMoveDict(board, mList, depth, chain)
print(options)


