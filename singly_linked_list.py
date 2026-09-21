from task_node import TaskNode


class SinglyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0
        self._next_id = 1

    @property
    def size(self):
        return self._size

    def is_empty(self):
        return self.head is None

    def add_task(self, title):
        node = TaskNode(self._next_id, title)
        self._next_id += 1
        if self.head is None:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self._size += 1
        return node

    def delete_task(self, task_id):
        previous = None
        current = self.head
        while current is not None:
            if current.task_id == task_id:
                if previous is None:
                    self.head = current.next
                else:
                    previous.next = current.next
                if current is self.tail:
                    self.tail = previous
                current.next = None
                self._size -= 1
                return True
            previous = current
            current = current.next
        return False

    def toggle_task(self, task_id):
        current = self.head
        while current is not None:
            if current.task_id == task_id:
                current.completed = not current.completed
                return True
            current = current.next
        return False

    def update_task(self, task_id, title):
        current = self.head
        while current is not None:
            if current.task_id == task_id:
                current.title = title
                return True
            current = current.next
        return False

    def clear_completed(self):
        removed = 0
        previous = None
        current = self.head
        while current is not None:
            following = current.next
            if current.completed:
                if previous is None:
                    self.head = following
                else:
                    previous.next = following
                if current is self.tail:
                    self.tail = previous
                current.next = None
                self._size -= 1
                removed += 1
            else:
                previous = current
            current = following
        return removed

    def traverse(self):
        current = self.head
        while current is not None:
            following = current.next
            yield current
            current = following

    def completed_count(self):
        total = 0
        for node in self.traverse():
            if node.completed:
                total += 1
        return total

    def to_dicts(self):
        return [
            {"id": node.task_id, "title": node.title, "completed": node.completed}
            for node in self.traverse()
        ]

    def load_from_dicts(self, items):
        self.head = None
        self.tail = None
        self._size = 0
        self._next_id = 1
        for item in items:
            try:
                title = str(item["title"]).strip()
                task_id = int(item["id"])
                completed = bool(item.get("completed", False))
            except (KeyError, TypeError, ValueError):
                continue
            if not title:
                continue
            node = TaskNode(task_id, title, completed)
            if self.head is None:
                self.head = node
            else:
                self.tail.next = node
            self.tail = node
            self._size += 1
            self._next_id = max(self._next_id, task_id + 1)
