Project Report

Project Name: “3 Stooges' Chess”
Produced by: Jake Schaefer, Rahim Hamid, Dean M Watkins

------------

What is our project?
 
Our project is a game - Chess


In defining a "standard chess game," our code produces a two-player adversarial game, the setting of which is a board comprising 64 squares of two varying colors, brown and beige. Two sides of the board consist of 16 pieces each, with 6 types of pieces (each with unique move sets): the King, the Queen, the Bishop, the Knight, the Rook, and the Pawn. For each side, there are 8 Pawns; 2 Rooks, Knights, and Bishops; and 1 King and Queen. The pieces of one side attempt to surround the opposing King in a manner by which said King cannot move in any direction without being captured in a follow-up move by their opposition. This would be a checkmate.
The player is assigned to the white pieces, and the AI to the black pieces.

------------

How is AI implemented?

Currently, the AI plays random moves (aside from the opening move e5), selected from a list of valid moves. We are working to try and implement basic openings and a system to evaluate the best moves for both sides and play accordingly. 

------------

How does the Player operate the game?

The Human Player exclusively plays the white side, beginning with moving any piece legally. This is achieved by clicking the tile containing the piece they wish to move, and then clicking a tile to which a legal move may be made. The opposing AI will move a black piece in turn. This sequence of events will continue until a checkmate occurs.

------------

Rules:
White begins on as the first turn, with turns alternating between black and white after that.
Pawns may move one or two spaces on their first turn, but only one space on subsequent turns. They capture one space diagonally in front of them.
Bishops move on the either light or dark square diagonals.
Knights move in an L-shape
Rooks move straight across ranks and files they occupy
Queens move both diagonals and straight across occupied ranks and files
Kings can move one square in any direction
Check occurs when an enemy piece is attacking the King. No move can be made that does not either move the King out of the way, captures the checking piece or places 
a piece in between the king and the checking piece (aside from the Knight).
Checkmate occurs when the king is in check and there are no other legal moves the side being checked is able to make to break the check. This ends the game. 

------------

Any known bugs/issues with the program?

None that we, the coders, and the play-testers have discovered over numerous hours of testing the program.
