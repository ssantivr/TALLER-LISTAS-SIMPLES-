class TaskFilter:
    ALL = "all"
    PENDING = "pending"
    COMPLETED = "completed"

    @staticmethod
    def matches(node, mode):
        if mode == TaskFilter.PENDING:
            return not node.completed
        if mode == TaskFilter.COMPLETED:
            return node.completed
        return True
