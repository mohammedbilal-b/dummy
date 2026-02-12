"""
Policy Rating Module

A comprehensive module for insurance policy rating and risk assessment.
"""

__version__ = "0.1.0"

from .policy_rater import PolicyRater
from .models import PolicyData, RiskAssessment, PremiumCalculation, PolicyType, RiskLevel

__all__ = [
    "PolicyRater",
    "PolicyData",
    "RiskAssessment",
    "PremiumCalculation",
    "PolicyType",
    "RiskLevel",
]
