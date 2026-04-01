# PawPal+

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Smarter Scheduling

The scheduler now supports task times, priority-based ordering, and filtering by pet or completion status. It also handles recurring daily and weekly tasks by automatically creating the next occurrence with an updated due date when a recurring task is completed. If two incomplete tasks are scheduled for the same date and time, the system returns a warning so the app can surface the conflict without crashing.

## Features

- Sorting by time, with scheduled tasks shown in chronological order and tasks without a time placed last
- Priority-based task ordering with `high`, `medium`, and `low` priorities
- Filtering tasks by completion status, pet name, or both at the same time
- Daily recurrence, which creates the next day's task when a daily task is marked complete
- Weekly recurrence, which creates the next week's task when a weekly task is marked complete
- Conflict warnings for duplicate scheduled times when two incomplete tasks share the same date and time
- Per-pet task management for adding, removing, and listing tasks across multiple pets
- Completion tracking so tasks can be marked complete or incomplete without deleting them

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Testing PawPal+

Run the test suite with:

```bash
python -m pytest
```

The tests cover the core scheduling behaviors in `pawpal_system.py`, including chronological task sorting, filtering by pet and completion status, recurrence logic for daily and weekly tasks, and conflict detection when two incomplete tasks share the same scheduled date and time. The suite also includes edge cases such as pets with no tasks, tasks without scheduled times, and recurring tasks that should not create duplicate follow-up tasks.

Confidence Level (1–5 stars) in the system's reliability: 4.5 stars

## 📸 Demo

<img src='/image.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>
