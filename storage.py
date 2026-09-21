import json
from pathlib import Path


class TaskStorage:
    def __init__(self, path=None):
        self.path = path or Path(__file__).resolve().parent / "tasks_data.json"

    def load(self):
        try:
            with open(self.path, "r", encoding="utf-8") as handle:
                data = json.load(handle)
        except (FileNotFoundError, OSError, json.JSONDecodeError):
            return []
        tasks = data.get("tasks", [])
        return tasks if isinstance(tasks, list) else []

    def save(self, tasks):
        payload = {"tasks": tasks}
        tmp_path = self.path.with_suffix(".tmp")
        try:
            with open(tmp_path, "w", encoding="utf-8") as handle:
                json.dump(payload, handle, indent=2)
            tmp_path.replace(self.path)
        except OSError:
            pass
