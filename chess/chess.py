import tkinter as tk
from tkinter import font
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

        self.chessboard: list = [[Tile(x, y, self.canvas) for x in range(8)] for y in range(8)]
        self.tile_ids = {}

        self.create_board(white_color="white", black_color="saddle brown")
        self.piece_images = Piece.load_images()
        self.canvas.bind("<B1-Motion>", self.mouse_moving_piece)
        self.canvas.bind("<ButtonRelease-1>", self.mouse_release_piece)
        self.master.bind("h", self.show_history)

        self.NewGame_Button = tk.Button(self.master, text="New Game", command=self.new_game)
        self.NewGame_Button.pack()
        self.state = None
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

    def place_pieces(self):
        piece_images = self.piece_images

        pieces = {"white": [], "black": []}

        for x in range(8):
            self.chessboard[1][x].piece = Piece(self.canvas, (x, 1), "pawn", "black", piece_images)
            pieces["black"].append(self.chessboard[1][x].piece)

        for x in range(8):
            self.chessboard[6][x].piece = Piece(self.canvas, (x, 6), "pawn", "white", piece_images)
            pieces["white"].append(self.chessboard[6][x].piece)

        piece_names = ("rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook")

        for color, y in (("white", 7), ("black", 0)):
            for x, piece_name in enumerate(piece_names):
                self.chessboard[y][x].piece = Piece(self.canvas, (x, y), piece_name, color, piece_images)
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
        chess_pieces = self.place_pieces()
        self.state = BoardState(self.chessboard, chess_pieces,self.piece_images, piece_stack_height=piece_stack_height)

    def mouse_press_tile(self, tile, event):
        if self.state.frozen:
            return

        if self.state.checkmate:
            return

        if not tile.piece:  # no piece inn pressed tile
            return
        piece = tile.piece
        if self.state.turn != piece.color:  # check if the move is made by the right player
            return

        self.state.selected = tile
        self.canvas.lift(tile.piece.img)

    def mouse_moving_piece(self, event):
        if self.state.frozen:
            return
        selected = self.state.selected

        if not selected:
            return
        selected.piece.move_to(event.x, event.y)

    def mouse_release_piece(self, event):
        if self.state.frozen:
            return

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

        if self.state.game_over:
            victory_color = None
            if self.state.checkmate:
                victory_color = "white" if self.state.turn == "black" else "black"
            self.state.victory_screen = VictoryScreen(victory_color, self.canvas)

    def show_history(self, event):
        print("History: ")
        for move in self.state.history:
            print(move)
        print()


def main():
    board = Chess()


if __name__ == "__main__":
    main()
