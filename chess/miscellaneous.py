class VictoryScreen:
    def __init__(self, color, canvas):
        self.x = 405
        self.y = 415
        self.canvas = canvas
        self.color = color
        self.font = ("Nimbus Roman", 90, "normal")
        self.font_color = "aquamarine"
        if color:
            self.victory_text = f"{color.capitalize()} wins!"
        else:
            self.victory_text = "Draw"

        self.text = canvas.create_text(self.x, self.y,fill=self.font_color, font=self.font, text=self.victory_text)

    def erase(self):
        self.canvas.delete(self.text)
