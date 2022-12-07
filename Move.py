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
        depth = 3
        leaves = []

        print("Known Opening Check")
        # Check For a Known Opening
        openMove = HistoryFunctions.checkForKnownOpening(lastMove)
        if openMove is not None:
            return curBoard.parse_san(openMove)

        firstLevelLegalMoves = list(curBoard.legal_moves)
        compColor = chess.BLACK
        oppColor = chess.WHITE
        if curBoard.turn:
            compColor = chess.WHITE
            oppColor = chess.BLACK

        print("Removed Hanging Moves")
        # Check for Moves Which will Hang a Piece and Remove Them from Considered Moves
        firstLevelLegalMoves = MoveHelper.removeHangMoves(curBoard, firstLevelLegalMoves, compColor, oppColor)

        print("Undefended Piece Check")
        # Check for Undefended Pieces to Attack
        hangAttack = MoveHelper.findHangingPieces(curBoard, firstLevelLegalMoves)
        if hangAttack is not None:
            return hangAttack

        # Calculate the Root Node
        thisRoot = MoveTree.Node(0, [], lastMove, [], curBoard)

        # Generate a Move Tree Starting from the Root Node (Board reflects last move played)
        #theseCurLeaves = MoveHelper.createMoveTree(thisRoot, depth, curBoard, leaves, firstLevelLegalMoves, compColor,
        #                                          oppColor)

        # for leaf in theseCurLeaves:
        #     print(leaf)
        #     exit()
        # print("Point Value Check")
        # # Attempt to Find Best Move by Point Vals
        # thisBestMove = MoveHelper.calculateByPointVals(theseCurLeaves)
        # if thisBestMove is not None:
        #     return thisBestMove
        #
        # print("MonteCarlo")
        # # Find Best Move from Leaves Using MonteCarlo
        # thisBestMove = MoveHelper.calculateByMonteCarlo(theseCurLeaves, curBoard)
        # return thisBestMove

    def getRandomMove(self, boardPosition):
        listOfLegal = list(boardPosition.legal_moves)
        moveNum = randint(0, len(listOfLegal) - 1)
        return listOfLegal[moveNum]
