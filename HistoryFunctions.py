import chess
from random import randint

def writeMoveHistory(move):
    with open('MoveHistory.txt', 'a') as MH:
        MH.write(str(move))
    MH.close()

def checkForKnownOpening(lastMove):
    moveHistory = open('./MoveHistory.txt', 'r')
    thisMoveHistory = moveHistory.readlines()
    thisMoveHistory = thisMoveHistory[0]
    openingData = open('./KnownOpenings.txt', 'r')
    knownOpenings = openingData.readlines()
    possibles = []
    for opening in knownOpenings:
        if thisMoveHistory == opening[:len(thisMoveHistory)] and thisMoveHistory != opening[:-1]:
            print("Found Match")
            possibles.append(opening)
    if len(possibles) != 0:
        whichPossible = randint(0, len(possibles) - 1)
        return possibles[whichPossible][len(thisMoveHistory):len(thisMoveHistory) + 4]
    else:
        return None
