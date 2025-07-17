from pydantic import BaseModel,Field

class analyzer_response(BaseModel):
    plan: str = Field(..., description="The learning plan for lecturer and practitioner to follow and synchronize output.")
    analysis: str = Field(..., description="The analysis of the student's performance.")