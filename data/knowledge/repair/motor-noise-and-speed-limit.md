# Motor Noise and Speed Limit Handling (Synthetic)

## Symptoms
- Periodic hub motor noise during acceleration;
- Dashboard shows speed limit, max speed capped at 15 km/h;
- Occasional "drive system protection" popup.

## Troubleshooting steps
1. Read fault codes: prioritize `MCU_OC_02` (over-current), `MCU_OT_01` (over-temperature).
2. Check rear wheel for debris wrap, abnormal bearing clearance.
3. Confirm recent water exposure or wading.
4. Verify OTA: some older versions falsely trigger speed limit on steep hills—suggest upgrade to v2.3.1+.

## Actions
- No fault code: tighten motor harness ground, road test 3 km and retest.
- Over-current code: create parts ticket; warehouse prioritizes same-batch controller/motor.
- When `TAG-safety-hazard` applies, do not close remotely by clearing codes only—schedule offline inspection.

## Agent forbidden phrases
- Do not promise "we can definitely fix it same day";
- Do not guide user to remove motor end cap themselves.
