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

        # Check for Moves Which will Hang a Piece and Remove Them from Considered Moves
        firstLevelLegalMoves = MoveHelper.removeHangMoves(curBoard, firstLevelLegalMoves, compColor, oppColor)

        # Check for Undefended Pieces to Attack
        hangAttack = MoveHelper.findHangingPieces(curBoard, firstLevelLegalMoves)
        if hangAttack is not None:
            return hangAttack

        print("Build Tree")
        # Create Alpha Beta Tree
        depth = 1
        # Create Root Node
        root = MoveTree.Node(curBoard, lastMove, 0, [], curBoard.turn)
        thisTree = MoveHelper.createABTree(root, depth)
        MoveHelper.traverseABTree(thisTree, [])
        bestMove = MoveHelper.findBestMoveFromABTree(thisTree)
        return bestMove

    def getRandomMove(self, boardPosition):
        listOfLegal = list(boardPosition.legal_moves)
        moveNum = randint(0, len(listOfLegal) - 1)
        return listOfLegal[moveNum]
