# genpark-referral-program-skill

> **GenPark AI Agent Skill** -- Design, simulate, and optimize customer referral programs with viral coefficient and ROI projections.

## Features

- Viral coefficient (K-factor) calculation
- K-factor grading: Weak / Moderate / Strong / Viral
- Reward cost modeling: cash (100%) vs credit (60%) vs discount (40%)
- 12-month customer growth simulation
- CAC comparison: referral vs standard acquisition
- Full ROI projection
- Program design recommendations

## Quick Start

```python
from client import ReferralProgramClient

client = ReferralProgramClient()
result = client.design(
    avg_order_value=65,
    customer_acquisition_cost=28,
    referrer_reward={"type": "credit", "value": 15},
    referee_reward={"type": "discount", "value": 20},
    current_customers=2500,
)
print(f"K-factor: {result['viral_coefficient']} ({result['k_factor_grade']})")
print(f"12m new customers: {result['program_roi']['total_new_customers_12m']}")
```

## Installation

```bash
python example_usage.py  # No external dependencies
```

---
Built by [GenPark](https://genpark.ai) | [alphaparkinc](https://github.com/alphaparkinc)
