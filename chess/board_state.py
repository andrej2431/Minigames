class BoardState:
    def __init__(self, chessboard, pieces, piece_images, turn="white", history=None, selected=None,
                 piece_stack_height=0):

        self.chessboard = chessboard
        self.pieces = pieces
        self.piece_images = piece_images
        self.tile_list = [tile for row in self.chessboard for tile in row]
        self.ongoing = True
        self.turn = turn
        self.move_number = 0

        self.check = False
        self.game_result = 0
        self.game_over = False
        self.frozen = False
        self.victory_screen = None
        self.toplevel = None
        self.selected = selected
        self.history = history if history else []
        self.repetition_history = []
        self.piece_stack_height = piece_stack_height

    def next_turn(self):
        snapshot = self.snapshot_board()
        self.repetition_history.append(snapshot)
        if self.turn == "white":
            self.turn = "black"
        else:
            self.turn = "white"

    def turn_result(self):
        def insufficient_material():

            count = 0
            white_knights = 0
            for piece in self.pieces['white']:
                if piece:
                    if piece.piece in ("pawn", "rook", "queen"):
                        return False
                    if piece.piece == "knight":
                        white_knights += 1
                    count += 1
            if count > 3 or (count == 3 and white_knights < 2):
                return False

            count2 = 0
            black_knights = 0
            for piece in self.pieces['black']:
                if piece:
                    if piece.piece in ("pawn", "queen", "rook"):
                        return False
                    if piece.piece == "knight":
                        black_knights += 1
                    count2 += 1
            if count2 > 3 or (count2 == 3 and black_knights < 2):
                return False

            if (black_knights == 2 and count > 1) or (white_knights == 2 and count2 > 1):
                return False

            return True

        if self.is_checked(self.turn):
            self.check = True
        else:
            self.check = False

        if self.is_stalemate(self.turn):  # if nothing can move
            self.game_over = True
            if self.check:  # if king is also checked
                self.game_result = 1  # checkmate
            else:
                self.game_result = 2  # stalemate
        elif self.repetition_history.count(self.repetition_history[-1]) >= 3:  # if repetition of 3 positions
            self.game_over = True
            self.game_result = 3
        elif insufficient_material():
            self.game_over = True
            self.game_result = 4

    def is_checked(self, color):
        king_tile = self.find_king_tile(color)
        if king_tile.is_checked(color, self):
            return True
        else:
            return False

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

    def check_around_king(self, color):
        king_tile = self.find_king_tile(color)

        if king_tile.king_tiles(self, color):
            return False
        else:
            return True

    def find_king_tile(self, color):
        king_tile = None
        for y in range(8):
            for x in range(8):
                piece = self.chessboard[y][x].piece
                if piece and piece.color == color and piece.piece == "king":
                    king_tile = self.chessboard[y][x]
        return king_tile

    def snapshot_board(self):
        board_snapshot = ""
        for row in self.chessboard:
            for tile in row:
                if tile.piece:
                    short = {"pawn": "p", "rook": "r", "bishop": "b", "knight": "k", "queen": "q", "king": "K"}
                    board_snapshot += tile.piece.color[0] + short[tile.piece.piece]

                else:
                    board_snapshot += "NN"
        return board_snapshot
