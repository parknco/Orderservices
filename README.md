# Order Service - GitHub Copilot Training Demo

A deliberately small FastAPI project for demonstrating AI pair programming in VS Code with GitHub Copilot.

## Existing functionality

- Create an order
- Retrieve an order
- Calculate order totals
- Route orders totaling EUR 5,000 or more to `MANUAL_REVIEW`
- Mark an order as `SHIPPED` from the service layer

## Deliberately missing functionality

Order cancellation is intentionally not implemented. During the training session, use the ticket below as the feature request:

> **JIRA-1842:** Customers should be able to cancel an order.

Use Copilot to clarify the requirement, create acceptance criteria, make an implementation plan, implement the feature, design tests, debug failures, review coverage, and create the GitHub Actions workflow.

## Run locally

```bash
python -m venv .venv
```

Activate the environment, then:

```bash
python -m pip install -r requirements.txt
pytest -v
uvicorn app:app --reload
```

API docs are available at `/docs` after starting the app.
