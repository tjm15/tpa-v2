# app/api/ai.py

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional, List

from app.services.ai_service import AIService
from app.models.policies import AIGuidance
from app.models.officer_reports import OfficerReport

router = APIRouter(prefix="/ai", tags=["AI"])


class GeneratePolicyGuidanceRequest(BaseModel):
    policyText: str
    context: Optional[dict] = None

class GeneratePolicyGuidanceResponse(BaseModel):
    suggestions: List[AIGuidance]

class GenerateSiteJustificationRequest(BaseModel):
    applicationId: str

class GenerateSiteJustificationResponse(BaseModel):
    justification: str

class GenerateScenarioCommentaryRequest(BaseModel):
    scenarioId: str

class GenerateScenarioCommentaryResponse(BaseModel):
    commentary: str

class GenerateReportDraftRequest(BaseModel):
    applicationId: str

class GenerateReportDraftResponse(BaseModel):
    report: OfficerReport


@router.post("/generate-policy-guidance", response_model=GeneratePolicyGuidanceResponse)
async def generate_policy_guidance(
    body: GeneratePolicyGuidanceRequest, ai: AIService = Depends()
):
    return GeneratePolicyGuidanceResponse(suggestions=[])


@router.post("/generate-site-justification", response_model=GenerateSiteJustificationResponse)
async def generate_site_justification(
    body: GenerateSiteJustificationRequest, ai: AIService = Depends()
):
    return GenerateSiteJustificationResponse(justification="")


@router.post("/generate-scenario-commentary", response_model=GenerateScenarioCommentaryResponse)
async def generate_scenario_commentary(
    body: GenerateScenarioCommentaryRequest, ai: AIService = Depends()
):
    return GenerateScenarioCommentaryResponse(commentary="")


@router.post("/generate-report-draft", response_model=GenerateReportDraftResponse)
async def generate_report_draft(
    body: GenerateReportDraftRequest, ai: AIService = Depends()
):
    return GenerateReportDraftResponse(
        report=OfficerReport(
            applicationId=body.applicationId,
            version="",
            sections=[],
            lastModified="",
            status="Draft",
        )
    )
