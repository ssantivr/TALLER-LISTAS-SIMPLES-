import tkinter as tk

from rounded_button import RoundedButton
from theme import Theme


class FooterView(tk.Frame):
    def __init__(self, parent, fonts, on_clear):
        super().__init__(parent, bg=Theme.SURFACE)
        inner = tk.Frame(self, bg=Theme.SURFACE)
        inner.pack(fill="x", padx=24, pady=12)
        self.info_label = tk.Label(
            inner,
            text="",
            font=fonts.small,
            bg=Theme.SURFACE,
            fg=Theme.MUTED,
            anchor="w",
        )
        self.info_label.pack(side="left")
        self.clear_button = RoundedButton(
            inner,
            "Clear completed",
            on_clear,
            fonts.small_bold,
            140,
            32,
            Theme.CARD,
            Theme.CARD_HOVER,
            Theme.DANGER,
            Theme.SURFACE,
            radius=8,
        )
        self.clear_button.pack(side="right")
        self.clear_button.set_enabled(False)

    def update_stats(self, pending, done):
        noun = "task" if pending == 1 else "tasks"
        self.info_label.configure(
            text=f"{pending} {noun} left  \u00b7  Double-click to edit"
        )
        self.clear_button.set_enabled(done > 0)
