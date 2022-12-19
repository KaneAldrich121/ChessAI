import chess
import AI

import Move
boardPosition = chess.Board("r3k1q1/4P3/8/8/8/8/4PP1P/4KPQP")
AIRunner = AI.ChessAI()
firstTurn = True
open('MoveHistory.txt', 'w').close()

# player1 = input('Player 1: Player or Computer? ')
# player2 = input('Player 2: Player or Computer? ')
player1 = "Player"
player2 = "Computer"
while True:
    print('\n', '\n', '\n')
    print(boardPosition)
    if boardPosition.turn:
        if player1 == "Player":
            # Human White
            boardPosition, lastMove = AIRunner.initiatePlayer(boardPosition)
        else:
            # Computer White
            if firstTurn:
                lastMove = None
            boardPosition, lastMove = AIRunner.initiateComputer(boardPosition, lastMove)
            firstTurn = False
            print('---------------------------------------------------------------------------------------')
    else:
        if player2 == "Player":
            # Human Black
            boardPosition, lastMove = AIRunner.initiatePlayer(boardPosition)
        else:
            # Computer Black
            boardPosition, lastMove = AIRunner.initiateComputer(boardPosition, lastMove)




