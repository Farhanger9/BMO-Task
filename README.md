# Agent task runner

A deliberately small React/FastAPI coding challenge. The synchronous backend is implemented through the HTTP and SQLite boundaries; the product UI is intentionally deferred.

## Proposed structure

```text
.
├── backend/
│   ├── app/
│   │   ├── agent/
│   │   │   ├── controller.py
│   │   │   └── models.py
│   │   ├── tools/
│   │   │   ├── calculator.py
│   │   │   ├── text_processor.py
│   │   │   ├── tool.py
│   │   │   └── weather_mock.py
│   │   ├── api.py
│   │   ├── api_models.py
│   │   ├── main.py
│   │   └── persistence.py
│   ├── tests/
│   │   ├── test_agent_controller.py
│   │   ├── test_api.py
│   │   ├── test_persistence.py
│   │   └── test_tools.py
│   └── pyproject.toml
└── frontend/
    ├── src/
    │   ├── api/
    │   │   └── tasks.ts
    │   ├── App.tsx
    │   ├── main.tsx
    │   └── styles.css
    ├── index.html
    ├── package.json
    ├── tsconfig.app.json
    ├── tsconfig.json
    └── vite.config.ts
```

The backend files now exist. The frontend API client above describes the intended later shape and will be added only when its behavior is implemented.

## Architectural boundaries

- `api.py` and `api_models.py` own HTTP routing, validation, and status-code mapping. They translate between transport data and the application boundary without deciding how tasks run.
- `agent/` owns task classification, tool selection, orchestration, and execution traces. It depends on tools and the repository contract through constructor injection, so it can be tested without FastAPI or SQLite.
- `tools/` contains the small shared `Tool` contract and the three independent implementations. Tools receive plain domain input and return explicit results; they know nothing about HTTP or persistence.
- `persistence.py` contains the task repository contract and its SQLite implementation together. Persistence is isolated behind that contract, while keeping the tiny data-access surface in one readable module.
- `main.py` is the composition root. It creates concrete dependencies and wires them into the API; it should contain configuration and lifecycle setup, not business rules.
- `frontend/src/api/tasks.ts` is the browser-side API boundary. `App.tsx` owns the small amount of UI state needed by the challenge, without introducing a component hierarchy or state library prematurely.

## Abstraction choices

Justified abstractions:

- A structural `Tool` protocol gives the controller one stable contract and lets tests provide a trivial fake tool. No inheritance or registration framework is required.
- A `TaskRepository` protocol isolates SQLite and makes controller tests deterministic. The abstraction stays task-specific rather than becoming a generic repository.
- `AgentController` provides one home for routing and orchestration rules that are independently testable from HTTP.
- Explicit task, tool-result, and trace models make execution behavior inspectable and error outcomes predictable.
- Constructor/function injection keeps dependency ownership visible and avoids mutable global state.

Over-engineering for this challenge:

- A dependency-injection container, service locator, plugin discovery, command bus, or event bus.
- Generic repository or CRUD base classes, unit-of-work machinery, and ORM models for a single SQLite-backed task aggregate.
- A class hierarchy for tools beyond the minimal protocol, or separate factories/registries before routing rules require them.
- Duplicate DTO layers for HTTP, application, domain, and persistence when a small number of boundary models can be reused safely.
- Async repository/tool APIs for synchronous SQLite and in-process operations.
- A frontend state library, generated API client, design system, or multi-page routing for one small workflow.

## Setup

Backend dependencies are declared in `backend/pyproject.toml`; frontend dependencies and scripts are in `frontend/package.json`.
