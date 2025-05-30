# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import (
    policies,
    sites,
    constraints,
    plan_documents,
    scenarios,
    goals,
    planning_applications,
    officer_reports,
    precedent_cases,
    ai,
)

app = FastAPI(
    title="The Planner's Assistant v2 API",
    version="0.0.1",
    description="API for The Planner's Assistant v2 application, covering both Plan-Making and Development Management workspaces.",
)

# CORS middleware for frontend integration (adjust origins in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers for each resource
app.include_router(policies.router, prefix="/policies", tags=["Policies"])
app.include_router(sites.router, prefix="/sites", tags=["Sites"])
app.include_router(constraints.router, prefix="/constraints", tags=["Constraints"])
app.include_router(plan_documents.router, prefix="/plan-documents", tags=["PlanDocuments"])
app.include_router(scenarios.router, prefix="/scenarios", tags=["Scenarios"])
app.include_router(goals.router, prefix="/goals", tags=["Goals"])
app.include_router(planning_applications.router, prefix="/planning-applications", tags=["PlanningApplications"])
app.include_router(officer_reports.router, prefix="/officer-reports", tags=["OfficerReports"])
app.include_router(precedent_cases.router, prefix="/precedent-cases", tags=["PrecedentCases"])
app.include_router(ai.router, prefix="/ai", tags=["AI"])
