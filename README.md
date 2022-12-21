# ChessAI
To Do:
- Add detection for moves which hang pieces and don't consider them (potentially imperfect but only in very unique cases I can figure out later)
- Add check detection and create a tree based on them to search for possible checkmates or other forced winning moves
- Optimize ABTree calculations, right now the slowest thing seems to be detecting how many pieces a move attacks, but nothing about it is particularly fast. Maybe experiment with some kind of dictionary to speed up repeated calculations?
