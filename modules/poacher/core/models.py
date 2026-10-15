"""
CompetitorPoacher: Pydantic v2 Models & Schemas
==============================================
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class TalentRecord(BaseModel):
    name: str
    title: str
    tenure_months: int
    flight_risk_score: float
    synthesized_email: Optional[str] = None
    verified_smtp: bool = False

class DissatisfactionSignal(BaseModel):
    source_platform: str # G2, Capterra, Trustpilot
    rating: int
    review_snippet: str
    pain_category: str
    target_competitor: str

class PoacherCard(BaseModel):
    card_id: str
    competitor_name: str
    target_domain: str
    tech_stack: List[str] = Field(default_factory=list)
    talent_roster: List[TalentRecord] = Field(default_factory=list)
    churn_signals: List[DissatisfactionSignal] = Field(default_factory=list)
    contract_tenders: List[Dict[str, Any]] = Field(default_factory=list)
    poaching_score: float = 0.0
    status: str = "DISCOVERED"
