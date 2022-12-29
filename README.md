# ChessAI
To Do:
- Optimize ABTree so that it can go even deeper. Experiment with pruning branches and also passing through the ABTree calculated in the previous iteration so that the algorithm only needs to build on itself, not recalculate nodes it has already seen. 
  - This could be done with a dictionary which maps board positions to evaluations, or by passing the subtree of the ABTree which coincides with the move the computer chooses back to main, and then further taking only the subtree which matches the move the player has chosen. It's worth noting that in the current implementation this will only save calculation of one level of depth, but every little bit helps. Worth noting that this cannot be combined with pruning branches, at least not without some extra checks. 
  - Figure out what parts of the current implementation are taking the longest and optimize them.
- Specifically investigate why the series d2d4, b8c6, e2e4, leads to c6b4. That's not the move we'd want to play there, maybe figure out a way to penalize moving the same piece twice in the AB evaluation stage?
- Position Evaluation for first 10 moves
