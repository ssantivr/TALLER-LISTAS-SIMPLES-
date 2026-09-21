import tkinter as tk

from task_filter import TaskFilter
from theme import Theme


class FilterBar(tk.Frame):
    def __init__(self, parent, fonts, on_change):
        super().__init__(
            parent,
            bg=Theme.SURFACE,
            padx=4,
            pady=4,
            highlightthickness=1,
            highlightbackground=Theme.BORDER,
        )
        self.fonts = fonts
        self.on_change = on_change
        self.active = TaskFilter.ALL
        self.all_label = self._create_segment(TaskFilter.ALL, "All")
        self.pending_label = self._create_segment(TaskFilter.PENDING, "Pending")
        self.completed_label = self._create_segment(TaskFilter.COMPLETED, "Completed")
        self._restyle_all()

    def _create_segment(self, mode, text):
        label = tk.Label(
            self,
            text=text,
            font=self.fonts.small_bold,
            bg=Theme.SURFACE,
            fg=Theme.MUTED,
            cursor="hand2",
            padx=14,
            pady=7,
        )
        label.pack(side="left", fill="x", expand=True, padx=2)
        label.bind("<Button-1>", lambda event, m=mode: self.select(m))
        label.bind("<Enter>", lambda event, l=label, m=mode: self._hover(l, m, True))
        label.bind("<Leave>", lambda event, l=label, m=mode: self._hover(l, m, False))
        return label

    def _style(self, label, mode):
        if mode == self.active:
            label.configure(bg=Theme.ACCENT, fg=Theme.ON_ACCENT)
        else:
            label.configure(bg=Theme.SURFACE, fg=Theme.MUTED)

    def _restyle_all(self):
        self._style(self.all_label, TaskFilter.ALL)
        self._style(self.pending_label, TaskFilter.PENDING)
        self._style(self.completed_label, TaskFilter.COMPLETED)

    def _hover(self, label, mode, inside):
        if mode == self.active:
            return
        if inside:
            label.configure(bg=Theme.CARD_HOVER, fg=Theme.TEXT)
        else:
            label.configure(bg=Theme.SURFACE, fg=Theme.MUTED)

    def select(self, mode):
        if mode == self.active:
            return
        self.active = mode
        self._restyle_all()
        self.on_change(mode)

    def update_counts(self, total, pending, done):
        self.all_label.configure(text=f"All  {total}")
        self.pending_label.configure(text=f"Pending  {pending}")
        self.completed_label.configure(text=f"Completed  {done}")
