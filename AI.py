import chess
import Move
class ChessAI:
    def initiatePlayer(self, boardPosition):
        success = False
        while not success:
            nextMove = input("Please enter a move: ")
            try:
                boardPosition.push_san(nextMove)
                success = True
            except Exception as e:
                print('Bad Move: ', str(e))
        return boardPosition, nextMove


    def initiateComputer(self, boardPosition, lastMove):
        moveRunner = Move.Move()
        bestMove = moveRunner.getBestMove(boardPosition, lastMove)
        boardPosition.push(bestMove)
        return boardPosition

    def MonteCarlo(self, boardPosition):
        print(boardPosition)



# AIRunner = ChessAI()
# AIRunner.initiatePlayer(chess.Board())
