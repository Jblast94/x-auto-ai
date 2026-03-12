
class BaseAgent:
    def __init__(self, name, role, description):
        self.name = name
        self.role = role
        self.description = description

    def execute_task(self, task):
        raise NotImplementedError
