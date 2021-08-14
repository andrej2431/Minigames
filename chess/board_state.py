class BoardState:
    def __init__(self, chessboard, pieces, turn="white", history=None, selected=None, piece_stack_height=0):
        self.chessboard = chessboard
        self.pieces = pieces
        self.tile_list = [tile for row in self.chessboard for tile in row]
        self.ongoing = True
        self.turn = turn
        self.move_number = 0

        self.check = False
        self.checkmate = False
        self.stalemate = False
        self.game_over = False
        self.victory_screen = None

        self.selected = selected
        self.history = history if history else []
        self.piece_stack_height = piece_stack_height

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

    def check_around_king(self, color):
        king_tile = self.find_king_tile(color)

        if king_tile.king_tiles(self,color):
            return False
        else:
            return True

    def is_stalemate(self, color):
        if not self.check_around_king(color):
            return False

        for tile in self.tile_list:
            if not tile.piece or tile.piece.color != color:
                continue
            piece = tile.piece
            if piece and piece.piece == "king":
                continue

            if tile.available_tiles_from_piece(self):
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
