---
description: "Task list for In-Memory Todo Python Console Application"
---

# Tasks: In-Memory Todo Python Console Application

**Input**: Design documents from `/specs/001-in-memory-todo/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project structure per implementation plan in src/
- [x] T002 Initialize Python project with pyproject.toml dependencies
- [ ] T003 [P] Configure linting and formatting tools for Python 3.13+

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Examples of foundational tasks (adjust based on your project):

- [x] T004 Create base Task model in src/todo_app/models.py
- [x] T005 [P] Implement in-memory storage manager in src/todo_app/storage.py
- [x] T006 [P] Setup CLI command parser in src/todo_app/cli.py
- [x] T007 Create main application entry point in src/todo_app/main.py
- [x] T008 Configure error handling and custom exceptions in src/todo_app/exceptions.py
- [ ] T009 Setup environment configuration management

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add and View Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to add tasks with titles and descriptions, and view them with unique IDs and status indicators

**Independent Test**: The application allows users to add tasks with titles and descriptions, and displays a list of all tasks with unique IDs and status indicators. The user can see their tasks and their completion status.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T010 [P] [US1] Manual test for add command in tests/manual_test_plan.md
- [ ] T011 [P] [US1] Manual test for list command in tests/manual_test_plan.md

### Implementation for User Story 1

- [x] T012 [P] [US1] Create Task class in src/todo_app/models.py with id, title, description, completed, created_at
- [x] T013 [P] [US1] Implement Task validation rules in src/todo_app/models.py
- [x] T014 [US1] Implement add_task method in src/todo_app/storage.py
- [x] T015 [US1] Implement get_all_tasks method in src/todo_app/storage.py
- [x] T016 [US1] Implement add command handler in src/todo_app/cli.py
- [x] T017 [US1] Implement list command handler in src/todo_app/cli.py
- [x] T018 [US1] Add console output formatting for tasks in src/todo_app/cli.py
- [x] T019 [US1] Integrate add/list commands with main application loop in src/todo_app/main.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Update and Delete Tasks (Priority: P2)

**Goal**: Enable users to modify or remove tasks from their todo list as their plans change

**Independent Test**: The application allows users to update existing tasks by ID and delete tasks by ID, with appropriate feedback for successful operations or error handling for invalid inputs.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T020 [P] [US2] Manual test for update command in tests/manual_test_plan.md
- [ ] T021 [P] [US2] Manual test for delete command in tests/manual_test_plan.md

### Implementation for User Story 2

- [x] T022 [P] [US2] Implement update_task method in src/todo_app/storage.py
- [x] T023 [P] [US2] Implement delete_task method in src/todo_app/storage.py
- [x] T024 [US2] Implement update command handler in src/todo_app/cli.py
- [x] T025 [US2] Implement delete command handler in src/todo_app/cli.py
- [x] T026 [US2] Add validation for existing task ID in update/delete operations in src/todo_app/storage.py
- [x] T027 [US2] Integrate update/delete commands with main application loop in src/todo_app/main.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Mark Task Completion Status (Priority: P3)

**Goal**: Enable users to track which tasks they have completed to maintain an accurate view of remaining work

**Independent Test**: The application allows users to toggle the completion status of tasks by ID, with appropriate feedback and visual indicators in the task list.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T028 [P] [US3] Manual test for complete command in tests/manual_test_plan.md
- [ ] T029 [P] [US3] Manual test for incomplete command in tests/manual_test_plan.md

### Implementation for User Story 3

- [x] T030 [P] [US3] Implement mark_task_complete method in src/todo_app/storage.py
- [x] T031 [P] [US3] Implement mark_task_incomplete method in src/todo_app/storage.py
- [x] T032 [US3] Implement complete command handler in src/todo_app/cli.py
- [x] T033 [US3] Implement incomplete command handler in src/todo_app/cli.py
- [x] T034 [US3] Update task display format to show [✓] for complete, [ ] for incomplete in src/todo_app/cli.py
- [x] T035 [US3] Integrate completion commands with main application loop in src/todo_app/main.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T036 [P] Add comprehensive error handling for all commands in src/todo_app/exceptions.py
- [x] T037 [P] Implement user-friendly error messages that explain what went wrong and suggest fixes in src/todo_app/exceptions.py
- [x] T038 [P] Add input validation for all commands in src/todo_app/cli.py
- [x] T039 [P] Add help command implementation in src/todo_app/cli.py
- [x] T040 [P] Add quit/exit command implementation in src/todo_app/main.py
- [x] T041 [P] Add validation for task title length (max 100 chars) and description length (max 500 chars) in src/todo_app/models.py
- [x] T042 [P] Add handling for edge cases (empty task list, invalid IDs) in src/todo_app/storage.py
- [x] T043 [P] Documentation updates in README.md
- [x] T044 [P] Run quickstart validation using specs/001-in-memory-todo/quickstart.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all models for User Story 1 together:
Task: "Create Task class in src/todo_app/models.py with id, title, description, completed, created_at"
Task: "Implement Task validation rules in src/todo_app/models.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence