# Range Anomaly Troubleshooting Guide (Qingshu Mobility · Synthetic Knowledge)

Applies to: E40 / E60 / E80 / S7 / S9 lithium series (synthetic doc, not a real service manual).

## 1. Symptom confirmation
1. Confirm with the user how they know the battery was fully charged (App SOC=100% or charger green light).
2. Confirm riding scenario: city only, long hills, two riders, low temperature (<5°C).
3. Record VIN (all Demo VINs start with QS0), OTA version, battery spec, and last deep charge/discharge time.

## 2. Quick triage
| Symptom | Likely cause | Frontline action |
|------|----------|----------|
| Full-charge range below ~50% of rated | BMS calibration drift / cell degradation | Pull SOH remotely; guide one deep charge/discharge calibration |
| Fast drop after climbing hills | Motor overload protection, low tire pressure | Check tire pressure 2.5–3.0 bar; query MCU over-current alerts |
| Very slow charging after 80% | Charger current limit or poor charging port contact | Try same-spec charger; inspect port for burn marks |
| Range cut in half in cold weather | Higher lithium internal resistance in cold | Explain physics; suggest indoor charging and warm-up before riding |

## 3. Standard scripts (quotable)
- "You reported range below rated—we'll do three steps first: confirm full-charge standard, verify OTA, and check battery health."
- "If SOH is below 80% and still under warranty, open an inspection ticket per the Qingshu warranty policy · battery volume."
- "Range drop in cold weather is a lithium battery physical trait, not necessarily a fault, but we'll help verify SOH."

## 4. Escalation criteria
- Same VIN calls in again ≥2 times within 30 days;
- Accompanied by battery temperature alert `BMS_OT_01`;
- User explicitly mentions media exposure intent → mark `TAG-reputation-risk` and escalate to specialist desk.

## 5. Shared-layer collaboration
- Fill-ticket Skill must write `tag_id` (e.g. `TAG-short-range`) and `sentiment` in `AIOutput`;
- If `TAG-open-complaint` also exists, renewal Planning Skill should block outreach after reading it.
