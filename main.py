import chess
import AI

import Move
boardPosition = chess.Board()
AIRunner = AI.ChessAI()
firstTurn = True
open('MoveHistory.txt', 'w').close()

# player1 = input('Player 1: Player or Computer? ')
# player2 = input('Player 2: Player or Computer? ')
player1 = "Player"
player2 = "Computer"
previousTree = None
lastMove = None
while True:
    if boardPosition.turn:
        if player1 == "Player":
            print('\n', '\n', '\n')
            if lastMove is not None:
                print(f"Computer Move: {lastMove}")
            print(boardPosition)
            if boardPosition.is_checkmate():
                print("Checkmate! You lose!")
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
            print('\n', '\n', '\n')
            print(boardPosition)
            # Human Black
            boardPosition, lastMove = AIRunner.initiatePlayer(boardPosition)
        else:
            # Computer Black
            boardPosition, lastMove, previousTree = AIRunner.initiateComputer(boardPosition, lastMove, previousTree)




