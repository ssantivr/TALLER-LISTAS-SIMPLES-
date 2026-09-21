import tkinter as tk

from theme import Theme


class EmptyStateView(tk.Frame):
    def __init__(self, parent, fonts, icon, title, message):
        super().__init__(parent, bg=Theme.BACKGROUND)
        tk.Label(
            self,
            text=icon,
            font=fonts.empty_icon,
            bg=Theme.BACKGROUND,
            fg=Theme.BORDER,
        ).pack(pady=(50, 4))
        tk.Label(
            self,
            text=title,
            font=fonts.empty_title,
            bg=Theme.BACKGROUND,
            fg=Theme.TEXT,
        ).pack()
        tk.Label(
            self,
            text=message,
            font=fonts.small,
            bg=Theme.BACKGROUND,
            fg=Theme.MUTED,
        ).pack(pady=(4, 0))
