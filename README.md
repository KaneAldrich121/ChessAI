# ChessAI
To Do:
- Add detection for moves which hang pieces and don't consider them (potentially imperfect but only in very unique cases I can figure out later)
- Add check detection and create a tree based on them to search for possible checkmates or other forced winning moves
- Modify MoveTree to have each node include a representation of the board the node is for, easier to use.
- Start looking for pins and other tactics to improve move finding when there is no obvious choice (hanging pieces)
- Continue streamlining slowest parts, currently the MonteCarlo process. 
