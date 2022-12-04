import chess
import AI
from Move import *
boardPosition = chess.Board()
AIRunner = AI.ChessAI()


while True:
    if boardPosition.turn:
        print(boardPosition)
        boardPosition, lastMove = AIRunner.initiatePlayer(boardPosition)
    else:
        boardPosition = AIRunner.initiateComputer(boardPosition, lastMove)




