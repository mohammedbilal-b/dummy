"""
Core policy rating engine.
"""

from .models import (
    PolicyData,
    PolicyType,
    RiskLevel,
    RiskAssessment,
    PremiumCalculation,
)


class PolicyRater:
    """
    Main policy rating engine that calculates premiums based on risk assessment.
    """

    # Base rates per $1000 of coverage by policy type
    BASE_RATES = {
        PolicyType.AUTO: 1.5,
        PolicyType.HOME: 0.8,
        PolicyType.LIFE: 1.2,
        PolicyType.HEALTH: 2.0,
    }

    # Age risk multipliers
    AGE_RISK_MULTIPLIERS = {
        (0, 25): 1.5,
        (25, 40): 1.0,
        (40, 60): 1.2,
        (60, 120): 1.4,
    }

    def __init__(self):
        """Initialize the policy rater."""
        pass

    def calculate_premium(self, policy_data: PolicyData) -> PremiumCalculation:
        """
        Calculate the premium for a policy based on risk assessment.

        Args:
            policy_data: The policy data to rate

        Returns:
            PremiumCalculation with all details
        """
        # Perform risk assessment
        risk_assessment = self.assess_risk(policy_data)

        # Calculate base premium
        base_rate = self.BASE_RATES[policy_data.policy_type]
        base_premium = (policy_data.coverage_amount / 1000) * base_rate

        # Apply risk-based adjustment
        risk_multiplier = self._get_risk_multiplier(risk_assessment.risk_level)
        risk_adjustment = base_premium * (risk_multiplier - 1.0)

        # Calculate final premium
        final_premium = base_premium + risk_adjustment

        return PremiumCalculation(
            base_premium=round(base_premium, 2),
            risk_adjustment=round(risk_adjustment, 2),
            final_premium=round(final_premium, 2),
            risk_assessment=risk_assessment,
        )

    def assess_risk(self, policy_data: PolicyData) -> RiskAssessment:
        """
        Assess risk level for a policy.

        Args:
            policy_data: The policy data to assess

        Returns:
            RiskAssessment with risk level and score
        """
        risk_factors = {}
        total_risk_score = 0.0

        # Age risk factor
        age_risk = self._calculate_age_risk(policy_data.age)
        risk_factors["age_risk"] = age_risk
        total_risk_score += age_risk * 0.25

        # Location risk factor
        location_risk = policy_data.location_risk_score
        risk_factors["location_risk"] = location_risk
        total_risk_score += location_risk * 0.30

        # Claims history risk factor
        claims_risk = min(policy_data.history_claims * 15, 100)
        risk_factors["claims_risk"] = claims_risk
        total_risk_score += claims_risk * 0.35

        # Credit score risk factor (if available)
        if policy_data.credit_score is not None:
            credit_risk = self._calculate_credit_risk(policy_data.credit_score)
            risk_factors["credit_risk"] = credit_risk
            total_risk_score += credit_risk * 0.10

        # Normalize risk score to 0-100 range
        risk_score = min(total_risk_score, 100.0)

        # Determine risk level
        risk_level = self._determine_risk_level(risk_score)

        return RiskAssessment(
            risk_level=risk_level,
            risk_score=round(risk_score, 2),
            factors=risk_factors,
        )

    def _calculate_age_risk(self, age: int) -> float:
        """Calculate risk score based on age."""
        for age_range, multiplier in self.AGE_RISK_MULTIPLIERS.items():
            if age_range[0] <= age < age_range[1]:
                # Convert multiplier to risk score (0-100)
                return (multiplier - 1.0) * 50 + 25
        return 25.0  # Default medium-low risk

    def _calculate_credit_risk(self, credit_score: int) -> float:
        """Calculate risk score based on credit score."""
        # Higher credit score = lower risk
        # Credit score range: 300-850
        # Invert the score so lower credit = higher risk
        normalized = (850 - credit_score) / (850 - 300)
        return normalized * 100

    def _determine_risk_level(self, risk_score: float) -> RiskLevel:
        """Determine risk level category from risk score."""
        if risk_score < 25:
            return RiskLevel.LOW
        elif risk_score < 50:
            return RiskLevel.MEDIUM
        elif risk_score < 75:
            return RiskLevel.HIGH
        else:
            return RiskLevel.VERY_HIGH

    def _get_risk_multiplier(self, risk_level: RiskLevel) -> float:
        """Get premium multiplier based on risk level."""
        multipliers = {
            RiskLevel.LOW: 0.8,
            RiskLevel.MEDIUM: 1.0,
            RiskLevel.HIGH: 1.3,
            RiskLevel.VERY_HIGH: 1.6,
        }
        return multipliers[risk_level]
