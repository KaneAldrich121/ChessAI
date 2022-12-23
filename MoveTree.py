import chess


class Node:
    def __init__(self, boardPosition, thisMove, ABValue, children, turn, changed):
        self.boardPosition = boardPosition
        self.thisMove = thisMove
        self.ABValue = ABValue
        self.children = children
        self.turn = turn
        self.changed = changed

    def __str__(self):
        return f'Children: {self.children}, ABValue: {self.ABValue}, Turn: {self.turn}, Last Move: {self.thisMove}'

