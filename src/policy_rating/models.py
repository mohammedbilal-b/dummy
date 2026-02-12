"""
Data models for policy rating system.
"""

from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field, field_validator


class PolicyType(str, Enum):
    """Types of insurance policies."""

    AUTO = "auto"
    HOME = "home"
    LIFE = "life"
    HEALTH = "health"


class RiskLevel(str, Enum):
    """Risk levels for policy assessment."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


class PolicyData(BaseModel):
    """Input data for policy rating."""

    policy_type: PolicyType
    coverage_amount: float = Field(gt=0, description="Coverage amount in dollars")
    age: int = Field(ge=0, le=120, description="Age of the policyholder")
    location_risk_score: float = Field(ge=0, le=100, description="Location risk score")
    history_claims: int = Field(ge=0, description="Number of historical claims")
    credit_score: Optional[int] = Field(default=None, ge=300, le=850, description="Credit score")

    @field_validator("coverage_amount")
    @classmethod
    def validate_coverage_amount(cls, v):
        if v <= 0:
            raise ValueError("Coverage amount must be positive")
        if v > 10_000_000:
            raise ValueError("Coverage amount exceeds maximum limit")
        return v


class RiskAssessment(BaseModel):
    """Results of risk assessment."""

    risk_level: RiskLevel
    risk_score: float = Field(ge=0, le=100, description="Computed risk score")
    factors: dict = Field(default_factory=dict, description="Risk factors breakdown")


class PremiumCalculation(BaseModel):
    """Results of premium calculation."""

    base_premium: float = Field(gt=0, description="Base premium amount")
    risk_adjustment: float = Field(description="Risk-based adjustment")
    final_premium: float = Field(gt=0, description="Final premium amount")
    risk_assessment: RiskAssessment

    @field_validator("final_premium")
    @classmethod
    def validate_final_premium(cls, v):
        if v <= 0:
            raise ValueError("Final premium must be positive")
        return v
