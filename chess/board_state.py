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

    def is_checked(self, color):
        king_tile = self.find_king_tile(color)
        if king_tile.is_checked(color, self):
            return True
        else:
            return False

    def is_checkmated(self, color):
        king_tile = self.find_king_tile(color)
        tiles_around = ((0, 1), (0, -1), (1, -1), (1, 0), (1, 1), (-1, -1), (-1, 0), (-1, 1))

        for around_x, around_y in tiles_around:
            x = king_tile.x + around_x
            y = king_tile.y + around_y
            around_tile = self.chessboard[y][x]
            around_piece = around_tile.piece
            if 0 <= x < 8 and 0 <= y < 8:
                if not (around_tile.is_checked(color,self) or (
                        around_piece and around_piece.color == color)):
                    return False
        return True

    def find_king_tile(self, color):
        king_tile = None
        for y in range(8):
            for x in range(8):
                piece = self.chessboard[y][x].piece
                if piece and piece.color == color and piece.piece == "king":
                    king_tile = self.chessboard[y][x]
        return king_tile
