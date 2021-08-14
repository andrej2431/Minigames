from piece_movesets import move_in_piece_moveset


class ChessMove:
    def __init__(self, start_tile, end_tile):
        self.piece = start_tile.piece
        self.end_piece = end_tile.piece
        self.start_tile = start_tile
        self.end_tile = end_tile
        self.coords = (end_tile.x - start_tile.x, end_tile.y - start_tile.y)

    def is_valid(self, state):
        if not move_in_piece_moveset(self.piece, self.coords[0], self.coords[1]):
            return False

        if self.end_piece and self.end_piece.color == self.piece.color:
            return False
        # TODO finish valid moves
        return True

    def attempt_move(self, state, canvas):
        if self.is_valid(state):
            self.execute(state)
        else:
            self.start_tile.recall_piece()
        canvas.tag_lower(self.piece.img, state.piece_stack_height)

    def execute(self, state):
        if self.end_piece:
            state.pieces[self.end_piece.color][self.end_piece.piece] -= 1
        self.end_tile.erase_piece()
        self.start_tile.move_piece_to(self.end_tile)
        state.history.append(self)
        state.next_turn()
        if state.is_checked(state.turn):
            if state.is_checkmated(state.turn):
                print("Game Over")
            else:
                print(f"{state.turn} king in check!!")

    def __repr__(self):
        start = (self.start_tile.x, self.start_tile.y)
        end = (self.end_tile.x, self.end_tile.y)
        captured = ""
        if self.end_piece:
            captured = self.end_piece.piece
        return f"{self.piece.color} {self.piece.piece} from {start} to {captured} {end}."
