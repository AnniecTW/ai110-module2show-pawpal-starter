from pathlib import Path
import sys
from datetime import date, timedelta

sys.path.append(str(Path(__file__).resolve().parents[1]))

from pawpal_system import Pet, Scheduler, Task, User


def test_mark_task_complete_changes_status():
    pet = Pet("Bella", "cat")
    task = Task("Feeding", 15, "high")
    pet.add_task(task)
    user = User("Ann", [pet])
    scheduler = Scheduler(user)

    result = scheduler.mark_task_complete("Bella", "Feeding")

    assert result is True
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet("Luna", "dog")
    task = Task("Walk", 30, "medium")

    initial_count = len(pet.tasks)
    pet.add_task(task)

    assert len(pet.tasks) == initial_count + 1


def test_sort_by_time_orders_tasks_by_time():
    pet = Pet("Mochi", "dog")
    later_task = Task("Evening walk", 30, "medium", time="18:00")
    earlier_task = Task("Breakfast", 15, "high", time="08:00")
    no_time_task = Task("Brush", 10, "low")
    pet.add_task(later_task)
    pet.add_task(earlier_task)
    pet.add_task(no_time_task)
    scheduler = Scheduler(User("Jordan", [pet]))

    result = scheduler.sort_by_time()

    assert [task.title for _, task in result] == [
        "Breakfast",
        "Evening walk",
        "Brush",
    ]


def test_filter_tasks_by_completion_status():
    pet = Pet("Bella", "cat")
    completed_task = Task("Feeding", 15, "high", True)
    incomplete_task = Task("Nap check", 5, "low")
    pet.add_task(completed_task)
    pet.add_task(incomplete_task)
    scheduler = Scheduler(User("Ann", [pet]))

    result = scheduler.filter_tasks(completed=True)

    assert [task.title for _, task in result] == ["Feeding"]


def test_filter_tasks_by_completion_status_and_pet_name():
    bella = Pet("Bella", "cat")
    luna = Pet("Luna", "dog")
    bella.add_task(Task("Feeding", 15, "high", True))
    luna.add_task(Task("Walk", 30, "medium", True))
    luna.add_task(Task("Brush", 10, "low"))
    scheduler = Scheduler(User("Ann", [bella, luna]))

    result = scheduler.filter_tasks(completed=True, pet_name="luna")

    assert [task.title for _, task in result] == ["Walk"]


def test_marking_daily_task_complete_creates_next_occurrence():
    pet = Pet("Bella", "cat")
    task = Task("Feeding", 15, "high", False, "08:00", "daily", date(2026, 3, 31))
    pet.add_task(task)
    scheduler = Scheduler(User("Ann", [pet]))

    result = scheduler.mark_task_complete("Bella", "Feeding")

    assert result is True
    assert len(pet.tasks) == 2
    assert pet.tasks[0].completed is True
    assert pet.tasks[1].title == "Feeding"
    assert pet.tasks[1].completed is False
    assert pet.tasks[1].time == "08:00"
    assert pet.tasks[1].recurrence == "daily"
    assert pet.tasks[1].due_date == date(2026, 4, 1)


def test_marking_non_recurring_task_complete_does_not_create_new_task():
    pet = Pet("Luna", "dog")
    task = Task("Walk", 30, "medium", False, "18:00")
    pet.add_task(task)
    scheduler = Scheduler(User("Ann", [pet]))

    result = scheduler.mark_task_complete("Luna", "Walk")

    assert result is True
    assert len(pet.tasks) == 1
    assert pet.tasks[0].completed is True


def test_marking_weekly_task_complete_moves_due_date_forward_seven_days():
    pet = Pet("Mochi", "dog")
    task = Task("Bath", 30, "medium", False, "09:00", "weekly", date(2026, 3, 31))
    pet.add_task(task)
    scheduler = Scheduler(User("Ann", [pet]))

    result = scheduler.mark_task_complete("Mochi", "Bath")

    assert result is True
    assert pet.tasks[1].due_date == date(2026, 4, 7)


def test_recurring_task_without_due_date_uses_today_as_base_date():
    pet = Pet("Luna", "dog")
    task = Task("Breakfast", 15, "high", False, "08:00", "daily")
    pet.add_task(task)
    scheduler = Scheduler(User("Ann", [pet]))

    result = scheduler.mark_task_complete("Luna", "Breakfast")

    assert result is True
    assert pet.tasks[1].due_date == date.today() + timedelta(days=1)


def test_detect_time_conflicts_returns_warning_for_overlapping_tasks():
    bella = Pet("Bella", "cat")
    luna = Pet("Luna", "dog")
    bella.add_task(Task("Breakfast", 15, "high", False, "08:00", due_date=date(2026, 3, 31)))
    luna.add_task(Task("Walk", 30, "medium", False, "08:00", due_date=date(2026, 3, 31)))
    scheduler = Scheduler(User("Ann", [bella, luna]))

    warnings = scheduler.detect_time_conflicts()

    assert len(warnings) == 1
    assert "Conflict at 08:00 on 2026-03-31" in warnings[0]
    assert "Bella: Breakfast" in warnings[0]
    assert "Luna: Walk" in warnings[0]


def test_sort_by_time_keeps_same_time_tasks_and_puts_no_time_last():
    bella = Pet("Bella", "cat")
    luna = Pet("Luna", "dog")
    bella.add_task(Task("Breakfast", 15, "high", False, "07:30"))
    luna.add_task(Task("Medication", 10, "high", False, "07:30"))
    bella.add_task(Task("Grooming", 20, "low"))
    scheduler = Scheduler(User("Ann", [bella, luna]))

    result = scheduler.sort_by_time()

    assert [task.title for _, task in result] == [
        "Breakfast",
        "Medication",
        "Grooming",
    ]


def test_pet_with_no_tasks_returns_empty_lists():
    bella = Pet("Bella", "cat")
    scheduler = Scheduler(User("Ann", [bella]))

    assert scheduler.get_all_tasks() == []
    assert scheduler.sort_by_time() == []
    assert scheduler.filter_tasks(pet_name="Bella") == []


def test_detect_time_conflicts_ignores_completed_tasks():
    bella = Pet("Bella", "cat")
    luna = Pet("Luna", "dog")
    bella.add_task(Task("Breakfast", 15, "high", True, "08:00", due_date=date(2026, 3, 31)))
    luna.add_task(Task("Walk", 30, "medium", False, "08:00", due_date=date(2026, 3, 31)))
    scheduler = Scheduler(User("Ann", [bella, luna]))

    warnings = scheduler.detect_time_conflicts()

    assert warnings == []


def test_marking_completed_recurring_task_again_does_not_duplicate_occurrence():
    pet = Pet("Bella", "cat")
    task = Task("Feeding", 15, "high", True, "08:00", "daily", date(2026, 3, 31))
    pet.add_task(task)
    scheduler = Scheduler(User("Ann", [pet]))

    result = scheduler.mark_task_complete("Bella", "Feeding")

    assert result is True
    assert len(pet.tasks) == 1
