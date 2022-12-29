import chess
import MoveTree
import AI
import PieceTables
from random import randint


def createABTree(rootNode, depth):
    movesToCheck = list(rootNode.boardPosition.legal_moves)
    movesToCheck = removeHangMoves(rootNode.boardPosition, movesToCheck, rootNode.turn, not rootNode.turn)
    for move in movesToCheck:
        # Create New Board Position
        thisBoard = rootNode.boardPosition.copy()
        thisBoard.push(move)
        # Find Alpha or Beta Value
        newABVal = findAlphaBetaVal(thisBoard)
        # Create New Node, Recurse Down into NewNode, Add it to Root Children
        newNode = MoveTree.Node(thisBoard, move, newABVal, [], thisBoard.turn, False)
        if depth - 1 > 0:
            newNode = createABTree(newNode, depth - 1)
        rootNode.children.append(newNode)
    return rootNode


def expandABTree(rootNode, expandDepth):
    if not rootNode.children:  # If Node is a leaf, create an ABTree here and attach to the tree
        rootNode = createABTree(rootNode, expandDepth)
        return
    else:
        for child in rootNode.children:
            child.changed = False
            expandABTree(child, expandDepth)
    return


def traverseABTree(rootNode, childValues):
    if not rootNode.children:  # If this node is a leaf (no children)
        foundValue = rootNode.ABValue
        return foundValue
    else:  # Node is not a leaf
        for treeChild in rootNode.children:
            childValue = traverseABTree(treeChild, childValues)
            if not rootNode.changed:
                rootNode.ABValue = childValue
                rootNode.changed = True
            elif rootNode.turn and childValue > rootNode.ABValue:
                rootNode.ABValue = childValue
            elif not rootNode.turn and childValue < rootNode.ABValue:
                rootNode.ABValue = childValue
        return rootNode.ABValue
    return


# Input: Board Position and Who's Turn it is
# Output: Either the Alpha or Beta Value of the given position depending on who's turn it is.
# Purpose: Finds Either the Alpha or Beta Value Depending on who's Turn it is.
def findAlphaBetaVal(boardPosition):
    # Is Checkmate?
    mate = 0
    if boardPosition.is_checkmate():
        if boardPosition.turn:
            mate = -1000
        else:
            mate = 1000

    # Calculate Point Difference
    whiteTotal = findAllPieceTotal(boardPosition, chess.WHITE)
    blackTotal = findAllPieceTotal(boardPosition, chess.BLACK)
    difference = whiteTotal - blackTotal

    # Find How Many Pieces this Move Attacks
    lastMove = boardPosition.peek()
    numberAttackedSquares = boardPosition.attacks(lastMove.to_square)
    piecesAttacked = 0

    # Pieces Attacked
    for square in numberAttackedSquares:
        if boardPosition.piece_at(square) and boardPosition.color_at(square) == boardPosition.turn:
            piecesAttacked += 1

    if boardPosition.turn:
        piecesAttacked *= -1

    # Position Calculation
    positionDifference = 0
    if boardPosition.fullmove_number <= 10:
        positionDifference = findPositionValue(lastMove.to_square, not boardPosition.turn,
                                        str(boardPosition.piece_at(lastMove.to_square)).lower())



    # AlphaBeta Function (Features = Difference, Pieces Attacked, Position (turn 10 and below), Mate)
    Value = (2 * difference) + (1.5 * piecesAttacked) + (1 * positionDifference) + mate
    return Value

def findPositionValue(squareName, turn, piece):
    pieceToTable = {'p': PieceTables.pawnTable, 'n': PieceTables.knightTable, 'b': PieceTables.bishopTable,
                    'r': PieceTables.rookTable, 'q': PieceTables.queenTable, 'k': PieceTables.kingTable,
                    7: PieceTables.pawnTable}
    boardOffset = 1
    if turn:
        boardOffset = 0
    fileNum = squareName // 8
    rankNum = squareName % 8
    table = pieceToTable[piece]
    squareValue = table[boardOffset][fileNum][rankNum]
    return squareValue





# Input: Current Board Position and Color in Question.
# Output: Sum Total of All Piece Values on the Board for the Given Color.
# Purpose: Calculates Sum Piece Total
def findAllPieceTotal(boardPosition, color):
    total = 0
    typeToValue = {1: 1, 2: 3, 3: 3, 4: 5, 5: 9, 6: 10}
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
        else:
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
    treeBestMoves = []
    treeBestEval = 10000  # Get minimum value of child nodes
    for treeChild in treeRoot.children:
        if treeChild.ABValue < treeBestEval:
            treeBestEval = treeChild.ABValue
            treeBestMoves.clear()
            treeBestMoves.append(treeChild)
        elif treeChild.ABValue == treeBestEval:
            treeBestMoves.append(treeChild)
    treeBestMove = None
    leastDepth = 100
    if treeBestEval > 500 or treeBestEval < -500:
        for possibleChild in treeBestMoves:
            thisDepth = findTreeDepth(possibleChild)
            if thisDepth < leastDepth:
                leastDepth = thisDepth
                treeBestMove = possibleChild
        return treeBestMove.thisMove, treeBestMove
    randomMove = randint(0, len(treeBestMoves) - 1)
    return treeBestMoves[randomMove].thisMove, treeBestMoves[randomMove]


def findTreeDepth(thisTree):
    depth = 0
    queue = thisTree.children
    while len(queue) != 0:
        size = len(queue)
        for i in range(0, size):
            thisNode = queue.pop(0)
            if not thisNode.children:
                return depth
            else:
                for thisChild in thisNode.children:
                    queue.append(thisChild)
        depth += 1
    return depth


def findTreeDepthMax(thisTree):
    depth = 0
    queue = []
    for child in thisTree.children:
        queue.append(child)
    while len(queue) != 0:
        size = len(queue)
        for i in range(0, size):
            thisNode = queue.pop(0)
            if not thisNode.children:
                return depth
            else:
                for thisChild in thisNode.children:
                    queue.append(thisChild)
        depth += 1
    return depth


def printTree(thisTree):
    level = 1
    queue = []
    for node in thisTree.children:
        queue.append(node)
    while len(queue) != 0:
        print(f'Level: {level}')
        thisLevelSize = len(queue)
        for i in range(0, thisLevelSize):
            thisNode = queue.pop(0)
            print(thisNode)
            for node in thisNode.children:
                queue.append(node)
        level += 1



if __name__ == '__main__':
    board = chess.Board()
    lastMove = board.parse_san('e2e4')
    board.push(lastMove)
    print(findAlphaBetaVal(board))

    # # Create Toy Tree
    # board = chess.Board("k3q3/5q2/8/8/8/8/8/5K2")
    # # Root Node
    # lastMove = board.parse_san('f1g1')
    # board.push(lastMove)
    # rootNode = MoveTree.Node(board, lastMove, 0, [], board.turn, False)
    # # Bad Child Depth 1
    # rightL1 = board.parse_san('e8d8')
    # board.push(rightL1)
    # badChild = MoveTree.Node(board, rightL1, findAlphaBetaVal(board, board.turn), [], board.turn, False)
    # rootNode.children.append(badChild)
    # board.pop()
    # # Good Child Depth 1
    # leftL1 = board.parse_san('e8g8')
    # board.push(leftL1)
    # goodChild = MoveTree.Node(board, leftL1, findAlphaBetaVal(board, board.turn), [], board.turn, False)
    # rootNode.children.append(goodChild)
    # board.pop()
    # # BAD CHILD CHILDREN
    # board.push(rightL1)
    # rightLeftL2 = board.parse_san('g1h1')
    # board.push(rightLeftL2)
    # level2BadGood = MoveTree.Node(board, rightLeftL2, findAlphaBetaVal(board, board.turn), [], board.turn, False)
    # rootNode.children[0].children.append(level2BadGood)
    # board.pop()
    # rightRightL2 = board.parse_san('g1h2')
    # board.push(rightRightL2)
    # level2BadBad = MoveTree.Node(board, rightRightL2, findAlphaBetaVal(board, board.turn), [], board.turn, False)
    # rootNode.children[0].children.append(level2BadBad)
    # board.pop()
    # board.pop()
    # # GOOD CHILD CHILDREN:
    # board.push(leftL1)
    # leftLeftL2 = board.parse_san('g1h1')
    # board.push(leftLeftL2)
    # level2GoodGood = MoveTree.Node(board, leftLeftL2, findAlphaBetaVal(board, board.turn), [], board.turn, False)
    # rootNode.children[1].children.append(level2GoodGood)
    # board.pop()
    # leftRightL2 = board.parse_san('g1h2')
    # board.push(leftRightL2)
    # level2GoodBad = MoveTree.Node(board, leftRightL2, findAlphaBetaVal(board, board.turn), [], board.turn, False)
    # rootNode.children[1].children.append(level2GoodBad)
    # board.pop()
    # board.pop()
    # # Board is at Start Position, add children for all children's children
    # # Add two children to Bad Move -> Good Response
    # board.push(rightL1)
    # board.push(rightLeftL2)
    # rightLeftLeftL3 = board.parse_san('d8g8')
    # board.push(rightLeftLeftL3)
    # level3BadGoodGood = MoveTree.Node(board, rightLeftLeftL3, findAlphaBetaVal(board, board.turn), [], board.turn, False)
    # rootNode.children[0].children[0].children.append(level3BadGoodGood)
    # board.pop()
    # rightLeftRightL3 = board.parse_san('d8d7')
    # board.push(rightLeftRightL3)
    # level3BadGoodBad = MoveTree.Node(board, rightLeftRightL3, findAlphaBetaVal(board, board.turn), [], board.turn, False)
    # rootNode.children[0].children[0].children.append(level3BadGoodBad)
    # board.pop()
    # board.pop()
    # # Add two children to Bad Move -> Bad Response
    # board.push(rightRightL2)
    # rightRightLeftL3 = board.parse_san('d8g8')
    # board.push(rightRightLeftL3)
    # level3BadBadGood = MoveTree.Node(board, rightRightLeftL3, findAlphaBetaVal(board, board.turn), [], board.turn, False)
    # rootNode.children[0].children[1].children.append(level3BadBadGood)
    # board.pop()
    # rightRightRightL3 = board.parse_san('d8d7')
    # board.push(rightRightRightL3)
    # level3BadBadBad = MoveTree.Node(board, rightRightRightL3, findAlphaBetaVal(board, board.turn), [], board.turn, False)
    # rootNode.children[0].children[1].children.append(level3BadBadBad)
    # board.pop()
    # board.pop()
    # board.pop()
    # # Add two children to Good Move -> Develop Move
    # board.push(leftL1)
    # board.push(leftLeftL2)
    # leftLeftLeftL3 = board.parse_san('f7h7')
    # board.push(leftLeftLeftL3)
    # level3GoodGoodBad = MoveTree.Node(board, leftLeftLeftL3, findAlphaBetaVal(board, board.turn), [], board.turn, False)
    # rootNode.children[1].children[0].children.append(level3GoodGoodBad)
    # board.pop()
    # leftLeftRightL3 = board.parse_san('g8h8')
    # board.push(leftLeftRightL3)
    # level3GoodGoodGood = MoveTree.Node(board, leftLeftRightL3, findAlphaBetaVal(board, board.turn), [], board.turn, False)
    # rootNode.children[1].children[0].children.append(level3GoodGoodGood)
    # board.pop()
    # board.pop()
    # # Add two children to Good Move -> Blunder
    # board.push(leftRightL2)
    # leftRightLeftL3 = board.parse_san('f7h7')
    # board.push(leftRightLeftL3)
    # level3GoodBadBad = MoveTree.Node(board, leftRightLeftL3, findAlphaBetaVal(board, board.turn), [], board.turn, False)
    # rootNode.children[1].children[1].children.append(level3GoodBadBad)
    # board.pop()
    # leftRightRightL3 = board.parse_san('g8h8')
    # board.push(leftRightRightL3)
    # level3GoodBadGood = MoveTree.Node(board, leftRightRightL3, findAlphaBetaVal(board, board.turn), [], board.turn, False)
    # rootNode.children[1].children[1].children.append(level3GoodBadGood)
    #
    # print("ROOT BEFORE TRAVERSAL: ", rootNode)
    # for child in rootNode.children:
    #     print("FIRST LEVEL CHILD: ", child)
    # for child in rootNode.children[0].children:
    #     print("SECOND LEVEL BAD NODE CHILD: ", child)
    # for child in rootNode.children[1].children:
    #     print("SECOND LEVEL GOOD NODE CHILD: ", child)
    # for child in rootNode.children[0].children[0].children:
    #     print("THIRD LEVEL: ", child)
    # for child in rootNode.children[0].children[1].children:
    #     print("THIRD LEVEL: ", child)
    # for child in rootNode.children[1].children[0].children:
    #     print("THIRD LEVEL: ", child)
    # for child in rootNode.children[1].children[1].children:
    #     print("THIRD LEVEL: ", child)
    #
    # print("\n \n \n \n")
    # traverseABTree(rootNode, [])
    #
    # print("ROOT AFTER TRAVERSAL: ", rootNode)
    # for child in rootNode.children:
    #     print("FIRST LEVEL CHILD: ", child)
    # for child in rootNode.children[0].children:
    #     print("SECOND LEVEL BAD NODE CHILD: ", child)
    # for child in rootNode.children[1].children:
    #     print("SECOND LEVEL GOOD NODE CHILD: ", child)
    # for child in rootNode.children[0].children[0].children:
    #     print("THIRD LEVEL: ", child)
    # for child in rootNode.children[0].children[1].children:
    #     print("THIRD LEVEL: ", child)
    # for child in rootNode.children[1].children[0].children:
    #     print("THIRD LEVEL: ", child)
    # for child in rootNode.children[1].children[1].children:
    #     print("THIRD LEVEL: ", child)
    # print(findBestMoveFromABTree(rootNode))
    # pass
