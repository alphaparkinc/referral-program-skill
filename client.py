"""
referral-program-skill: Client SDK
Design and simulate customer referral programs with viral coefficient and ROI projection.
"""
from __future__ import annotations
from typing import Optional

REWARD_COST_MAP = {"cash": 1.0, "credit": 0.6, "discount": 0.4}

PROGRAM_BENCHMARKS = {
    "k_factor_low":    0.15,
    "k_factor_good":   0.40,
    "k_factor_viral":  1.00,
    "share_rate":      0.30,
    "conversion_rate": 0.25,
}


class ReferralProgramClient:
    """
    SDK for designing and simulating customer referral programs.
    Calculates viral coefficient (K-factor), ROI, and month-by-month growth.
    """

    def design(
        self,
        avg_order_value: float,
        customer_acquisition_cost: float,
        referrer_reward: dict,
        referee_reward: dict,
        current_customers: int = 1000,
        share_rate: float = 0.30,
        conversion_rate: float = 0.25,
        simulation_months: int = 12,
    ) -> dict:
        """
        Design and simulate a referral program.

        Args:
            avg_order_value:           Average order value (USD).
            customer_acquisition_cost: Current CAC (USD).
            referrer_reward:           {type: 'cash'|'credit'|'discount', value: float}.
            referee_reward:            {type: 'cash'|'credit'|'discount', value: float}.
            current_customers:         Starting customer base.
            share_rate:                % of customers who share (default 30%).
            conversion_rate:           % of referred who convert (default 25%).
            simulation_months:         Months to simulate.

        Returns:
            dict with viral_coefficient, program_roi, growth_simulation, recommendations
        """
        ref_r_type = referrer_reward.get("type", "discount")
        ref_r_val  = float(referrer_reward.get("value", 10))
        ref_e_type = referee_reward.get("type", "discount")
        ref_e_val  = float(referee_reward.get("value", 10))

        # Effective cost per reward (cash costs more than credit/discount)
        cost_per_referral = (
            ref_r_val * REWARD_COST_MAP.get(ref_r_type, 0.5) +
            ref_e_val * REWARD_COST_MAP.get(ref_e_type, 0.5)
        )

        # Viral coefficient K = share_rate * conversion_rate * invitations_per_share
        invites_per_sharer = 3  # average invitations sent
        k_factor = round(share_rate * conversion_rate * invites_per_sharer, 3)

        # Growth simulation
        customers = float(current_customers)
        simulation = []
        total_referrals = 0
        total_reward_cost = 0.0
        total_revenue = 0.0

        for month in range(1, simulation_months + 1):
            new_from_referral = customers * share_rate * invites_per_sharer * conversion_rate
            customers += new_from_referral
            reward_cost = new_from_referral * cost_per_referral
            revenue = new_from_referral * avg_order_value
            total_referrals += new_from_referral
            total_reward_cost += reward_cost
            total_revenue += revenue
            simulation.append({
                "month": month,
                "total_customers": round(customers),
                "new_from_referral": round(new_from_referral, 1),
                "reward_cost_usd": round(reward_cost, 2),
                "referral_revenue_usd": round(revenue, 2),
            })

        # ROI
        total_new_customers = round(customers) - current_customers
        referral_cac = total_reward_cost / max(total_referrals, 1)
        cac_savings = (customer_acquisition_cost - referral_cac) * total_new_customers
        roi_pct = (total_revenue - total_reward_cost) / max(total_reward_cost, 1) * 100

        program_roi = {
            "total_new_customers_12m": total_new_customers,
            "referral_cac_usd": round(referral_cac, 2),
            "standard_cac_usd": customer_acquisition_cost,
            "cac_savings_usd": round(cac_savings, 2),
            "total_reward_cost_usd": round(total_reward_cost, 2),
            "total_referral_revenue_usd": round(total_revenue, 2),
            "roi_pct": round(roi_pct, 1),
        }

        recommendations = self._generate_recommendations(k_factor, ref_r_type, ref_e_type, roi_pct, share_rate)

        return {
            "viral_coefficient": k_factor,
            "k_factor_grade": "Viral" if k_factor >= 1 else "Strong" if k_factor >= 0.4 else "Moderate" if k_factor >= 0.15 else "Weak",
            "program_design": {
                "referrer_reward": f"{ref_r_type.title()} reward: ${ref_r_val:.2f}",
                "referee_reward": f"{ref_e_type.title()} reward: ${ref_e_val:.2f}",
                "cost_per_successful_referral": round(cost_per_referral, 2),
            },
            "program_roi": program_roi,
            "growth_simulation": simulation,
            "recommendations": recommendations,
        }

    @staticmethod
    def _generate_recommendations(k, ref_r_type, ref_e_type, roi, share_rate) -> list[str]:
        recs = []
        if k < 0.15:
            recs.append("K-factor is low. Increase referrer reward or add a time-limited bonus to boost sharing.")
        elif k >= 1.0:
            recs.append("Viral K-factor achieved! Each customer brings more than 1 new customer on average.")
        if ref_r_type == "cash":
            recs.append("Cash rewards drive highest sharing rates but cost more. Consider credit at 60% effective cost.")
        if ref_e_type == "discount":
            recs.append("First-order discount for referees increases conversion -- consider 15-20% for best results.")
        if roi > 300:
            recs.append(f"Excellent ROI ({roi:.0f}%). Consider scaling the program with paid promotion to referrers.")
        recs.append("Track referral link performance per customer to identify your top advocates for VIP treatment.")
        recs.append("Add a leaderboard or milestone bonus (e.g., refer 5 friends, get a free product) to gamify the program.")
        return recs[:4]
