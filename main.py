from pawpal_system import Task, Pet, User, Scheduler


def print_task_list(title: str, tasks: list[tuple[Pet, Task]]) -> None:
    print(f"\n{title}")
    print("-" * len(title))
    for pet, task in tasks:
        status = "complete" if task.completed else "incomplete"
        time_text = task.time or "no time"
        print(
            f"{pet.name}: {task.title} at {time_text} | "
            f"{task.priority} priority | {status}"
        )


def print_warnings(title: str, warnings: list[str]) -> None:
    print(f"\n{title}")
    print("-" * len(title))
    if not warnings:
        print("No conflicts detected.")
        return
    for warning in warnings:
        print(f"WARNING: {warning}")


# Create pets
luna = Pet("Luna", "dog", 10)
bella = Pet("Bella", "cat", 4)

# Create owner
ann = User("Ann", [bella, luna])

# Create tasks out of order by time
evening_walk = Task("Evening Walk", 30, "medium", False, "18:00")
breakfast = Task("Breakfast", 15, "high", True, "08:00")
medication = Task("Medication", 10, "high", False, "07:30")
grooming = Task("Grooming", 20, "low")
playtime = Task("Playtime", 25, "medium", True, "12:30")
vet_visit = Task("Vet Visit", 45, "high", False, "07:30")

# Add tasks in mixed order
luna.add_task(evening_walk)
luna.add_task(medication)
bella.add_task(grooming)
bella.add_task(breakfast)
bella.add_task(playtime)
bella.add_task(vet_visit)

# Create scheduler
ann_sc = Scheduler(ann)

print_task_list("All Tasks (Original Order)", ann_sc.get_all_tasks())
print_task_list("Tasks Sorted By Time", ann_sc.sort_by_time())
print_task_list("Completed Tasks", ann_sc.filter_tasks(completed=True))
print_task_list("Bella's Tasks", ann_sc.filter_tasks(pet_name="Bella"))
print_task_list(
    "Luna's Incomplete Tasks",
    ann_sc.filter_tasks(completed=False, pet_name="Luna"),
)
print_warnings("Conflict Warnings", ann_sc.detect_time_conflicts())
