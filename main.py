import tkinter as tk

from singly_linked_list import SinglyLinkedList
from storage import TaskStorage
from todo_view import TodoView
from window_chrome import apply_dark_title_bar, build_app_icon


class Application:
    def __init__(self):
        self.root = tk.Tk()
        self.storage = TaskStorage()
        self.task_list = SinglyLinkedList()
        self.task_list.load_from_dicts(self.storage.load())
        self.view = TodoView(self.root, self.task_list, on_change=self._save)
        self._icon = build_app_icon()
        self.root.iconphoto(True, self._icon)
        apply_dark_title_bar(self.root)
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _save(self):
        self.storage.save(self.task_list.to_dicts())

    def _on_close(self):
        self._save()
        self.root.destroy()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    Application().run()
