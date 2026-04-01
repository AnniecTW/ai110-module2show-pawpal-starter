from __future__ import annotations
from datetime import date, timedelta
from dataclasses import dataclass, field
from collections import defaultdict


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str
    completed: bool = False
    time: str | None = None
    recurrence: str | None = None
    due_date: date | None = None

    def mark_complete(self) -> None:
        self.completed = True

    def mark_incomplete(self) -> None:
        self.completed = False

    def create_next_occurrence(self) -> Task | None:
        """Create the next pending copy of a recurring daily or weekly task."""
        if self.recurrence not in {"daily", "weekly"}:
            return None

        base_due_date = self.due_date or date.today()
        days_to_add = 1 if self.recurrence == "daily" else 7

        return Task(
            self.title,
            self.duration_minutes,
            self.priority,
            False,
            self.time,
            self.recurrence,
            base_due_date + timedelta(days=days_to_add),
        )


@dataclass
class Pet:
    name: str
    species: str
    age: int | None = None
    tasks: list[Task] = field(default_factory=list, repr=False)

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def remove_task(self, task_title: str) -> bool:
        for index, task in enumerate(self.tasks):
            if task.title == task_title:
                del self.tasks[index]
                return True
        return False

    def get_tasks(self) -> list[Task]:
        return list(self.tasks)


@dataclass
class User:
    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)

    def remove_pet(self, pet_name: str) -> bool:
        for index, pet in enumerate(self.pets):
            if pet.name == pet_name:
                del self.pets[index]
                return True
        return False

    def get_all_tasks(self) -> list[tuple[Pet, Task]]:
        all_tasks: list[tuple[Pet, Task]] = []
        for pet in self.pets:
            for task in pet.tasks:
                all_tasks.append((pet, task))
        return all_tasks


class Scheduler:
    def __init__(self, user: User):
        self.user = user

    def get_all_tasks(self) -> list[tuple[Pet, Task]]:
        return self.user.get_all_tasks()

    def get_incomplete_tasks(self) -> list[tuple[Pet, Task]]:
        return [
            (pet, task)
            for pet, task in self.user.get_all_tasks()
            if not task.completed
        ]

    def get_completed_tasks(self) -> list[tuple[Pet, Task]]:
        return [
            (pet, task)
            for pet, task in self.user.get_all_tasks()
            if task.completed
        ]

    def get_tasks_by_priority(self) -> list[tuple[Pet, Task]]:
        """Return all tasks sorted from highest to lowest priority."""
        priority_order = {"high": 0, "medium": 1, "low": 2}
        return sorted(
            self.user.get_all_tasks(),
            key=lambda item: priority_order.get(item[1].priority.lower(), 99),
        )

    def get_tasks_with_priority(self, priority: str) -> list[tuple[Pet, Task]]:
        return [
            (pet, task)
            for pet, task in self.user.get_all_tasks()
            if task.priority.lower() == priority.lower()
        ]

    def filter_tasks(
        self,
        completed: bool | None = None,
        pet_name: str | None = None,
    ) -> list[tuple[Pet, Task]]:
        """Filter tasks by completion status, pet name, or both."""
        filtered_tasks = self.user.get_all_tasks()

        if completed is not None:
            filtered_tasks = [
                (pet, task) for pet, task in filtered_tasks if task.completed == completed
            ]

        if pet_name is not None:
            filtered_tasks = [
                (pet, task)
                for pet, task in filtered_tasks
                if pet.name.lower() == pet_name.lower()
            ]

        return filtered_tasks

    def detect_time_conflicts(self) -> list[str]:
        """Return warning messages for incomplete tasks that share the same date and time."""
        grouped_tasks = defaultdict(list)

        for pet, task in self.get_incomplete_tasks():
            if not task.time:
                continue
            grouped_tasks[(task.due_date, task.time)].append((pet.name, task.title))

        warnings = []
        for (due_date, time), entries in grouped_tasks.items():
            if len(entries) < 2:
                continue

            date_text = due_date.isoformat() if due_date else "unspecified date"
            task_list = ", ".join(f"{pet_name}: {task_title}" for pet_name, task_title in entries)
            warnings.append(f"Conflict at {time} on {date_text}: {task_list}")

        return warnings

    def add_task_to_pet(self, pet_name: str, task: Task) -> bool:
        pet = self._find_pet(pet_name)
        if pet is None:
            return False
        pet.add_task(task)
        return True

    def mark_task_complete(self, pet_name: str, task_title: str) -> bool:
        """Mark a task complete and enqueue its next occurrence when it recurs."""
        pet = self._find_pet(pet_name)
        if pet is None:
            return False

        for task in pet.tasks:
            if task.title == task_title:
                if task.completed:
                    return True
                task.mark_complete()
                next_task = task.create_next_occurrence()
                if next_task is not None:
                    pet.add_task(next_task)
                return True
        return False

    def mark_task_incomplete(self, pet_name: str, task_title: str) -> bool:
        pet = self._find_pet(pet_name)
        if pet is None:
            return False

        for task in pet.tasks:
            if task.title == task_title:
                task.mark_incomplete()
                return True
        return False

    def _find_pet(self, pet_name: str) -> Pet | None:
        for pet in self.user.pets:
            if pet.name == pet_name:
                return pet
        return None
    
    def print_schedule(self):
        """Print a pet-by-pet schedule ordered by priority for terminal demos."""
        by_pet = defaultdict(list)
        for pet, task in self.get_all_tasks():
            age_text = f", {pet.age}y" if pet.age is not None else ""
            pet_label = f"{pet.name} ({pet.species}{age_text})"
            by_pet[pet_label].append(task)

        print("Today's Schedule")
        print("=" * 44)
        priority_order = {"high": 0, "medium": 1, "low": 2}

        for pet_label, tasks in by_pet.items():
            print(f"\n🐾 {pet_label}")
            for t in sorted(tasks, key=lambda x: priority_order.get(x.priority.lower(), 99)):
                status = "✅" if t.completed else "⬜"
                print(
                    f"  {status} {t.title:<16} "
                    f"({t.duration_minutes} min) [{t.priority}]"
                )
    
    def sort_by_time(self):
        """Return all tasks ordered by time, placing unscheduled tasks last."""
        return sorted(
            self.user.get_all_tasks(),
            key=lambda item: (item[1].time is None, item[1].time or ""),
        )
