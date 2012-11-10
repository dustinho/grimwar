

class TKUnit:
    def __init__(self, name):
        self.name = name
        self.canvas_items = []

    def paint(self, canvas, x_pixel, y_pixel):
        item1_str = self.name
        item1_opts = { "text": item1_str, "fill": "black", "font": ("ms serif", 14) }

        item1 = canvas.create_text(x_pixel, y_pixel, **item1_opts)
        self.canvas_items.append(item1)

    def clear(self, canvas):
        for item in self.canvas_items:
            canvas.delete(item)
        self.canvas_items = []
