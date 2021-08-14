import tkinter as tk


class Tile:
    def __init__(self, x, y, canvas, size=100):
        self.piece = None
        self.x = x
        self.y = y
        self.size = size
        self.canvas = canvas

        self.rect = canvas.create_rectangle(x * size, y * size, (x + 1) * size, (y + 1) * size, fill="", width=0,
                                            tag="tile")

    def recall_piece(self):
        if not self.piece:
            raise ValueError(f"Tile({self.x}, {self.y}) doesn't have a piece for some reason!")

        center_x = self.x * self.size + self.size // 2
        center_y = self.y * self.size + self.size // 2

        self.piece.move_to(center_x, center_y)

    def erase_piece(self):
        if not self.piece:
            return
        self.piece.erase()
        self.piece = None

    def move_piece_to(self, end_tile):
        end_tile.piece = self.piece
        self.piece = None
        end_tile.recall_piece()

    def is_checked(self, color, state):
        for tile in self.knight_tiles(state, color=color):
            piece = tile.piece
            if piece and piece.color != color and piece.piece == "knight":
                return True

        # ---- bishop/queen diagonal check
        for tile in self.bishop_tiles(state, color=color):
            piece = tile.piece
            if piece and piece.color != color and piece.piece in ("bishop", "queen"):
                return True

        # rook/queen straight check
        for tile in self.rook_tiles(state, color=color):
            piece = tile.piece
            if piece and piece.color != color and piece.piece in ("rook", "queen"):
                return True

        # pawn check
        for pawn_x, pawn_y in ((-1, 1), (1, 1)):
            if color == "white":
                pawn_y *= -1
            piece = state.chessboard[pawn_y+self.y][pawn_x + self.x].piece
            if piece and piece.color!=color and piece.piece == "pawn":
                return True
        return False

    def knight_tiles(self, state, color=None):
        tiles = []
        knight_attacks = ((1, 2), (-1, 2), (1, -2), (-1, -2), (2, 1), (-2, 1), (2, -1), (-2, -1))
        for knight_x, knight_y in knight_attacks:
            x = knight_x + self.x
            y = knight_y + self.y
            if 0 <= x < 8 and 0 <= y < 8:
                tile = state.chessboard[y][x]
                if color and tile.piece and tile.piece.color == color:
                    continue
                tiles.append(tile)

        return tiles

    def bishop_tiles(self, state, color=None):
        tiles = []
        for x_mul, y_mul in ((1, 1), (-1, 1), (1, -1), (-1, -1)):
            for x in range(1, 8):
                y = x*y_mul+self.y
                x = x*x_mul+self.x
                if not (0 <= x < 8 and 0 <= y < 8):
                    break
                tile = state.chessboard[y][x]

                if color and tile.piece and tile.piece.color == color:
                    break
                tiles.append(tile)
                if tile.piece:
                    break
        return tiles

    def rook_tiles(self, state, color=None):
        tiles = []
        for x_mul, y_mul in ((0, -1), (0, 1), (-1, 0), (1, 0)):
            for x in range(1, 8):
                y = x*y_mul+self.y
                x = x*x_mul+self.x
                if not (0 <= x < 8 and 0 <= y < 8):
                    break
                tile = state.chessboard[y][x]

                if color and tile.piece and tile.piece.color == color:
                    break
                tiles.append(tile)
                if tile.piece:
                    break
        return tiles

    def __repr__(self):
        return f"Tile({self.x},{self.y}):{self.piece}"
