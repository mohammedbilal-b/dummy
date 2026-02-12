"""
Unit tests for PolicyRater class.
"""

from policy_rating import PolicyRater
from policy_rating.models import (
    PolicyData,
    PolicyType,
    RiskLevel,
)


class TestPolicyRater:
    """Tests for PolicyRater class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.rater = PolicyRater()

    def test_calculate_premium_low_risk(self):
        """Test premium calculation for low-risk policy."""
        policy = PolicyData(
            policy_type=PolicyType.AUTO,
            coverage_amount=50000.0,
            age=35,
            location_risk_score=10.0,
            history_claims=0,
            credit_score=800,
        )

        result = self.rater.calculate_premium(policy)

        assert result.base_premium > 0
        assert result.final_premium > 0
        assert result.risk_assessment.risk_level in [RiskLevel.LOW, RiskLevel.MEDIUM]

    def test_calculate_premium_high_risk(self):
        """Test premium calculation for high-risk policy."""
        policy = PolicyData(
            policy_type=PolicyType.AUTO,
            coverage_amount=50000.0,
            age=20,
            location_risk_score=80.0,
            history_claims=5,
            credit_score=350,
        )

        result = self.rater.calculate_premium(policy)

        assert result.base_premium > 0
        assert result.final_premium > result.base_premium
        assert result.risk_assessment.risk_level in [RiskLevel.HIGH, RiskLevel.VERY_HIGH]

    def test_assess_risk_low_risk(self):
        """Test risk assessment for low-risk profile."""
        policy = PolicyData(
            policy_type=PolicyType.HOME,
            coverage_amount=200000.0,
            age=40,
            location_risk_score=15.0,
            history_claims=0,
            credit_score=780,
        )

        assessment = self.rater.assess_risk(policy)

        assert assessment.risk_level in [RiskLevel.LOW, RiskLevel.MEDIUM]
        assert assessment.risk_score < 50
        assert "age_risk" in assessment.factors
        assert "location_risk" in assessment.factors
        assert "claims_risk" in assessment.factors

    def test_assess_risk_high_risk(self):
        """Test risk assessment for high-risk profile."""
        policy = PolicyData(
            policy_type=PolicyType.AUTO,
            coverage_amount=30000.0,
            age=19,
            location_risk_score=90.0,
            history_claims=3,
            credit_score=320,
        )

        assessment = self.rater.assess_risk(policy)

        assert assessment.risk_level in [RiskLevel.HIGH, RiskLevel.VERY_HIGH]
        assert assessment.risk_score >= 50

    def test_assess_risk_without_credit_score(self):
        """Test risk assessment without credit score."""
        policy = PolicyData(
            policy_type=PolicyType.LIFE,
            coverage_amount=500000.0,
            age=45,
            location_risk_score=30.0,
            history_claims=1,
        )

        assessment = self.rater.assess_risk(policy)

        assert assessment.risk_score >= 0
        assert (
            "credit_risk" not in assessment.factors or assessment.factors.get("credit_risk") is None
        )

    def test_different_policy_types_have_different_base_rates(self):
        """Test that different policy types have different base rates."""
        base_policy_data = {
            "coverage_amount": 100000.0,
            "age": 35,
            "location_risk_score": 25.0,
            "history_claims": 0,
        }

        auto_policy = PolicyData(policy_type=PolicyType.AUTO, **base_policy_data)
        home_policy = PolicyData(policy_type=PolicyType.HOME, **base_policy_data)

        auto_premium = self.rater.calculate_premium(auto_policy)
        home_premium = self.rater.calculate_premium(home_policy)

        assert auto_premium.base_premium != home_premium.base_premium

    def test_age_risk_calculation(self):
        """Test age risk calculation across different age groups."""
        young_risk = self.rater._calculate_age_risk(22)
        middle_risk = self.rater._calculate_age_risk(35)
        senior_risk = self.rater._calculate_age_risk(70)

        assert young_risk > middle_risk
        assert senior_risk > middle_risk

    def test_credit_risk_calculation(self):
        """Test credit risk calculation."""
        high_credit_risk = self.rater._calculate_credit_risk(350)
        low_credit_risk = self.rater._calculate_credit_risk(800)

        assert high_credit_risk > low_credit_risk

    def test_risk_level_determination(self):
        """Test risk level determination from risk score."""
        assert self.rater._determine_risk_level(15.0) == RiskLevel.LOW
        assert self.rater._determine_risk_level(35.0) == RiskLevel.MEDIUM
        assert self.rater._determine_risk_level(60.0) == RiskLevel.HIGH
        assert self.rater._determine_risk_level(85.0) == RiskLevel.VERY_HIGH

    def test_risk_multiplier(self):
        """Test risk multiplier retrieval."""
        low_mult = self.rater._get_risk_multiplier(RiskLevel.LOW)
        medium_mult = self.rater._get_risk_multiplier(RiskLevel.MEDIUM)
        high_mult = self.rater._get_risk_multiplier(RiskLevel.HIGH)
        very_high_mult = self.rater._get_risk_multiplier(RiskLevel.VERY_HIGH)

        assert low_mult < medium_mult < high_mult < very_high_mult

    def test_premium_calculation_all_policy_types(self):
        """Test premium calculation works for all policy types."""
        base_data = {
            "coverage_amount": 100000.0,
            "age": 40,
            "location_risk_score": 30.0,
            "history_claims": 1,
        }

        for policy_type in PolicyType:
            policy = PolicyData(policy_type=policy_type, **base_data)
            result = self.rater.calculate_premium(policy)

            assert result.base_premium > 0
            assert result.final_premium > 0
            assert result.risk_assessment.risk_score >= 0
