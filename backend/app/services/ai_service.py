class AIService:
    async def generate_policy_guidance(self, policy_text: str, context: dict | None = None):
        if context is None:
            context = {}
        # Stub: Replace with actual AI logic
        return []

    async def generate_site_justification(self, application_id: str):
        # Stub: Replace with actual AI logic
        return f"Stub justification for application_id: {application_id}"

    async def generate_scenario_commentary(self, scenario_id: str):
        # Stub: Replace with actual AI logic
        return f"Stub commentary for scenario_id: {scenario_id}"

    async def generate_report_draft(self, application_id: str):
        # Stub: Replace with actual AI logic
        return None
