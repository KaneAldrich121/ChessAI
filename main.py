import chess
import AI
import Move

while True:
    if Move.board.turn:
        print(Move.board)
        nextMove = input("Please enter a move: ")
        try:
            Move.board.push_san(nextMove)
        except Exception as e:
            print('Bad Move: ', str(e))
    else:
        break
