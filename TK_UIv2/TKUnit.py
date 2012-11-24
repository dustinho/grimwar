

class TKUnit:
    def __init__(self, name, ammo, life, direction, color):
        self.name = name
        self.ammo = str(ammo)
        self.life = str(life)
        self.direction = str(direction)
        self.color = color
        self.canvas_items = []

    def paint(self, canvas, x_pixel, y_pixel):
        item1_str = self.name
        item1_opts = { "text": item1_str, "fill": self.color, "font": ("ms serif", 14) }

        item1 = canvas.create_text(x_pixel, y_pixel - 9, **item1_opts)
        self.canvas_items.append(item1)

        item2_str = self.ammo
        item2_opts = { "text": item2_str, "fill": self.color, "font": ("ms serif", 10) }
        
        item2 = canvas.create_text(x_pixel - 11, y_pixel + 10, **item2_opts)
        self.canvas_items.append(item2)

        item3_str = self.life
        item3_opts = { "text": item3_str, "fill": self.color, "font": ("ms serif", 10) }
        
        item3 = canvas.create_text(x_pixel + 12, y_pixel + 10, **item3_opts)
        self.canvas_items.append(item3)

        item4_str = self.direction
        item4_opts = { "text": item4_str, "fill": self.color, "font": ("ms serif", 8) }
        
        item4 = canvas.create_text(x_pixel, y_pixel + 20, **item4_opts)
        self.canvas_items.append(item4)
        

    def clear(self, canvas):
        for item in self.canvas_items:
            canvas.delete(item)
        self.canvas_items = []
