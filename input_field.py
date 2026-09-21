import tkinter as tk

from theme import Theme


class InputField(tk.Frame):
    def __init__(self, parent, fonts, placeholder, on_submit):
        super().__init__(parent, bg=Theme.BORDER, padx=1, pady=1)
        self.placeholder = placeholder
        self.on_submit = on_submit
        self.has_focus = False
        self.showing_placeholder = False
        self.entry = tk.Entry(
            self,
            font=fonts.body,
            bg=Theme.SURFACE,
            fg=Theme.TEXT,
            insertbackground=Theme.TEXT,
            relief="flat",
            highlightthickness=0,
            bd=0,
        )
        self.entry.pack(fill="x", ipady=10, ipadx=10)
        self.entry.bind("<FocusIn>", self._on_focus_in)
        self.entry.bind("<FocusOut>", self._on_focus_out)
        self.entry.bind("<Return>", self._on_return)
        self._show_placeholder()

    def get_value(self):
        if self.showing_placeholder:
            return ""
        return self.entry.get().strip()

    def clear(self):
        self.entry.delete(0, "end")
        self.showing_placeholder = False
        self.entry.configure(fg=Theme.TEXT)
        if not self.has_focus:
            self._show_placeholder()

    def focus_input(self):
        self.entry.focus_set()

    def flash_error(self):
        self.configure(bg=Theme.DANGER)
        self.after(700, self._reset_border)

    def _reset_border(self):
        if self.winfo_exists():
            self.configure(bg=Theme.ACCENT if self.has_focus else Theme.BORDER)

    def _show_placeholder(self):
        self.entry.delete(0, "end")
        self.entry.insert(0, self.placeholder)
        self.entry.configure(fg=Theme.MUTED)
        self.showing_placeholder = True

    def _on_focus_in(self, event):
        self.has_focus = True
        self.configure(bg=Theme.ACCENT)
        if self.showing_placeholder:
            self.entry.delete(0, "end")
            self.entry.configure(fg=Theme.TEXT)
            self.showing_placeholder = False

    def _on_focus_out(self, event):
        self.has_focus = False
        self.configure(bg=Theme.BORDER)
        if self.entry.get() == "":
            self._show_placeholder()

    def _on_return(self, event):
        self.on_submit()
