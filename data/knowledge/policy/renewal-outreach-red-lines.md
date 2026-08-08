# Smart Vehicle Connectivity Renewal Outreach Red Lines (Synthetic)

1. Users with tag `TAG-open-complaint` are **forbidden** from auto outbound calls and discount Push.
2. Outreach order: Push → SMS → AI call → human; max 3 combined channel touches per user per day.
3. Non-smart vehicles go to `non_smart` pool—product upgrade guidance only, not counted in renewal rate denominator.
4. Only high intent (`intent_level=high`) may transfer to human.
5. Must `read_ai_outputs` / read shared tags before outreach; do not rely on department-private lists alone.

## Story2 alignment
Planning Skill `renewal_plan` should return `allow_outreach=false` with block reason if open-complaint tag is found.
