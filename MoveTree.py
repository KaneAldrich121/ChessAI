import chess


class Node:
    def __init__(self, boardPosition, thisMove, ABValue, children, turn):
        self.boardPosition = boardPosition
        self.thisMove = thisMove
        self.ABValue = ABValue
        self.children = children
        self.turn = turn

    def __str__(self):
        return f'Children: {self.children}, ABValue: {self.ABValue}, Turn: {self.turn}, Last Move: {self.thisMove}'

