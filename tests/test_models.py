"""
Unit tests for data models.
"""

import pytest
from pydantic import ValidationError
from policy_rating.models import (
    PolicyData,
    PolicyType,
    RiskLevel,
    RiskAssessment,
    PremiumCalculation,
)


class TestPolicyData:
    """Tests for PolicyData model."""

    def test_valid_policy_data(self):
        """Test creating a valid PolicyData instance."""
        data = PolicyData(
            policy_type=PolicyType.AUTO,
            coverage_amount=50000.0,
            age=35,
            location_risk_score=25.0,
            history_claims=0,
            credit_score=750,
        )
        assert data.policy_type == PolicyType.AUTO
        assert data.coverage_amount == 50000.0
        assert data.age == 35
        assert data.credit_score == 750

    def test_invalid_coverage_amount(self):
        """Test that negative coverage amount raises validation error."""
        with pytest.raises(ValidationError):
            PolicyData(
                policy_type=PolicyType.AUTO,
                coverage_amount=-1000.0,
                age=35,
                location_risk_score=25.0,
                history_claims=0,
            )

    def test_excessive_coverage_amount(self):
        """Test that coverage amount exceeding maximum raises validation error."""
        with pytest.raises(ValidationError):
            PolicyData(
                policy_type=PolicyType.AUTO,
                coverage_amount=20_000_000.0,
                age=35,
                location_risk_score=25.0,
                history_claims=0,
            )

    def test_invalid_age(self):
        """Test that invalid age raises validation error."""
        with pytest.raises(ValidationError):
            PolicyData(
                policy_type=PolicyType.AUTO,
                coverage_amount=50000.0,
                age=150,
                location_risk_score=25.0,
                history_claims=0,
            )

    def test_invalid_credit_score(self):
        """Test that invalid credit score raises validation error."""
        with pytest.raises(ValidationError):
            PolicyData(
                policy_type=PolicyType.AUTO,
                coverage_amount=50000.0,
                age=35,
                location_risk_score=25.0,
                history_claims=0,
                credit_score=200,
            )

    def test_optional_credit_score(self):
        """Test that credit score is optional."""
        data = PolicyData(
            policy_type=PolicyType.HOME,
            coverage_amount=200000.0,
            age=45,
            location_risk_score=30.0,
            history_claims=1,
        )
        assert data.credit_score is None


class TestRiskAssessment:
    """Tests for RiskAssessment model."""

    def test_valid_risk_assessment(self):
        """Test creating a valid RiskAssessment instance."""
        assessment = RiskAssessment(
            risk_level=RiskLevel.MEDIUM,
            risk_score=45.5,
            factors={"age_risk": 25.0, "claims_risk": 15.0},
        )
        assert assessment.risk_level == RiskLevel.MEDIUM
        assert assessment.risk_score == 45.5
        assert "age_risk" in assessment.factors


class TestPremiumCalculation:
    """Tests for PremiumCalculation model."""

    def test_valid_premium_calculation(self):
        """Test creating a valid PremiumCalculation instance."""
        assessment = RiskAssessment(
            risk_level=RiskLevel.LOW,
            risk_score=20.0,
            factors={},
        )
        calc = PremiumCalculation(
            base_premium=500.0,
            risk_adjustment=-100.0,
            final_premium=400.0,
            risk_assessment=assessment,
        )
        assert calc.base_premium == 500.0
        assert calc.final_premium == 400.0

    def test_invalid_negative_premium(self):
        """Test that negative final premium raises validation error."""
        assessment = RiskAssessment(
            risk_level=RiskLevel.LOW,
            risk_score=20.0,
            factors={},
        )
        with pytest.raises(ValidationError):
            PremiumCalculation(
                base_premium=500.0,
                risk_adjustment=-600.0,
                final_premium=-100.0,
                risk_assessment=assessment,
            )
