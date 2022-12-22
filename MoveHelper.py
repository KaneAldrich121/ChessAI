import chess
import MoveTree
import AI
from random import randint


def createABTree(rootNode, depth):
    movesToCheck = list(rootNode.boardPosition.legal_moves)
    movesToCheck = removeHangMoves(rootNode.boardPosition, movesToCheck, rootNode.turn, not rootNode.turn)
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


def traverseABTree(rootNode, childValues):
    if not rootNode.children:  # If Child List is Empty (This is a leaf)
        if len(childValues) == 0:
            childValues.append(rootNode.ABValue)
        else:
            if board.turn and rootNode.ABValue < childValues[0]:
                childValues[0] = rootNode.ABValue
            elif not board.turn and rootNode.ABValue > childValues[0]:
                childValues[0] = rootNode.ABValue
        return
    else:
        for thisChild in rootNode.children:
            if len(childValues) != 0:
                if board.turn and rootNode.ABValue < childValues[0]:
                    childValues[0] = rootNode.ABValue
                elif not board.turn and rootNode.ABValue > childValues[0]:
                    childValues[0] = rootNode.ABValue
            traverseABTree(thisChild, childValues)

        if len(childValues) != 0:
            rootNode.ABValue = childValues[0]
    return


# Input: Board Position and Who's Turn it is
# Output: Either the Alpha or Beta Value of the given position depending on who's turn it is.
# Purpose: Finds Either the Alpha or Beta Value Depending on who's Turn it is.
def findAlphaBetaVal(boardPosition, turnColor):
    # Is Checkmate?
    mate = 0
    if boardPosition.is_checkmate():
        mate = 1000

    # Calculate Point Difference
    whiteTotal = findAllPieceTotal(boardPosition, chess.WHITE)
    blackTotal = findAllPieceTotal(boardPosition, chess.BLACK)
    difference = abs(whiteTotal - blackTotal)

    # Find How Many Pieces this Move Attacks
    lastMove = boardPosition.pop()
    boardPosition.push(lastMove)
    numberAttackedSquares = boardPosition.attacks(lastMove.to_square)
    numberAttacked = 0
    for square in numberAttackedSquares:
        if boardPosition.piece_at(square) and boardPosition.color_at(square) == boardPosition.turn:
            numberAttacked += 1

    # AlphaBeta Function (Features = Difference, Pieces Attacked, Mate)
    Value = 1.5 * difference + 1 * numberAttacked + mate
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
    goodMoves = []
    for move in consideredMoves:
        if not curBoard.is_capture(move):
            testBoard = curBoard.copy()
            testBoard.push(move)
            defenders = len(testBoard.attackers(compColor, move.to_square))
            defPositions = testBoard.attackers(compColor, move.to_square)
            attackers = len(testBoard.attackers(oppColor, move.to_square))
            attPositions = testBoard.attackers(oppColor, move.to_square)
            if defenders >= attackers:
                goodMoves.append(move)
    return goodMoves


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

# Input: Root of the ABTree
# Output: Best Move Found by the ABTree.
# Purpose: If Root is Black then next move will be white and we maximize, if root is white
# #   then next move is black and we minimize. Values at ABValue are created from the children of the node.
def findBestMoveFromABTree(treeRoot):
    treeBestMove = None
    treeBestEval = 1000  # Get minimum value of child nodes
    for treeChild in treeRoot.children:
        if treeChild.ABValue < treeBestEval:
            treeBestEval = treeChild.ABValue
            treeBestMove = treeChild.thisMove
    return treeBestMove


if __name__ == '__main__':
    # Create Toy Tree
    board = chess.Board("r1b1kbnr/pppp1ppp/8/8/2BpP2q/3P4/PPP2PPP/RNBQK2R w KQkq")
    # Root Node
    lastMove = board.parse_san('e1g1')
    board.push(lastMove)
    rootNode = MoveTree.Node(board, lastMove, 0, [], board.turn)
    # Bad Child Depth 1
    badMove = board.parse_san('h4h6')
    board.push(badMove)
    badChild = MoveTree.Node(board, badMove, findAlphaBetaVal(board, board.turn), [], board.turn)
    rootNode.children.append(badChild)
    board.pop()
    # Good Child Depth 1
    goodMove = board.parse_san('h4f6')
    board.push(goodMove)
    goodChild = MoveTree.Node(board, goodMove, findAlphaBetaVal(board, board.turn), [], board.turn)
    rootNode.children.append(goodChild)
    board.pop()
    # BAD CHILD CHILDREN
    board.push(badMove)
    # CHILD WHICH TAKES QUEEN
    goodResponse = board.parse_san('c1h6')
    board.push(goodResponse)
    level2BadGood = MoveTree.Node(board, goodResponse, findAlphaBetaVal(board, board.turn), [], board.turn)
    rootNode.children[0].children.append(level2BadGood)
    board.pop()
    # CHILD WHICH MISSES CAPTURE
    badResponse = board.parse_san('c1e3')
    board.push(badResponse)
    level2BadBad = MoveTree.Node(board, badResponse, findAlphaBetaVal(board, board.turn), [], board.turn)
    rootNode.children[0].children.append(level2BadBad)
    board.pop()
    board.pop()
    # GOOD CHILD CHILDREN:
    board.push(goodMove)
    # CHILD WHICH CONTINUES DEVELOPMENT
    developMove = board.parse_san('c1e3')
    board.push(developMove)
    level2GoodGood = MoveTree.Node(board, developMove, findAlphaBetaVal(board, board.turn), [], board.turn)
    rootNode.children[1].children.append(level2GoodGood)
    board.pop()
    # CHILD WHICH BLUNDERS
    blunderMove = board.parse_san('h2h4')
    board.push(blunderMove)
    level2GoodBad = MoveTree.Node(board, blunderMove, findAlphaBetaVal(board, board.turn), [], board.turn)
    rootNode.children[1].children.append(level2GoodBad)
    board.pop()
    board.pop()
    # Board is at Start Position, add children for all children's children
    # Add two children to Bad Move -> Good Response
    # Child that takes bishop
    board.push(badMove)
    board.push(goodResponse)
    takeBishop = board.parse_san('g7h6')
    board.push(takeBishop)
    level3BadGoodGood = MoveTree.Node(board, takeBishop, findAlphaBetaVal(board, board.turn), [], board.turn)
    rootNode.children[0].children[0].children.append(level3BadGoodGood)
    board.pop()
    # Child that does not take bishop
    leaveBishop = board.parse_san('g8f6')
    board.push(leaveBishop)
    level3BadGoodBad = MoveTree.Node(board, leaveBishop, findAlphaBetaVal(board, board.turn), [], board.turn)
    rootNode.children[0].children[0].children.append(level3BadGoodBad)
    board.pop()
    board.pop()
    # Add two children to Bad Move -> Bad Response
    # Black takes white bishop
    board.push(badResponse)
    takeWhiteBishop = board.parse_san('d4e3')
    board.push(takeWhiteBishop)
    level3BadBadGood = MoveTree.Node(board, takeWhiteBishop, findAlphaBetaVal(board, board.turn), [], board.turn)
    rootNode.children[0].children[1].children.append(level3BadBadGood)
    board.pop()
    # Black doesn't take white bishop
    developBlackBishop = board.parse_san('f8b4')
    board.push(developBlackBishop)
    level3BadBadBad = MoveTree.Node(board, developBlackBishop, findAlphaBetaVal(board, board.turn), [], board.turn)
    rootNode.children[0].children[1].children.append(level3BadBadBad)
    board.pop()
    board.pop()
    board.pop()
    # Add two children to Good Move -> Develop Move
    board.push(goodMove)
    board.push(developMove)
    # Black Takes the Bishop
    blackAttack = board.parse_san('d4e3')
    board.push(blackAttack)
    level3GoodGoodBad = MoveTree.Node(board, blackAttack, findAlphaBetaVal(board, board.turn), [], board.turn)
    rootNode.children[1].children[0].children.append(level3GoodGoodBad)
    board.pop()
    # Black Leaves the Bishop
    blackPass = board.parse_san('f8c5')
    board.push(blackPass)
    level3GoodGoodGood = MoveTree.Node(board, blackPass, findAlphaBetaVal(board, board.turn), [], board.turn)
    rootNode.children[1].children[0].children.append(level3GoodGoodGood)
    board.pop()
    board.pop()
    # Add two children to Good Move -> Blunder
    board.push(blunderMove)
    #Black takes pawn
    blackTakes = board.parse_san('f6h4')
    board.push(blackTakes)
    level3GoodBadBad = MoveTree.Node(board, blackTakes, findAlphaBetaVal(board, board.turn), [], board.turn)
    rootNode.children[1].children[1].children.append(level3GoodBadBad)
    board.pop()
    # Black leaves pawn
    blackLeaves = board.parse_san('h7h5')
    board.push(blackLeaves)
    level3GoodBadGood = MoveTree.Node(board, blackLeaves, findAlphaBetaVal(board, board.turn), [], board.turn)
    rootNode.children[1].children[1].children.append(level3GoodBadGood)

    print("ROOT: ", rootNode)
    for child in rootNode.children:
        print("FIRST LEVEL CHILD: ", child)
    for child in rootNode.children[0].children:
        print("SECOND LEVEL BAD NODE CHILD: ", child)
    for child in rootNode.children[1].children:
        print("SECOND LEVEL GOOD NODE CHILD: ", child)
    for child in rootNode.children[0].children[0].children:
        print("THIRD LEVEL: ", child)
    for child in rootNode.children[1].children[0].children:
        print("THIRD LEVEL: ", child)
    for child in rootNode.children[0].children[1].children:
        print("THIRD LEVEL: ", child)
    for child in rootNode.children[1].children[1].children:
        print("THIRD LEVEL: ", child)

    print("\n \n \n \n")
    traverseABTree(rootNode, [])

    print("ROOT: ", rootNode)
    for child in rootNode.children:
        print("FIRST LEVEL CHILD: ", child)
    for child in rootNode.children[0].children:
        print("SECOND LEVEL BAD NODE CHILD: ", child)
    for child in rootNode.children[1].children:
        print("SECOND LEVEL GOOD NODE CHILD: ", child)
    for child in rootNode.children[0].children[0].children:
        print("THIRD LEVEL: ", child)
    for child in rootNode.children[1].children[0].children:
        print("THIRD LEVEL: ", child)
    for child in rootNode.children[0].children[1].children:
        print("THIRD LEVEL: ", child)
    for child in rootNode.children[1].children[1].children:
        print("THIRD LEVEL: ", child)


    print(findBestMoveFromABTree(rootNode))


