Project Report

Project Name: “3 Stooges' Chess”
Produced by: Jake Schaefer, Rahim Hamid, Dean M Watkins

------------

What is our project?
 
Our project is a game– it presents a standard chess game.

In defining a "standard chess game," our code produces a two-player adversarial game, the setting of which is a board comprising 64 squares of two varying colors, brown and beige. Two sides of the board consist of 16 pieces each, with 6 types of pieces (each with unique move sets): the King, the Queen, the Bishop, the Knight, the Rook, and the Pawn. For each side, there are 8 Pawns; 2 Rooks, Knights, and Bishops; and 1 King and Queen. The pieces of one side attempt to surround the opposing King in a manner by which said King cannot move in any direction without being captured in a follow-up move by their opposition. This would be a checkmate.
The player is assigned to the white pieces, and the AI to the black pieces.

------------

How is AI implemented?

The player plays against an richly complex A.I., the difficulty of which varies, as per the selection of the player before the game. These levels of difficulty are as follows: Random, Easy, Hard, Extreme. In order to implement such difficulties, we train/operate the A.I. differently for each difficulty:
- Random -> Uses exclusively random legal moves
- Easy -> Trained on Jake’s games on Chess.com
- Hard -> Rahim's games on Chess.com
- Extreme -> Carlsen’s games

------------

How does the Player operate the game?

Initially, the player will be displayed the four aforementioned difficulty levels, and will select one by typing it in. Thereafter, the visual of a chessboard is produced, and the game commences. 
The player begins by moving a white piece. This is achieved by clicking the tile containing the piece they wish to move, and then clicking a tile to which a legal move may be made. The opposing AI will move a black piece in turn. This sequence of events will continue until a checkmate occurs.
The player may also engage in castling, en passant, and fancy draws, by clicking accordingly (EDIT).

------------

Any known bugs/issues with the program?

None that we, the coders, and the play-testers have discovered over numerous hours of testing the program.