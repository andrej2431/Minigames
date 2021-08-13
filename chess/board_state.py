class BoardState:
    def __init__(self, chessboard, turn="white", history=None, selected=None, piece_stack_height=0):
        self.chessboard = chessboard
        self.ongoing = True
        self.turn = turn
        self.move_number = 0
        self.selected = selected
        self.history = history if history else []
        self.piece_stack_height = piece_stack_height

        self.pieces = {"white": {"pawn": 8, "rook": 2, "knight": 2, "bishop": 2, "king": 1, "queen": 1},
                       "black": {"pawn": 8, "rook": 2, "knight": 2, "bishop": 2, "king": 1, "queen": 1}}

    def next_turn(self):
        if self.turn == "white":
            self.turn = "black"
        else:
            self.turn = "white"
        self.move_number += 1
