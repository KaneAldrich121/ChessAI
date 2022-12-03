import chess
import AI
# import Move

board = chess.Board()
while True:
    if board.turn:
        print(board)
        print(list(board.legal_moves))
        nextMove = input("Please enter a move: ")
        try:
            board.push_san(nextMove)
        except Exception as e:
            print('Bad Move: ', str(e))
    else:
        legalMoves = list(board.legal_moves)
        board.push(legalMoves[0])
        # nextMove = Move.getNextMove(board, 2)
