from datetime import date
import streamlit as st
from pawpal_system import Task, Pet, User, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if "owner" not in st.session_state:
    st.session_state.owner = User(owner_name)

if st.session_state.owner.name != owner_name:
    st.session_state.owner = User(owner_name)

if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler(st.session_state.owner)

if st.session_state.scheduler.user is not st.session_state.owner:
    st.session_state.scheduler = Scheduler(st.session_state.owner)


def find_pet(name: str) -> Pet | None:
    for pet in st.session_state.owner.pets:
        if pet.name == name:
            return pet
    return None


def get_warning_messages() -> list[str]:
    return st.session_state.scheduler.detect_time_conflicts()


st.markdown("### Add a Pet")
with st.form("add_pet_form"):
    new_pet_name = st.text_input("Pet name", value=pet_name)
    new_pet_species = st.selectbox("Pet species", ["dog", "cat", "other"], index=0)
    new_pet_age = st.number_input("Pet age", min_value=0, max_value=40, value=1)
    add_pet_submitted = st.form_submit_button("Add pet")

if add_pet_submitted:
    if not new_pet_name.strip():
        st.error("Pet name is required.")
    elif find_pet(new_pet_name.strip()) is not None:
        st.warning(f"{new_pet_name.strip()} is already in this session.")
    else:
        st.session_state.owner.add_pet(
            Pet(new_pet_name.strip(), new_pet_species, int(new_pet_age))
        )
        st.success(f"Added pet: {new_pet_name.strip()}")

st.markdown("### Tasks")
st.caption("Schedule a task for one of the pets stored in this session.")

pet_names = [pet.name for pet in st.session_state.owner.pets]

if pet_names:
    with st.form("add_task_form"):
        selected_pet_name = st.selectbox("Choose pet", pet_names)
        task_title = st.text_input("Task title", value="Morning walk")
        task_time = st.text_input("Time (HH:MM)", value="08:00")
        task_due_date = st.date_input("Due date", value=date.today())
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        priority = st.selectbox("Priority", ["high", "medium", "low"], index=0)
        recurrence = st.selectbox("Recurrence", ["none", "daily", "weekly"], index=0)
        task_completed = st.checkbox("Completed", value=False)
        add_task_submitted = st.form_submit_button("Schedule task")

    if add_task_submitted:
        normalized_time = task_time.strip() or None
        normalized_recurrence = None if recurrence == "none" else recurrence
        task = Task(
            task_title.strip(),
            int(duration),
            priority,
            task_completed,
            normalized_time,
            normalized_recurrence,
            task_due_date,
        )
        added = st.session_state.scheduler.add_task_to_pet(selected_pet_name, task)
        if added:
            st.success(f"Scheduled '{task.title}' for {selected_pet_name}.")
            for warning_message in get_warning_messages():
                st.warning(warning_message)
        else:
            st.error("Could not find that pet.")
else:
    st.info("Add a pet first before scheduling tasks.")

st.caption(
    f"Session owner in vault: {st.session_state.owner.name} | "
    f"Pets saved: {len(st.session_state.owner.pets)}"
)

if st.session_state.owner.pets:
    st.write("Current pets:")
    st.table(
        [
            {"name": pet.name, "species": pet.species, "age": pet.age}
            for pet in st.session_state.owner.pets
        ]
    )

st.markdown("### Filter Tasks")
status_filter = st.selectbox("Completion status", ["all", "complete", "incomplete"], index=0)
pet_filter_options = ["all"] + pet_names
selected_pet_filter = st.selectbox("Pet filter", pet_filter_options, index=0)

completed_filter = None
if status_filter == "complete":
    completed_filter = True
elif status_filter == "incomplete":
    completed_filter = False

pet_name_filter = None if selected_pet_filter == "all" else selected_pet_filter
filtered_tasks = st.session_state.scheduler.filter_tasks(
    completed=completed_filter,
    pet_name=pet_name_filter,
)

scheduled_tasks = [
    {
        "pet": pet.name,
        "title": task.title,
        "time": task.time or "",
        "due_date": task.due_date.isoformat() if task.due_date else "",
        "duration_minutes": task.duration_minutes,
        "priority": task.priority,
        "recurrence": task.recurrence or "",
        "completed": task.completed,
    }
    for pet, task in filtered_tasks
]

if scheduled_tasks:
    st.write("Current tasks:")
    st.table(scheduled_tasks)
    for warning_message in get_warning_messages():
        st.warning(warning_message)
else:
    st.info("No tasks yet. Add one above.")

incomplete_tasks = st.session_state.scheduler.get_incomplete_tasks()
if incomplete_tasks:
    st.markdown("### Complete a Task")
    with st.form("complete_task_form"):
        completion_options = [
            f"{pet.name} | {task.title} | {task.time or 'no time'}"
            for pet, task in incomplete_tasks
        ]
        selected_task_label = st.selectbox("Choose task to mark complete", completion_options)
        complete_task_submitted = st.form_submit_button("Mark complete")

    if complete_task_submitted:
        selected_index = completion_options.index(selected_task_label)
        selected_pet, selected_task = incomplete_tasks[selected_index]
        completed = st.session_state.scheduler.mark_task_complete(
            selected_pet.name,
            selected_task.title,
        )
        if completed:
            st.success(f"Marked '{selected_task.title}' complete for {selected_pet.name}.")
            if selected_task.recurrence in {"daily", "weekly"}:
                st.info("Created the next recurring occurrence automatically.")
            for warning_message in get_warning_messages():
                st.warning(warning_message)
        else:
            st.error("Could not complete that task.")

st.divider()

st.subheader("Build Schedule")
st.caption("This uses your Scheduler object to organize the tasks stored in session.")

if st.button("Generate schedule"):
    all_tasks = st.session_state.scheduler.get_all_tasks()
    has_scheduled_time = any(task.time for _, task in all_tasks)
    planned_tasks = (
        st.session_state.scheduler.sort_by_time()
        if has_scheduled_time
        else st.session_state.scheduler.get_tasks_by_priority()
    )

    if planned_tasks:
        st.write("Today's schedule:")
        st.table(
            [
                {
                    "pet": pet.name,
                    "task": task.title,
                    "time": task.time or "",
                    "due_date": task.due_date.isoformat() if task.due_date else "",
                    "duration_minutes": task.duration_minutes,
                    "priority": task.priority,
                    "recurrence": task.recurrence or "",
                    "completed": task.completed,
                }
                for pet, task in planned_tasks
            ]
        )
        for warning_message in get_warning_messages():
            st.warning(warning_message)
    else:
        st.info("No scheduled tasks to display.")
