import tkinter as tk
from tkinter import ttk

from theme import Theme


class ScrollableFrame(tk.Frame):
    STYLE_NAME = "Dark.Vertical.TScrollbar"

    def __init__(self, parent):
        super().__init__(parent, bg=Theme.BACKGROUND)
        self._configure_scrollbar_style()
        self.canvas = tk.Canvas(
            self,
            bg=Theme.BACKGROUND,
            highlightthickness=0,
            bd=0,
            yscrollincrement=20,
        )
        self.scrollbar = ttk.Scrollbar(
            self,
            orient="vertical",
            style=self.STYLE_NAME,
            command=self.canvas.yview,
        )
        self.canvas.configure(yscrollcommand=self._on_scroll)
        self.scrollbar.pack(side="right", fill="y", padx=(6, 0))
        self.canvas.pack(side="left", fill="both", expand=True)

        self.body = tk.Frame(self.canvas, bg=Theme.BACKGROUND)
        self.window_id = self.canvas.create_window((0, 0), window=self.body, anchor="nw")

        self.body.bind("<Configure>", self._on_body_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.bind_all("<MouseWheel>", self._on_wheel, add="+")
        self.bind_all("<Button-4>", self._on_wheel, add="+")
        self.bind_all("<Button-5>", self._on_wheel, add="+")

    def _configure_scrollbar_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.layout(
            self.STYLE_NAME,
            [
                (
                    "Vertical.Scrollbar.trough",
                    {
                        "sticky": "ns",
                        "children": [
                            ("Vertical.Scrollbar.thumb", {"expand": "1", "sticky": "nswe"})
                        ],
                    },
                )
            ],
        )
        style.configure(
            self.STYLE_NAME,
            troughcolor=Theme.BACKGROUND,
            background=Theme.CARD_HOVER,
            bordercolor=Theme.BACKGROUND,
            lightcolor=Theme.CARD_HOVER,
            darkcolor=Theme.CARD_HOVER,
            arrowsize=10,
            gripcount=0,
        )
        style.map(
            self.STYLE_NAME,
            background=[
                ("disabled", Theme.BACKGROUND),
                ("pressed", Theme.MUTED),
                ("active", Theme.MUTED),
            ],
            lightcolor=[
                ("disabled", Theme.BACKGROUND),
                ("pressed", Theme.MUTED),
                ("active", Theme.MUTED),
            ],
            darkcolor=[
                ("disabled", Theme.BACKGROUND),
                ("pressed", Theme.MUTED),
                ("active", Theme.MUTED),
            ],
        )

    def clear(self):
        for child in self.body.winfo_children():
            child.destroy()

    def get_position(self):
        return self.canvas.yview()[0]

    def set_position(self, fraction):
        self.canvas.update_idletasks()
        self.canvas.yview_moveto(fraction)

    def scroll_to_top(self):
        self.set_position(0.0)

    def scroll_to_bottom(self):
        self.set_position(1.0)

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

    def _on_scroll(self, first, last):
        self.scrollbar.set(first, last)
        if float(first) <= 0.0 and float(last) >= 1.0:
            self.scrollbar.state(["disabled"])
        else:
            self.scrollbar.state(["!disabled"])

    def _on_body_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        self.canvas.itemconfigure(self.window_id, width=event.width)

    def _on_wheel(self, event):
        if not self._pointer_inside():
            return
        if self.body.winfo_reqheight() <= self.canvas.winfo_height():
            return
        if event.num == 4:
            step = -2
        elif event.num == 5:
            step = 2
        else:
            step = -2 if event.delta > 0 else 2
        self.canvas.yview_scroll(step, "units")
