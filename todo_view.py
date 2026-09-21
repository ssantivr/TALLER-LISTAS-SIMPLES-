import tkinter as tk

from empty_state_view import EmptyStateView
from filter_bar import FilterBar
from font_set import FontSet
from footer_view import FooterView
from header_view import HeaderView
from input_field import InputField
from rounded_button import RoundedButton
from scrollable_frame import ScrollableFrame
from task_filter import TaskFilter
from task_row_view import TaskRowView
from theme import Theme


class TodoView:
    def __init__(self, root, task_list, on_change=None):
        self.root = root
        self.task_list = task_list
        self.on_change = on_change or (lambda: None)
        self.filter_mode = TaskFilter.ALL
        self._configure_window()
        self.fonts = FontSet()
        self._build_header()
        self._build_input()
        self._build_filter_bar()
        self._build_footer()
        self._build_list_area()
        self.refresh()
        self.input_field.focus_input()

    def _configure_window(self):
        self.root.title("Modern To-Do List")
        self.root.minsize(500, 560)
        self.root.configure(bg=Theme.BACKGROUND)
        self.root.update_idletasks()
        width = 560
        height = min(780, self.root.winfo_screenheight() - 100)
        x = (self.root.winfo_screenwidth() - width) // 2
        y = max((self.root.winfo_screenheight() - height) // 2 - 20, 0)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def _build_header(self):
        self.header = HeaderView(self.root, self.fonts)
        self.header.pack(fill="x", padx=24, pady=(24, 16))

    def _build_input(self):
        wrapper = tk.Frame(self.root, bg=Theme.BACKGROUND)
        wrapper.pack(fill="x", padx=24, pady=(0, 12))
        self.add_button = RoundedButton(
            wrapper,
            "Add",
            self._on_add,
            self.fonts.button,
            84,
            42,
            Theme.ACCENT,
            Theme.ACCENT_HOVER,
            Theme.ON_ACCENT,
            Theme.BACKGROUND,
            radius=12,
        )
        self.add_button.pack(side="right", padx=(10, 0))
        self.input_field = InputField(
            wrapper,
            self.fonts,
            "What needs to be done?",
            self._on_add,
        )
        self.input_field.pack(side="left", fill="x", expand=True)

    def _build_filter_bar(self):
        self.filter_bar = FilterBar(self.root, self.fonts, self._on_filter_change)
        self.filter_bar.pack(fill="x", padx=24, pady=(0, 14))

    def _build_footer(self):
        self.footer = FooterView(self.root, self.fonts, self._on_clear_completed)
        self.footer.pack(fill="x", side="bottom")

    def _build_list_area(self):
        self.scroll_area = ScrollableFrame(self.root)
        self.scroll_area.pack(fill="both", expand=True, padx=(24, 18), pady=(0, 10))

    def _on_add(self):
        title = self.input_field.get_value()
        if not title:
            self.input_field.flash_error()
            return
        self.task_list.add_task(title)
        self.input_field.clear()
        if self.filter_mode == TaskFilter.COMPLETED:
            self.filter_bar.select(TaskFilter.ALL)
        else:
            self.refresh()
        self.scroll_area.scroll_to_bottom()
        self.on_change()

    def _on_toggle(self, task_id):
        self.task_list.toggle_task(task_id)
        self.refresh()
        self.on_change()

    def _on_delete(self, task_id):
        self.task_list.delete_task(task_id)
        self.refresh()
        self.on_change()

    def _on_edit(self, task_id, title):
        self.task_list.update_task(task_id, title)
        self.refresh()
        self.on_change()

    def _on_clear_completed(self):
        self.task_list.clear_completed()
        self.refresh()
        self.on_change()

    def _on_filter_change(self, mode):
        self.filter_mode = mode
        self.refresh()
        self.scroll_area.scroll_to_top()

    def _show_empty_state(self):
        if self.filter_mode == TaskFilter.PENDING:
            icon = "\u2713"
            title = "All caught up"
            message = "You have no pending tasks."
        elif self.filter_mode == TaskFilter.COMPLETED:
            icon = "\u25cb"
            title = "Nothing completed yet"
            message = "Finish a task and it will show up here."
        else:
            icon = "\u25cb"
            title = "No tasks yet"
            message = "Type above and press Enter to add your first task."
        EmptyStateView(self.scroll_area.body, self.fonts, icon, title, message).pack(fill="x")

    def refresh(self):
        position = self.scroll_area.get_position()
        self.scroll_area.clear()

        shown = 0
        for node in self.task_list.traverse():
            if TaskFilter.matches(node, self.filter_mode):
                row = TaskRowView(
                    self.scroll_area.body,
                    node,
                    self.fonts,
                    self._on_toggle,
                    self._on_delete,
                    self._on_edit,
                )
                row.pack(fill="x", pady=(0, 8))
                shown += 1
        if shown == 0:
            self._show_empty_state()

        total = self.task_list.size
        done = self.task_list.completed_count()
        pending = total - done
        self.header.update_stats(total, done)
        self.filter_bar.update_counts(total, pending, done)
        self.footer.update_stats(pending, done)
        self.scroll_area.set_position(position)
