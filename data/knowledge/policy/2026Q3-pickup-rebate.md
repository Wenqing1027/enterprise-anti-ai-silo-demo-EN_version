# 2026Q3 Pickup Rebate Policy (Synthetic)

Version: `2026Q3-pickup-rebate-V3`

## Tiers
| Tier | Monthly cumulative pickup | Rebate rate | Notes |
|------|------------|----------|------|
| Bronze | ≥300 units | 2.0% | |
| Silver | ≥800 units | 3.5% | Full color mix bonus up to +0.5% |
| Gold | ≥1200 units | 4.2% | |
| Diamond | ≥1800 units | 5.0% | Requires compliance inspection pass |

## Order review rules (illustrative)
- When hero colors (matte black/star gray) are out of stock, suggest same-price-band substitute colors;
- Flame red long-term stockout—prioritize star gray substitute;
- Tier tier-up incentive reminders paused for tier-1 dealers with open P0 complaints.

## Settlement fields
Settlement must include: `settlement_id`, `dealer_id`, `policy_version`, `current_rebate_tier`, `payable_amt`, `clawback_amt`.
