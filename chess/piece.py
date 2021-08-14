import tkinter as tk


class Piece:

    @classmethod
    def load_images(cls):
        w_p = tk.PhotoImage(file='img/w_p.png')
        w_k = tk.PhotoImage(file='img/w_k.png')
        w_kt = tk.PhotoImage(file='img/w_kt.png')
        w_q = tk.PhotoImage(file='img/w_q.png')
        w_r = tk.PhotoImage(file='img/w_r.png')
        w_b = tk.PhotoImage(file='img/w_b.png')

        b_p = tk.PhotoImage(file='img/b_p.png')
        b_k = tk.PhotoImage(file='img/b_k.png')
        b_kt = tk.PhotoImage(file='img/b_kt.png')
        b_q = tk.PhotoImage(file='img/b_q.png')
        b_r = tk.PhotoImage(file='img/b_r.png')
        b_b = tk.PhotoImage(file='img/b_b.png')
        piece_images = {("white", "pawn"): w_p, ("black", "pawn"): b_p, ("white", "knight"): w_kt,
                        ("black", "knight"): b_kt,
                        ("white", "bishop"): w_b, ("black", "bishop"): b_b, ("white", "rook"): w_r,
                        ("black", "rook"): b_r,
                        ("white", "queen"): w_q, ("black", "queen"): b_q, ("white", "king"): w_k,
                        ("black", "king"): b_k}
        return piece_images

    def __init__(self, canvas, coords, piece, color, piece_images, size=100):
        self.coords = coords
        self.x, self.y = coords
        self.x = self.x * size + size // 2
        self.y = self.y * size + size // 2
        self.piece = piece
        self.color = color
        self.loaded_image = piece_images[(color, piece)]
        self.canvas = canvas
        self.img = canvas.create_image(self.x, self.y, image=self.loaded_image)

    def move_to(self, x, y):
        coords = self.canvas.coords(self.img)
        self.canvas.move(self.img, x - coords[0], y - coords[1])

    def erase(self):
        self.canvas.delete(self.img)


    def __repr__(self):
        return f"{self.color} {self.piece}"
