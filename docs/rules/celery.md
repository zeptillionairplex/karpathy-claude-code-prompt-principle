# Celery

## Position in Clean Architecture

Celery tasks live in the **infrastructure layer** — they are async message adapters, not business logic containers. The pattern mirrors HTTP handlers: just as a handler translates an HTTP request into a use case call, a task translates an async message into a use case call.

```
FastAPI handler  →  .delay() / .apply_async()  →  Broker (Redis)
                                                        ↓
                                              Celery Worker
                                                        ↓
                                              infrastructure/tasks.py
                                                        ↓
                                              UseCase.execute()
                                                        ↓
                                              Repository → DB
```

## Project Structure

```
app/
├── celery_app.py                      # Celery instance + config
└── modules/
    └── article/
        ├── application/
        │   └── use_cases.py           # Business logic — no Celery dependency
        └── infrastructure/
            ├── repositories.py
            └── tasks.py               # Celery tasks — calls use cases only
```

## Task Pattern

```python
# infrastructure/tasks.py
from app.celery_app import celery
from app.modules.article.application.use_cases import GenerateReportUseCase
from app.modules.article.infrastructure.repositories import ArticleRepository

@celery.task(bind=True, max_retries=3)
def generate_report_task(self, article_id: int) -> None:
    repo = ArticleRepository()
    use_case = GenerateReportUseCase(repo)
    try:
        use_case.execute(article_id)
    except Exception as exc:
        self.retry(exc=exc, countdown=60)
```

## Celery App Config

```python
# celery_app.py
from celery import Celery

celery = Celery("app")
celery.config_from_object({
    "broker_url": "redis://localhost:6379/0",
    "result_backend": "redis://localhost:6379/1",
    "task_serializer": "json",
    "result_serializer": "json",
    "accept_content": ["json"],
    "task_track_started": True,
    "task_acks_late": True,
    "worker_prefetch_multiplier": 1,
})
celery.autodiscover_tasks(["app.modules.article.infrastructure"])
```

## FastAPI ↔ Celery Integration

```python
# presentation/routers.py
@router.post("/articles/{id}/report")
async def request_report(article_id: int):
    task = generate_report_task.delay(article_id)
    return {"task_id": task.id, "status": "PENDING"}

@router.get("/tasks/{task_id}")
async def get_task_status(task_id: str):
    result = AsyncResult(task_id)
    return {"task_id": task_id, "status": result.status, "result": result.result}
```

## Chaining (complex workflows)

```python
from celery import chain

workflow = chain(
    validate_data_task.s(data),
    process_data_task.s(),
    notify_completion_task.s(user_id),
)
result = workflow.apply_async()
```

## Scheduled Tasks (Celery Beat)

```python
# celery_app.py
celery.conf.beat_schedule = {
    "cleanup-expired-sessions": {
        "task": "app.modules.auth.infrastructure.tasks.cleanup_sessions_task",
        "schedule": crontab(hour=2, minute=0),
    },
}
```

## Rules

- Task name: `verb_noun_task` — `send_email_task`, `generate_report_task`
- Task args: serializable primitives only — `int`, `str`, `dict`. Never ORM objects.
- Always include `bind=True` and `max_retries`.
- No business logic inside a task function. Call a use case instead.
- Inside a task, use sync DB sessions — Celery workers run outside the async event loop.
- Split large workloads: `task.chunks(items, 100)()`

## Testing

```python
# conftest.py
@pytest.fixture(autouse=True)
def celery_eager(settings):
    settings.CELERY_ALWAYS_EAGER = True  # run tasks synchronously in tests
```

Use cases must be testable without Celery — inject the repository directly in unit tests.
