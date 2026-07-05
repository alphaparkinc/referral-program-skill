"""
example_usage.py -- Demonstrates the ReferralProgramClient SDK.
"""
from client import ReferralProgramClient

def main():
    client = ReferralProgramClient()

    print("[Referral Program Designer]")
    result = client.design(
        avg_order_value=65.00,
        customer_acquisition_cost=28.00,
        referrer_reward={"type": "credit", "value": 15},
        referee_reward={"type": "discount", "value": 20},
        current_customers=2500,
        share_rate=0.30,
        conversion_rate=0.25,
        simulation_months=12,
    )

    print(f"Viral Coefficient (K): {result['viral_coefficient']} ({result['k_factor_grade']})")
    print(f"Program Design: {result['program_design']}")
    roi = result["program_roi"]
    print(f"\n12-Month ROI Projection:")
    print(f"  New customers via referral: {roi['total_new_customers_12m']:,}")
    print(f"  Referral CAC: ${roi['referral_cac_usd']} vs Standard CAC: ${roi['standard_cac_usd']}")
    print(f"  CAC Savings: ${roi['cac_savings_usd']:,.2f}")
    print(f"  Reward Cost: ${roi['total_reward_cost_usd']:,.2f}")
    print(f"  Referral Revenue: ${roi['total_referral_revenue_usd']:,.2f}")
    print(f"  ROI: {roi['roi_pct']}%")
    print(f"\nGrowth Simulation (first 6 months):")
    print(f"{'Month':<7} {'Customers':>12} {'New Refs':>10} {'Revenue':>12}")
    for m in result["growth_simulation"][:6]:
        print(f"{m['month']:<7} {m['total_customers']:>12,} {m['new_from_referral']:>10.1f} ${m['referral_revenue_usd']:>10.2f}")
    print(f"\nRecommendations:")
    for r in result["recommendations"]:
        print(f"  - {r}")

if __name__ == "__main__":
    main()
