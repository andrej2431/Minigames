class VictoryScreen:
    def __init__(self, game_result, color, canvas):
        self.x = 405
        self.y = 415
        self.canvas = canvas
        self.color = color
        self.font = ("Nimbus Roman", 90, "normal")
        self.font_color = "gold"
        self.background_color = "RoyalBlue2"

        game_result_map = {0: "game_ongoing?", 1: f"Checkmate\n{color} wins!", 2: "Draw by\nstalemate",
                           3: "Draw by\nrepetition", 4: "Draw by\ninsufficient\nmaterial",
                           5:f"Draw by offer",6:f"{color} wins by\nresignation!"}
        self.game_result_text = game_result_map[game_result]
        self.background = canvas.create_rectangle(self.x - 400, self.y - 210, self.x + 390, self.y + 180,
                                                 fill=self.background_color)
        self.text = canvas.create_text(self.x, self.y, fill=self.font_color, font=self.font,
                                       text=self.game_result_text)

    def erase(self):
        self.canvas.delete(self.text)
        self.canvas.delete(self.background)
