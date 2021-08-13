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
        print(f"moving from {self.x},{self.y} to {end_tile.x}, {end_tile.y}")
        end_tile.recall_piece()

    def __repr__(self):
        return f"Tile({self.x},{self.y}):{self.piece}"
