---
description: "Task list for Kubernetes deployment of Todo + Chatbot application"
---

# Tasks: Kubernetes Deployment for Fullstack Todo + Chatbot

**Input**: Design documents from `/specs/2-kubernetes-deployment/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Kubernetes/IaC project**: `k8s/`, `fullstack-todo/frontend/`, `fullstack-todo/backend/`, `fullstack-todo/chatbot_backend/`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create k8s directory structure in fullstack-todo/k8s/
- [X] T002 Create Helm chart directory structure at fullstack-todo/k8s/charts/todo-app/
- [X] T003 [P] Create manifests directory structure at fullstack-todo/k8s/manifests/

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Create Helm Chart.yaml for todo-app chart in fullstack-todo/k8s/charts/todo-app/Chart.yaml
- [X] T005 Create Helm values.yaml for todo-app chart in fullstack-todo/k8s/charts/todo-app/values.yaml
- [X] T006 [P] Create namespace.yaml manifest in fullstack-todo/k8s/manifests/namespace.yaml
- [X] T007 [P] Create db-pvc.yaml manifest in fullstack-todo/k8s/manifests/db-pvc.yaml
- [X] T008 [P] Create ingress.yaml manifest in fullstack-todo/k8s/manifests/ingress.yaml
- [X] T009 Configure environment for AI-assisted tools (Gordon, kubectl-ai, kagent)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Deploy Fullstack Application on Kubernetes (Priority: P1) 🎯 MVP

**Goal**: Deploy the complete Todo + Chatbot application stack on a local Kubernetes cluster using Minikube and ensure all services work together properly

**Independent Test**: Successfully deploy all three services (frontend, backend, chatbot_backend) to a local Minikube cluster and verify they are all running and communicating properly

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests first, ensure they FAIL before implementation**

- [X] T010 [P] [US1] Create deployment validation script for services connectivity in scripts/validate-deployment.sh

### Implementation for User Story 1

- [X] T010 [P] [US1] Create frontend-deployment.yaml template in fullstack-todo/k8s/charts/todo-app/templates/frontend-deployment.yaml
- [X] T011 [P] [US1] Create backend-deployment.yaml template in fullstack-todo/k8s/charts/todo-app/templates/backend-deployment.yaml
- [X] T012 [P] [US1] Create chatbot-deployment.yaml template in fullstack-todo/k8s/charts/todo-app/templates/chatbot-deployment.yaml
- [X] T013 [P] [US1] Create db-deployment.yaml template in fullstack-todo/k8s/charts/todo-app/templates/db-deployment.yaml
- [X] T014 [P] [US1] Create frontend-service.yaml template in fullstack-todo/k8s/charts/todo-app/templates/frontend-service.yaml
- [X] T015 [P] [US1] Create backend-service.yaml template in fullstack-todo/k8s/charts/todo-app/templates/backend-service.yaml
- [X] T016 [P] [US1] Create chatbot-service.yaml template in fullstack-todo/k8s/charts/todo-app/templates/chatbot-service.yaml
- [X] T017 [P] [US1] Create db-service.yaml template in fullstack-todo/k8s/charts/todo-app/templates/db-service.yaml
- [X] T018 [US1] Configure NodePort service for frontend access
- [X] T019 [US1] Create ClusterIP services for backend and chatbot services
- [X] T020 [US1] Set up service-to-service communication using Kubernetes DNS

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Use AI-Assisted DevOps Tools for Deployment (Priority: P2)

**Goal**: Leverage AI-assisted tools (Gordon, kubectl-ai, kagent) throughout the deployment process to accelerate containerization, deployment, and management tasks

**Independent Test**: Use AI tools to generate Dockerfiles, deployment commands, and perform cluster operations instead of manual creation

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [X] T021 [P] [US2] Create AI-tool validation script to confirm AI tools were used in fullstack-todo/scripts/validate-ai-tools.sh

### Implementation for User Story 2

- [X] T022 [P] [US2] Use Gordon to generate frontend Dockerfile in fullstack-todo/frontend/Dockerfile
- [X] T023 [P] [US2] Use Gordon to generate backend Dockerfile in fullstack-todo/backend/Dockerfile
- [X] T024 [P] [US2] Use Gordon to generate chatbot_backend Dockerfile in fullstack-todo/chatbot_backend/Dockerfile
- [X] T025 [US2] Generate Docker images for each service using Docker Desktop
- [X] T026 [US2] Use kubectl-ai to assist with deployment command generation
- [X] T027 [US2] Use kagent for cluster health analysis during deployment

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Containerize All Application Components (Priority: P3)

**Goal**: Containerize all application components (frontend, backend, chatbot_backend) with production-ready configurations so they can run reliably in the Kubernetes environment

**Independent Test**: Build Docker images for each service and ensure they start properly in containerized environments

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [X] T028 [P] [US3] Create Docker image validation script in fullstack-todo/scripts/validate-images.sh

### Implementation for User Story 3

- [X] T029 [US3] Configure production-ready multi-stage build for frontend Dockerfile
- [X] T030 [US3] Configure production-ready multi-stage build for backend Dockerfile
- [X] T031 [US3] Configure production-ready multi-stage build for chatbot_backend Dockerfile
- [X] T032 [US3] Set up proper environment variable injection for all Docker images
- [X] T033 [US3] Configure health checks (liveness/readiness) for all containers
- [X] T034 [US3] Configure resource requests and limits in all deployments
- [X] T035 [US3] Add official language-specific slim/alpine base images to Dockerfiles

**Checkpoint**: At this point, User Stories 1, 2 AND 3 should all work independently

---

## Phase 6: User Story 4 - Validate Service Connectivity and Reproducibility (Priority: P4)

**Goal**: Verify that services communicate properly within the cluster and the deployment is reproducible via Helm so the deployment is reliable and can be consistently recreated

**Independent Test**: Verify network connectivity between services and redeploy from Helm charts to confirm reproducibility

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [X] T036 [P] [US4] Create Helm reproducibility test in fullstack-todo/scripts/test-helm-reproducibility.sh

### Implementation for User Story 4

- [X] T037 [P] [US4] Create Application ConfigMap for service communication in fullstack-todo/k8s/charts/todo-app/templates/app-configmap.yaml
- [X] T038 [P] [US4] Create Database ConfigMap in fullstack-todo/k8s/charts/todo-app/templates/db-configmap.yaml
- [X] T039 [P] [US4] Create Database Credentials Secret in fullstack-todo/k8s/charts/todo-app/templates/db-secret.yaml
- [X] T040 [US4] Implement service-to-service communication using Kubernetes DNS service discovery
- [X] T041 [US4] Test deployment reproducibility via Helm chart with multiple install/uninstall cycles
- [X] T042 [US4] Validate service-to-service connectivity inside cluster
- [X] T043 [US4] Verify frontend can communicate with both backend and chatbot services

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T044 [P] Update quickstart.md with deployment instructions from docs/deployment.md
- [X] T045 Add RBAC configuration for service-to-service authentication in fullstack-todo/k8s/charts/todo-app/templates/rbac.yaml
- [X] T046 Add comprehensive liveness and readiness probes to all deployments
- [X] T047 [P] Add documentation for AI-assisted DevOps workflows in docs/ai-workflows.md
- [X] T050 Final validation of all success criteria in fullstack-todo/scripts/final-validation.sh
- [X] T051 Run quickstart.md validation to ensure deployment works end-to-end

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Integrates with all previous stories for validation

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
# Launch all deployment templates for User Story 1 together:
Task: "Create frontend-deployment.yaml template in fullstack-todo/k8s/charts/todo-app/templates/frontend-deployment.yaml"
Task: "Create backend-deployment.yaml template in fullstack-todo/k8s/charts/todo-app/templates/backend-deployment.yaml"
Task: "Create chatbot-deployment.yaml template in fullstack-todo/k8s/charts/todo-app/templates/chatbot-deployment.yaml"

# Launch all service templates for User Story 1 together:
Task: "Create frontend-service.yaml template in fullstack-todo/k8s/charts/todo-app/templates/frontend-service.yaml"
Task: "Create backend-service.yaml template in fullstack-todo/k8s/charts/todo-app/templates/backend-service.yaml"
Task: "Create chatbot-service.yaml template in fullstack-todo/k8s/charts/todo-app/templates/chatbot-service.yaml"
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
5. Add User Story 4 → Test independently → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
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