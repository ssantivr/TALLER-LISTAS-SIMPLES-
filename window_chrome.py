import sys
import tkinter as tk

from theme import Theme


def apply_dark_title_bar(root):
    if sys.platform != "win32":
        return
    try:
        import ctypes

        root.update_idletasks()
        hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
        enabled = ctypes.c_int(1)
        for attribute in (20, 19):
            result = ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd, attribute, ctypes.byref(enabled), ctypes.sizeof(enabled)
            )
            if result == 0:
                break
    except Exception:
        pass


def build_app_icon(size=32):
    image = tk.PhotoImage(width=size, height=size)
    background = Theme.BACKGROUND
    accent = Theme.ACCENT
    check = Theme.ON_ACCENT
    radius = size * 0.28
    margin = size * 0.08
    cx0, cy0 = margin, margin
    cx1, cy1 = size - margin, size - margin

    def inside_rounded_square(x, y):
        nx = min(max(x, cx0), cx1)
        ny = min(max(y, cy0), cy1)
        corner_x = cx0 + radius if x < cx0 + radius else (cx1 - radius if x > cx1 - radius else None)
        corner_y = cy0 + radius if y < cy0 + radius else (cy1 - radius if y > cy1 - radius else None)
        if corner_x is not None and corner_y is not None:
            return (x - corner_x) ** 2 + (y - corner_y) ** 2 <= radius ** 2
        return cx0 <= x <= cx1 and cy0 <= y <= cy1

    def near_check_stroke(x, y):
        segments = (
            ((size * 0.27, size * 0.52), (size * 0.44, size * 0.70)),
            ((size * 0.44, size * 0.70), (size * 0.76, size * 0.32)),
        )
        thickness = size * 0.09
        for (x1, y1), (x2, y2) in segments:
            dx, dy = x2 - x1, y2 - y1
            length_sq = dx * dx + dy * dy
            t = 0.0 if length_sq == 0 else max(0.0, min(1.0, ((x - x1) * dx + (y - y1) * dy) / length_sq))
            px, py = x1 + t * dx, y1 + t * dy
            if (x - px) ** 2 + (y - py) ** 2 <= (thickness / 2) ** 2:
                return True
        return False

    rows = []
    for y in range(size):
        row = []
        for x in range(size):
            if inside_rounded_square(x + 0.5, y + 0.5):
                row.append(check if near_check_stroke(x + 0.5, y + 0.5) else accent)
            else:
                row.append(background)
        rows.append("{" + " ".join(row) + "}")
    image.put(" ".join(rows))
    return image
