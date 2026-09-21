import tkinter as tk

from theme import Theme


class CheckCircle(tk.Canvas):
    SIZE = 28

    def __init__(self, parent, completed, background, command):
        super().__init__(
            parent,
            width=self.SIZE,
            height=self.SIZE,
            bg=background,
            highlightthickness=0,
            bd=0,
            cursor="hand2",
        )
        self.completed = completed
        self.command = command
        self.hovered = False
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<ButtonRelease-1>", self._on_release)
        self._draw()

    def set_background(self, color):
        self.configure(bg=color)

    def _on_enter(self, event):
        self.hovered = True
        self._draw()

    def _on_leave(self, event):
        self.hovered = False
        self._draw()

    def _on_release(self, event):
        if 0 <= event.x <= self.SIZE and 0 <= event.y <= self.SIZE:
            self.command()

    def _draw_check(self, color):
        self.create_line(
            9, 14, 13, 18, 20, 10,
            fill=color,
            width=3,
            capstyle="round",
            joinstyle="round",
        )

    def _draw(self):
        self.delete("all")
        if self.completed:
            self.create_oval(3, 3, 25, 25, fill=Theme.SUCCESS, outline=Theme.SUCCESS)
            self._draw_check(Theme.BACKGROUND)
        else:
            color = Theme.ACCENT_HOVER if self.hovered else Theme.ACCENT
            self.create_oval(3, 3, 25, 25, outline=color, width=2)
            if self.hovered:
                self._draw_check(Theme.MUTED)
