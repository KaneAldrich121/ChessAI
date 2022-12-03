import chess


class Node:
    def __init__(self, evalHere: int, historyToHere: list[chess.Move], thisMove: chess.Move,
                 children: list['Node']):
        self.evalHere = evalHere
        self.historyToHere = historyToHere
        self.thisMove = thisMove
        self.children = children

    def __str__(self):
        return f"History to here: {self.historyToHere} This move: {self.thisMove} Children: {self.children}"

    def addNode(self, eval: int, history: list[chess.Move], move: chess.Move, children: list['Node']):
        thisNode = Node(eval, history, move, children)
        return thisNode
