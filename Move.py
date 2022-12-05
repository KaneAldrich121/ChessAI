import chess
import MoveTree
import MoveHelper
import HistoryFunctions
import AI
from random import randint


class Move:

    def getBestMove(self, curBoard, lastMove):  # Takes Current Board and Last Move
        AIRunner = AI.ChessAI()
        # Check for Checkmate:
        if curBoard.is_checkmate():
            print("You Win! Good game")
            exit()
        if lastMove is None:
            return curBoard.parse_san('e2e4')

        # Generate Move Object for the Move Called lastMoveMove (this is the last move played) and Add to Board
        if type(lastMove) == str:
            curBoard.pop()
            lastMove = curBoard.parse_san(lastMove)
            curBoard.push(lastMove)

        # Set Variables Needed
        depth = 2
        leaves = []

        # Check For a Known Opening
        openMove = HistoryFunctions.checkForKnownOpening(lastMove)
        if openMove is not None:
            return curBoard.parse_san(openMove)

        firstLevelLegalMoves = set(curBoard.legal_moves)

        # Check for Moves Which will Hang a Piece

        # Check for Undefended Pieces to Attack
        goodPossibles = MoveHelper.findHangingPieces(curBoard)
        bestMove = None
        if len(goodPossibles) is not 0:
            for move in goodPossibles:
                firstLevelLegalMoves.remove(move)
                lowestVal = 100
                if MoveHelper.findPieceValue(move.from_square, curBoard) < lowestVal:
                    lowestVal = MoveHelper.findPieceValue(move.from_square, curBoard)
                    bestMove = move
        if bestMove is not None:
            return bestMove


        # Calculate the Root Node
        thisRoot = MoveTree.Node(0, [], lastMove, [])

        # Generate a Move Tree Starting from the Root Node (Board reflects last move played)
        endRoot, theseCurLeaves = MoveHelper.createMoveTree(thisRoot, depth, curBoard, leaves)

        # Attempt to Find Best Move by Point Vals
        thisBestMove = MoveHelper.calculateByPointVals(theseCurLeaves)
        if thisBestMove is not None:
            return thisBestMove

        # Find Best Move from Leaves Using MonteCarlo
        thisBestMove = MoveHelper.calculateByMonteCarlo(theseCurLeaves, curBoard)
        return thisBestMove

    def getRandomMove(self, boardPosition):
        listOfLegal = list(boardPosition.legal_moves)
        moveNum = randint(0, len(listOfLegal) - 1)
        return listOfLegal[moveNum]
