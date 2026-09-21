import tkinter as tk

from shapes import ShapeFactory
from theme import Theme


class ProgressBar(tk.Canvas):
    def __init__(self, parent, height=8):
        super().__init__(
            parent,
            height=height,
            bg=Theme.BACKGROUND,
            highlightthickness=0,
            bd=0,
        )
        self.bar_height = height
        self.current = 0.0
        self.target = 0.0
        self.job = None
        self.bind("<Configure>", self._on_configure)

    def set_value(self, fraction):
        self.target = max(0.0, min(1.0, fraction))
        if self.job is None:
            self._animate()

    def _on_configure(self, event):
        self._draw()

    def _animate(self):
        difference = self.target - self.current
        if abs(difference) < 0.004:
            self.current = self.target
            self.job = None
            self._draw()
            return
        self.current += difference * 0.22
        self._draw()
        self.job = self.after(16, self._animate)

    def _draw(self):
        self.delete("all")
        width = self.winfo_width()
        if width <= 1:
            return
        radius = self.bar_height / 2
        self.create_polygon(
            *ShapeFactory.rounded_points(0, 0, width, self.bar_height, radius),
            smooth=True,
            fill=Theme.TRACK,
            outline="",
        )
        if self.current > 0:
            fill_width = max(width * self.current, self.bar_height)
            color = Theme.SUCCESS if self.target >= 1.0 else Theme.ACCENT
            self.create_polygon(
                *ShapeFactory.rounded_points(0, 0, fill_width, self.bar_height, radius),
                smooth=True,
                fill=color,
                outline="",
            )
