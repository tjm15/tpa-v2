# TPA v2 Backend

This directory contains the FastAPI backend for The Planner's Assistant v2 application.

## Project Structure

```
tpa_backend/
├── app/
│   ├── __init__.py
│   ├── main.py                     # Main FastAPI application
│   ├── models/                     # Pydantic models
│   │   ├── __init__.py
│   │   ├── common_models.py        # Shared enums and base models
│   │   ├── constraint_models.py
│   │   ├── document_models.py
│   │   ├── goal_models.py
│   │   ├── officer_report_models.py
│   │   ├── planning_application_models.py
│   │   ├── policy_models.py
│   │   ├── precedent_models.py
│   │   ├── scenario_models.py
│   │   └── site_models.py
│   ├── routers/                    # API route definitions
│   │   ├── __init__.py
│   │   ├── ai.py
│   │   ├── constraints.py
│   │   ├── goals.py
│   │   ├── plan_documents.py
│   │   ├── planning_applications.py # Includes officer_reports logic
│   │   ├── policies.py
│   │   ├── precedent_cases.py
│   │   ├── scenarios.py
│   │   └── sites.py
│   ├── crud/                       # Data Access Layer (database interactions - stubs for now)
│   │   ├── __init__.py
│   │   └── base_crud.py
│   ├── core/                       # Core components like configuration
│   │   ├── __init__.py
│   │   └── config.py
│   └── services/                   # Business logic layer (stubs for now)
│       └── __init__.py
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## Setup

1.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

To run the FastAPI development server:

```bash
uvicorn app.main:app --reload
```

The API will typically be available at `http://127.0.0.1:8000`.
The OpenAPI documentation (Swagger UI) will be at `http://127.0.0.1:8000/docs`.
Alternative ReDoc documentation will be at `http://127.0.0.1:8000/redoc`.

## Development Notes

* **Models (`app/models/`)**: Pydantic models define the data structures and perform validation. They are based on the TypeScript interfaces from the frontend.
* **Routers (`app/routers/`)**: Each router handles API endpoints for a specific resource (e.g., policies, sites).
* **CRUD (`app/crud/`)**: This layer is intended for database interaction logic. Currently, it contains stubs. You'll need to implement actual database operations here (e.g., using SQLAlchemy with a chosen database).
* **Services (`app/services/`)**: This layer is for more complex business logic that might involve multiple CRUD operations or external service calls.
* **Configuration (`app/core/config.py`)**: For managing application settings (e.g., database URLs, API keys).

This scaffold provides a starting point. You will need to:
1.  Implement the actual logic within the route stubs (database operations, business logic).
2.  Set up a database and integrate it using an ORM like SQLAlchemy.
3.  Implement authentication and authorization.
4.  Expand on error handling and request validation as needed.
5.  Write comprehensive tests.
