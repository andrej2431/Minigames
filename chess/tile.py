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
        self.piece.unmoved = False
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
            x, y = pawn_x + self.x, pawn_y + self.y
            if not (0 <= x < 8 and 0 <= y < 8):
                continue
            piece = state.chessboard[y][x].piece
            if piece and piece.color != color and piece.piece == "pawn":
                return True
        return False

    def pawn_tiles(self, state, color=None):
        if not color or not self.piece:
            return []

        tiles = []

        x, y, y_mul = self.x, self.y, -1 if color == "white" else 1
        for new_x, new_y in ((x, y + y_mul), (x, y + 2 * y_mul), (x - 1, y + y_mul), (x + 1, y + y_mul)):
            if not (0 <= new_x < 8 and 0 <= new_y < 8):
                continue
            end_tile = state.chessboard[new_y][new_x]
            if new_x != x and end_tile.piece and end_tile.piece.color != color:
                tiles.append(end_tile)
            elif new_x == x and not end_tile.piece and (abs(new_y - y) == 1 or self.piece.unmoved):
                tiles.append(end_tile)

        return tiles

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
                y = x * y_mul + self.y
                x = x * x_mul + self.x
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
                y = x * y_mul + self.y
                x = x * x_mul + self.x
                if not (0 <= x < 8 and 0 <= y < 8):
                    break
                tile = state.chessboard[y][x]

                if color and tile.piece and tile.piece.color == color:
                    break
                tiles.append(tile)
                if tile.piece:
                    break
        return tiles

    def king_tiles(self, state, color=None):
        tiles = []
        tiles_around = ((0, 1), (0, -1), (1, -1), (1, 0), (1, 1), (-1, -1), (-1, 0), (-1, 1))
        for around_x, around_y in tiles_around:
            x = self.x + around_x
            y = self.y + around_y

            if 0 <= x < 8 and 0 <= y < 8:
                around_tile = state.chessboard[y][x]
                around_piece = around_tile.piece
                if not (around_tile.is_checked(color, state) or (
                        around_piece and around_piece.color == color)):
                    tiles.append(around_tile)
        return tiles

    def available_tiles_from_piece(self, state):
        if not self.piece:
            return []

        piece = self.piece

        if piece.piece == "knight":
            available_tiles = self.knight_tiles(state, piece.color)
        elif piece.piece == "bishop":
            available_tiles = self.bishop_tiles(state, color=piece.color)
        elif piece.piece == "rook":
            available_tiles = self.rook_tiles(state, color=piece.color)
        elif piece.piece == "queen":
            available_tiles = self.rook_tiles(state, color=piece.color)
            available_tiles.extend(self.bishop_tiles(state, color=piece.color))
        elif piece.piece == "pawn":
            available_tiles = self.pawn_tiles(state, color=piece.color)

        elif piece.piece == "king":
            available_tiles = self.king_tiles(state, color=piece.color)
        else:
            available_tiles = []

        check_proof_tiles = []

        for tile in available_tiles:
            temp_piece = tile.piece
            if temp_piece and temp_piece.piece == "king":
                continue
            tile.piece = piece
            self.piece = None

            if not state.is_checked(piece.color):
                check_proof_tiles.append(tile)
            self.piece = piece
            tile.piece = temp_piece

        return check_proof_tiles

    def __repr__(self):
        return f"Tile({self.x},{self.y}):{self.piece}"
