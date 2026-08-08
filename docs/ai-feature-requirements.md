# AI Feature Requirements

> **Enterprise scenario**: Smart electric mobility (portfolio mapping: **Qingshu Mobility**)  
> **Source**: Internal material synthesis (AI system map, XMind roadmap, VoC, renewal funnel, BIS, channel activation, user ops, business flows, etc.)  
> **Scope**: Defines **what capabilities are needed**, not whether data is complete today  
> **Version**: V1.0 · 2026-08-01  
> **Purpose**: Portfolio demo feature map and basis for mounting **Skills**; **do not** expose real customer names in code or synthetic-data narratives as production deliverables

**Architecture (V2)**: Each feature maps to one or more platform **control loops** (Retrieve / Act / Extract / Plan), shared **tool classes** (Read / Knowledge / Write-Govern), and department **Skills**. See [Design decisions](./design-decisions.md), [Department flow diagrams](./planning/02-module-2-department-flow-diagrams.md), [Cross-department Act features](./react/01-module-1-background-cross-dept-features-tone.md), and [Standard field glossary](./standard-field-glossary.md).

**Loop legend**: Primary V2 loops are **Retrieve** (RAG), **Act** (multi-step tools), **Extract** (structured fields), **Plan** (orchestration / gates). **Rule+LLM** and **Vision** are extension sub-modes per DD-03, not separate platform loops.

---

## How to read this document

| Column | Meaning |
|--------|---------|
| Feature ID | Stable ID for Skill / CapabilityCatalog references |
| Feature name | Original material name or a reasonable merge |
| One-line purpose | Business outcome |
| Owning department | Primary owner (inferred entries marked in Notes) |
| Suggested loop(s) | V2 control loop + extension sub-modes |
| Linked reports / outputs | Report-style deliverables when applicable |
| Notes | Cross-dept reuse, inference, hard prerequisites, etc. |

---

## 1. Group governance / strategy

| Feature ID | Feature name | One-line purpose | Owning department | Suggested loop(s) | Linked reports / outputs | Notes |
|------------|--------------|------------------|-------------------|-------------------|--------------------------|-------|
| F-STR-001 | Smart query (Text2SQL + attribution) | Query metrics in natural language and return attribution | Strategy Committee / Executive Committee | Retrieve + Act | Executive cockpit input | Shared cross-dept foundation |
| F-STR-002 | Executive cockpit (weekly strategy brief + risk alerts) | Push periodic strategy summaries and risk signals to leadership | Strategy / Management | Plan + Rule+LLM | Executive cockpit · weekly strategy brief | |
| F-STR-003 | Strategy performance management (KPI breakdown) | Break group KPIs down to war zones and product lines | Strategy Committee | Plan | — | |
| F-STR-004 | War-zone sales / store openings / customer health rollup | Aggregate war-zone operating health for executive decisions | Strategy / Four Regional War Zones | Plan | Tier-1 dealer health index | |
| F-STR-005 | Brand strategy (social sentiment + competitor quarterly) | Inform brand strategy from sentiment and competitor moves | Strategy / Brand | Retrieve + Extract | Competitor industry report, sentiment dashboard | |
| F-STR-006 | Four-dimension risk & compliance alert | Quantitative alerts on compliance risk dimensions | Strategy / Legal & Audit | Rule+LLM | Risk alert dashboard | |
| F-STR-007 | Executive meeting AI summary | Draft must-discuss items, watch list, and closed-loop review | Management | Plan | VoC weekly/monthly report, resolution list | |

---

## 2. Data Research Institute / digital asset foundation

| Feature ID | Feature name | One-line purpose | Owning department | Suggested loop(s) | Linked reports / outputs | Notes |
|------------|--------------|------------------|-------------------|-------------------|--------------------------|-------|
| F-DAT-001 | Data governance (warehouse dimensions + unified dictionary) | Unify metric definitions for group-wide AI/BI | Data Research Institute | Rule+LLM | — | Cross-dept supply |
| F-DAT-002 | Metric semantic layer | Unified semantic layer for query and reporting | Data Research Institute | Retrieve | Smart query | Cross-dept |
| F-DAT-003 | Smart query (Text2SQL) | Let business users query data in natural language | Data Research Institute | Act | — | Cross-dept |
| F-DAT-004 | Supply chain collaboration (supplier risk + alternates) | Assess supplier risk and recommend alternatives | Data Research Institute / Supply Center | Plan + Rule+LLM | Partner risk report, stockout loss estimate | |
| F-DAT-005 | Budget & cash flow forecast (3–6 months) | Support finance on medium-term cash flow | Data Research Institute / Finance | Plan | Budget & cash flow forecast table | |
| F-DAT-006 | Channel wide table · matrix account monitoring | Aggregate channel and matrix-account data for analysis | Data Research Institute | Extract | Retail / matrix reports | |
| F-DAT-007 | Retail ops daily Excel automation | Replace manual export with automated retail daily report | Data Research Institute / Retail Ops | Plan | Retail ops daily data report | |
| F-DAT-008 | CV QC annotation dataset | Training/label data for manufacturing QC AI | Data Research Institute | Vision | — | |
| F-DAT-009 | Dealer self-service query foundation | Natural-language inventory/sales lookup for dealers | Data Research Institute | Act | — | Phase 4 |
| F-DAT-010 | Internal knowledge base (vectors + motor/battery graph) | Unified knowledge source for RAG/Q&A | Digital asset foundation | Retrieve | — | Cross-dept |
| F-DAT-011 | Repair knowledge base RAG Q&A | Support service/App repair Q&A | Digital asset foundation / Service | Retrieve | Q&A coverage report | Cross-dept |
| F-DAT-012 | Digital asset library structuring + RAG | Structure PDF/Word/video for retrieval | Digital asset foundation | Retrieve + Extract | — | Cross-dept |
| F-DAT-013 | Smart service foundation (ticket fill + assist + NLP) | Unified customer-service AI processing layer | Digital asset foundation / Service | Act + Extract | — | Cross-dept |
| F-DAT-014 | OneID user master data | Unified identity for segments, push, Q&A, campaigns | Data platform / IT | Rule+LLM | OneID coverage report | Cross-dept |

---

## 3. Procurement platform

| Feature ID | Feature name | One-line purpose | Owning department | Suggested loop(s) | Linked reports / outputs | Notes |
|------------|--------------|------------------|-------------------|-------------------|--------------------------|-------|
| F-PUR-001 | Procurement follow-up bot (overdue PO chase + logistics confirm) | Auto chase overdue POs and confirm logistics | Procurement platform | Act | — | |
| F-PUR-002 | Partner risk control (comprehensive assessment) | Assess supplier/partner risk | Procurement platform | Rule+LLM + Retrieve | Partner risk assessment report | |
| F-PUR-003 | Smart order tracking | Automate purchase-order follow-up | Procurement platform | Act | — | XMind “Fast” track |
| F-PUR-004 | Agent expediting | Multi-step reasoning to trigger procurement reminders | Procurement platform | Plan + Act | — | |

---

## 4. Manufacturing · PMC / planning

| Feature ID | Feature name | One-line purpose | Owning department | Suggested loop(s) | Linked reports / outputs | Notes |
|------------|--------------|------------------|-------------------|-------------------|--------------------------|-------|
| F-PMC-001 | Smart production scheduling (color pre-plan) | Pre-schedule by color and similar dims to cut stockouts/backlog | PMC | Plan + Rule+LLM | Package C color plan, stockout loss estimate | |

---

## 5. Manufacturing · production / quality / equipment

| Feature ID | Feature name | One-line purpose | Owning department | Suggested loop(s) | Linked reports / outputs | Notes |
|------------|--------------|------------------|-------------------|-------------------|--------------------------|-------|
| F-MFG-001 | BIS (OBD QC) | AI-assisted bench/OBD inspection with QC report | Manufacturing / Quality | Vision + Rule+LLM | OBD bench inspection report | |
| F-MFG-002 | OBD bench inspection · PDA frame binding | Collect line inspection data and bind traceability | Manufacturing / Quality | Extract | OBD bench report, traceability data pack | |
| F-MFG-003 | Optical spectrum QC | AI analysis for paint and optical QC | Quality | Vision | Optical QC report | |
| F-MFG-004 | Acoustic sensor anomaly alert | Predictive maintenance from acoustic anomalies | Equipment | Rule+LLM + Vision | Sensor maintenance alert | |
| F-MFG-005 | OBD/CV inspection | Computer vision for vehicle/process QC | Quality | Vision | Vehicle QC report | |
| F-MFG-006 | Release qualified units + traceability pack | Auto-generate traceability pack after QC pass | Quality | Extract | Traceability data pack | |

---

## 6. Supply center

| Feature ID | Feature name | One-line purpose | Owning department | Suggested loop(s) | Linked reports / outputs | Notes |
|------------|--------------|------------------|-------------------|-------------------|--------------------------|-------|
| F-SUP-001 | Supply chain collaboration (risk + alternates) | Recommend alternate supply when stockout/risk | Supply center | Plan + Rule+LLM | Partner risk, stockout loss estimate | Overlaps Data Research Institute |
| F-SUP-002 | Stockout loss estimate | Estimate sales loss from stockouts to drive replenishment | Supply / Channel | Rule+LLM | Stockout loss estimate report | Cross-dept (inferred) |

---

## 7. Brand ops platform / Brand Research Institute (incl. BIS)

| Feature ID | Feature name | One-line purpose | Owning department | Suggested loop(s) | Linked reports / outputs | Notes |
|------------|--------------|------------------|-------------------|-------------------|--------------------------|-------|
| F-BRD-001 | Brand asset AIGC pack | Batch-generate brand communication assets | Brand ops | Vision + Retrieve | Package D content | |
| F-BRD-002 | LoRA visual assets · sentiment SEIPR alert | Custom visuals plus early sentiment warning | Brand ops | Vision + Rule+LLM | Sentiment monitoring dashboard | |
| F-BRD-003 | AI video generation (KOS / e-commerce) | Short video for store associates / e-commerce | Brand ops | Vision | — | |
| F-BRD-004 | Brand video | AI-produced brand videos | Brand ops | Vision | — | |
| F-BRD-005 | Matrix account monitoring | Monitor matrix account content and performance | Brand / Retail | Extract | Store sell-through weekly · account module | |
| F-BRD-006 | Digital human | Digital avatar / broadcast | Brand ops | Vision | — | XMind single item |
| F-BRD-007 | GEO | Generative engine optimization workstream | Brand ops | Retrieve | — | XMind schedule |
| F-BRD-008 | BIS · NLP semantic analysis (MI) | Check message consistency across web, speeches, service | Brand Research Institute | Extract + Retrieve | MI baseline diagnosis report | |
| F-BRD-009 | BIS · omnichannel sentiment monitoring | 24/7 social and news sentiment | Brand / PR | Extract + Rule+LLM | Omnichannel sentiment dashboard | |
| F-BRD-010 | BIS · crisis early-warning system | Detect brand crises and draft response options | Brand / PR | Plan + Rule+LLM | Crisis early-warning report | |
| F-BRD-011 | BIS · AI-assisted design review | Auto-check VI compliance of marketing assets | Brand Research Institute | Vision | VI baseline diagnosis report | |
| F-BRD-012 | BIS · digital visual templates + AI VI compliance | Auto-review VI on short-video / e-commerce / live assets | Brand Research Institute | Vision | BI compliance report | |
| F-BRD-013 | BVP test plan + first test | Test candidate BVP recall, comprehension, purchase intent | Brand Research Institute | Extract | BVP first-test report | |
| F-BRD-014 | Corporate image diagnosis | Baseline vs desired image from sentiment + research | Brand Research Institute | Retrieve + Extract | Corporate image diagnosis report | |
| F-BRD-015 | App / mini-program experience audit | Score feature vs brand consistency | Brand Research Institute / Digital | Extract | App experience audit report | |
| F-BRD-016 | ESG report draft | Draft energy, emissions, CSR disclosure | Brand / Manufacturing | Plan | ESG report draft | |
| F-BRD-017 | Experience NPS real-time capture | Real-time NPS at key touchpoints + NLP | Brand Research Institute | Extract | Management cockpit | |

---

## 8. New retail division

| Feature ID | Feature name | One-line purpose | Owning department | Suggested loop(s) | Linked reports / outputs | Notes |
|------------|--------------|------------------|-------------------|-------------------|--------------------------|-------|
| F-RET-001 | Multi-platform service hub auto-reply | AI replies across shelf and interest e-commerce platforms | New retail | Act + Retrieve | — | |
| F-RET-002 | Online platform sales (smart service) | AI handles sales inquiries on e-commerce platforms | New retail | Act + Retrieve | — | |
| F-RET-003 | Retail reporting automation | Auto reports for sell-through, redemption, hot SKUs | New retail / Retail ops | Plan | Retail data reports, daily report | |

---

## 9. Operations platform (channel / terminal / orders / policy)

| Feature ID | Feature name | One-line purpose | Owning department | Suggested loop(s) | Linked reports / outputs | Notes |
|------------|--------------|------------------|-------------------|-------------------|--------------------------|-------|
| F-OPS-001 | Smart query + channel analysis report | Natural-language channel queries plus auto analysis report | Ops · Channel | Plan + Retrieve | Channel analysis report, Package A monthly | |
| F-OPS-002 | Channel analysis report (AI) | Auto report on attainment, rank, anomalies, actions | Channel | Plan | Channel analysis, big marketing analysis | |
| F-OPS-003 | Smart order create/review (Agent) | Review orders; suggest substitutes, stockouts, status | Orders / Policy | Act + Rule+LLM | Package C · pickup & policy tips | Cross war zone / PMC |
| F-OPS-004 | Sales policy parsing | Parse rebate tiers; generate pickup advice | Orders / Policy | Extract + Rule+LLM | Policy simulator, rebate settlement | |
| F-OPS-005 | Policy tier analysis · rebate settlement | Match policies and assist rebate settlement | Ops / Finance | Rule+LLM | Rebate settlement statement | |
| F-OPS-006 | Smart risk control (franchisees) | Risk assessment for new dealer onboarding | Ops · Risk control | Rule+LLM + Retrieve | Franchise risk report | Package E gate |
| F-OPS-007 | Store fit-out grade assessment | AI-assisted fit-out grading and support quota | Channel / Retail QC | Vision + Rule+LLM | Package E · store opening pack | |
| F-OPS-008 | Tier-1 dealer health index | Single health score from sales, compliance, complaints | Channel | Rule+LLM | Tier-1 dealer health index | Inferred |
| F-OPS-009 | Policy simulator | Simulate “move X units to tier Y for Z rebate” | Orders / Policy | Rule+LLM | Policy simulator report | |
| F-OPS-010 | Regional market battle map | County capacity × competitor penetration × store ROI | Channel / Rollup | Plan | Regional market battle map | Inferred |
| F-OPS-011 | Benchmark replication playbook | Extract repeatable actions from benchmark dealers | Channel / Retail | Extract + Plan | Benchmark replication report | |
| F-OPS-012 | Real-time alert notifications (Package B) | Push alerts on sales, compliance, stockout, complaints, competitors | Channel (+ others) | Rule+LLM | Package B · real-time alerts | |
| F-OPS-013 | Store opening pack (Package E) | Opening progress, grade, support quota, new dealer list | Channel | Plan | Package E · store opening pack | |
| F-OPS-014 | Channel assessment report | Comprehensive channel assessment output | Operations | Plan | Channel assessment report | Weak source fields |

---

## 10. Four regional war zones

| Feature ID | Feature name | One-line purpose | Owning department | Suggested loop(s) | Linked reports / outputs | Notes |
|------------|--------------|------------------|-------------------|-------------------|--------------------------|-------|
| F-WZ-001 | Offline RAG Q&A · KOS video · pickup tips | AI Q&A, content, and pickup hints for dealers/stores | Four Regional War Zones | Retrieve + Act | Packages C, D | |
| F-WZ-002 | Smart order review · policy tier analysis (war zone) | War-zone-side order and policy assistance | Four Regional War Zones | Act + Rule+LLM | Package C | |
| F-WZ-003 | Channel activation packs (A–E) localized delivery | AI reports reviewed by war zone before dealer delivery | Four Regional War Zones | Plan | Packages A–E | |
| F-WZ-004 | Associate productivity diagnosis | Find effective selling accounts; suggest improvements | War zone / Retail | Extract + Rule+LLM | Associate productivity report | Inferred |

---

## 11. Retail quality inspection

| Feature ID | Feature name | One-line purpose | Owning department | Suggested loop(s) | Linked reports / outputs | Notes |
|------------|--------------|------------------|-------------------|-------------------|--------------------------|-------|
| F-QC-001 | Non-exclusive store inspection (camera/CV) | Detect non-exclusive display, VI violations, etc. | Retail QC | Vision | Store inspection report | |
| F-QC-002 | Image diff · brand compliance flags | Compare morning/evening store panoramas for violations | Retail QC | Vision | Image diff flag report | |
| F-QC-003 | BIS · store AI image inspection | VI/poster/material/uniform compliance + rectification tickets | Retail QC / Brand | Vision | BI compliance report, inspection report | |

---

## 12. Service division (after-sales / hotline / smart service)

| Feature ID | Feature name | One-line purpose | Owning department | Suggested loop(s) | Linked reports / outputs | Notes |
|------------|--------------|------------------|-------------------|-------------------|--------------------------|-------|
| F-SVC-001 | Smart ticket fill | Dialog → draft work order | Service division | Extract + Act | Ticket data analysis report | |
| F-SVC-002 | Agent assist answers | Real-time scripts and knowledge for agents | Service division | Retrieve | — | |
| F-SVC-003 | Repair service bot | Dedicated AI for repair inquiries | Service division | Retrieve + Act | — | |
| F-SVC-004 | Repair knowledge base RAG Q&A | Self-service repair Q&A to reduce hotline load | Service / Foundation | Retrieve | Q&A coverage report | |
| F-SVC-005 | VoC fault clustering · prediction input | Cluster tickets for product/quality insight | Service division | Extract | VoC insight, fault ticket analysis | |
| F-SVC-006 | NLP clustering + smart fill (corpus loopback) | Cluster hotline/e-commerce corpus into VoC tag library | Service division | Extract | VoC tag library | Cross product/brand/quality |
| F-SVC-007 | Customer issue prediction | Predict fault/inquiry type from keywords | Service division | Extract | — | |
| F-SVC-008 | BIS · smart QA system (LLM) | Full SOP compliance on sales/service recordings | Service / Brand | Extract + Rule+LLM | Smart QA compliance report | |
| F-SVC-009 | BIS · Voice of Customer (VoC) system | Cluster feedback, top issues, risk alerts | Service / Brand | Extract | VoC report series | |
| F-SVC-010 | BIS · BI behavior analysis dashboard | Real-time consistency across touchpoints | Service / Brand | Rule+LLM | Management cockpit | |
| F-SVC-011 | Regional service & complaint report | Regional complaints, warranty, fault clusters | Service division | Plan | Regional service & complaint report | |

---

## 13. Product ops / product innovation / technology research

| Feature ID | Feature name | One-line purpose | Owning department | Suggested loop(s) | Linked reports / outputs | Notes |
|------------|--------------|------------------|-------------------|-------------------|--------------------------|-------|
| F-PRD-001 | Competitor industry intel report | Auto-collect competitor price, promos, reputation | Product ops | Extract + Retrieve | Competitor industry report, battle card | |
| F-PRD-002 | Competitor report → R&D insight input | Feed competitor intel into product innovation | Product ops → R&D | Retrieve | R&D insight report | |
| F-PRD-003 | Complaint–sales correlation alert | Cross-domain link of rising complaints and falling sales | Product ops | Rule+LLM | Complaint–sales correlation alert | Inferred |
| F-PRD-004 | R&D insight (patent clusters + tech maturity) | Patent and trend analysis for R&D direction | Product Innovation Institute | Retrieve + Extract | R&D insight report | |
| F-PRD-005 | Motor/battery knowledge graph | Structured tech knowledge for R&D/service retrieval | Technology Research Institute | Retrieve | — | Via foundation layer |

---

## 14. Finance & treasury

| Feature ID | Feature name | One-line purpose | Owning department | Suggested loop(s) | Linked reports / outputs | Notes |
|------------|--------------|------------------|-------------------|-------------------|--------------------------|-------|
| F-FIN-001 | Smart expense · three-way match | AI review of expense docs and variance detection | Finance | Extract + Rule+LLM | Three-way match variance report | |
| F-FIN-002 | Budget & cash flow forecast (3–6 months) | Finance forecasting support | Finance | Plan | Budget & cash flow forecast | |
| F-FIN-003 | Sales policy rebate settlement | Assist automated rebate calculation | Finance / Ops | Rule+LLM | Rebate settlement statement | |

---

## 15. HR platform

| Feature ID | Feature name | One-line purpose | Owning department | Suggested loop(s) | Linked reports / outputs | Notes |
|------------|--------------|------------------|-------------------|-------------------|--------------------------|-------|
| F-HR-001 | Employee AI assistant · policy Q&A · training coach | Policy RAG and training simulations | HR | Retrieve + Act | — | |
| F-HR-002 | Recruiting bot + job matching | Recruiting Q&A and role matching | HR | Retrieve + Extract | — | |
| F-HR-003 | Policy RAG (cross-dept line) | Structure HR policies for all departments | HR | Retrieve | — | Cross-dept |

---

## 16. Legal & audit center

| Feature ID | Feature name | One-line purpose | Owning department | Suggested loop(s) | Linked reports / outputs | Notes |
|------------|--------------|------------------|-------------------|-------------------|--------------------------|-------|
| F-LEG-001 | Smart contract review notes | AI pre-review of contract terms and risks | Legal & audit | Extract + Retrieve | — | |
| F-LEG-002 | Four-dimension risk & compliance alert | Quantitative compliance metric alerts | Legal & audit | Rule+LLM | Risk alert dashboard | |

---

## 17. Executive office

| Feature ID | Feature name | One-line purpose | Owning department | Suggested loop(s) | Linked reports / outputs | Notes |
|------------|--------------|------------------|-------------------|-------------------|--------------------------|-------|
| F-SEC-001 | Press release / speech draft generation | Draft official copy and speeches (human final review) | Executive office | Retrieve | — | Package D content supply; not auto-sent |

---

## 18. User ops / App / renewal

| Feature ID | Feature name | One-line purpose | Owning department | Suggested loop(s) | Linked reports / outputs | Notes |
|------------|--------------|------------------|-------------------|-------------------|--------------------------|-------|
| F-UO-001 | Renewal · AI outbound (bot first, human handoff) | Connected-vehicle renewal outreach; high intent → human | User ops | Act + Rule+LLM | Renewal ops scorecard | |
| F-UO-002 | Renewal · rule-based pool & tagging | Filter lists by expiry, activity, renewal page visit, etc. | User ops | Rule+LLM | Renewal funnel analysis | Phase 1: rules first |
| F-UO-003 | Renewal · channel escalation ladder | Push → SMS → AI call → human / WeCom auto-escalation | User ops | Rule+LLM + Plan | Outreach capability matrix | |
| F-UO-004 | Renewal · personalized outreach | App targeted offers and segment pop-ups | User ops | Rule+LLM | — | |
| F-UO-005 | Renewal · intent score (model) | Multi-feature intent score to rank outbound lists | User ops | Rule+LLM | Renewal funnel analysis | Phase 2 / data-led |
| F-UO-006 | Renewal · outbound QA loop | Auto intent tags, order write-back, scorecard | User ops | Extract + Rule+LLM | Renewal ops scorecard | |
| F-UO-007 | Renewal · AI task & copy assignment per user | Auto-assign tasks and copy in renewal flows | User ops | Plan | — | |
| F-UO-008 | Renewal · non-connected vehicle pool rules | Separate pool and outreach for non-smart vehicles | User ops | Rule+LLM | — | |
| F-UO-009 | User ops · smart Q&A MVP | In-app repair/usage Q&A to reduce hotline | User ops / App | Retrieve | Q&A coverage report | |
| F-UO-010 | User ops · RAG knowledge auto-update | Summarize new top questions and update KB | User ops | Extract + Retrieve | Q&A coverage report | |
| F-UO-011 | User ops · AI segmentation + strategy draft | RFM/IoT clustering → ops strategy draft | User ops | Extract + Plan | Segment size report | |
| F-UO-012 | User ops · campaign planning assistant | Input goal/audience/budget → 2–3 campaign options | User ops | Plan | Campaign performance benchmark | |
| F-UO-013 | User ops · AIGC copy / push | Personalized push and multi-variant campaign copy | User ops | Retrieve | — | |
| F-UO-014 | User ops · AI monthly report / anomaly alerts | Auto monthly on bind rate, MAU, activation, etc. | User ops | Plan + Rule+LLM | AI monthly / anomaly alert, activation baseline | |
| F-UO-015 | User ops · KOC identification | Find community KOCs for content/campaigns | User ops | Extract | KOC candidate pool | |
| F-UO-016 | User ops · AI content moderation | NLP + image filter for UGC violations | User ops | Extract + Vision | — | |
| F-UO-017 | User ops · proactive Agent outreach (P2) | Read-only IoT; proactive maintenance/battery reminders | User ops / IoT | Act + Plan | IoT availability report | |
| F-UO-018 | User ops · tag-driven journeys | Tag-triggered outreach journeys (sensitive → human approval) | User ops | Rule+LLM + Plan | Outreach capability matrix | |
| F-UO-019 | GreenBot unified smart service (Phase 2) | Unified App service / outbound / SMS agent | User ops / Service | Act + Retrieve | — | |
| F-UO-020 | Activation funnel analysis | Bind and feature conversion funnel with priorities | App product | Plan | Activation funnel report | |
| F-UO-021 | O2O conversion funnel analysis | Platform order → lead → store visit → bind | New retail / User ops | Plan | O2O conversion funnel | |

---

## 19. IoT / vehicle (inferred)

| Feature ID | Feature name | One-line purpose | Owning department | Suggested loop(s) | Linked reports / outputs | Notes |
|------------|--------------|------------------|-------------------|-------------------|--------------------------|-------|
| F-IOT-001 | IoT cross-check (alert edition) | Cross-check user complaints with vehicle alerts by VIN | IoT / Quality / VoC | Rule+LLM | Investigation lead pack | |
| F-IOT-002 | OTA version coarse correlation | Correlate OTA version with feedback/alert volume | IoT / Product | Rule+LLM | Model issue brief, investigation leads | |
| F-IOT-003 | Vehicle telemetry → proactive Agent | Mileage/battery health drives proactive service | IoT / User ops | Act | IoT availability report | |

---

## 20. VoC platform consumers

| Feature ID | Feature name | One-line purpose | Owning department | Suggested loop(s) | Linked reports / outputs | Notes |
|------------|--------------|------------------|-------------------|-------------------|--------------------------|-------|
| F-VOC-001 | Multi-channel ingest + speech-to-text | Unify hotline, community, satisfaction voices | After-sales / Service | Extract | — | |
| F-VOC-002 | Auto tagging + sentiment analysis | Structure raw voice for downstream insight | UX research / Ops | Extract | All VoC reports | **Hard req: ship with dashboard** |
| F-VOC-003 | Model–issue matrix | Full issue view by vehicle model for prioritization | Product / R&D | Plan | Model × issue brief | |
| F-VOC-004 | Issue ranking / trend monitoring | Top issues and worsening trends for exec meetings | Product / Quality / Service | Rule+LLM | Issue ranking / trends | |
| F-VOC-005 | Weak root-cause leads | Feedback × after-sales × IoT alerts → investigation leads | Quality / After-sales | Rule+LLM | Investigation lead pack | |
| F-VOC-006 | Vehicle improvement brief | Model × issue themed output | Product / R&D | Plan | Model / issue brief | |
| F-VOC-007 | Targeted survey AI decision | Recommend whether to run follow-up survey | UX research | Rule+LLM | — | |
| F-VOC-008 | Batch trace leads / after-sales fault analysis | Track concentrated faults; batch/supplier checks | Quality / Supply chain | Rule+LLM | Batch quality trace report | After fields complete |
| F-VOC-009 | Suspicious signal → quality escalation | Anomaly rules trigger cross-team investigation | Quality | Rule+LLM | Investigation lead pack | |
| F-VOC-010 | OTA/batch anomaly brief | Anomaly-triggered brief material (human approval) | Quality / PR | Plan | Major complaint brief pack | |
| F-VOC-011 | Suspicious signal notify + action advice | On-call response to negative clusters and recovery | After-sales / Service | Rule+LLM + Plan | Package B complaint alert | |
| F-VOC-012 | Low score / negative → callback task suggestion | Flag low-score users and suggest callbacks | After-sales | Rule+LLM | — | |
| F-VOC-013 | Internal sentiment monitoring | App community + hotline time-series watch | Brand / PR | Rule+LLM | Sentiment monitoring dashboard | |
| F-VOC-014 | Spike detection / sentiment hotspot brief | Theme/negative spike alerts and brief material | Brand / PR | Rule+LLM | Crisis alert, brief | |
| F-VOC-015 | Public sentiment weak monitoring | Official media, news, app stores, etc. | Brand / PR | Extract | Sentiment dashboard | Free public sources |
| F-VOC-016 | Auto weekly/monthly report | Periodic NPS, trends, sentiment events NLG summary | Brand / Management | Plan | VoC auto weekly/monthly | |
| F-VOC-017 | Sentiment map / dimension slices | Weak touchpoints by region/store/channel | Region / Store mgmt | Extract | Sentiment map | |
| F-VOC-018 | NPS / CSAT monitoring | Regional/store satisfaction tracking | Region / Store mgmt | Rule+LLM | Management cockpit | |
| F-VOC-019 | Channel store response governance | Role/region response rates and survey governance | Regional mgmt | Rule+LLM | Satisfaction survey analysis | |
| F-VOC-020 | Management cockpit | KPI + top issues + alerts on one screen | Management | Plan | Management cockpit | |
| F-VOC-021 | Themed closed-loop TopN + verification | Cross-dept top issues: ownership, fix, recurrence check | Management | Plan + Rule+LLM | Resolution list | |
| F-VOC-022 | VoC Agent scenario guide | Role-based “what to review this week” | All VoC users | Plan + Retrieve | — | |
| F-VOC-023 | Tag system build & correction | Issue class + sentiment required; human correction | UX research / Ops | Extract | — | See `data/vocab/tag_vocabulary.json` |
| F-VOC-024 | Survey AI assist (topics / follow-ups / dup detect) | Survey design and outreach optimization | UX research | Plan | — | |
| F-VOC-025 | Open-ended survey AI tagging | Auto-ingest and tag satisfaction open responses | UX research | Extract | Satisfaction survey analysis | |
| F-VOC-026 | Non-vehicle themed brief | App/hotline/after-sales blocks × issues | Digital / Service product | Plan | Non-vehicle brief | |
| F-VOC-027 | Competitor comparison report (VoC) | Competitor vs own issue feedback stats | Product / Brand | Plan | Competitor comparison report | Phase 2 |
| F-VOC-028 | Satisfaction survey analysis | Consumer/channel satisfaction and drivers of dissatisfaction | Data Research Institute / BUs | Plan | Satisfaction survey analysis report | |

---

## 21. IT / process management

| Feature ID | Feature name | One-line purpose | Owning department | Suggested loop(s) | Linked reports / outputs | Notes |
|------------|--------------|------------------|-------------------|-------------------|--------------------------|-------|
| F-IT-001 | AI redundancy detection | Find duplicate process steps | IT / Process | Extract | AI redundancy detection report | |
| F-IT-002 | AI root-cause diagnosis | Causal chain for process bottlenecks | IT / Process | Plan | Process root-cause report | |
| F-IT-003 | AI simulation sandbox | What-if for process redesign | IT / Process | Plan | Scenario comparison report | |
| F-IT-004 | AI auto placement | Auto-attach new projects to static process map | IT / Process | Rule+LLM | — | |
| F-IT-005 | Organizational memory (vector store + RAG) | Retrieve past decisions and optimization plans | IT / Process | Retrieve | — | |
| F-IT-006 | AI suggestion inbox | Permission-scoped L1/L2/L3 optimization proposals | IT / Process | Plan | — | |

---

## 22. Cross-department shared capabilities (separate list)

| Feature ID | Feature name | Departments involved | One-line purpose | Suggested loop(s) |
|------------|--------------|----------------------|------------------|-------------------|
| F-X-001 | Digital asset library foundation (RAG) | All | Unified structured knowledge; departments consume via RAG | Retrieve |
| F-X-002 | BI semantic layer + smart query | All | Unified query and auto reporting | Act + Retrieve |
| F-X-003 | VoC tag library (corpus loopback line) | Service → Product/Brand/Quality | Service corpus clustering feeds company-wide insight | Extract |
| F-X-004 | Agent order create/review | Ops → War zone/PMC | Multi-step suggestions on orders, scheduling, rebates | Act + Rule+LLM |
| F-X-005 | AIGC content production & distribution line | Brand → Retail/War zone/E-commerce | Video/assets → matrix/e-commerce → performance loopback | Vision + Plan |
| F-X-006 | Sales–production decision line (forecast + rules + Agent) | Mfg/inventory/orders → War zone/PMC/Finance | Scheduling, orders, rebate advice | Plan + Rule+LLM |
| F-X-007 | Quality inspection & prediction line | Mfg → Quality/Service | OBD/sensor/CV → QC reports/alerts/traceability | Vision + Rule+LLM |
| F-X-008 | OneID user master data | User ops/Service/App/store/e-commerce | Unified identity for segments, push, Q&A, campaigns | Rule+LLM |
| F-X-009 | Anti-AI-Silo shared Tool/DataFetcher | Full demo | Multiple loop types × Skills share tools and output layer | Architecture principle |

---

## 23. Report catalog (linked to features)

| Report ID | Report name | Primary owner | Main driving feature IDs |
|-----------|-------------|---------------|--------------------------|
| R-001 | Channel analysis report | Channel | F-OPS-001/002 |
| R-002 | Package A · channel ops monthly (external) | Channel | F-OPS-001, F-WZ-003 |
| R-003 | Package B · real-time alert notifications | Channel (+ others) | F-OPS-012 |
| R-004 | Package C · pickup & policy tips | Orders / Policy | F-OPS-003/004 |
| R-005 | Package D · retail enablement / store sell-through weekly | Retail ops | F-RET-003, F-BRD-005 |
| R-006 | Package E · store opening pack | Channel | F-OPS-013/007 |
| R-007 | Big marketing analysis report | Brand marketing rollup | F-OPS-002, etc. |
| R-008 | Retail ops daily / retail data report | Retail ops | F-DAT-007, F-RET-003 |
| R-009 | Competitor industry report / battle card | Product ops | F-PRD-001 |
| R-010 | Franchise risk report | Ops · Risk control | F-OPS-006 |
| R-011 | Store inspection report | Retail QC | F-QC-001/003 |
| R-012 | Image diff · brand compliance flag report | Retail QC | F-QC-002 |
| R-013 | Regional market battle map | Channel / Rollup | F-OPS-010 |
| R-014 | Stockout loss estimate report | Supply / Channel | F-SUP-002 |
| R-015 | Benchmark replication report | Channel / Retail | F-OPS-011 |
| R-016 | Associate productivity report | Retail / War zone | F-WZ-004 |
| R-017 | Policy simulator report | Orders / Policy | F-OPS-009 |
| R-018 | Tier-1 dealer health index | Channel | F-OPS-008 |
| R-019 | Sales policy rebate settlement | Finance / Ops | F-OPS-005, F-FIN-003 |
| R-020 | Regional service & complaint report | Service division | F-SVC-011 |
| R-021 | New retail & live commerce ops report | New retail | F-RET-003 |
| R-022 | Management cockpit (VoC) | Management | F-VOC-020 |
| R-023 | VoC auto weekly/monthly report | Brand / Management | F-VOC-016 |
| R-024 | Cockpit snapshot / resolution list | Management | F-STR-007, F-VOC-021 |
| R-025 | Model × issue brief | Product / R&D | F-VOC-003/006 |
| R-026 | Non-vehicle brief | Digital / Service product | F-VOC-026 |
| R-027 | Major complaint brief pack | Quality / PR | F-VOC-010 |
| R-028 | Competitor comparison report (VoC) | Product / Brand | F-VOC-027 |
| R-029 | Batch quality trace report | Quality / Supply chain | F-VOC-008 |
| R-030 | Investigation lead pack | Quality / After-sales | F-VOC-005/009 |
| R-031 | Issue ranking / sentiment map / trend monitoring | Multi-dept | F-VOC-004/017 |
| R-032 | Satisfaction survey analysis report | Data Research Institute, etc. | F-VOC-028 |
| R-033 | VoC insight report (BIS) | Brand / Service | F-SVC-009 |
| R-034 | Renewal funnel analysis report | User ops | F-UO-002/005 |
| R-035 | Connected App service half-year analysis | User ops | F-UO-001, etc. |
| R-036 | Renewal ops scorecard | User ops | F-UO-006 |
| R-037 | Registration / conversion report (overflow) | User ops | F-UO-004 |
| R-038 | Activation rate baseline dashboard | User ops / App | F-UO-014/020 |
| R-039 | OneID coverage report | IT / Data platform | F-DAT-014 |
| R-040 | Touchpoint heat map / channel concentration | Service / App | F-UO-021 related |
| R-041 | Activation funnel report | App product | F-UO-020 |
| R-042 | Q&A coverage report | Service / Service | F-UO-009/010 |
| R-043 | Segment size distribution report | User ops | F-UO-011 |
| R-044 | KOC candidate pool | Community ops | F-UO-015 |
| R-045 | Campaign performance benchmark | Marketing / Retail | F-UO-012 |
| R-046 | Outreach capability matrix | IT / Marketing | F-UO-003/018 |
| R-047 | O2O conversion funnel | New retail / E-commerce | F-UO-021 |
| R-048 | IoT availability report | IoT / Vehicle | F-IOT-003 |
| R-049 | AI monthly report / anomaly alert (user ops) | User ops | F-UO-014 |
| R-050 | MI baseline diagnosis report | Brand Research Institute | F-BRD-008 |
| R-051 | BVP first-test report | Brand Research Institute | F-BRD-013 |
| R-052 | VI baseline diagnosis report | Brand Research Institute | F-BRD-011 |
| R-053 | Corporate image diagnosis report | Brand / PR | F-BRD-014 |
| R-054 | App / mini-program experience audit report | Brand / Digital | F-BRD-015 |
| R-055 | Omnichannel sentiment monitoring dashboard | Brand / PR | F-BRD-009 |
| R-056 | Crisis early-warning report | Brand / PR | F-BRD-010 |
| R-057 | ESG report draft | Brand / Manufacturing | F-BRD-016 |
| R-058 | Four-region ticket analysis report | Service / BI | F-SVC-005 |
| R-059 | Ticket data analysis report | Smart service | F-SVC-001 |
| R-060 | Vehicle fault ticket analysis report | Smart service | F-SVC-005 |
| R-061 | Hotline call analysis report | Smart service | F-SVC-007 |
| R-062 | Smart QA compliance report (recordings) | Service / Brand | F-SVC-008 |
| R-063 | OBD bench inspection report | Manufacturing / Quality | F-MFG-001/002 |
| R-064 | Vehicle QC report / traceability data pack | Manufacturing / Quality | F-MFG-005/006 |
| R-065 | Optical QC report | Quality | F-MFG-003 |
| R-066 | Sensor maintenance / acoustic anomaly alert | Equipment | F-MFG-004 |
| R-067 | Partner risk assessment report | Procurement | F-PUR-002 |
| R-068 | R&D insight report | R&D | F-PRD-004 |
| R-069 | Three-way match variance report | Finance | F-FIN-001 |
| R-070 | Budget & cash flow forecast | Finance | F-FIN-002 |
| R-071 | Executive cockpit · weekly strategy brief | Strategy | F-STR-002 |
| R-072 | Complaint–sales correlation alert | Product ops | F-PRD-003 |
| R-073 | AI redundancy / scenario comparison / process root-cause reports | IT / Process | F-IT-001/002/003 |

---

## Appendix: XMind seven-branch mapping summary

| Branch | Representative items | Main feature ID prefixes |
|--------|---------------------|--------------------------|
| Fast | Non-exclusive store inspection, smart order tracking, franchise risk control | F-QC, F-PUR, F-OPS-006 |
| Smart customer service | Smart ticket fill, agent assist, repair bot, recruiting bot, etc. | F-SVC, F-HR-002 |
| AI smart reports | Channel analysis, retail reports, competitor intel, press drafts, smart scheduling | F-OPS, F-RET, F-PRD, F-SEC, F-PMC |
| Smart manufacturing | OBD/BIS, sensors, optical QC | F-MFG |
| Video AI production & distribution | AI video, brand video, matrix monitoring | F-BRD |
| Standalone items | Policy parsing, digital human, GEO, fit-out grading, order review | F-OPS, F-BRD |
| Digital asset tuning | Internal KB, repair KB, data governance | F-DAT |

---

## Revision history

| Version | Date | Notes |
|---------|------|-------|
| V1.0 | 2026-08-01 | Initial release: full feature set + report mapping for demo modeling |
