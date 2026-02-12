#!/usr/bin/env python
"""
Example usage of the Policy Rating Module.

This script demonstrates how to use the policy rating module to calculate
insurance premiums based on various risk factors.
"""

from policy_rating import PolicyRater, PolicyData, PolicyType, RiskLevel


def print_separator():
    """Print a separator line."""
    print("=" * 70)


def print_premium_details(result, policy_type):
    """Print detailed premium calculation results."""
    print(f"\n{policy_type} Insurance Premium Calculation")
    print_separator()
    print(f"Base Premium:        ${result.base_premium:>10,.2f}")
    print(f"Risk Adjustment:     ${result.risk_adjustment:>10,.2f}")
    print(f"Final Premium:       ${result.final_premium:>10,.2f}")
    print_separator()
    print(f"Risk Level:          {result.risk_assessment.risk_level.value.upper()}")
    print(f"Risk Score:          {result.risk_assessment.risk_score:>10.2f}/100")
    print("\nRisk Factors:")
    for factor, value in result.risk_assessment.factors.items():
        print(f"  - {factor:20s}: {value:>6.2f}")
    print()


def example_auto_insurance():
    """Example: Calculate premium for auto insurance."""
    rater = PolicyRater()

    policy = PolicyData(
        policy_type=PolicyType.AUTO,
        coverage_amount=50000.0,
        age=28,
        location_risk_score=35.0,
        history_claims=1,
        credit_score=680,
    )

    result = rater.calculate_premium(policy)
    print_premium_details(result, "Auto")


def example_home_insurance():
    """Example: Calculate premium for home insurance."""
    rater = PolicyRater()

    policy = PolicyData(
        policy_type=PolicyType.HOME,
        coverage_amount=300000.0,
        age=45,
        location_risk_score=20.0,
        history_claims=0,
        credit_score=750,
    )

    result = rater.calculate_premium(policy)
    print_premium_details(result, "Home")


def example_life_insurance():
    """Example: Calculate premium for life insurance."""
    rater = PolicyRater()

    policy = PolicyData(
        policy_type=PolicyType.LIFE,
        coverage_amount=750000.0,
        age=55,
        location_risk_score=40.0,
        history_claims=2,
        credit_score=700,
    )

    result = rater.calculate_premium(policy)
    print_premium_details(result, "Life")


def example_comparison():
    """Example: Compare premiums for different risk profiles."""
    rater = PolicyRater()

    print("\nPremium Comparison: Low Risk vs. High Risk")
    print_separator()

    # Low risk profile
    low_risk = PolicyData(
        policy_type=PolicyType.AUTO,
        coverage_amount=50000.0,
        age=35,
        location_risk_score=10.0,
        history_claims=0,
        credit_score=800,
    )
    low_result = rater.calculate_premium(low_risk)

    # High risk profile
    high_risk = PolicyData(
        policy_type=PolicyType.AUTO,
        coverage_amount=50000.0,
        age=22,
        location_risk_score=80.0,
        history_claims=3,
        credit_score=350,
    )
    high_result = rater.calculate_premium(high_risk)

    print(f"\nLow Risk Profile:")
    print(f"  Risk Level: {low_result.risk_assessment.risk_level.value.upper()}")
    print(f"  Risk Score: {low_result.risk_assessment.risk_score:.2f}")
    print(f"  Premium:    ${low_result.final_premium:,.2f}")

    print(f"\nHigh Risk Profile:")
    print(f"  Risk Level: {high_result.risk_assessment.risk_level.value.upper()}")
    print(f"  Risk Score: {high_result.risk_assessment.risk_score:.2f}")
    print(f"  Premium:    ${high_result.final_premium:,.2f}")

    difference = high_result.final_premium - low_result.final_premium
    percentage = (difference / low_result.final_premium) * 100

    print(f"\nDifference: ${difference:,.2f} ({percentage:.1f}% more for high risk)")
    print()


def main():
    """Run all examples."""
    print("\n" + "=" * 70)
    print(" " * 15 + "POLICY RATING MODULE - EXAMPLES")
    print("=" * 70)

    example_auto_insurance()
    example_home_insurance()
    example_life_insurance()
    example_comparison()


if __name__ == "__main__":
    main()
