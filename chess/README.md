# Chess

A fully functional chess minigame created using tkinter canvas.  
Pieces are moved using usual drag and drop with mouse that shows possible moves with held piece.  
Game is over when one player loses or it's a draw:
- A player can lose when they get checkmated or when they resign.
- The game is drawn by stalemate,draw offer,repetition and insufficient material(two knights is considered draw).


There are 4 usable buttons, namely New Game, Resign, Draw and Undo. 
- New Game resets the board with it being whites' turn
- Resign resigns the game for the player whose turn currently is
- Draw draws the game
- Undo undoes last turn, repeatable until start of the game

The game has all of these obviously fully functional:
- Inability to make a move that puts your king into check
- En Passant move 
- Castle on both sides works
- Pawn Promotion with selectable piece to promote to 
- Always checking for checkmate,stalemate and other ways the game might have ended

Overall the game works pretty well with no major bugs that break it (though there is minor bug that I noticed which prevents the pieces to be clicked sometimes).
I made the minigame relatively fast with minimal refactoring and/or planning ahead as I didn't want it to take up too much time, so the code is quite messy.
