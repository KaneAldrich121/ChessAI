import chess
import MoveTree


class Move:
    # Takes Board Position and Depth to Search and Returns
    def createMoveTree(self, thisRoot, curDepth, curBoard, curLeaves):
        # Base Case Check:
        if curDepth == 0:
            curLeaves.append(thisRoot)
            return

        # Update History
        newHistory = thisRoot.historyToHere.copy()
        newHistory.append(thisRoot.thisMove)

        for move in list(curBoard.legal_moves):
            # Make a Node for the Child Move
            node = MoveTree.Node(self.calculateMoveTotal(curBoard, move), newHistory, move, [])
            # Append the Child Node to Children
            thisRoot.children.append(node)
            curBoard.push(move)
            self.createMoveTree(node, curDepth - 1, curBoard, curLeaves)
            curBoard.pop()
        return thisRoot, curLeaves

    def calculateMoveTotal(self, thisBoard, move):
        # pieceVals = {"P": 1, "N": 3, "B": 3, "R": 5, "Q": 8, "K": 10,
        #              "p": 1, "n": 3, "b": 3, "r": 5, "q": 8, "k": 10}
        # print("This Board: ", thisBoard)
        # print("This Move: ", move)
        # capture = thisBoard.is_capture(move)
        # gain = 0
        # if capture:
        #     moveString = str(move)
        #     attackedSquare = moveString[2:]
        #     attackedPiece = thisBoard.piece_at(chess.parse_square(attackedSquare))
        #     gain = pieceVals[str(attackedPiece)]
        # if not thisBoard.turn:
        #     gain = -gain
        # return gain
        return 0

    def getBestMove(self, lastMove, curBoard):
        # Check for Checkmate:
        if curBoard.is_checkmate():
            print("You Win! Good game")
            exit()

        # Generate Move Object for the Move Called thisMove (this is the last move played)
        firstSquare = lastMove[:2]
        secondSquare = lastMove[2:]
        fromSquare = chess.parse_square(firstSquare)
        toSquare = chess.parse_square(secondSquare)
        thisMove = chess.Move(fromSquare, toSquare)

        # Set Variables Needed
        depth = 2
        leaves = []

        # Calculate the Root Node
        thisRoot = MoveTree.Node(moveOperator.calculateMoveTotal(curBoard, thisMove), [], thisMove, [])

        # Generate a Move Tree Starting from the Root Node (Board reflects last move played)
        theseOptions, theseCurLeaves = moveOperator.createMoveTree(thisRoot, depth, curBoard, leaves)

        # Find Best Move from Leaves
        bestMove = None
        bestEval = -9999
        for leaf in theseCurLeaves:
            if leaf.evalHere > bestEval:
                bestEval = leaf.evalHere
                bestMove = leaf.historyToHere[1]
        return bestMove


moveOperator = Move()
board = chess.Board()
