# Policy Rating Module - Quick Reference

## Quick Install

```bash
pip install -e .
```

## Basic Usage

```python
from policy_rating import PolicyRater, PolicyData, PolicyType

# Initialize rater
rater = PolicyRater()

# Create policy
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
print(f"Premium: ${result.final_premium:.2f}")
```

## Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=policy_rating --cov-report=html
```

## Code Quality

```bash
# Format
black src tests

# Lint
flake8 src tests
```

## Policy Types

- `PolicyType.AUTO` - Auto insurance
- `PolicyType.HOME` - Home insurance
- `PolicyType.LIFE` - Life insurance
- `PolicyType.HEALTH` - Health insurance

## Risk Levels

- `RiskLevel.LOW` - Score < 25
- `RiskLevel.MEDIUM` - Score 25-49
- `RiskLevel.HIGH` - Score 50-74
- `RiskLevel.VERY_HIGH` - Score ≥ 75

## Input Validation

- `coverage_amount`: 0 < amount ≤ 10,000,000
- `age`: 0 ≤ age ≤ 120
- `location_risk_score`: 0 ≤ score ≤ 100
- `history_claims`: claims ≥ 0
- `credit_score`: 300 ≤ score ≤ 850 (optional)

## Examples

Run the example script:

```bash
python example.py
```

See `CONTRIBUTING.md` for development guidelines.
