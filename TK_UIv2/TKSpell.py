class TKSpell:
    def __init__(self, name, cast_time, color):
        self.name = name
        self.cast_time = cast_time
        self.color = color
        self.canvas_items = []


    def paint(self, canvas, pixel):
        item1_str = self.name
        item1_opts = { "text": item1_str, "fill": self.color, "font": ("ms serif", 14) }

        item1 = canvas.create_text(pixel[0], pixel[1], **item1_opts)
        self.canvas_items.append(item1)

        item2_str = self.cast_time
        item2_opts = { "text": item2_str, "fill": self.color, "font": ("ms serif", 14) }

        item2 = canvas.create_text(pixel[0], pixel[1] + 10, **item2_opts)
        self.canvas_items.append(item2)

    def clear(self, canvas):
        for item in self.canvas_items:
            canvas.delete(item)
        self.canvas_items = []
