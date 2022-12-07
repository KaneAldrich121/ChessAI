import chess
import MoveTree
import AI
from random import randint



def createMoveTree():
    return None

# NEEDS REWORKING
def evaluateBoard(boardPosition, consideredMove):
    pieceVals = {'p': 1, 'n': 3, 'b': 3, "r": 5, "q": 8, "k": 10,
                 'P': 1, 'N': 3, 'B': 3, "R": 5, "Q": 8, "K": 10}
    # Finds who will potentially attack back
    compColor = chess.BLACK
    oppColor = chess.WHITE
    oppKing = "K"
    if boardPosition.turn:
        compColor = chess.WHITE
        oppColor = chess.BLACK
        oppKing = "k"
    # Is this Move Checkmate?
    if boardPosition.is_checkmate():
        return 1000
    # Does this Move Give a Check? Does it lead to Mate?
    if boardPosition.is_check() and boardPosition.turn == oppColor:
        foundMate = lookForCheckmate(boardPosition)
        if foundMate:
            return 1000

    # Does this Move Attack a Piece?
    print(boardPosition.is_capture(consideredMove))
    if boardPosition.is_capture(consideredMove) and boardPosition.piece_at(consideredMove.to_square) is not None:
        gain, temp = calculatePointDifference({consideredMove.from_square}, {consideredMove.to_square})
        return gain

    # Does this move restrict the king? TESTED
    previousBoard = boardPosition.copy()
    nextBoard = boardPosition.copy()
    nextBoard.push(consideredMove)
    previousBoard.pop()
    previousKingMoves = list(previousBoard.legal_moves)
    currentKingMoves = list(nextBoard.legal_moves)
    for move in previousKingMoves:
        if previousBoard.piece_at(move.from_square).symbol() != "K":
            previousKingMoves.remove(move)
    for move in currentKingMoves:
        if nextBoard.piece_at(move.from_square).symbol() != oppKing:
            currentKingMoves.remove(move)
    if len(currentKingMoves) < len(previousKingMoves):
        return 3

    # Base Case
    return 0


def lookForCheckmate(boardPosition):
    testBoard = boardPosition.copy()
    return False

def analyzePin(boardPosition, consideredMove):
    # Finds who is being pinned
    compColor = chess.BLACK
    oppColor = chess.WHITE
    if boardPosition.turn:
        compColor = chess.WHITE
        oppColor = chess.BLACK
    testBoard = boardPosition.copy()
    attackingValue = findPieceValue(consideredMove.to_square, boardPosition)
    # Need to Find What Piece is Pinned
    pinnedSquare = 0
    for attackedSquare in boardPosition.attacks(consideredMove.to_square):
        if boardPosition.is_pinned(oppColor, attackedSquare) and boardPosition.piece_at(attackedSquare) is not None:
            pinnedSquare = attackedSquare
            break
    attackedValue = findPieceValue(pinnedSquare, boardPosition)
    if attackedValue > attackingValue:
        return 10
    return 5


# Input: Set of Attacking Squares of Computer Color, set of attacking squares of Opp Color, Board Position
# Output: Returns difference in point values of the comp's attacking pieces and opp's attacking pieces. If this is
#   great than 0, it benefits the comp to attack the square. Also returns the square of the lowest value attacking
#   piece, which is likely the one which should attack first.
# Purpose: Takes a possible attack move and determines if it benefits the computer to initiate the attack, and if so
#   with what piece.
def calculatePointDifference(myAttackerSquareSet, oppAttackerSquareSet, boardPosition):
    pieceVals = {'p': 1, 'n': 3, 'b': 3, "r": 5, "q": 8, "k": 10,
                 'P': 1, 'N': 3, 'B': 3, "R": 5, "Q": 8, "K": 10}
    myTotal = 0
    lowest = 1000
    lowestSquare = None
    for square in myAttackerSquareSet:
        attackingPiece = boardPosition.piece_at(square)
        attackingPieceVal = pieceVals[chess.PIECE_SYMBOLS[attackingPiece.piece_type]]
        myTotal += attackingPieceVal
        if attackingPieceVal < lowest:
            lowest = attackingPieceVal
            lowestSquare = square
    oppTotal = 0
    for square in oppAttackerSquareSet:
        attackingPiece = boardPosition.piece_at(square)
        attackingPieceVal = pieceVals[chess.PIECE_SYMBOLS[attackingPiece.piece_type]]
        oppTotal += attackingPieceVal
    return myTotal - oppTotal, lowestSquare

# Input: Board Position
# Output: List of moves which attack a hanging piece.
# Purpose: Current thought is that attacking a piece which is hanging must be at worst a decent move.
def findHangingPieces(curBoard, firstLevelLegalMoves):
    goodPossibles = []
    oppColor = chess.WHITE
    compColor = chess.BLACK
    if curBoard.turn:
        oppColor = chess.BLACK
        compColor = chess.WHITE
    for pieceType in chess.PIECE_TYPES:
        allPiecesSquares = curBoard.pieces(pieceType, oppColor)
        for pieceSquare in allPiecesSquares:
            if len(curBoard.attackers(oppColor, pieceSquare)) < len(curBoard.attackers(compColor, pieceSquare)):
                myAttackerSquareSet = curBoard.attackers(compColor, pieceSquare)
                oppAttackerSquareSet = curBoard.attackers(oppColor, pieceSquare)
                dif, low = calculatePointDifference(myAttackerSquareSet, oppAttackerSquareSet, curBoard)
                if dif > 0:
                    goodPossibles.append(curBoard.find_move(low, pieceSquare))
    bestMove = None
    if len(goodPossibles) != 0:
        lowestVal = 100
        for move in goodPossibles:
            firstLevelLegalMoves.remove(move)
            if findPieceValue(move.from_square, curBoard) < lowestVal:
                lowestVal = findPieceValue(move.from_square, curBoard)
                bestMove = move
    if bestMove is not None:
        return bestMove
    return None

# Input: Set of all currently considered first level legal moves.
# Output: Set of legal moves which are either attacks or do not hang a piece.
# Purpose: Remove moves which obviously lose material so they are not considered in the move tree.
def removeHangMoves(curBoard, consideredMoves, compColor, oppColor):
    for move in consideredMoves:
        compAttackSet = curBoard.attackers(compColor, move.to_square)
        oppAttackSet = curBoard.attackers(oppColor, move.to_square)
        if not curBoard.is_capture(move):
            if len(oppAttackSet) > len(compAttackSet)-1:
                consideredMoves.remove(move)
    return consideredMoves

# Input: Leaves generated by the Move Tree
# Output: Best move according to the capture point values calculated in the move tree.
# Purpose: Attempts to find the best move as generated by the move tree. Returns none if point vals are all the same.

def calculateByPointVals(leaves):
    maxPointVal = 0
    thisBestMove = None
    for leaf in leaves:
        if leaf.pointDif > maxPointVal:
            maxPointVal = leaf.pointDif
            thisBestMove = leaf.historyToHere[1]
    if thisBestMove is not None:
        return thisBestMove
    else:
        return None


# Input: All leaves generated by the move tree.
# Output: Best move according to MonteCarlo process (try every move, simulate rest of game with random moves, record
#   result 10 times. Move with the highest win rate selected.
# Purpose: Current last resort for trying to find a good move.
def calculateByMonteCarlo(leaves, curBoard):
    maxResultsLength = 0
    thisBestMove = None
    AIRunner = AI.ChessAI()
    for leaf in leaves:
        results = []
        testBoard = curBoard.copy()
        for i in range(1, len(leaf.historyToHere) - 1):
            testBoard.push(leaf.historyToHere[i])
        for i in range(0, 10):
            result = AIRunner.MonteCarlo(testBoard)
            if curBoard.turn == chess.WHITE and result.winner == chess.WHITE:
                results.append(1)
            elif curBoard.turn == chess.BLACK and result.winner == chess.BLACK:
                results.append(1)
        if len(results) > maxResultsLength:
            maxResultsLength = len(results)
            thisBestMove = leaf.historyToHere[1]
    if thisBestMove == None:
        rand = randint(0, len(leaves)-1)
        thisBestMove = leaves[rand].historyToHere[1]
    return thisBestMove


# Input: A square on the board and the given board position.
# Output: Point value of the piece at the given square.
# Purpose: Helper function for calculating move values.
def findPieceValue(square, boardPosition):
    pieceVals = {'p': 1, 'n': 3, 'b': 3, "r": 5, "q": 8, "k": 10,
                 'P': 1, 'N': 3, 'B': 3, "R": 5, "Q": 8, "K": 10}
    attackingPiece = boardPosition.piece_at(square)
    attackingVal = pieceVals[chess.PIECE_SYMBOLS[attackingPiece.piece_type]]
    return attackingVal


def performAllChecks(curBoard, move):
    testBoard = curBoard.copy()
    testBoard.push(move)
    # Note the colors here are different because this function is designed for use in the MoveTree, therefore both
    #   white and black moves will be being calculated with this function.
    compColor = chess.BLACK
    oppColor = chess.WHITE
    if testBoard.turn:
        compColor = chess.WHITE
        oppColor = chess.BLACK
    possibleMoves = list(testBoard.legal_moves)
    # Remove Hanging Moves
    possibleMoves = removeHangMoves(curBoard, possibleMoves, compColor, oppColor)
    return possibleMoves


if __name__ == '__main__':
    board = chess.Board("1b5k/8/8/8/8/8/R1Q5/7K")
    board.turn = chess.BLACK
    board.push_san("h8g8")
    board.push_san("c2b1")
    board.push_san("g8h8")
    print(evaluateBoard(board, board.parse_san("b1b7")))
