import chess
import AI
from Move import *

board = chess.Board()

while True:
    if board.turn:
        print(board)
        nextMove = input("Please enter a move: ")
        try:
            board.push_san(nextMove)
        except Exception as e:
            print('Bad Move: ', str(e))
    else:
        board.push(Move().getBestMove(nextMove, board))



