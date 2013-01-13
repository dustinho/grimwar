from Tkinter import E, W

class TKUnit:
    def __init__(self, name, attack, will, hp, direction, color):
        self.name = name
        self.attack = str(attack)
        self.will = str(will)
        self.hp = str(hp)
        self.direction = str(direction)
        self.color = color
        self.canvas_items = []

    def paint(self, canvas, pixel):
        x = pixel[0]
        y = pixel[1]

        name_str = self.name
        name_opts = { "text": name_str, "fill": self.color, "font": ("ms serif", 14) }

        name = canvas.create_text(x, y - 9, **name_opts)
        self.canvas_items.append(name)

        attack_str = self.attack
        attack_opts = { "anchor":E, "text": attack_str, 
                "fill": self.color, "font": ("ms serif", 10) }
        attack = canvas.create_text(x - 15, y + 10, **attack_opts)
        self.canvas_items.append(attack)

        will_str = self.will
        will_opts = { "text": will_str, "fill": self.color, "font": ("ms serif", 10) }
        
        will = canvas.create_text(x, y + 10, **will_opts)
        self.canvas_items.append(will)

        hp_str = self.hp
        hp_opts = { "anchor":W, "text": hp_str, 
                "fill": self.color, "font": ("ms serif", 10) }
        
        hp = canvas.create_text(x + 15, y + 10, **hp_opts)
        self.canvas_items.append(hp)

        direction_str = self.direction
        direction_opts = { "text": direction_str, "fill": self.color, "font": ("ms serif", 8) }
        
        direction = canvas.create_text(x, y + 20, **direction_opts)
        self.canvas_items.append(direction)
        

    def clear(self, canvas):
        for item in self.canvas_items:
            canvas.delete(item)
        self.canvas_items = []
