"""
Integration tests for the policy rating system.
"""

from policy_rating import PolicyRater, PolicyData, PolicyType


class TestPolicyRatingIntegration:
    """Integration tests for the complete policy rating workflow."""

    def setup_method(self):
        """Set up test fixtures."""
        self.rater = PolicyRater()

    def test_complete_auto_policy_workflow(self):
        """Test complete workflow for auto insurance policy."""
        # Create policy data
        policy = PolicyData(
            policy_type=PolicyType.AUTO,
            coverage_amount=75000.0,
            age=28,
            location_risk_score=45.0,
            history_claims=1,
            credit_score=680,
        )

        # Calculate premium
        result = self.rater.calculate_premium(policy)

        # Verify all components are present
        assert result.base_premium > 0
        assert result.final_premium > 0
        assert result.risk_assessment is not None
        assert result.risk_assessment.risk_score >= 0
        assert len(result.risk_assessment.factors) > 0

        # Verify calculation consistency
        calculated_final = result.base_premium + result.risk_adjustment
        assert abs(calculated_final - result.final_premium) < 0.01

    def test_complete_home_policy_workflow(self):
        """Test complete workflow for home insurance policy."""
        policy = PolicyData(
            policy_type=PolicyType.HOME,
            coverage_amount=300000.0,
            age=52,
            location_risk_score=20.0,
            history_claims=0,
            credit_score=740,
        )

        result = self.rater.calculate_premium(policy)

        assert result.base_premium > 0
        assert result.final_premium > 0
        assert result.risk_assessment.risk_level is not None

    def test_policy_comparison(self):
        """Test comparing premiums between similar policies with different risk profiles."""
        low_risk_policy = PolicyData(
            policy_type=PolicyType.LIFE,
            coverage_amount=500000.0,
            age=35,
            location_risk_score=10.0,
            history_claims=0,
            credit_score=800,
        )

        high_risk_policy = PolicyData(
            policy_type=PolicyType.LIFE,
            coverage_amount=500000.0,
            age=35,
            location_risk_score=85.0,
            history_claims=4,
            credit_score=350,
        )

        low_risk_result = self.rater.calculate_premium(low_risk_policy)
        high_risk_result = self.rater.calculate_premium(high_risk_policy)

        # High risk should have higher premium
        assert high_risk_result.final_premium > low_risk_result.final_premium
        assert (
            high_risk_result.risk_assessment.risk_score > low_risk_result.risk_assessment.risk_score
        )

    def test_edge_case_minimum_values(self):
        """Test edge case with minimum valid values."""
        policy = PolicyData(
            policy_type=PolicyType.AUTO,
            coverage_amount=1000.0,
            age=18,
            location_risk_score=0.0,
            history_claims=0,
            credit_score=300,
        )

        result = self.rater.calculate_premium(policy)

        assert result.base_premium > 0
        assert result.final_premium > 0

    def test_edge_case_maximum_values(self):
        """Test edge case with maximum valid values."""
        policy = PolicyData(
            policy_type=PolicyType.HEALTH,
            coverage_amount=10_000_000.0,
            age=120,
            location_risk_score=100.0,
            history_claims=10,
            credit_score=850,
        )

        result = self.rater.calculate_premium(policy)

        assert result.base_premium > 0
        assert result.final_premium > 0

    def test_multiple_policy_calculations(self):
        """Test calculating premiums for multiple policies in sequence."""
        policies = [
            PolicyData(
                policy_type=PolicyType.AUTO,
                coverage_amount=50000.0,
                age=30,
                location_risk_score=25.0,
                history_claims=0,
            ),
            PolicyData(
                policy_type=PolicyType.HOME,
                coverage_amount=250000.0,
                age=45,
                location_risk_score=30.0,
                history_claims=1,
            ),
            PolicyData(
                policy_type=PolicyType.LIFE,
                coverage_amount=750000.0,
                age=55,
                location_risk_score=40.0,
                history_claims=2,
            ),
        ]

        results = []
        for policy in policies:
            result = self.rater.calculate_premium(policy)
            results.append(result)

        assert len(results) == 3
        for result in results:
            assert result.base_premium > 0
            assert result.final_premium > 0
