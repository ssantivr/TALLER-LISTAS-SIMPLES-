import tkinter as tk
from datetime import datetime

from progress_bar import ProgressBar
from theme import Theme


class HeaderView(tk.Frame):
    def __init__(self, parent, fonts):
        super().__init__(parent, bg=Theme.BACKGROUND)
        top = tk.Frame(self, bg=Theme.BACKGROUND)
        top.pack(fill="x")
        tk.Label(
            top,
            text="My Tasks",
            font=fonts.title,
            bg=Theme.BACKGROUND,
            fg=Theme.TEXT,
        ).pack(side="left")
        tk.Label(
            top,
            text=self._today_text(),
            font=fonts.small,
            bg=Theme.BACKGROUND,
            fg=Theme.MUTED,
        ).pack(side="right", anchor="s", pady=(0, 6))

        self.subtitle_label = tk.Label(
            self,
            text="",
            font=fonts.small,
            bg=Theme.BACKGROUND,
            fg=Theme.MUTED,
            anchor="w",
        )
        self.subtitle_label.pack(fill="x")

        progress_row = tk.Frame(self, bg=Theme.BACKGROUND)
        progress_row.pack(fill="x", pady=(14, 0))
        self.percent_label = tk.Label(
            progress_row,
            text="0%",
            font=fonts.small_bold,
            bg=Theme.BACKGROUND,
            fg=Theme.MUTED,
            width=5,
            anchor="e",
        )
        self.percent_label.pack(side="right")
        self.progress_bar = ProgressBar(progress_row)
        self.progress_bar.pack(side="left", fill="x", expand=True)

    @staticmethod
    def _today_text():
        now = datetime.now()
        return f"{now.strftime('%A, %B')} {now.day}"

    def update_stats(self, total, done):
        pending = total - done
        if total == 0:
            self.subtitle_label.configure(text="Start by adding your first task")
        else:
            self.subtitle_label.configure(text=f"{pending} pending  \u00b7  {done} done")
        fraction = done / total if total > 0 else 0.0
        self.progress_bar.set_value(fraction)
        self.percent_label.configure(
            text=f"{int(fraction * 100)}%",
            fg=Theme.SUCCESS if total > 0 and done == total else Theme.MUTED,
        )
