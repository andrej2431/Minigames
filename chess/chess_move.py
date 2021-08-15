import tkinter as tk
from functools import partial

from tile import Tile


class ChessMove:
    def __init__(self, start_tile, end_tile):
        self.piece = start_tile.piece
        self.piece_snapshot = (self.piece.color, self.piece.piece, self.piece.unmoved)
        self.end_piece = end_tile.piece
        self.end_piece_snapshot = None if not self.end_piece else (
            self.end_piece.color, self.end_piece.piece, self.end_piece.unmoved)
        self.start_tile = start_tile
        self.end_tile = end_tile
        self.coords = (end_tile.x - start_tile.x, end_tile.y - start_tile.y)
        self.en_passant = None
        self.castle_rook = None

    def is_valid(self, state):
        if self.end_tile in self.start_tile.available_tiles_from_piece(state):
            return True
        else:
            return False

    def attempt_move(self, state, canvas):
        if self.is_valid(state):
            self.execute(state, canvas)
        else:
            self.start_tile.recall_piece()

        if state.move_number == 0 or state.game_over:
            return
        canvas.tag_lower(self.piece.img, state.piece_stack_height)

    def execute(self, state, canvas):
        if self.end_piece:
            for i, piece in enumerate(state.pieces[self.end_piece.color]):
                if piece is self.end_piece:
                    state.pieces[self.end_piece.color][i] = None
        self.end_tile.erase_piece()
        self.castle_if_castle(state)
        self.kill_if_en_passant(state)
        self.start_tile.move_piece_to(self.end_tile)
        state.history.append(self)
        state.move_number += 1

        self.promote_if_pawn_promotion(state, canvas)

        if state.move_number == 0 or state.game_over:
            return

        state.next_turn()
        state.turn_result()

    def promote_if_pawn_promotion(self, state, canvas):

        def is_pawn_promotion():
            if self.piece.piece == "pawn":
                if self.coords[1] > 0 and self.end_tile.y == 7:
                    return True
                elif self.coords[1] < 0 and self.end_tile.y == 0:
                    return True
            return False

        def pawn_promotion_window():
            toplevel = tk.Toplevel()
            state.toplevel = toplevel

            result_piece = tk.StringVar()
            result_piece.set("queen")

            def close_toplevel(picked_piece):
                result_piece.set(picked_piece)
                toplevel.destroy()

            for row, col, piece in zip((0, 0, 1, 1), (0, 1, 0, 1), ("rook", "knight", "bishop", "queen")):
                image = state.piece_images[(self.piece.color, piece)]
                button = tk.Button(toplevel, image=image, command=partial(close_toplevel, piece))
                button.grid(row=row, column=col)

            state.frozen = True
            canvas.wait_window(toplevel)
            state.frozen = False
            return result_piece.get()

        if is_pawn_promotion():
            piece_name = pawn_promotion_window()
            if state.move_number == 0 or state.game_over:
                return
            self.piece.piece = piece_name
            canvas.itemconfig(self.piece.img, image=state.piece_images[(self.piece.color, piece_name)])
            return True

    def kill_if_en_passant(self, state):
        def is_en_passant():
            if not state.history:
                return False
            last_move = state.history[-1]
            last_piece = last_move.piece_snapshot
            other_tile = state.chessboard[self.start_tile.y][self.end_tile.x]
            if last_move.end_tile is other_tile and last_piece[1] == "pawn" and abs(last_move.coords[1]) == 2:
                return True
            return False

        if is_en_passant():
            tile = state.chessboard[self.start_tile.y][self.end_tile.x]
            self.en_passant = (tile, tile.piece)
            tile.erase_piece()

    def castle_if_castle(self, state):
        if not Tile.is_castle(self.start_tile, self.coords, state):
            return

        if self.coords[0] == 2:
            rook_tile = state.chessboard[self.start_tile.y][self.start_tile.x + 3]
            rook_end_tile = state.chessboard[self.start_tile.y][self.start_tile.x + 1]
        else:
            rook_tile = state.chessboard[self.start_tile.y][self.start_tile.x - 4]
            rook_end_tile = state.chessboard[self.start_tile.y][self.start_tile.x - 1]

        self.castle_rook = (rook_tile, rook_end_tile)
        rook_tile.move_piece_to(rook_end_tile)

    def __repr__(self):
        start = (self.start_tile.x, self.start_tile.y)
        end = (self.end_tile.x, self.end_tile.y)
        captured = ""
        if self.end_piece:
            captured = self.end_piece.piece
        return f"{self.piece.color} {self.piece_snapshot[1]} from {start} to {captured} {end}."
