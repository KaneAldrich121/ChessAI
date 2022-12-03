import chess
import MoveTree


class Move:
    # Takes Board Position and Depth to Search and Returns
    def createMoveTree(self, thisRoot, curDepth, curBoard, curLeaves):
        # Base Case Check:
        if curDepth == 0:
            curLeaves.append(thisRoot)
            return
        # Update Board
        curBoard.push(thisRoot.thisMove)
        # Update History
        newHistory = thisRoot.historyToHere.copy()
        newHistory.append(thisRoot.thisMove)

        for move in list(board.legal_moves):
            # Make a Node for the Child Move
            node = MoveTree.Node(self.calculateMoveTotal(curBoard, move), newHistory, move, [])
            # Append the Child Node to Children
            thisRoot.children.append(node)
            self.createMoveTree(node, curDepth - 1, curBoard, curLeaves)
        curBoard.pop()
        return thisRoot, curLeaves

    def calculateMoveTotal(self, thisBoard, move):
        pieceVals = {"P": 1, "N": 3, "B": 3, "R": 5, "Q": 8, "K": 10,
                     "p": 1, "n": 3, "b": 3, "r": 5, "q": 8, "k": 10}
        capture = thisBoard.is_capture(move)
        gain = 0
        if capture:
            moveString = str(move)
            attackedSquare = moveString[2:]
            attackedPiece = board.piece_at(chess.parse_square(attackedSquare))
            gain = pieceVals[str(attackedPiece)]
        if not thisBoard.turn:
            gain = -gain
        return gain

    def getBestMove(self):
        pass

moveOperator = Move()
board = chess.Board()
thisMove = chess.Move(12, 28)
depth = 2
leaves = []
# Setting Up Create Tree Call
root = MoveTree.Node(moveOperator.calculateMoveTotal(board, thisMove), [], thisMove, [])
options, curLeaves = moveOperator.createMoveTree(root, depth, board, leaves)
bestMove = None
bestEval = -9999
for leaf in curLeaves:
    if leaf.evalHere > bestEval:
        bestEval = leaf.evalHere
        bestMove = leaf.historyToHere[1]
print(bestMove)






