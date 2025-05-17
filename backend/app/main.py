# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import (
    policies,
    sites,
    constraints,
    plan_documents,
    scenarios,
    goals,
    planning_applications,
    precedent_cases,
    ai
)
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    version="v1.0.0",
    description="API for the Town Planning Assistant v2 application"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Include routers
app.include_router(policies.router, prefix=settings.API_V1_STR, tags=["Policies"])
app.include_router(sites.router, prefix=settings.API_V1_STR, tags=["Sites"])
app.include_router(constraints.router, prefix=settings.API_V1_STR, tags=["Constraints"])
app.include_router(plan_documents.router, prefix=settings.API_V1_STR, tags=["PlanDocuments"])
app.include_router(scenarios.router, prefix=settings.API_V1_STR, tags=["Scenarios"])
app.include_router(goals.router, prefix=settings.API_V1_STR, tags=["Goals"])
app.include_router(planning_applications.router, prefix=settings.API_V1_STR, tags=["PlanningApplications"])
app.include_router(precedent_cases.router, prefix=settings.API_V1_STR, tags=["PrecedentCases"])
app.include_router(ai.router, prefix=settings.API_V1_STR, tags=["AI"])


@app.get(f"{settings.API_V1_STR}/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    """
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    # This is for running directly with `python app/main.py`
    # For development, uvicorn app.main:app --reload is preferred
    uvicorn.run(app, host="0.0.0.0", port=8000)
