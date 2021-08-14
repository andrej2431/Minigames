import tkinter as tk
from piece import Piece
from tile import Tile
from board_state import BoardState
from chess_move import ChessMove
from functools import partial


class Chess:
    def __init__(self):
        master = tk.Tk()
        self.size = 100
        master.geometry("803x900+1000+0")  # TODO  remove the special window positioning
        master.resizable(0, 0)
        self.master = master
        self.canvas = tk.Canvas(master, width=800, height=800)

        self.chessboard: list = [[Tile(x, y, self.canvas) for x in range(8)] for y in range(8)]
        self.tile_ids = {}

        self.create_board(white_color="white", black_color="saddle brown")
        piece_stack_height = self.canvas.create_rectangle(0, 0, 0, 0, fill="", width=0)
        self.place_pieces()

        self.state = BoardState(self.chessboard, piece_stack_height=piece_stack_height)

        self.canvas.bind("<B1-Motion>", self.mouse_moving_piece)
        self.canvas.bind("<ButtonRelease-1>", self.mouse_release_piece)
        self.master.bind("h", self.show_history)
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

    def place_pieces(self):
        piece_images = Piece.load_images()

        for x in range(8):
            self.chessboard[1][x].piece = Piece(self.canvas, (x, 1), "pawn", "black", piece_images)

        for x in range(8):
            self.chessboard[6][x].piece = Piece(self.canvas, (x, 6), "pawn", "white", piece_images)

        piece_names = ("rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook")

        for color, y in (("white", 7), ("black", 0)):
            for x, piece_name in enumerate(piece_names):
                self.chessboard[y][x].piece = Piece(self.canvas, (x, y), piece_name, color, piece_images)

        for y in range(8):
            for x in range(8):
                tile = self.chessboard[y][x]
                self.canvas.lift(tile.rect)
                self.canvas.tag_bind(tile.rect, "<Button-1>", partial(self.mouse_press_tile, tile))

                self.tile_ids[tile.rect] = tile

    def mouse_press_tile(self, tile, event):
        if not tile.piece:  # no piece inn pressed tile
            return
        piece = tile.piece
        if self.state.turn != piece.color:  # check if the move is made by the right player
            return

        self.state.selected = tile
        self.canvas.lift(tile.piece.img)

    def mouse_moving_piece(self, event):
        selected = self.state.selected

        if not selected:
            return
        selected.piece.move_to(event.x, event.y)

    def mouse_release_piece(self, event):
        selected = self.state.selected

        if not selected:
            return

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

    def show_history(self,event):
        print("History: ")
        for move in self.state.history:
            print(move)
        print()


def main():
    board = Chess()


if __name__ == "__main__":
    main()
