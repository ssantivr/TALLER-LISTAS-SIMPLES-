import tkinter as tk

from check_circle import CheckCircle
from theme import Theme


class TaskRowView(tk.Frame):
    def __init__(self, parent, node, fonts, on_toggle, on_delete, on_edit):
        super().__init__(parent, bg=Theme.CARD)
        self.node = node
        self.fonts = fonts
        self.on_toggle = on_toggle
        self.on_delete = on_delete
        self.on_edit = on_edit
        self.editing = False
        self.edit_entry = None
        self._build()
        self._bind_hover()
        self.bind("<Configure>", self._on_resize, add="+")

    def _build(self):
        task_id = self.node.task_id
        completed = self.node.completed
        stripe_color = Theme.SUCCESS if completed else Theme.ACCENT
        text_color = Theme.MUTED if completed else Theme.TEXT
        text_font = self.fonts.done if completed else self.fonts.body

        self.stripe = tk.Frame(self, width=4, bg=stripe_color)
        self.stripe.pack(side="left", fill="y")

        self.check = CheckCircle(
            self,
            completed,
            Theme.CARD,
            lambda: self.on_toggle(task_id),
        )
        self.check.pack(side="left", padx=(12, 4), pady=12)

        self.delete_label = tk.Label(
            self,
            text="\u2715",
            font=self.fonts.icon,
            bg=Theme.CARD,
            fg=Theme.MUTED,
            cursor="hand2",
            padx=8,
        )
        self.delete_label.pack(side="right", padx=(0, 10))
        self.delete_label.bind("<Button-1>", lambda event: self.on_delete(task_id))
        self.delete_label.bind(
            "<Enter>", lambda event: self.delete_label.configure(fg=Theme.DANGER), add="+"
        )
        self.delete_label.bind(
            "<Leave>", lambda event: self.delete_label.configure(fg=Theme.MUTED), add="+"
        )

        self.title_label = tk.Label(
            self,
            text=self.node.title,
            font=text_font,
            bg=Theme.CARD,
            fg=text_color,
            anchor="w",
            justify="left",
            wraplength=300,
        )
        self.title_label.pack(side="left", fill="x", expand=True, padx=8, pady=12)
        self.title_label.bind("<Double-Button-1>", self._start_edit)

    def _bind_hover(self):
        self.bind("<Enter>", self._on_enter, add="+")
        self.bind("<Leave>", self._on_leave, add="+")
        self.stripe.bind("<Enter>", self._on_enter, add="+")
        self.stripe.bind("<Leave>", self._on_leave, add="+")
        self.check.bind("<Enter>", self._on_enter, add="+")
        self.check.bind("<Leave>", self._on_leave, add="+")
        self.title_label.bind("<Enter>", self._on_enter, add="+")
        self.title_label.bind("<Leave>", self._on_leave, add="+")
        self.delete_label.bind("<Enter>", self._on_enter, add="+")
        self.delete_label.bind("<Leave>", self._on_leave, add="+")

    def _pointer_inside(self):
        try:
            widget = self.winfo_containing(*self.winfo_pointerxy())
        except KeyError:
            return False
        while widget is not None:
            if widget is self:
                return True
            widget = widget.master
        return False

    def _apply_background(self, color):
        self.configure(bg=color)
        self.check.set_background(color)
        self.title_label.configure(bg=color)
        self.delete_label.configure(bg=color)

    def _on_enter(self, event):
        self._apply_background(Theme.CARD_HOVER)

    def _on_leave(self, event):
        if not self._pointer_inside():
            self._apply_background(Theme.CARD)

    def _on_resize(self, event):
        if event.widget is self:
            self.title_label.configure(wraplength=max(event.width - 130, 120))

    def _start_edit(self, event=None):
        if self.editing:
            return
        self.editing = True
        self.title_label.pack_forget()
        self.edit_entry = tk.Entry(
            self,
            font=self.fonts.body,
            bg=Theme.SURFACE,
            fg=Theme.TEXT,
            insertbackground=Theme.TEXT,
            relief="flat",
            highlightthickness=1,
            highlightbackground=Theme.BORDER,
            highlightcolor=Theme.ACCENT,
        )
        self.edit_entry.insert(0, self.node.title)
        self.edit_entry.pack(side="left", fill="x", expand=True, padx=8, pady=10, ipady=4)
        self.edit_entry.focus_set()
        self.edit_entry.select_range(0, "end")
        self.edit_entry.bind("<Return>", self._commit_edit)
        self.edit_entry.bind("<Escape>", self._cancel_edit)
        self.edit_entry.bind("<FocusOut>", self._commit_edit)

    def _restore_label(self):
        self.edit_entry.destroy()
        self.edit_entry = None
        self.title_label.pack(side="left", fill="x", expand=True, padx=8, pady=12)

    def _commit_edit(self, event=None):
        if not self.editing:
            return
        self.editing = False
        new_title = self.edit_entry.get().strip()
        if new_title and new_title != self.node.title:
            self.on_edit(self.node.task_id, new_title)
        else:
            self._restore_label()

    def _cancel_edit(self, event=None):
        if not self.editing:
            return "break"
        self.editing = False
        self._restore_label()
        return "break"
