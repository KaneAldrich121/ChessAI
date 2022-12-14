import chess
import Move
import MoveHelper
import HistoryFunctions
class ChessAI:
    def initiatePlayer(self, boardPosition):
        success = False
        while not success:
            nextMove = input("Please enter a move: ")
            try:
                boardPosition.push_san(nextMove)
                HistoryFunctions.writeMoveHistory(nextMove)
                success = True
            except Exception as e:
                print('Bad Move: ', str(e))
        return boardPosition, nextMove


    def initiateComputer(self, boardPosition, lastMove, previousTree):
        moveRunner = Move.Move()
        knownMove = HistoryFunctions.checkForKnownOpening(lastMove)
        if knownMove is not None:
            bestMove = boardPosition.parse_san(knownMove)
            boardPosition.push(bestMove)
            HistoryFunctions.writeMoveHistory(bestMove)
            return boardPosition, bestMove, None
        bestMove, previousTree = moveRunner.getBestMove(boardPosition, lastMove, previousTree)
        print("Computer Move: ", bestMove)
        boardPosition.push(bestMove)
        HistoryFunctions.writeMoveHistory(bestMove)
        if boardPosition.is_checkmate():
            print("Checkmate! You lose!")
        if boardPosition.is_stalemate():
            print("Stalemate! It's a Draw.")
        return boardPosition, bestMove, previousTree

    def MonteCarlo(self, boardPosition):
        result = self.initiateRandomComputer(boardPosition)
        return result

    def initiateRandomComputer(self, boardPosition):
        while not boardPosition.is_checkmate() and not boardPosition.is_stalemate() and \
                not boardPosition.is_seventyfive_moves():
            moveRunner = Move.Move()
            randomMove = moveRunner.getRandomMove(boardPosition)
            boardPosition.push(randomMove)
        return boardPosition.outcome()




# AIRunner = ChessAI()
# AIRunner.initiatePlayer(chess.Board())
