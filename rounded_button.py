import tkinter as tk

from shapes import ShapeFactory
from theme import Theme


class RoundedButton(tk.Canvas):
    def __init__(
        self,
        parent,
        text,
        command,
        font,
        width,
        height,
        background,
        hover_background,
        foreground,
        canvas_background,
        radius=10,
    ):
        super().__init__(
            parent,
            width=width,
            height=height,
            bg=canvas_background,
            highlightthickness=0,
            bd=0,
            cursor="hand2",
        )
        self.command = command
        self.button_width = width
        self.button_height = height
        self.normal_background = background
        self.hover_background = hover_background
        self.normal_foreground = foreground
        self.enabled = True
        self.shape_id = self.create_polygon(
            *ShapeFactory.rounded_points(1, 1, width - 1, height - 1, radius),
            smooth=True,
            fill=background,
            outline="",
        )
        self.text_id = self.create_text(
            width / 2, height / 2, text=text, font=font, fill=foreground
        )
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<ButtonRelease-1>", self._on_release)

    def set_enabled(self, enabled):
        self.enabled = enabled
        if enabled:
            self.itemconfigure(self.shape_id, fill=self.normal_background)
            self.itemconfigure(self.text_id, fill=self.normal_foreground)
            self.configure(cursor="hand2")
        else:
            self.itemconfigure(self.shape_id, fill=Theme.DISABLED_BG)
            self.itemconfigure(self.text_id, fill=Theme.DISABLED_FG)
            self.configure(cursor="arrow")

    def _on_enter(self, event):
        if self.enabled:
            self.itemconfigure(self.shape_id, fill=self.hover_background)

    def _on_leave(self, event):
        if self.enabled:
            self.itemconfigure(self.shape_id, fill=self.normal_background)

    def _on_release(self, event):
        inside = 0 <= event.x <= self.button_width and 0 <= event.y <= self.button_height
        if self.enabled and inside:
            self.command()
