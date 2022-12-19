import chess
import MoveTree
import AI
from random import randint


def createABTree(rootNode, depth):
    movesToCheck = list(rootNode.boardPosition.legal_moves)
    for move in movesToCheck:
        # Create New Board Position
        thisBoard = rootNode.boardPosition.copy()
        thisBoard.push(move)
        # Find Alpha or Beta Value
        newABVal = findAlphaBetaVal(thisBoard, thisBoard.turn)
        # Create New Node, Recurse Down into NewNode, Add it to Root Children
        newNode = MoveTree.Node(thisBoard, move, newABVal, [], thisBoard.turn)
        if depth - 1 > 0:
            newNode = createABTree(newNode, depth - 1)
        rootNode.children.append(newNode)
    return rootNode

def traverseABTree(rootNode, curBestAlpha, curBestBeta):
    if rootNode.children != []:
        for child in rootNode.children:
            newAlpha, newBeta = traverseABTree(child, -1000, 1000)
            if rootNode.turn:
                if newBeta < rootNode.ABValue:
                    rootNode.ABValue = newBeta
            else:
                if newAlpha > rootNode.ABValue:
                    rootNode.ABValue = newAlpha
    if rootNode.turn:
        if rootNode.ABValue < curBestBeta:
            curBestBeta = rootNode.ABValue
    else:
        if rootNode.ABValue > curBestAlpha:
            curBestAlpha = rootNode.ABValue
    return curBestAlpha, curBestBeta





# Input: Board Position and Who's Turn it is
# Output: Either the Alpha or Beta Value of the given position depending on who's turn it is.
# Purpose: Finds Either the Alpha or Beta Value Depending on who's Turn it is.
def findAlphaBetaVal(boardPosition, turnColor):
    # Calculate Point Difference
    whiteTotal = findAllPieceTotal(boardPosition, chess.WHITE)
    blackTotal = findAllPieceTotal(boardPosition, chess.BLACK)
    difference = abs(whiteTotal - blackTotal)

    #

    # AlphaBeta Function (Features = Difference)
    Value = 1.5 * difference
    return Value

# Input: Current Board Position and Color in Question.
# Output: Sum Total of All Piece Values on the Board for the Given Color.
# Purpose: Calculates Sum Piece Total
def findAllPieceTotal(boardPosition, color):
    total = 0
    typeToValue = {1: 1, 2: 3, 3: 3, 4: 5, 5: 8, 6: 10}
    for pieceType in range(1, 7):
        total += len(boardPosition.pieces(pieceType, color)) * typeToValue[pieceType]
    return total



# Input: Set of Attacking Squares of Computer Color, set of attacking squares of Opp Color, Board Position
# Output: Returns difference in point values of the comp's attacking pieces and opp's attacking pieces. If this is
#   greater than 0, it benefits the comp to attack the square. Also returns the square of the lowest value attacking
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
# CHECK: How does this algorithm behave when it has multiple hanging moves to evaluate
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
            if len(oppAttackSet) > len(compAttackSet) - 1:
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
        rand = randint(0, len(leaves) - 1)
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
    board = chess.Board("r3k2q/4P3/8/8/8/8/4PP1P/4KPQP")
    board.turn = False
    root = MoveTree.Node(board, board.parse_san('h8g8'), findAlphaBetaVal(board, False), [], board.turn)
    root.boardPosition.push_san('h8g8')
    root.turn = True
    thisRoot = createABTree(root, 2)
    for child in thisRoot.children[0].children:
        print(child)
    traverseABTree(thisRoot, -1000, 1000)
    print(thisRoot.children[0])







