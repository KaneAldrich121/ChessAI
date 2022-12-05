import chess
import MoveTree
import AI
from random import randint

def createMoveTree(thisRoot, curDepth, curBoard, curLeaves):
    # Base Case Check:
    if curDepth == 0:
        curLeaves.append(thisRoot)
        return

    # Update History
    newHistory = thisRoot.historyToHere.copy()
    newHistory.append(thisRoot.thisMove)

    for move in list(curBoard.legal_moves):
        pointDif = thisRoot.pointDif
        # Calculate Point Difference for New Move
        if calculateMinPieceGain(curBoard, move) is not None:
            pointDif += calculateMinPieceGain(curBoard, move)
        else:
            break
        # Make a Node for the Child Move
        node = MoveTree.Node(pointDif, newHistory, move, [])
        # Append the Child Node to Current Node Children
        thisRoot.children.append(node)
        # Update Board With New Considered Move
        curBoard.push(move)
        # Create a Move Tree with New Considered Board and Move
        createMoveTree(node, curDepth - 1, curBoard, curLeaves)
        curBoard.pop()
    return thisRoot, curLeaves


def calculateMinPieceGain(boardPosition, lastMove):
    pieceVals = {'p': 1, 'n': 3, 'b': 3, "r": 5, "q": 8, "k": 10,
                 'P': 1, 'N': 3, 'B': 3, "R": 5, "Q": 8, "K": 10}
    # Finds who will potentially attack back
    if boardPosition.turn:
        myColor = chess.WHITE
        oppColor = chess.BLACK
    else:
        myColor = chess.BLACK
        oppColor = chess.WHITE
    if boardPosition.is_capture(lastMove):
        attackingPiece = boardPosition.piece_at(lastMove.from_square)
        attackedPiece = boardPosition.piece_at(lastMove.to_square)
        attackingVal = pieceVals[chess.PIECE_SYMBOLS[attackingPiece.piece_type]]
        attackedVal = pieceVals[chess.PIECE_SYMBOLS[attackedPiece.piece_type]]
        attackGain = attackedVal
        if not boardPosition.is_attacked_by(oppColor, lastMove.to_square):
            return 10000
        else:
            # This Finds the Set of all Squares which attack the given square, use later
            # allAttackerSquares = list(boardPosition.attackers(color, lastMove.to_square))
            return attackGain - attackingVal
    else:
        attackers = len(boardPosition.attackers(oppColor, lastMove.to_square))
        defenders = len(boardPosition.attackers(myColor, lastMove.to_square))
        if attackers > defenders:
            return None
        else:
            return 0

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


def findHangingPieces(curBoard):
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
    return goodPossibles


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

def findPieceValue(square, boardPosition):
    pieceVals = {'p': 1, 'n': 3, 'b': 3, "r": 5, "q": 8, "k": 10,
                 'P': 1, 'N': 3, 'B': 3, "R": 5, "Q": 8, "K": 10}
    attackingPiece = boardPosition.piece_at(square)
    attackingVal = pieceVals[chess.PIECE_SYMBOLS[attackingPiece.piece_type]]
    return attackingVal