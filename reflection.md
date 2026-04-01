# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
  My UML design includes classes Task, User, Pet, and Scheduler.
  1. Task:
  - Id
  - Type
  2. User:
  - Id
  - Available time
  - Preference
  - add_pet()
  - schedule_task()
  3. Pet:
  - Id
  4. Scheduler
  - Id
  - Assigned_time

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

| Class     | Add                                   | Why                                |
| --------- | ------------------------------------- | ---------------------------------- |
| Pet       | `name: str`, `species: str`           | Identify pets and match task types |
| Task      | `duration: int`, `priority: int`      | Enable scheduling logic            |
| Scheduler | `pet: Pet`                            | Link tasks to specific pets        |
| User      | time slots (instead of single string) | Enable conflict detection          |

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
  My scheduler consider contraints such as time, prority, and complete status.
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
  One tradeoff my scheduler makes is that it keeps the logic simple by only supporting basic recurrence rules like daily and weekly tasks. That makes the code easier to understand and test, but it also means it cannot handle more complex scheduling cases like monthly tasks or custom repeat patterns.
- Why is that tradeoff reasonable for this scenario?
  That tradeoff is reasonable for this scenario because most pet care tasks, like feeding, walking, or giving medicine, usually happen on simple daily or weekly schedules. Keeping the recurrence logic simple makes the app easier to build, test, and explain, while still covering the most common needs of a pet owner.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
  I started by creating an initial UML for the system, then asked AI to review it and point out any missing attributes, methods, or potential design issues. It gave a number of suggestions that I found practical and useful. I also found AI helpful for debugging, especially when I provided enough context about the code.
- What kinds of prompts or questions were most helpful?
  I found that including absolute file paths in my prompts helped prevent AI from getting confused about the project structure. In general, the more specific the prompt, the better the results. Providing a few example outputs or expected behaviors also made the responses more efficient and accurate.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
  There was a moment when AI suggested updating app.py to align with the `Task` object I had designed earlier. I almost accepted it, but decided to go the other way instead. I asked it to update the `Task` object to match `app.py`, because the logic in `app.py` made more sense to me at that point.
- How did you evaluate or verify what the AI suggested?
  I reviewed the code line by line to make sure I understood what each part was doing before accepting any changes. If something felt unclear or didn’t make sense, I cross-checked it with another AI and refined it until I was confident it was correct.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
  I tested the main scheduling behaviors in PawPal+. I checked that tasks are sorted in the correct time order, that tasks without a set time show up last, and that filtering works by pet name and completion status. I also tested recurring tasks to make sure marking a daily or weekly task complete creates the next occurrence correctly. On top of that, I tested conflict detection so the scheduler warns the user when two incomplete tasks are scheduled for the same date and time.
- Why were these tests important?
  These tests were important because they cover the core features that make the scheduler useful and reliable. Sorting and filtering help the user actually understand the schedule, recurrence makes repeated pet care tasks easier to manage, and conflict detection helps catch scheduling problems before they become confusing. I also included edge cases, like pets with no tasks or tasks with no time, because those situations can easily cause bugs if they are not tested.

**b. Confidence**

- How confident are you that your scheduler works correctly?
  I’m pretty confident that it works correctly for the main features because I tested sorting, filtering, recurrence, and conflict detection. The tests passed, so I think the scheduler is reliable for the core use cases.
- What edge cases would you test next if you had more time?
  I would test more unusual cases, like multiple recurring tasks at the same time, invalid time inputs, duplicate task titles, and what happens when a user edits or deletes a recurring task. I’d also test more situations with empty task lists and tasks on different dates.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
  I’m most satisfied with the scheduler logic in pawpal_system.py, especially the way it handles sorting, filtering, recurrence, and conflict warnings. I think those features make the app feel more practical and closer to a real pet care planner.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
  If I had another iteration, I would improve the UI and make the scheduling system more flexible. For example, I would add support for more complex recurrence options, better editing and deleting of recurring tasks, and a clearer way to display conflicts and daily plans in the app.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
  I learned that system design should still be led by humans at the beginning, since we have a clearer understanding of our own requirements and real-world edge cases. For the coding part, using AI to help generate code and then carefully reviewing it is a practical and efficient way to build solutions quickly. At the same time, I think it’s important that humans stay in control of the overall direction and make the final decisions.
