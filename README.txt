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

The AI goes after pieces it can capture in a hierarchy (Queen, Rook, Bishop, Knight then Pawn), otherwise playing random moves if no immediate captures are
available. 

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

How to Run The Game:

The main file is the board_random_AI.py file, which contains the code for: Board class (methods: self, get_square, draw, makeButton, nextturn, kingLoc, moveTo, 
testmove, untestmove, callmove, get_all_moves), Movetypes class (moves for each piece, types of moves, check functions) and the main function. This is the file that 
should be actually run to play the game. 
The pieces.py file initializes the color and piece names for each piece
The Tile.py file contains the Tile class, defining functions for checking for empty tiles, enemy and ally tiles and checks for color of pieces
The chessai.py contains code for the AI, currently not integrated into the main file

Additionally - there are .png images for each piece in the game (black and white respectively) in addition to their highlighted counterparts. Additionally the 
"WhiteBackground.jpeg" is needed to initialize the board. The audio files "piecenoise.mp3" and "Kaisse.mp3" are used for playing the piece moving noises and 
background music that plays during the game. These should be loaded into the .venv file of the project if they are not already present (which they should already be)

------------

Any known bugs/issues with the program?

Currently, the features for stalemate and castling have not been implemented. The AI is also as of yet not able to parse potential moves and make moves
accordingly. Pawn Promotion currently does not occur and results in the pawns simply stopping at the end of the board. 
