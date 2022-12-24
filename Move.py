import chess
import MoveTree
import MoveHelper
import HistoryFunctions
import AI
import time
from random import randint


class Move:

    def getBestMove(self, curBoard, lastMove, previousTree):  # Takes Current Board and Last Move
        AIRunner = AI.ChessAI()
        # Check for Checkmate:
        if curBoard.is_checkmate():
            print("You Win! Good game")
            exit()
        if curBoard.is_stalemate():
            print("Stalemate! It's a Draw.")
            exit()

        # Generate Move Object for the Move Called lastMoveMove (this is the last move played) and Add to Board
        if type(lastMove) == str:
            curBoard.pop()
            lastMove = curBoard.parse_san(lastMove)
            curBoard.push(lastMove)

        # Set Variables Needed

        # Check For a Known Opening
        # tic = time.perf_counter()
        # openMove = HistoryFunctions.checkForKnownOpening(lastMove)
        # if openMove is not None:
        #     return curBoard.parse_san(openMove)
        # toc = time.perf_counter()
        # print(f"Time for Known Opening Check: {toc-tic:0.4f}")

        firstLevelLegalMoves = list(curBoard.legal_moves)
        firstLevelLegalMoves = MoveHelper.removeHangMoves(curBoard, firstLevelLegalMoves,
                                                          curBoard.turn, not curBoard.turn)
        compColor = chess.BLACK
        oppColor = chess.WHITE
        if curBoard.turn:
            compColor = chess.WHITE
            oppColor = chess.BLACK

        # Check for Undefended Pieces to Attack
        # hangAttack = MoveHelper.findHangingPieces(curBoard, firstLevelLegalMoves)
        # if hangAttack is not None:
        #     return hangAttack

        # Create Alpha Beta Tree
        createDepth = 3
        possibleMoves = len(firstLevelLegalMoves)
        if possibleMoves < 5:
            print("LESS THAN 5 MOVES")
            expandDepth = 4
        elif possibleMoves < 10:
            print("LESS THAN 10 MOVES")
            expandDepth = 3
        else:
            expandDepth = 2
        startingEval = 0
        children = []
        # If previous tree is available, move root to the node which corresponds with the user's move, otherwise create
        # new node.
        if previousTree is not None:
            for child in previousTree.children:
                if child.thisMove == lastMove:
                    root = child
                    startingEval = child.ABValue
                    children = child.children
                    break
            tic = time.perf_counter()
            MoveHelper.expandABTree(root, expandDepth)
            toc = time.perf_counter()
            print(f"Time for Expand Tree: {toc - tic:0.4f}")
            print("EXPANDED TREE DEPTH: ", MoveHelper.findTreeDepthMax(root))
        else:
            root = MoveTree.Node(curBoard, lastMove, startingEval, children, curBoard.turn, False)
            tic = time.perf_counter()
            root = MoveHelper.createABTree(root, createDepth)
            toc = time.perf_counter()
            print(f"Time for Creating New Tree: {toc - tic:0.4f}")
        if not root.children:
            return list(curBoard.legal_moves)[0], []

        tic = time.perf_counter()
        MoveHelper.traverseABTree(root, [])
        toc = time.perf_counter()
        print(f"Time for Traversal: {toc - tic:0.4f}")
        tic = time.perf_counter()
        bestMove, rootChosen = MoveHelper.findBestMoveFromABTree(root)
        toc = time.perf_counter()
        print(f"Time for Finding Best Move: {toc - tic:0.4f}")
        return bestMove, rootChosen

    def getRandomMove(self, boardPosition):
        listOfLegal = list(boardPosition.legal_moves)
        moveNum = randint(0, len(listOfLegal) - 1)
        return listOfLegal[moveNum]
