import tkinter as tk
from functools import partial

from piece import Piece
from tile import Tile
from board_state import BoardState
from chess_move import ChessMove
from miscellaneous import *


class Chess:
    def __init__(self):
        master = tk.Tk()
        self.size = 100
        master.geometry("803x900+1000+0")
        master.resizable(0, 0)
        self.master = master
        self.canvas = tk.Canvas(master, width=800, height=800)

        self.chessboard: list = [[Tile(x, y, self.canvas) for x in range(8)]
                                 for y in range(8)]
        self.tile_ids = {}
        self.state = None

        self.create_board(white_color="white", black_color="saddle brown")
        self.create_menu()
        self.piece_images = Piece.load_images()
        self.canvas.bind("<B1-Motion>", self.mouse_moving_piece)
        self.canvas.bind("<ButtonRelease-1>", self.mouse_release_piece)
        self.master.bind("h", self.show_history)

        self.new_game()

        self.canvas.mainloop()

    def create_board(self, white_color="white", black_color="black"):
        size = self.size
        canvas = self.canvas
        tile_is_white = True

        for x in range(0, 8 * size, size):
            for y in range(0, 8 * size, size):
                if tile_is_white:
                    color = white_color
                else:
                    color = black_color
                canvas.create_rectangle(x, y, x + size, y + size, fill=color)

                tile_is_white = not tile_is_white
            tile_is_white = not tile_is_white
        canvas.pack()

    def create_menu(self):
        new_game_button = tk.Button(self.master, text="New Game", command=self.new_game)
        resign_button = tk.Button(self.master, text="Resign", command=self.resign)
        undo_button = tk.Button(self.master, text="Undo", command=self.undo)
        draw_button = tk.Button(self.master, text="Draw", command=self.draw)
        new_game_button.pack()
        resign_button.pack()
        undo_button.pack()
        draw_button.pack()

    def create_victory_screen(self):
        if self.state.victory_screen:
            return
        last_color = "white" if self.state.turn != "white" else "black"
        self.state.victory_screen = self.state.victory_screen = VictoryScreen(self.state.game_result, last_color,
                                                                              self.canvas)

    def undo(self):

        if not self.state or self.state.frozen:
            return

        if self.state.game_over or not self.state.history:
            return

        move = self.state.history[-1]
        piece, piece_sh = move.piece, move.piece_snapshot
        end_piece, end_piece_sh = move.end_piece, move.end_piece_snapshot
        start_tile, end_tile = move.start_tile, move.end_tile

        if piece.piece != piece_sh[1]:
            self.canvas.itemconfig(piece.img, image=piece.loaded_image)
        end_tile.move_piece_to(start_tile)
        if piece_sh[2] and not piece.unmoved:
            piece.unmoved = True

        if move.en_passant:
            end_piece, end_piece_sh = move.en_passant[1], (move.en_passant[1].color, "pawn", False)
            end_tile = move.en_passant[0]

        if end_piece:
            end_piece_image = self.state.piece_images[(end_piece.color, end_piece_sh[1])]
            end_piece.redraw(end_piece_image)
            end_tile.piece = end_piece

        if move.castle_rook:
            rook_tile, rook_end_tile = move.castle_rook
            rook_end_tile.move_piece_to(rook_tile)
            rook_tile.piece.unmoved = True

        self.state.turn = "white" if self.state.turn != "white" else "black"
        self.state.history.pop(-1)
        print(move)

    def draw(self):
        state = self.state
        if not state:
            return
        state.game_result = 5
        state.game_over = True
        if state.toplevel:
            state.toplevel.destroy()
        self.create_victory_screen()

    def resign(self):
        state = self.state
        if not state:
            return

        state.game_result = 6
        state.game_over = True
        if state.toplevel:
            state.toplevel.destroy()
        self.create_victory_screen()

    def place_pieces(self, stack_height):
        piece_images = self.piece_images

        pieces = {"white": [], "black": []}

        for x in range(8):
            self.chessboard[1][x].piece = Piece(self.canvas, (x, 1), "pawn", "black", piece_images, stack_height)
            pieces["black"].append(self.chessboard[1][x].piece)

        for x in range(8):
            self.chessboard[6][x].piece = Piece(self.canvas, (x, 6), "pawn", "white", piece_images, stack_height)
            pieces["white"].append(self.chessboard[6][x].piece)

        piece_names = ("rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook")

        for color, y in (("white", 7), ("black", 0)):
            for x, piece_name in enumerate(piece_names):
                self.chessboard[y][x].piece = Piece(self.canvas, (x, y), piece_name, color, piece_images, stack_height)
                pieces[color].append(self.chessboard[y][x].piece)

        for y in range(8):
            for x in range(8):
                tile = self.chessboard[y][x]
                self.canvas.lift(tile.rect)
                self.canvas.tag_bind(tile.rect, "<Button-1>", partial(self.mouse_press_tile, tile))

                self.tile_ids[tile.rect] = tile

        return pieces

    def new_game(self):
        if self.state:
            self.canvas.delete(self.state.piece_stack_height)
            if self.state.victory_screen:
                self.state.victory_screen.erase()
            if self.state.toplevel:
                self.state.toplevel.destroy()
        for x in range(8):
            for y in range(8):
                self.chessboard[y][x].erase_piece()

        piece_stack_height = self.canvas.create_rectangle(0, 0, 0, 0, fill="", width=0)
        chess_pieces = self.place_pieces(piece_stack_height)
        self.state = BoardState(self.chessboard, chess_pieces, self.piece_images,
                                piece_stack_height=piece_stack_height)

    def mouse_press_tile(self, tile, event):

        if self.state.frozen or self.state.game_over:
            return

        if not tile.piece:  # no piece inn pressed tile
            return
        piece = tile.piece
        if self.state.turn != piece.color:  # check if the move is made by the right player
            return

        self.state.selected = tile
        self.canvas.lift(tile.piece.img)
        self.show_available_moves()

    def mouse_moving_piece(self, event):
        if self.state.frozen or self.state.game_over:
            return
        selected = self.state.selected

        if not selected:
            return
        selected.piece.move_to(event.x, event.y)

    def mouse_release_piece(self, event):

        if self.state.frozen:
            return

        self.hide_available_moves()

        selected = self.state.selected

        if not selected:
            return

        selected.piece.lower("A")
        objects = self.canvas.find_overlapping(event.x, event.y, event.x, event.y)
        tile = None
        for object_id in objects:
            if "tile" in self.canvas.gettags(object_id):
                tile = self.tile_ids[object_id]
                break

        if tile:
            chess_move = ChessMove(selected, tile)
            chess_move.attempt_move(self.state, self.canvas)
        else:
            selected.recall_piece()
            self.canvas.tag_lower(selected.piece.img, self.state.piece_stack_height)
        self.state.selected = None

        if self.state.game_over:
            self.create_victory_screen()

    def show_history(self, event):
        print("History: ")
        for move in self.state.history:
            print(move)
        print()

    def show_available_moves(self):
        tile = self.state.selected

        for available_tile in tile.available_tiles_from_piece(self.state):
            available_tile.show_circle()
            self.state.available_tiles.append(available_tile)

    def hide_available_moves(self):
        for tile in self.state.available_tiles:
            tile.hide_circle()
        self.state.available_tiles = []


def main():
    board = Chess()


if __name__ == "__main__":
    main()
