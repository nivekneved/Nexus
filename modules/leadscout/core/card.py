"""
LeadScout-Core: LeadCard Pydantic v2 Schema
==========================================
State store object tracking discovered attributes and completed probes.
"""

from typing import List, Dict, Any, Optional, Set
from pydantic import BaseModel, Field

class LeadCard(BaseModel):
    lead_id: str
    company_name: str
    domain: Optional[str] = None

    # Domain & Tech intelligence
    mx_records: List[str] = Field(default_factory=list)
    spf_record: Optional[str] = None
    email_provider: Optional[str] = None
    tech_stack: List[str] = Field(default_factory=list)

    # Staff & Identity intelligence
    staff_members: List[Dict[str, str]] = Field(default_factory=list) # [{name, title, profile_url}]
    social_profiles: Dict[str, str] = Field(default_factory=dict) # {platform: url}
    bio_keywords: List[str] = Field(default_factory=list)
    gravatar_avatar: Optional[str] = None

    # Deliverability intelligence
    email_permutations: List[str] = Field(default_factory=list)
    confirmed_emails: List[Dict[str, Any]] = Field(default_factory=list) # [{email, status, score}]
    catch_all: Optional[bool] = None

    # State tracking
    completed_probes: Set[str] = Field(default_factory=set)
    qualification_score: float = 0.0
    status: str = "INITIALIZED"

    class Config:
        arbitrary_types_allowed = True
