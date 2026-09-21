from tkinter import font as tkfont


class FontSet:
    CANDIDATES = (
        "Segoe UI",
        "SF Pro Text",
        "Helvetica Neue",
        "Ubuntu",
        "Noto Sans",
        "DejaVu Sans",
        "Helvetica",
    )

    def __init__(self):
        family = self._pick_family()
        self.title = tkfont.Font(family=family, size=24, weight="bold")
        self.body = tkfont.Font(family=family, size=12)
        self.done = tkfont.Font(family=family, size=12, overstrike=True)
        self.small = tkfont.Font(family=family, size=10)
        self.small_bold = tkfont.Font(family=family, size=10, weight="bold")
        self.icon = tkfont.Font(family=family, size=12, weight="bold")
        self.button = tkfont.Font(family=family, size=11, weight="bold")
        self.empty_icon = tkfont.Font(family=family, size=34)
        self.empty_title = tkfont.Font(family=family, size=15, weight="bold")

    @staticmethod
    def _pick_family():
        installed = tkfont.families()
        for name in FontSet.CANDIDATES:
            if name in installed:
                return name
        return tkfont.nametofont("TkDefaultFont").actual("family")
