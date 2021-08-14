class ChessMove:
    def __init__(self, start_tile, end_tile):
        self.piece = start_tile.piece
        self.end_piece = end_tile.piece
        self.start_tile = start_tile
        self.end_tile = end_tile
        self.coords = (end_tile.x - start_tile.x, end_tile.y - start_tile.y)

    def is_valid(self, state):
        if self.end_tile in self.start_tile.available_tiles_from_piece(state):
            return True
        else:
            return False

    def attempt_move(self, state, canvas):
        if self.is_valid(state) or self.is_castle(state):
            self.execute(state)
        else:
            self.start_tile.recall_piece()
        canvas.tag_lower(self.piece.img, state.piece_stack_height)

    def is_castle(self, state):
        piece = self.piece
        start_tile = self.start_tile
        if piece.piece == "king" and piece.unmoved and not start_tile.is_checked(piece.color, state):
            if self.coords == (2, 0):
                rook_x = start_tile.x + 3
            elif self.coords == (-2, 0):
                rook_x = start_tile.x - 4
            else:
                return False
            rook_tile = state.chessboard[start_tile.y][rook_x]

            if rook_tile.piece and rook_tile.piece.piece == "rook" and rook_tile.piece.unmoved:
                sign = (rook_tile.x - start_tile.x) // abs((rook_tile.x - start_tile.x))
                print(start_tile.x, rook_tile.x, sign)
                for x in range(start_tile.x + sign, rook_tile.x, sign):
                    print(x)
                    tile = state.chessboard[start_tile.y][x]
                    print(tile)
                    if tile.piece or tile.is_checked(piece.color, state):
                        return False
                return True
        return False

    def castle_if_castle(self, state):
        if not self.is_castle(state):
            return

        if self.coords[0] == 2:
            rook_tile = state.chessboard[self.start_tile.y][self.start_tile.x + 3]
            rook_end_tile = state.chessboard[self.start_tile.y][self.start_tile.x + 1]
        else:
            rook_tile = state.chessboard[self.start_tile.y][self.start_tile.x - 4]
            rook_end_tile = state.chessboard[self.start_tile.y][self.start_tile.x - 1]

        rook_tile.move_piece_to(rook_end_tile)

    def execute(self, state):
        if self.end_piece:
            for i, piece in enumerate(state.pieces[self.end_piece.color]):
                if piece is self.end_piece:
                    state.pieces[self.end_piece.color][i] = None
        self.end_tile.erase_piece()
        self.castle_if_castle(state)
        self.start_tile.move_piece_to(self.end_tile)
        state.history.append(self)

        state.next_turn()
        if state.is_stalemate(state.turn):
            state.game_over = True

        if state.is_checked(state.turn):
            state.check = True
            if state.is_stalemate(state.turn):
                state.checkmate = True
                state.game_over = True
        elif state.is_stalemate(state.turn):
            state.stalemate = True
            state.game_over = True

        else:
            state.check = False

    def __repr__(self):
        start = (self.start_tile.x, self.start_tile.y)
        end = (self.end_tile.x, self.end_tile.y)
        captured = ""
        if self.end_piece:
            captured = self.end_piece.piece
        return f"{self.piece.color} {self.piece.piece} from {start} to {captured} {end}."
