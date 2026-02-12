# Policy Rating Module

A comprehensive Python module for insurance policy rating and risk assessment. This module provides tools for calculating insurance premiums based on various risk factors including age, location, claims history, and credit score.

## Features

- **Risk Assessment**: Comprehensive risk evaluation based on multiple factors
- **Premium Calculation**: Accurate premium calculations for different policy types
- **Multiple Policy Types**: Support for Auto, Home, Life, and Health insurance
- **Data Validation**: Robust input validation using Pydantic models
- **Extensible Design**: Easy to add new risk factors and policy types

## Installation

### From source

```bash
git clone https://github.com/mohammedbilal-b/dummy.git
cd dummy
pip install -e .
```

### Development installation

```bash
pip install -e ".[dev]"
```

Or install development dependencies separately:

```bash
pip install -r requirements-dev.txt
```

## Quick Start

```python
from policy_rating import PolicyRater, PolicyData, PolicyType

# Create a policy rater instance
rater = PolicyRater()

# Define policy data
policy = PolicyData(
    policy_type=PolicyType.AUTO,
    coverage_amount=50000.0,
    age=35,
    location_risk_score=25.0,
    history_claims=0,
    credit_score=750
)

# Calculate premium
result = rater.calculate_premium(policy)

print(f"Base Premium: ${result.base_premium:.2f}")
print(f"Risk Adjustment: ${result.risk_adjustment:.2f}")
print(f"Final Premium: ${result.final_premium:.2f}")
print(f"Risk Level: {result.risk_assessment.risk_level}")
print(f"Risk Score: {result.risk_assessment.risk_score}")
```

## Policy Types

The module supports the following policy types:

- **AUTO**: Automobile insurance
- **HOME**: Homeowners insurance
- **LIFE**: Life insurance
- **HEALTH**: Health insurance

## Risk Factors

The risk assessment considers the following factors:

1. **Age Risk** (25% weight): Risk based on policyholder's age
2. **Location Risk** (30% weight): Risk based on location score (0-100)
3. **Claims History** (35% weight): Risk based on number of historical claims
4. **Credit Score** (10% weight, optional): Risk based on credit score (300-850)

## Risk Levels

- **LOW**: Risk score < 25
- **MEDIUM**: Risk score 25-49
- **HIGH**: Risk score 50-74
- **VERY_HIGH**: Risk score ≥ 75

## API Reference

### PolicyRater

Main class for calculating insurance premiums.

#### Methods

- `calculate_premium(policy_data: PolicyData) -> PremiumCalculation`
  - Calculates the premium for a policy based on risk assessment
  
- `assess_risk(policy_data: PolicyData) -> RiskAssessment`
  - Assesses risk level for a policy

### PolicyData

Input model for policy information.

#### Fields

- `policy_type: PolicyType` - Type of insurance policy
- `coverage_amount: float` - Coverage amount in dollars (> 0, ≤ 10,000,000)
- `age: int` - Age of policyholder (0-120)
- `location_risk_score: float` - Location risk score (0-100)
- `history_claims: int` - Number of historical claims (≥ 0)
- `credit_score: Optional[int]` - Credit score (300-850, optional)

### PremiumCalculation

Output model for premium calculation results.

#### Fields

- `base_premium: float` - Base premium amount
- `risk_adjustment: float` - Risk-based adjustment
- `final_premium: float` - Final premium amount
- `risk_assessment: RiskAssessment` - Detailed risk assessment

### RiskAssessment

Output model for risk assessment results.

#### Fields

- `risk_level: RiskLevel` - Overall risk level
- `risk_score: float` - Computed risk score (0-100)
- `factors: dict` - Breakdown of individual risk factors

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=policy_rating --cov-report=html

# Run specific test file
pytest tests/test_policy_rater.py
```

### Code Quality

```bash
# Format code with black
black src tests

# Lint with flake8
flake8 src tests

# Type checking with mypy
mypy src
```

### Project Structure

```
dummy/
├── src/
│   └── policy_rating/
│       ├── __init__.py
│       ├── models.py           # Data models
│       └── policy_rater.py     # Main rating engine
├── tests/
│   ├── test_models.py          # Model tests
│   ├── test_policy_rater.py    # PolicyRater tests
│   └── test_integration.py     # Integration tests
├── setup.py                     # Package setup
├── requirements.txt             # Production dependencies
├── requirements-dev.txt         # Development dependencies
├── pyproject.toml              # Tool configurations
├── .flake8                      # Flake8 configuration
└── README.md                    # This file
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License

