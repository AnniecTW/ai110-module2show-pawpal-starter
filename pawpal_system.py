from dataclasses import dataclass, field


@dataclass
class Task:
    id: int
    type: str


@dataclass
class Pet:
    id: int


@dataclass
class UserTask:
    id: int
    assigned_time: str
    task: Task = None


class User:
    def __init__(self, id: int, available_time: str, preference: str):
        self.id = id
        self.available_time = available_time
        self.preference = preference
        self.pets: list[Pet] = []
        self.user_tasks: list[UserTask] = []

    def add_pet(self, pet: Pet):
        pass

    def schedule_task(self, task: Task, assigned_time: str):
        pass
