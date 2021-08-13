def move_in_piece_moveset(piece, x_move, y_move):
    print(x_move, y_move)

    movesets = {
        "pawn": ((0, 1), (0, 2), (1, 1)),
        "rook": ((0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
                 (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)),
        "knight": ((2, 1), (1, 2)),
        "bishop": ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7)),
        "king": ((0, 1), (1, 0), (1, 1)),
        "queen": ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7),
                  (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
                  (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0))
    }
    if not ((abs(x_move), abs(y_move)) in movesets[piece.piece]):
        return False

    if piece.piece == "pawn" and ((piece.color == "white" and y_move > 0) or (piece.color == "black" and y_move < 0)):
        return False
    return True
