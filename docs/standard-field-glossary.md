# Standard Field Glossary

> **Scope**: Regardless of who uses the data — a unified data dictionary generalized from AI features and report fields
> **Enterprise context**: Smart electric two-wheel mobility (portfolio: Qingshu Mobility)
> **Version**: V1.0 · 2026-08-01
> **Companion**: `standard-field-glossary.csv` in the same directory (importable for modeling); see `ai-feature-requirements.md` for feature-side requirements
> **Implementation mapping**: Priority entities in `shared/models` are Customer / Vehicle / Ticket / Order / TagVocabulary / AIOutput; remaining fields are extension attributes or report views

---

## 0. Usage Rules

| Rule | Description |
|------|-------------|
| Department-neutral | Fields belong to data domains/entities, not departments |
| One meaning, one name | Each business meaning maps to a single `field_name` (e.g., sales volume is always `sales_qty`) |
| Industry-meaningful examples | `example` values reflect smart e-bike scenarios for synthetic data |
| Report reuse | `related_reports` is for traceability only, not an authorization model |
| Demo minimum core | Entities marked ★ are prioritized for Pydantic models |

## 1. Entity Overview (★ = Demo Phase 1 priority)

| Data Domain | Entity | Description | Priority |
|-------------|--------|-------------|----------|
| Metadata | ReportMeta | Report instance metadata | P1 |
| Organization | Org / Region | Organization tree and administrative regions | P0 |
| Channel Master Data | Dealer / Store / Guide | Dealers, stores, sales guides | P0 |
| Customer & User ★ | Customer / UserBehavior / Renewal | Customers, behavior, renewal pool | P0 |
| Vehicle ★ | Vehicle | VIN/model/color/OTA/smart vehicle | P0 |
| Product SKU | SKU / Competitor | SKUs and competitors | P1 |
| Sales Targets | SalesMetric / Health | Sales, contract achievement, health index | P1 |
| Channel Development | StoreDev / Risk | Store opening and risk control | P2 |
| Order, Inventory & Policy ★ | Order / Inventory / Policy / ColorPlan | Orders, inventory, rebates, production planning | P0 |
| Retail & Marketing | Retail / Campaign / Content / Outreach | Retail, campaigns, content, outreach | P1 |
| Service Tickets ★ | Ticket / VoC | Tickets and VoC tags/sentiment | P0 |
| Connected Vehicle IoT | Telemetry | Mileage, battery, fault codes | P1 |
| Manufacturing Quality | Quality | OBD/optical/traceability | P2 |
| Inspection & Compliance | Inspection / Brand | Inspection images and brand sentiment | P2 |
| Finance | Finance | Three-way match and cash flow forecast | P2 |
| App Activation | Activation / O2O | Activation funnel and O2O | P1 |
| Alerts & Collaboration | Alert / Collab | Alerts and cross-department closed loops | P1 |
| Shared AI Assets ★ | AIOutput / TagVocabulary / CapabilityCatalog / RunLog | Explicit anti-silo layer | P0 |
| Process, HR & Legal | Process / HR / Legal / Knowledge | Processes, roles, contracts, knowledge base | P2 |

## 2. Field Details (400 total)

### Metadata

| Field ID | Entity | Field Name | Display Name | Type | Unit | Example | Description | Related Reports (trace) |
|----------|--------|------------|--------------|------|------|---------|-------------|---------------------------|
| SF-0001 | ReportMeta | `report_id` | Report ID | string | - | CH-RPT-2026-07-EAST | Unique identifier for a single report instance | All reports |
| SF-0002 | ReportMeta | `report_type` | Report Type | enum | - | channel_analysis | Report type code | All reports |
| SF-0003 | ReportMeta | `period` | Reporting Period | string | - | 2026-07 | Month/week/day/custom interval | All reports |
| SF-0004 | ReportMeta | `period_type` | Period Type | enum | - | month | Period granularity | All reports |
| SF-0005 | ReportMeta | `period_start` | Period Start | date | - | 2026-07-01 | Statistics start date | All reports |
| SF-0006 | ReportMeta | `period_end` | Period End | date | - | 2026-07-31 | Statistics end date | All reports |
| SF-0007 | ReportMeta | `generated_at` | Generated At | datetime | - | 2026-08-01T10:00:00+08:00 | Report generation timestamp | All reports |
| SF-0008 | ReportMeta | `data_as_of` | Data As Of | datetime | - | 2026-07-31T23:59:59+08:00 | Data cutoff timestamp | All reports |
| SF-0009 | ReportMeta | `run_id` | Run ID | string | - | run_abc123 | Agent/pipeline run identifier | All reports |
| SF-0010 | ReportMeta | `producer_skill` | Producer Skill | string | - | channel_analysis | Producer skill that writes to the shared layer | AI outputs |
| SF-0011 | ReportMeta | `traffic_light` | Traffic Light | enum | - | yellow | Red/yellow/green status indicator | Channel / alert reports |
| SF-0012 | ReportMeta | `narrative_summary` | NLG Summary | text | - | East region pickup achievement 83%; color stockout is the top anomaly driver | Natural-language summary | Weekly-monthly reports / dashboard |
| SF-0013 | ReportMeta | `action_suggestions` | Action Suggestions | json | - | ["Replenish color production","Push for gold tier"] | Structured list of recommended actions | Channel / VoC / operations |

### Organization

| Field ID | Entity | Field Name | Display Name | Type | Unit | Example | Description | Related Reports (trace) |
|----------|--------|------------|--------------|------|------|---------|-------------|---------------------------|
| SF-0014 | Org | `org_id` | Organization ID | string | - | WZ-EAST | Unique organization node identifier | Channel / warzone reports |
| SF-0015 | Org | `org_name` | Organization Name | string | - | East Warzone | Organization display name | Channel / warzone reports |
| SF-0016 | Org | `org_level` | Organization Level | enum | - | warzone | Hierarchy level in the org tree | All business reports |
| SF-0017 | Org | `parent_org_id` | Parent Organization ID | string | - | NATION-CN | Parent node in the organization tree | All business reports |
| SF-0018 | Org | `org_path` | Organization Path | string | - | National/East/Jiangsu South/Tier1-A | Full hierarchical path | All business reports |
| SF-0019 | Region | `province` | Province | string | - | Jiangsu | Administrative region — province | Renewal / VoC / channel |
| SF-0020 | Region | `city` | City | string | - | Nanjing | Administrative region — city | Renewal / VoC / channel |
| SF-0021 | Region | `county_code` | County Code | string | - | 320115 | National standard county/district code | Battle map / store opening |
| SF-0022 | Region | `county_name` | County Name | string | - | Jiangning District | County/district name | Battle map / store opening |

### Channel Master Data

| Field ID | Entity | Field Name | Display Name | Type | Unit | Example | Description | Related Reports (trace) |
|----------|--------|------------|--------------|------|------|---------|-------------|---------------------------|
| SF-0023 | Dealer | `dealer_id` | Tier-1 / Dealer ID | string | - | DLR-3201 | Unique dealer identifier | Pack A / C / E |
| SF-0024 | Dealer | `dealer_name` | Dealer Name | string | - | Qingshu Nanjing Jiangning Tier-1 Network | Dealer name | Pack A / C / E |
| SF-0025 | Dealer | `legal_person` | Legal Representative | string | - | Wang XX | Registered legal person | Risk control / franchise |
| SF-0026 | Dealer | `open_account_date` | Account Opening Date | date | - | 2024-03-12 | Dealer account opening date | Pack E |
| SF-0027 | Dealer | `developer_name` | Developer Name | string | - | Li Kaifa | Channel development owner | Pack E |
| SF-0028 | Store | `store_id` | Store ID | string | - | ST-8891 | Unique store identifier | Retail / inspection / Pack D |
| SF-0029 | Store | `store_name` | Store Name | string | - | Qingshu Nanjing Jiangning Flagship Store | Store name | Retail / inspection |
| SF-0030 | Store | `store_address` | Store Address | string | - | No. 88 XX Road, Dongshan Subdistrict, Jiangning District | Full street address | Store opening / inspection |
| SF-0031 | Store | `store_type` | Store Type | enum | - | exclusive | Store format type | Compliance / retail |
| SF-0032 | Store | `store_grade` | Store Grade | enum | - | A | Store grade rating | Fit-out grading / Pack E |
| SF-0033 | Store | `store_area_sqm` | Store Area | number | sqm | 120 | Floor area of the store | Fit-out grading |
| SF-0034 | Store | `biz_district` | Business District | string | - | Dongshan Trade Area | Trade area for store-opening Gantt | Pack E |
| SF-0035 | Guide | `guide_id` | Sales Guide ID | string | - | GD-1022 | Sales guide staff identifier | Staff productivity diagnostics |
| SF-0036 | Guide | `channel_account_id` | Social Account ID | string | - | DY-991 | Douyin/Channels etc. account ID | Social matrix / productivity |

### Customer & User

| Field ID | Entity | Field Name | Display Name | Type | Unit | Example | Description | Related Reports (trace) |
|----------|--------|------------|--------------|------|------|---------|-------------|---------------------------|
| SF-0037 | Customer | `customer_id` | Customer ID | string | - | CUS-10086 | Unified customer master data ID | Renewal / service / operations |
| SF-0038 | Customer | `phone_masked` | Phone (Masked) | string | - | 138****5678 | Masked mobile phone number | OneID / outreach |
| SF-0039 | Customer | `openid` | OpenID | string | - | oxxx | WeChat OpenID | OneID |
| SF-0040 | Customer | `unionid` | UnionID | string | - | uxxx | WeChat UnionID | OneID |
| SF-0041 | Customer | `identity_type` | Identity Type | enum | - | end_user | User identity category | Ticket analysis |
| SF-0042 | Customer | `oneid` | OneID | string | - | OID-9f3a | Cross-system unified identity | OneID report |
| SF-0043 | Customer | `oneid_match_method` | OneID Match Method | enum | - | phone | Identity resolution method | OneID report |
| SF-0044 | UserBehavior | `app_register_flag` | App Registered Flag | boolean | - | true | Whether the user registered in the app | Activation rate |
| SF-0045 | UserBehavior | `bind_vehicle_flag` | Vehicle Bound Flag | boolean | - | true | Whether vehicle binding is complete | Activation rate / funnel |
| SF-0046 | UserBehavior | `last_active_at` | Last Active At | datetime | - | 2026-07-20T21:00:00+08:00 | Last app/connected-vehicle activity time | Renewal / segmentation |
| SF-0047 | UserBehavior | `active_days_30d` | Active Days (30d) | int | days | 12 | Active days in the last 30 days | Renewal / segmentation |
| SF-0048 | UserBehavior | `mau_flag` | MAU Flag | boolean | - | true | Whether counted as MAU in the calendar month | Activation rate / monthly report |
| SF-0049 | UserBehavior | `dau_flag` | DAU Flag | boolean | - | false | Whether counted as DAU for the day | Activation rate |
| SF-0050 | UserBehavior | `rfm_segment` | RFM Segment | enum | - | high_value | RFM customer segment | Segmentation report |
| SF-0051 | UserBehavior | `r_days` | R Value (Days Since Last Activity) | int | days | 18 | Recency — days since last activity | Segmentation report |
| SF-0052 | UserBehavior | `f_month` | F Value (Monthly Interactions) | int | times | 7 | Frequency — monthly interaction count | Segmentation report |
| SF-0053 | UserBehavior | `m_value` | M Value (Value Contribution) | number | CNY | 860 | Monetary value — parts/service spend etc. | Segmentation report |
| SF-0054 | UserBehavior | `first_touch_channel` | First Touch Channel | string | - | 400 | First contact channel | Touchpoint heatmap |
| SF-0055 | UserBehavior | `last_touch_channel` | Last Touch Channel | string | - | App | Most recent contact channel | Touchpoint heatmap |
| SF-0056 | Renewal | `service_expire_date` | Service Expiry Date | date | - | 2026-08-15 | Connected-vehicle service expiry date | Renewal funnel |
| SF-0057 | Renewal | `due_renew_flag` | Due Renew Flag | boolean | - | true | Whether due for renewal pool entry | Renewal funnel |
| SF-0058 | Renewal | `paid_flag` | Paid Flag | boolean | - | false | Whether payment occurred (distinguish new vs renewal) | Renewal funnel |
| SF-0059 | Renewal | `paid_type` | Paid Type | enum | - | renew | Payment type | Renewal funnel |
| SF-0060 | Renewal | `active_t30_flag` | Active T-30 Flag | boolean | - | true | Active within 30 days before expiry | Renewal funnel |
| SF-0061 | Renewal | `active_t7_flag` | Active T-7 Flag | boolean | - | false | Active within 7 days before expiry | Renewal funnel |
| SF-0062 | Renewal | `sleep_90d_app_flag` | App Sleep 90d Flag | boolean | - | true | No app usage in the last 90 days | Renewal funnel |
| SF-0063 | Renewal | `active_90d_4g_flag` | 4G Active 90d Flag | boolean | - | true | 4G vehicle with connectivity in last 90 days | Renewal funnel |
| SF-0064 | Renewal | `renew_intent_score` | Renew Intent Score | number | 0-1 | 0.78 | Model/rule-based renewal intent score | Renewal scorecard |
| SF-0065 | Renewal | `renew_pool_layer` | Renew Pool Layer | enum | - | T-30 | Renewal pool tier | Renewal pool scrubbing |
| SF-0066 | Renewal | `outreach_channel` | Outreach Channel | enum | - | ai_call | Outreach channel used | Outreach matrix |
| SF-0067 | Renewal | `intent_level` | Call Intent Level | enum | - | high | Outbound call intent level | Renewal scorecard |

### Vehicle

| Field ID | Entity | Field Name | Display Name | Type | Unit | Example | Description | Related Reports (trace) |
|----------|--------|------------|--------------|------|------|---------|-------------|---------------------------|
| SF-0068 | Vehicle | `vin` | VIN | string | - | LQXXXX2026A0001 | Vehicle identification number | Quality / VoC / IoT |
| SF-0069 | Vehicle | `frame_no` | Frame Part No. | string | - | FR-778812 | Frame component number for PDA binding | OBD / traceability |
| SF-0070 | Vehicle | `sn` | Serial Number | string | - | SN-202607-8891 | Production line serial number | Quality inspection |
| SF-0071 | Vehicle | `vehicle_model` | Vehicle Model | string | - | E60 | Model code/name | Nearly all reports |
| SF-0072 | Vehicle | `vehicle_config` | Configuration Type | string | - | Lithium flagship trim | Trim/configuration tier | Fault analysis |
| SF-0073 | Vehicle | `color` | Color | string | - | Matte black | Body color | Production planning / stockout / retail |
| SF-0074 | Vehicle | `battery_type` | Battery Type | enum | - | lithium | Battery chemistry/type | Competitive / product |
| SF-0075 | Vehicle | `battery_spec` | Battery Spec | string | - | 48V24Ah | Voltage and amp-hour specification | Competitive / service |
| SF-0076 | Vehicle | `claimed_range_km` | Claimed Range | number | km | 80 | Official rated range | Competitive / product |
| SF-0077 | Vehicle | `purchase_date` | Purchase Date | date | - | 2025-08-01 | Customer purchase date | Activation rate breakdown |
| SF-0078 | Vehicle | `purchase_year` | Purchase Year | int | year | 2025 | Year of purchase | Activation rate |
| SF-0079 | Vehicle | `is_smart_vehicle` | Smart Vehicle Flag | boolean | - | true | Whether vehicle has 4G/connectivity | Renewal pool |
| SF-0080 | Vehicle | `plant` | Manufacturing Plant | string | - | East China Plant 1 | Production plant/site | Fault / quality |
| SF-0081 | Vehicle | `line_id` | Production Line ID | string | - | LINE-03 | Production line identifier | OBD |
| SF-0082 | Vehicle | `batch_no` | Production Batch No. | string | - | BATCH-2026W28-E60 | Vehicle production batch | Traceability / VoC |
| SF-0083 | Vehicle | `ota_version` | OTA Version | string | - | v2.3.1 | On-vehicle software version | IoT / VoC |

### Product SKU

| Field ID | Entity | Field Name | Display Name | Type | Unit | Example | Description | Related Reports (trace) |
|----------|--------|------------|--------------|------|------|---------|-------------|---------------------------|
| SF-0084 | SKU | `sku_id` | SKU ID | string | - | SKU-E60-BK | Unique SKU identifier | Order / retail / inventory |
| SF-0085 | SKU | `sku_name` | SKU Name | string | - | E60 Matte Black | SKU display name | Order / retail |
| SF-0086 | SKU | `asp_cny` | Average Selling Price (ASP) | number | CNY | 3299 | Average unit selling price | Stockout loss / retail |
| SF-0087 | SKU | `hot_slow_flag` | Hot/Slow Flag | enum | - | hot | Hot/normal/slow mover tag | Sell-through weekly report |
| SF-0088 | SKU | `substitute_sku_id` | Substitute SKU | string | - | SKU-E60-GY | Substitute SKU mapping for stockouts | Order audit / Pack C |
| SF-0089 | Competitor | `competitor_brand` | Competitor Brand | string | - | Yadea | Competitor brand name | Competitive intelligence report |
| SF-0090 | Competitor | `competitor_model` | Competitor Model | string | - | Guan Neng XX | Competitor model name | Competitive intelligence report |
| SF-0091 | Competitor | `competitor_price_cny` | Competitor Price | number | CNY | 3699 | Competitor list/promo price | Competitive intelligence report |
| SF-0092 | Competitor | `competitor_share` | Competitor Regional Share | number | % | 28.0 | Competitor regional market share | Battle map |
| SF-0093 | Competitor | `competitor_share_pp_change` | Share Change (pp) | number | pp | -1.2 | Period-over-period share change in percentage points | Competitive / battle map |
| SF-0094 | Competitor | `promo_type` | Promotion Type | string | - | Trade-in promotion | Promotion activity type | Competitive intelligence report |
| SF-0095 | Competitor | `promo_region` | Promotion Region | string | - | Jiangsu-Anhui | Promotion activity region | Competitive intelligence report |
| SF-0096 | Competitor | `promo_window` | Promotion Window | string | - | 2026-07-01~07-31 | Promotion time window | Competitive intelligence report |
| SF-0097 | Competitor | `price_cut_amt` | Price Cut Amount | number | CNY | 300 | Price reduction amount | Competitive alert |
| SF-0098 | Competitor | `sentiment_score` | Sentiment Score | number | 0-1 | 0.62 | Competitor reputation score | Competitive intelligence report |
| SF-0099 | Competitor | `launch_date` | Launch Date | date | - | 2026-06-18 | Competitor launch date | Competitive intelligence report |

### Sales Targets

| Field ID | Entity | Field Name | Display Name | Type | Unit | Example | Description | Related Reports (trace) |
|----------|--------|------------|--------------|------|------|---------|-------------|---------------------------|
| SF-0100 | SalesMetric | `sales_qty` | Pickup / Sales Quantity | int | units | 12480 | Pickup-based sales volume in units | Channel analysis |
| SF-0101 | SalesMetric | `sales_target_qty` | Sales Target Quantity | int | units | 15000 | Sales target in units | Channel analysis |
| SF-0102 | SalesMetric | `sales_achieve_rate` | Sales Achievement Rate | number | % | 83.2 | Sales vs target | Channel analysis |
| SF-0103 | SalesMetric | `contract_qty` | Contract Quantity | int | units | 11200 | Signed contract volume in units | Channel analysis |
| SF-0104 | SalesMetric | `contract_target_qty` | Contract Target Quantity | int | units | 13000 | Contract target in units | Channel analysis |
| SF-0105 | SalesMetric | `contract_achieve_rate` | Contract Achievement Rate | number | % | 86.2 | Contract vs target | Channel analysis |
| SF-0106 | SalesMetric | `yoy_sales_qty` | YoY Sales Quantity | int | units | 10900 | Same period last year sales volume | Channel analysis |
| SF-0107 | SalesMetric | `yoy_rate` | YoY Growth Rate | number | % | 14.5 | Year-over-year growth | Channel analysis |
| SF-0108 | SalesMetric | `mom_sales_qty` | MoM Sales Quantity | int | units | 13100 | Prior month sales volume | Channel / alerts |
| SF-0109 | SalesMetric | `mom_rate` | MoM Growth Rate | number | % | -4.7 | Month-over-month growth | Channel / alerts |
| SF-0110 | SalesMetric | `rank_warzone` | Warzone Rank | int | - | 2 | Rank within major warzone | Channel analysis |
| SF-0111 | SalesMetric | `rank_subzone` | Subzone Rank | int | - | 5 | Rank within sub-warzone | Channel analysis |
| SF-0112 | SalesMetric | `rank_dealer` | Tier-1 Dealer Rank | int | - | 18 | Tier-1 dealer rank | Pack A |
| SF-0113 | SalesMetric | `full_achieve_outlet_cnt` | 100% Achievement Outlet Count | int | count | 86 | Outlets at 100% target | Outlet health |
| SF-0114 | SalesMetric | `full_achieve_outlet_ratio` | 100% Achievement Outlet Ratio | number | % | 41.3 | Share of outlets at 100% target | Outlet health |
| SF-0115 | SalesMetric | `abnormal_outlet_cnt` | Abnormal Outlet Count | int | count | 23 | Count of abnormal outlets | Pack B |
| SF-0116 | SalesMetric | `abnormal_outlet_ratio` | Abnormal Outlet Ratio | number | % | 11.1 | Share of abnormal outlets | Pack B |
| SF-0117 | SalesMetric | `abnormal_reason` | Abnormal Reason | string | - | Color stockout | Root cause of abnormality | Pack B |
| SF-0118 | SalesMetric | `abnormal_reason_cnt` | Abnormal Reason Count | int | times | 9 | Occurrence count for this reason | Pack B |
| SF-0119 | SalesMetric | `core_market_gap_to_top3` | Core Market Gap to Top 3 | int | units | 1260 | Gap vs regional #1 in core markets | Channel analysis |
| SF-0120 | SalesMetric | `online_sales_qty` | Online Sales Quantity | int | units | 860 | E-commerce/live-stream sales volume | New retail / Pack A |
| SF-0121 | Health | `health_index` | Business Health Index | number | 0-100 | 72 | Composite tier-1 dealer health score | Health index |
| SF-0122 | Health | `sales_score` | Sales Score | number | 0-100 | 75 | Health index sub-score — sales | Health index |
| SF-0123 | Health | `retail_score` | Retail Score | number | 0-100 | 68 | Health index sub-score — retail | Health index |
| SF-0124 | Health | `compliance_score` | Compliance Score | number | 0-100 | 80 | Health index sub-score — compliance | Health index |
| SF-0125 | Health | `complaint_score` | Complaint Score | number | 0-100 | 70 | Health index sub-score — complaints | Health index |
| SF-0126 | Health | `inventory_turn_score` | Inventory Turn Score | number | 0-100 | 65 | Health index sub-score — inventory turnover | Health index |

### Channel Development

| Field ID | Entity | Field Name | Display Name | Type | Unit | Example | Description | Related Reports (trace) |
|----------|--------|------------|--------------|------|------|---------|-------------|---------------------------|
| SF-0127 | StoreDev | `blank_l1_plan_cnt` | Blank Tier-1 Plan Count | int | count | 18 | Planned blank tier-1 network openings | Pack E |
| SF-0128 | StoreDev | `blank_l1_opened_cnt` | Blank Tier-1 Opened Count | int | count | 11 | Opened blank tier-1 networks | Pack E |
| SF-0129 | StoreDev | `blank_l1_achieve_rate` | Blank Tier-1 Achievement Rate | number | % | 61.1 | Opened vs planned blank tier-1 | Pack E |
| SF-0130 | StoreDev | `store_dev_plan_cnt` | Store Development Plan Count | int | count | 120 | Annual store development plan count | Pack E |
| SF-0131 | StoreDev | `store_dev_done_cnt` | Store Development Done Count | int | count | 74 | Cumulative completed store openings | Pack E |
| SF-0132 | StoreDev | `store_dev_rate` | Store Development Rate | number | % | 61.7 | Completion vs plan | Pack E |
| SF-0133 | StoreDev | `market_capacity_annual` | Annual County Market Capacity | int | units | 42000 | Annual two-wheel EV market capacity in county | Battle map |
| SF-0134 | StoreDev | `self_coverage_flag` | Own Brand Coverage Flag | enum | - | blank | Own-brand coverage marker | Battle map |
| SF-0135 | StoreDev | `open_roi_months` | Store Opening ROI (Months) | number | months | 14 | Predicted payback period in months | Battle map / Pack E |
| SF-0136 | StoreDev | `support_quota_total_wan` | Support Quota Total | number | 10k CNY | 15 | Total store-opening support quota | Pack E |
| SF-0137 | StoreDev | `support_quota_applied_wan` | Support Quota Applied | number | 10k CNY | 8 | Applied support quota | Pack E |
| SF-0138 | StoreDev | `support_quota_remain_wan` | Support Quota Remaining | number | 10k CNY | 7 | Remaining support quota | Pack E |
| SF-0139 | StoreDev | `first_order_qty` | First Order Quantity | int | units | 80 | New dealer first batch pickup volume | Pack E |
| SF-0140 | StoreDev | `m1_m3_order_qty` | M1-M3 Order Quantity | int | units | 210 | New dealer pickup in months 1–3 | Pack E |
| SF-0141 | StoreDev | `gantt_owner` | Store Opening Owner | string | - | Zhang San | Store-opening Gantt owner | Pack E |
| SF-0142 | StoreDev | `gantt_start` | Store Opening Start Date | date | - | 2026-07-01 | Gantt start date | Pack E |
| SF-0143 | StoreDev | `gantt_end` | Store Opening End Date | date | - | 2026-09-15 | Gantt end date | Pack E |
| SF-0144 | StoreDev | `fitout_suggest_grade` | Fit-out Suggested Grade | enum | - | B | Recommended fit-out grade | Pack E |
| SF-0145 | Risk | `credit_code` | Unified Social Credit Code | string | - | 9132XXXXXXXX | Business registration code | Franchise / partner risk control |
| SF-0146 | Risk | `reg_capital_wan` | Registered Capital | number | 10k CNY | 500 | Registered capital | Risk control |
| SF-0147 | Risk | `lawsuit_cnt_3y` | Lawsuit Count (3y) | int | cases | 2 | Litigation count in last 3 years | Risk control |
| SF-0148 | Risk | `dishonest_flag` | Dishonest Flag | boolean | - | false | Whether on dishonesty enforcement list | Risk control |
| SF-0149 | Risk | `negative_news_cnt_90d` | Negative News Count (90d) | int | items | 1 | Negative news items in last 90 days | Risk control |
| SF-0150 | Risk | `risk_level` | Risk Level | enum | - | medium | Risk level classification | Risk control report |
| SF-0151 | Risk | `risk_score` | Risk Score | number | 0-100 | 62 | Composite risk score | Risk control report |
| SF-0152 | Risk | `admission_suggest` | Admission Recommendation | enum | - | supplement | Franchise admission recommendation | Franchise risk control |

### Order, Inventory & Policy

| Field ID | Entity | Field Name | Display Name | Type | Unit | Example | Description | Related Reports (trace) |
|----------|--------|------------|--------------|------|------|---------|-------------|---------------------------|
| SF-0153 | Order | `order_id` | Order ID | string | - | SO-77821 | Unique order number | Pack C / order audit |
| SF-0154 | Order | `order_qty` | Order Quantity | int | units | 30 | Units ordered | Pack C |
| SF-0155 | Order | `order_status` | Order Status | enum | - | pending_audit | Draft/pending audit/approved/rejected/shipped/completed | Pack C |
| SF-0156 | Order | `audit_result` | Audit Result | enum | - | suggest_substitute | Approved/rejected for stockout/suggest substitute | Smart order audit |
| SF-0157 | Inventory | `wms_stock_qty` | WMS Stock Quantity | int | units | 120 | Warehouse on-hand inventory | Pack C / B |
| SF-0158 | Inventory | `wms_in_transit_qty` | WMS In-Transit Quantity | int | units | 45 | In-transit warehouse quantity | Pack C |
| SF-0159 | Inventory | `store_stock_qty` | Store Stock Quantity | int | units | 8 | Store on-hand inventory | Pack C / D |
| SF-0160 | Inventory | `stock_days_cover` | Stock Days Cover | number | days | 1.2 | Days of inventory coverage | Stockout alert |
| SF-0161 | Inventory | `stock_age_days` | Stock Age (Days) | int | days | 51 | Slow-moving inventory age | Sell-through weekly report |
| SF-0162 | Inventory | `inventory_turn_days` | Inventory Turn Days | number | days | 28 | Inventory turnover days | Health index / benchmarks |
| SF-0163 | Inventory | `shortage_days` | Stockout Days | int | days | 11 | Consecutive stockout days | Stockout loss |
| SF-0164 | Inventory | `demand_daily_est` | Estimated Daily Demand | number | units/day | 18 | Estimated daily demand | Stockout loss |
| SF-0165 | Inventory | `lost_units_est` | Estimated Lost Units | int | units | 198 | Estimated units lost to stockout | Stockout loss |
| SF-0166 | Inventory | `lost_gmv_est` | Estimated Lost GMV | number | CNY | 653202 | Estimated GMV lost to stockout | Stockout loss |
| SF-0167 | Inventory | `lost_margin_est` | Estimated Lost Margin | number | CNY | 117576 | Estimated gross margin lost to stockout | Stockout loss |
| SF-0168 | Inventory | `shortage_root_cause` | Stockout Root Cause | enum | - | color_plan | Production/logistics/color plan/supply | Stockout loss |
| SF-0169 | Inventory | `replenish_qty_suggest` | Suggested Replenish Quantity | int | units | 200 | Recommended replenishment quantity | Stockout loss |
| SF-0170 | Inventory | `eta_date` | ETA Date | date | - | 2026-08-05 | Expected arrival date for replenishment | Stockout / Pack C |
| SF-0171 | Policy | `policy_version` | Policy Version | string | - | 2026Q3-Pickup-Rebate-V3 | Sales policy version | Pack C / settlement |
| SF-0172 | Policy | `current_rebate_tier` | Current Rebate Tier | string | - | Silver tier | Current rebate tier name | Policy alerts |
| SF-0173 | Policy | `current_pickup_qty_mtd` | Current Pickup Qty MTD | int | units | 612 | Month-to-date cumulative pickup | Policy simulation |
| SF-0174 | Policy | `qty_to_next_tier` | Qty to Next Tier | int | units | 188 | Units needed to reach next tier | Policy simulation |
| SF-0175 | Policy | `next_tier_name` | Next Tier Name | string | - | Gold tier | Target tier name | Policy simulation |
| SF-0176 | Policy | `next_tier_rebate_amt` | Next Tier Rebate Amount | number | CNY | 28000 | Projected incremental rebate at next tier | Policy simulation |
| SF-0177 | Policy | `rebate_rate` | Rebate Rate | number | % | 3.5 | Rebate percentage | Settlement statement |
| SF-0178 | Policy | `color_bonus_amt` | Color Completeness Bonus | number | CNY | 2000 | Color completeness bonus amount | Settlement statement |
| SF-0179 | Policy | `clawback_amt` | Clawback Amount | number | CNY | 500 | Clawback for violations/non-achievement | Settlement statement |
| SF-0180 | Policy | `payable_amt` | Payable Amount | number | CNY | 29500 | Payable rebate amount | Settlement statement |
| SF-0181 | Policy | `settlement_id` | Settlement ID | string | - | STL-2026Q3-3201 | Settlement statement identifier | Rebate settlement |
| SF-0182 | Policy | `pay_status` | Payment Status | enum | - | unpaid | Payment status | Settlement statement |
| SF-0183 | ColorPlan | `color_plan_week` | Color Plan Week | string | - | 2026-W31 | Color production planning week | PMC / Pack C |
| SF-0184 | ColorPlan | `color_plan_qty` | Color Plan Quantity | int | units | 120 | Planned production quantity for color | PMC |

### Retail & Marketing

| Field ID | Entity | Field Name | Display Name | Type | Unit | Example | Description | Related Reports (trace) |
|----------|--------|------------|--------------|------|------|---------|-------------|---------------------------|
| SF-0185 | Retail | `retail_qty` | Retail Quantity | int | units | 46 | Card-scan/retail volume in units | Pack D / daily report |
| SF-0186 | Retail | `retail_qty_day` | Daily Retail Quantity | int | units | 6 | Daily retail volume | Retail daily report |
| SF-0187 | Retail | `retail_qty_mtd` | MTD Retail Quantity | int | units | 142 | Month-to-date retail volume | Retail daily report |
| SF-0188 | Retail | `retail_yoy` | Retail YoY | number | % | 8.2 | Retail year-over-year growth | Pack D |
| SF-0189 | Retail | `writeoff_qty` | Write-off Quantity | int | units | 28 | Campaign write-off units | Pack D |
| SF-0190 | Retail | `redeem_rate` | Redemption Rate | number | % | 62.0 | Redeemed vs expected redemption | Pack D / campaigns |
| SF-0191 | Retail | `gross_margin_amt` | Gross Margin Amount | number | CNY | 9860 | Gross margin amount | Retail report |
| SF-0192 | Retail | `gross_margin_rate` | Gross Margin Rate | number | % | 17.9 | Gross margin percentage | Retail report |
| SF-0193 | Retail | `non_exclusive_rate` | Non-Exclusive Rate | number | % | 0 | Mixed/non-exclusive store share | Compliance / retail |
| SF-0194 | Retail | `non_exclusive_flag` | Non-Exclusive Flag | boolean | - | false | Whether store is non-exclusive | Inspection |
| SF-0195 | Campaign | `campaign_id` | Campaign ID | string | - | CAMP-Summer-TradeIn | Marketing campaign identifier | Pack D / campaign performance |
| SF-0196 | Campaign | `campaign_name` | Campaign Name | string | - | Summer trade-in promotion | Campaign name | Pack D |
| SF-0197 | Campaign | `campaign_goal` | Campaign Goal | string | - | Improve renewal conversion | Campaign objective | Campaign planning |
| SF-0198 | Campaign | `campaign_budget` | Campaign Budget | number | CNY | 50000 | Campaign budget | Campaign performance |
| SF-0199 | Campaign | `participants` | Participants | int | people | 3200 | Participant count | Campaign performance |
| SF-0200 | Campaign | `campaign_roi` | Campaign ROI | number | - | 2.4 | Return on investment | Campaign performance |
| SF-0201 | Campaign | `campaign_complaint_rate` | Campaign Complaint Rate | number | % | 0.3 | Campaign-related complaint rate | Campaign performance |
| SF-0202 | Content | `short_video_cnt` | Short Video Count | int | items | 2140 | Short video output count | New retail / Pack A |
| SF-0203 | Content | `short_video_valid_participate_rate` | Short Video Valid Participation Rate | number | % | 38.5 | Valid participation share | Pack A |
| SF-0204 | Content | `followers` | Followers | int | people | 12400 | Account follower count | Social matrix monitoring |
| SF-0205 | Content | `play_cnt` | Play Count | int | times | 86000 | Video play count | Social matrix / productivity |
| SF-0206 | Content | `gmv_convert_rate` | GMV Conversion Rate | number | % | 1.8 | Play-to-purchase conversion | Social matrix / productivity |
| SF-0207 | Content | `deals_cnt` | Deal Count | int | orders | 36 | Guide deal count | Staff productivity diagnostics |
| SF-0208 | Content | `gmv` | GMV | number | CNY | 118764 | Gross merchandise value | Productivity / live stream |
| SF-0209 | Content | `aov` | Average Order Value | number | CNY | 3299 | Average transaction value | Staff productivity diagnostics |
| SF-0210 | Content | `valid_seller_flag` | Valid Seller Flag | boolean | - | true | Whether account qualifies as active seller | Staff productivity diagnostics |
| SF-0211 | Content | `live_sessions` | Live Sessions | int | sessions | 12 | Live stream session count | New retail report |
| SF-0212 | Content | `live_watch_uv` | Live Watch UV | int | people | 5600 | Live stream unique viewers | New retail report |
| SF-0213 | Content | `influencer_cvr` | Influencer CVR | number | % | 2.1 | Influencer conversion rate | New retail report |
| SF-0214 | Content | `refund_rate` | Refund Rate | number | % | 1.2 | Refund share | New retail report |
| SF-0215 | Content | `content_script_id` | Content Script ID | string | - | SCRIPT-Range-Compare-01 | Script/asset identifier | Pack D |
| SF-0216 | Content | `benchmark_case_id` | Benchmark Case ID | string | - | CASE-Suzhou-Wuzhong-Store | Benchmark case identifier | Benchmark report |
| SF-0217 | Outreach | `channel_quota_daily` | Channel Daily Quota | int | times | 5000 | Daily outreach quota per channel | Outreach matrix |
| SF-0218 | Outreach | `delivery_rate` | Delivery Rate | number | % | 96.2 | Message delivery rate | Outreach matrix |
| SF-0219 | Outreach | `open_rate` | Open Rate | number | % | 28.4 | Open/click rate | Outreach matrix |
| SF-0220 | Outreach | `connect_rate` | Connect Rate | number | % | 41.0 | Outbound call connect rate | Renewal scorecard |
| SF-0221 | Outreach | `transfer_human_cnt` | Transfer to Human Count | int | people | 86 | High-intent transfers to human agents | Renewal scorecard |
| SF-0222 | Outreach | `template_approve_days` | Template Approval Days | number | days | 2 | Template approval cycle in days | Outreach matrix |

### Service Tickets

| Field ID | Entity | Field Name | Display Name | Type | Unit | Example | Description | Related Reports (trace) |
|----------|--------|------------|--------------|------|------|---------|-------------|---------------------------|
| SF-0223 | Ticket | `ticket_id` | Ticket ID | string | - | TK-20260728-8891 | Unique service ticket identifier | Service / VoC |
| SF-0224 | Ticket | `ticket_type` | Ticket Type | enum | - | fault | Fault/consult/complaint/other | Ticket analysis |
| SF-0225 | Ticket | `fault_category` | Fault Category | enum | - | battery | Battery/motor/brake/controller/charging/display/frame/lights/tires/other | Fault analysis |
| SF-0226 | Ticket | `consult_category` | Consult Category | string | - | Vehicle information | Consultation category | Inbound call analysis |
| SF-0227 | Ticket | `ticket_channel` | Ticket Channel | string | - | 400 | 400/App/e-commerce/store etc. | VoC aggregation |
| SF-0228 | Ticket | `ticket_status` | Ticket Status | enum | - | open | Open/processing/closed | Customer service |
| SF-0229 | Ticket | `ticket_created_at` | Ticket Created At | datetime | - | 2026-07-28T09:12:00+08:00 | Ticket creation time | Customer service |
| SF-0230 | Ticket | `handle_duration_min` | Handle Duration (Min) | number | minutes | 18 | Handling duration in minutes | QA / BIS |
| SF-0231 | Ticket | `is_complaint` | Is Complaint | boolean | - | true | Complaint flag | Complaint report |
| SF-0232 | Ticket | `three_guarantees_reject_flag` | Three-Guarantee Reject Flag | boolean | - | false | Three-guarantee warranty rejection flag | Regional complaint report |
| SF-0233 | Ticket | `desc_text` | Description Text | text | - | Riding range noticeably below rated spec | Original issue description | Form fill / VoC |
| SF-0234 | Ticket | `desc_chars` | Description Length | int | chars | 86 | Description character count | Fault analysis |
| SF-0235 | Ticket | `transcript_text` | Transcript Text | text | - | (Full call transcript) | Call transcription text | VoC |
| SF-0236 | Ticket | `agent_id` | Agent ID | string | - | AG-2201 | Agent/outbound caller identifier | QA / renewal |
| SF-0237 | Ticket | `sop_item` | SOP Check Item | string | - | Confirm VIN and vehicle model | SOP quality check item | Smart QA |
| SF-0238 | Ticket | `sop_pass_fail` | SOP Pass/Fail | enum | - | pass | SOP pass or fail | Smart QA |
| SF-0239 | Ticket | `risk_words` | Risk Words | json | - | ["Absolutely no problem"] | Risk phrase keywords | Smart QA |
| SF-0240 | VoC | `feedback_id` | Feedback ID | string | - | FB-99102 | Unique VoC feedback identifier | VoC suite |
| SF-0241 | VoC | `nps` | NPS | number | - | 32 | Net Promoter Score | Dashboard / weekly-monthly reports |
| SF-0242 | VoC | `csat` | CSAT | number | - | 4.1 | Customer satisfaction (1–5) | Dashboard |
| SF-0243 | VoC | `nps_delta` | NPS Delta | number | - | -3 | Period NPS change | Weekly-monthly reports |
| SF-0244 | VoC | `feedback_cnt` | Feedback Count | int | items | 1280 | Feedback count in period | Dashboard |
| SF-0245 | VoC | `tag_id` | Tag ID | string | - | TAG-short-range | Standard tag identifier | Tagging / shared semantics |
| SF-0246 | VoC | `tag_name` | Tag Name | string | - | Short range | Tag name | Tagging |
| SF-0247 | VoC | `tag_domain` | Tag Domain | enum | - | product | Tag domain category | Tag vocabulary |
| SF-0248 | VoC | `sentiment` | Sentiment | enum | - | neg | Sentiment polarity | Tagging hard requirement |
| SF-0249 | VoC | `sentiment_score` | Sentiment Score | number | -1~1 | -0.72 | Sentiment intensity score | Sentiment map |
| SF-0250 | VoC | `problem_theme` | Problem Theme | string | - | Short range | Theme cluster name | Rankings / thematic reports |
| SF-0251 | VoC | `theme_cnt` | Theme Count | int | items | 246 | Feedback count for theme | Rankings |
| SF-0252 | VoC | `neg_ratio` | Negative Ratio | number | % | 68.0 | Negative share for theme | Rankings |
| SF-0253 | VoC | `wow_change` | WoW Change | number | % | 22.0 | Week-over-week change | Trend monitoring |
| SF-0254 | VoC | `closed_loop_rate` | Closed-Loop Rate | number | % | 54.0 | Closed vs should-close ratio | Resolutions / Top N |
| SF-0255 | VoC | `recurrence_rate` | Recurrence Rate | number | % | 12.0 | Recurrence share | Closed-loop verification |
| SF-0256 | VoC | `cover_dim` | Report Cover Dimension | enum | - | vehicle | Vehicle/non-vehicle/all coverage | Thematic reports |
| SF-0257 | VoC | `module_name` | Non-Vehicle Module | enum | - | app | App/mini-app/website/hotline/aftersales | Non-vehicle thematic |
| SF-0258 | VoC | `sample_voice` | Sample Voice | text | - | Full charge only gets half the manual range | Representative anonymized voice of customer | Special reports / themes |
| SF-0259 | VoC | `clue_confidence` | Clue Confidence | enum | - | medium | Investigation clue confidence | Investigation clue pack |
| SF-0260 | VoC | `severity_risk_level` | PR Crisis Risk Level | enum | - | P1 | Public relations crisis risk level | Crisis / special reports |
| SF-0261 | VoC | `consumer_sat_score` | Consumer Satisfaction Score | number | % | 82.9 | Survey consumer satisfaction | Satisfaction report |
| SF-0262 | VoC | `channel_sat_score` | Channel Satisfaction Score | number | % | 77.1 | Survey channel satisfaction | Satisfaction report |
| SF-0263 | VoC | `survey_recover_rate` | Survey Recovery Rate | number | % | 6.1 | Survey response vs push rate | Satisfaction report |
| SF-0264 | VoC | `dissatisfaction_reason` | Dissatisfaction Reason | string | - | Short range | Open-ended/option dissatisfaction reason | Satisfaction report |

### Connected Vehicle IoT

| Field ID | Entity | Field Name | Display Name | Type | Unit | Example | Description | Related Reports (trace) |
|----------|--------|------------|--------------|------|------|---------|-------------|---------------------------|
| SF-0265 | Telemetry | `fault_code` | Fault / Alert Code | string | - | BMS_OT_01 | On-vehicle alert code | IoT / troubleshooting |
| SF-0266 | Telemetry | `iot_alert_cnt` | IoT Alert Count | int | times | 3 | Alert count in period | Dashboard / IoT |
| SF-0267 | Telemetry | `mileage_km` | Mileage (km) | number | km | 3260 | Cumulative/period mileage | IoT availability |
| SF-0268 | Telemetry | `soc_pct` | State of Charge (SOC) | number | % | 64 | Remaining battery charge | Proactive service |
| SF-0269 | Telemetry | `telemetry_coverage_rate` | Telemetry Coverage Rate | number | % | 81.0 | Share of vehicles with telemetry | IoT availability |
| SF-0270 | Telemetry | `battery_health_pct` | Battery Health (%) | number | % | 92 | Approximate state of health | Proactive service |

### Manufacturing Quality

| Field ID | Entity | Field Name | Display Name | Type | Unit | Example | Description | Related Reports (trace) |
|----------|--------|------------|--------------|------|------|---------|-------------|---------------------------|
| SF-0271 | Quality | `test_station` | Test Station | string | - | OBD-Dyno-02 | Quality inspection station | OBD report |
| SF-0272 | Quality | `test_ts` | Test Timestamp | datetime | - | 2026-07-28T14:22:00+08:00 | Inspection timestamp | OBD report |
| SF-0273 | Quality | `obd_protocol` | OBD Protocol | string | - | ISO15765 | Communication protocol | OBD report |
| SF-0274 | Quality | `voltage_v` | Voltage (V) | number | V | 54.6 | Measured voltage | OBD report |
| SF-0275 | Quality | `current_a` | Current (A) | number | A | 12.3 | Measured current | OBD report |
| SF-0276 | Quality | `speed_rpm` | Speed (rpm) | number | rpm | 480 | Motor speed | OBD report |
| SF-0277 | Quality | `controller_temp_c` | Controller Temperature (°C) | number | °C | 46 | Controller temperature rise | OBD report |
| SF-0278 | Quality | `qc_result` | QC Result | enum | - | pass | Pass/fail quality result | Quality / traceability |
| SF-0279 | Quality | `operator_id` | Operator ID | string | - | OP-331 | Inspector employee ID | OBD |
| SF-0280 | Quality | `part_name` | Part Name | string | - | Controller | Component name | Traceability |
| SF-0281 | Quality | `part_batch_no` | Part Batch No. | string | - | PB-CTRL-2026W27 | Component batch number | Batch traceability |
| SF-0282 | Quality | `supplier_id` | Supplier ID | string | - | SUP-8821 | Supplier identifier | Traceability / risk control |
| SF-0283 | Quality | `delta_e` | Color Delta E | number | - | 0.8 | Optical color difference | Optical QC |
| SF-0284 | Quality | `gloss` | Gloss | number | - | 85 | Paint gloss measurement | Optical QC |
| SF-0285 | Quality | `defect_type` | Defect Type | string | - | Color variance | Orange peel/color variance/grain etc. | Optical QC |
| SF-0286 | Quality | `anomaly_score` | Anomaly Score | number | 0-1 | 0.86 | Acoustic/sensor anomaly score | Equipment alert |
| SF-0287 | Quality | `predict_fail_days` | Predicted Fail Days | int | days | 14 | Predicted days to failure | Predictive maintenance window |
| SF-0288 | Quality | `release_ts` | Release Timestamp | datetime | - | 2026-07-28T16:00:00+08:00 | Qualified release time | Traceability package |
| SF-0289 | Quality | `trace_package_url` | Trace Package URL | string | - | s3://trace/VINxxx.zip | Traceability data package URL | Traceability package |
| SF-0290 | Quality | `recall_level` | Recall Assessment Level | enum | - | watch | Watch/targeted/recall evaluation | Batch traceability |

### Inspection & Compliance

| Field ID | Entity | Field Name | Display Name | Type | Unit | Example | Description | Related Reports (trace) |
|----------|--------|------------|--------------|------|------|---------|-------------|---------------------------|
| SF-0291 | Inspection | `inspect_id` | Inspection ID | string | - | INS-20260728-014 | Inspection task identifier | Inspection report |
| SF-0292 | Inspection | `inspect_time` | Inspection Time | datetime | - | 2026-07-28T08:30:00+08:00 | Inspection timestamp | Inspection report |
| SF-0293 | Inspection | `check_item` | Check Item | string | - | Storefront VI completeness | Inspection checklist item name | Inspection report |
| SF-0294 | Inspection | `ai_confidence` | AI Confidence | number | 0-1 | 0.91 | Visual recognition confidence | Inspection / image diff |
| SF-0295 | Inspection | `pass_fail` | Pass/Fail | enum | - | fail | Pass or fail result | Inspection report |
| SF-0296 | Inspection | `photo_url` | Photo URL | string | - | https://.../store.jpg | Evidence photo URL | Inspection / image diff |
| SF-0297 | Inspection | `morning_photo_url` | Morning Photo URL | string | - | https://.../am.jpg | Morning panoramic photo for AM/PM diff | Image differential |
| SF-0298 | Inspection | `evening_photo_url` | Evening Photo URL | string | - | https://.../pm.jpg | Evening panoramic photo for AM/PM diff | Image differential |
| SF-0299 | Inspection | `competitor_logo_detected` | Competitor Logo Detected | json | - | ["Competitor A"] | Detected competitor logos | Image differential |
| SF-0300 | Inspection | `suspect_type` | Suspect Type | string | - | Non-exclusive stock display | Violation suspect type | Image differential |
| SF-0301 | Inspection | `vi_score` | VI Consistency Score | number | 0-100 | 78 | Visual identity consistency score | VI diagnostics / inspection |
| SF-0302 | Inspection | `rectify_ticket_id` | Rectification Ticket ID | string | - | RC-8891 | Rectification work order ID | Inspection |
| SF-0303 | Inspection | `due_date` | Due Date | date | - | 2026-08-05 | Rectification deadline | Alerts / inspection |
| SF-0304 | Brand | `mention_cnt_24h` | Brand Mentions (24h) | int | times | 1260 | Brand mention count in 24 hours | Brand sentiment dashboard |
| SF-0305 | Brand | `reputation_score` | Reputation Score | number | 0-100 | 71 | Brand reputation score | Brand sentiment dashboard |
| SF-0306 | Brand | `hotspot_term` | Hotspot Term | string | - | Inflated range claims | Sentiment hotspot term | Crisis alert |
| SF-0307 | Brand | `growth_velocity` | Volume Growth Velocity | number | - | 3.2 | Sudden volume growth rate | Crisis alert |
| SF-0308 | Brand | `mi_consistency_score` | MI Consistency Score | number | 0-100 | 66 | Mission-identity word-deed consistency | MI diagnostics |
| SF-0309 | Brand | `bvp_memorability` | BVP Memorability | number | 0-1 | 0.42 | Brand value proposition memorability | BVP report |
| SF-0310 | Brand | `bvp_understanding` | BVP Understanding | number | 0-1 | 0.55 | Brand value proposition understanding | BVP report |
| SF-0311 | Brand | `purchase_intent` | Purchase Intent | number | 0-1 | 0.48 | Purchase intent score | BVP / survey |
| SF-0312 | Brand | `energy_kwh_per_vehicle` | Energy per Vehicle | number | kWh/unit | 128 | Manufacturing energy per vehicle | ESG |
| SF-0313 | Brand | `co2e_t` | CO2e Equivalent | number | tCO2e |  sequester | Carbon emission equivalent | ESG |
| SF-0314 | Brand | `scrap_battery_recycle_rate` | Scrap Battery Recycle Rate | number | % | 91.0 | End-of-life battery recycling rate | ESG |

### Finance

| Field ID | Entity | Field Name | Display Name | Type | Unit | Example | Description | Related Reports (trace) |
|----------|--------|------------|--------------|------|------|---------|-------------|---------------------------|
| SF-0315 | Finance | `expense_id` | Expense ID | string | - | EXP-202607-118 | Expense reimbursement ID | Three-way match |
| SF-0316 | Finance | `invoice_no` | Invoice No. | string | - | INV-8891200 | Invoice number | Three-way match |
| SF-0317 | Finance | `po_no` | PO No. | string | - | PO-55201 | Purchase order number | Three-way match / PO tracking |
| SF-0318 | Finance | `receipt_amt` | Receipt Amount | number | CNY | 1280.00 | Bank receipt amount | Three-way match |
| SF-0319 | Finance | `invoice_amt` | Invoice Amount | number | CNY | 1280.00 | Invoice amount | Three-way match |
| SF-0320 | Finance | `po_amt` | PO Amount | number | CNY | 1300.00 | Purchase order amount | Three-way match |
| SF-0321 | Finance | `match_status` | Three-Way Match Status | enum | - | mismatch | Match or mismatch status | Three-way match |
| SF-0322 | Finance | `diff_amt` | Difference Amount | number | CNY | 20.00 | Variance amount | Three-way match |
| SF-0323 | Finance | `diff_reason` | Difference Reason | string | - | Tax amount mismatch | Variance root cause | Three-way match |
| SF-0324 | Finance | `revenue_forecast` | Revenue Forecast | number | CNY | 1.2e8 | Monthly revenue forecast | Cash flow forecast |
| SF-0325 | Finance | `pickup_forecast_units` | Pickup Forecast Units | int | units | 52000 | Pickup volume forecast | Cash flow forecast |
| SF-0326 | Finance | `rebate_cashout_forecast` | Rebate Cash-out Forecast | number | CNY | 8.5e6 | Rebate cash outflow forecast | Cash flow forecast |
| SF-0327 | Finance | `opex_forecast` | OPEX Forecast | number | CNY | 2.1e7 | Operating expense forecast | Cash flow forecast |
| SF-0328 | Finance | `net_cash_forecast` | Net Cash Forecast | number | CNY | 1.5e7 | Net cash flow forecast | Cash flow forecast |
| SF-0329 | Finance | `forecast_confidence_low` | Forecast Confidence Low | number | CNY | 1.1e7 | Confidence interval lower bound | Cash flow forecast |
| SF-0330 | Finance | `forecast_confidence_high` | Forecast Confidence High | number | CNY | 1.9e7 | Confidence interval upper bound | Cash flow forecast |

### App Activation

| Field ID | Entity | Field Name | Display Name | Type | Unit | Example | Description | Related Reports (trace) |
|----------|--------|------------|--------------|------|------|---------|-------------|---------------------------|
| SF-0331 | Activation | `cum_sales_units` | Cumulative Sales Units | int | units | 2500000 | Cumulative vehicle sales | Activation rate baseline |
| SF-0332 | Activation | `active_owners_est` | Active Owners (Est.) | int | people | 1800000 | Estimated active vehicle owners | Activation rate baseline |
| SF-0333 | Activation | `app_register_cnt` | App Register Count | int | people | 920000 | Registered app users | Activation rate baseline |
| SF-0334 | Activation | `bind_vehicle_cnt` | Bind Vehicle Count | int | vehicles | 610000 | Completed vehicle bindings | Activation rate baseline |
| SF-0335 | Activation | `mau` | MAU | int | people | 210000 | Monthly active users | Activation rate / monthly report |
| SF-0336 | Activation | `dau` | DAU | int | people | 42000 | Daily active users | Activation rate |
| SF-0337 | Activation | `activation_rate` | Activation Rate | number | % | 33.9 | Binding/active-owner based activation rate | Activation rate baseline |
| SF-0338 | Activation | `funnel_step` | Funnel Step | string | - | Bind vehicle | Open→login→bind→vehicle control→retention | Activation funnel |
| SF-0339 | Activation | `funnel_uv` | Funnel UV | int | people | 88000 | Unique users at funnel step | Activation funnel |
| SF-0340 | Activation | `funnel_cvr` | Funnel CVR | number | % | 62.0 | Conversion to next step | Activation funnel |
| SF-0341 | Activation | `tab_name` | App Tab Name | string | - | My vehicle | App feature tab name | Activation funnel |
| SF-0342 | Activation | `pv` | Page Views | int | times | 560000 | Page view count | Activation funnel |
| SF-0343 | Activation | `uv` | Unique Visitors | int | people | 120000 | Unique visitor count | Activation funnel |
| SF-0344 | Activation | `stay_seconds` | Stay Seconds | number | seconds | 46 | Session dwell time in seconds | Activation funnel |
| SF-0345 | Activation | `push_click_rate` | Push Click Rate | number | % | 8.6 | Push notification click-through rate | Outreach / activation |
| SF-0346 | Activation | `faq_cnt` | FAQ Entry Count | int | items | 320 | Knowledge base FAQ entries | Q&A coverage |
| SF-0347 | Activation | `top20_ticket_coverage_rate` | Top 20 Ticket Coverage Rate | number | % | 71.0 | FAQ coverage of top 20 ticket types | Q&A coverage |
| SF-0348 | Activation | `oneid_coverage_rate` | OneID Coverage Rate | number | % | 64.0 | Identifiable user share | OneID report |
| SF-0349 | Activation | `orphan_user_cnt` | Orphan User Count | int | people | 120000 | Users that cannot be stitched | OneID report |
| SF-0350 | Activation | `koc_score` | KOC Score | number | 0-100 | 81 | Community KOC score | KOC pool |
| SF-0351 | Activation | `post_cnt` | Post Count | int | items | 24 | Community post count | KOC pool |
| SF-0352 | Activation | `interact_rate` | Interaction Rate | number | % | 6.8 | Interactions over impressions | KOC pool |
| SF-0353 | O2O | `platform_order_cnt` | Platform Order Count | int | orders | 1500 | E-commerce platform orders | O2O funnel |
| SF-0354 | O2O | `lead_phone_cnt` | Lead Phone Count | int | count | 980 | Lead capture phone count | O2O funnel |
| SF-0355 | O2O | `store_redeem_cnt` | Store Redemption Count | int | orders | 420 | In-store redemption count | O2O funnel |

### Alerts & Collaboration

| Field ID | Entity | Field Name | Display Name | Type | Unit | Example | Description | Related Reports (trace) |
|----------|--------|------------|--------------|------|------|---------|-------------|---------------------------|
| SF-0356 | Alert | `alert_id` | Alert ID | string | - | ALERT-20260728-014 | Unique alert identifier | Pack B |
| SF-0357 | Alert | `alert_type` | Alert Type | enum | - | shortage | Sales decline/compliance/stockout/complaint/competitor | Pack B |
| SF-0358 | Alert | `metric_name` | Trigger Metric Name | string | - | mom_rate | Metric that triggered the alert | Pack B |
| SF-0359 | Alert | `metric_value` | Trigger Metric Value | number | - | -12.4 | Actual metric value | Pack B |
| SF-0360 | Alert | `threshold_value` | Threshold Value | number | - | -10.0 | Rule threshold | Pack B / rules engine |
| SF-0361 | Alert | `severity` | Severity | enum | - | P0 | P0/P1/P2 severity level | Alerts / crisis |
| SF-0362 | Alert | `required_action` | Required Action | string | - | Replenish color within 3 days | Required remediation action | Pack B |
| SF-0363 | Alert | `verify_method` | Verify Method | string | - | Second inspection | Verification/acceptance method | Pack B |
| SF-0364 | Collab | `cross_issue_cnt` | Cross-Department Issue Count | int | count | 17 | Cross-functional issue count | Integrated marketing report |
| SF-0365 | Collab | `closed_cnt` | Closed Count | int | count | 9 | Closed issue count | Integrated marketing / resolutions |
| SF-0366 | Collab | `overdue_cnt` | Overdue Count | int | count | 3 | Overdue unresolved count | Integrated marketing / resolutions |
| SF-0367 | Collab | `response_hours` | Response Hours | number | hours | 26 | Average response time in hours | Integrated marketing |
| SF-0368 | Collab | `pilot_vs_control_delta` | Pilot vs Control Delta | number | - | 8.5 | Pilot vs control group metric delta | Integrated marketing |
| SF-0369 | Collab | `resolution_id` | Resolution ID | string | - | RES-2026W30-01 | Meeting resolution identifier | Resolution tracker |
| SF-0370 | Collab | `owner_dept` | Owner Department | string | - | Product Innovation Institute | Responsible department | Resolutions / special reports |
| SF-0371 | Collab | `verify_metric` | Verification Metric | string | - | Negative share for range theme | Post-resolution verification KPI | Resolution tracker |

### Shared AI Assets

| Field ID | Entity | Field Name | Display Name | Type | Unit | Example | Description | Related Reports (trace) |
|----------|--------|------------|--------------|------|------|---------|-------------|---------------------------|
| SF-0372 | AIOutput | `ai_output_id` | AI Output ID | string | - | AIO-10001 | Unique shared output identifier | Anti-silo story |
| SF-0373 | AIOutput | `producer_skill` | Producer Skill | string | - | fill_ticket | Producer skill identifier | Anti-silo |
| SF-0374 | AIOutput | `consumer_allow` | Allowed Consumers | json | - | ["renewal_plan","voc_weekly"] | Subscribable consumer skill list | Anti-silo |
| SF-0375 | AIOutput | `payload` | Payload | json | - | {"tags":["Open complaint"],"vin":"..."} | Structured output content | Anti-silo |
| SF-0376 | AIOutput | `payload_schema` | Payload Schema | string | - | ticket_draft_v1 | Payload structure version | Anti-silo |
| SF-0377 | TagVocabulary | `tag_vocab_version` | Tag Vocabulary Version | string | - | voc-tags-2026.07 | Shared semantic version | Tag governance |
| SF-0378 | TagVocabulary | `tag_parent_id` | Parent Tag ID | string | - | TAG-ROOT-PRODUCT | Parent tag in tag tree | Tag governance |
| SF-0379 | CapabilityCatalog | `skill_id` | Skill ID | string | - | repair_kb | Capability catalog primary key | Capability catalog |
| SF-0380 | CapabilityCatalog | `skill_desc` | Skill Description | text | - | Repair knowledge base Q&A | Capability description | Capability catalog |
| SF-0381 | CapabilityCatalog | `input_schema` | Input Schema | json | - | {"query":"string"} | Input contract schema | Capability catalog |
| SF-0382 | CapabilityCatalog | `output_schema` | Output Schema | json | - | {"answer":"string"} | Output contract schema | Capability catalog |
| SF-0383 | CapabilityCatalog | `allowed_tools` | Allowed Tools | json | - | ["search_kb","get_vehicle"] | Callable tool list | Capability catalog |
| SF-0384 | RunLog | `step_name` | Step Name | string | - | retrieve | Control loop step name | Collaboration layer |
| SF-0385 | RunLog | `step_status` | Step Status | enum | - | ok | ok/error/skipped | Collaboration layer |
| SF-0386 | RunLog | `step_ts` | Step Timestamp | datetime | - | 2026-08-01T12:00:00+08:00 | Step timestamp | Collaboration layer |

### Process, HR & Legal

| Field ID | Entity | Field Name | Display Name | Type | Unit | Example | Description | Related Reports (trace) |
|----------|--------|------------|--------------|------|------|---------|-------------|---------------------------|
| SF-0387 | Process | `process_id` | Process ID | string | - | PROC-Store-Opening-Approval | Process definition identifier | Process report |
| SF-0388 | Process | `redundant_step` | Redundant Step | string | - | Duplicate stamp node | Redundant process step detected | Redundancy detection report |
| SF-0389 | Process | `bottleneck_step` | Bottleneck Step | string | - | Quota approval | Bottleneck step in process | Process root-cause analysis |
| SF-0390 | Process | `cycle_time_hours` | Cycle Time (Hours) | number | hours | 72 | Process cycle time | Process simulation |
| SF-0391 | Process | `proposal_level` | Proposal Level | enum | - | L2 | L1/L2/L3 recommendation level | AI recommendation inbox |
| SF-0392 | HR | `job_id` | Job ID | string | - | JOB-After-Sales-Specialist | Recruiting position identifier | Job matching |
| SF-0393 | HR | `match_score` | Match Score | number | 0-100 | 84 | Person-job match score | Job matching |
| SF-0394 | Legal | `contract_id` | Contract ID | string | - | CT-2026-889 | Contract number | Contract review |
| SF-0395 | Legal | `clause_risk_level` | Clause Risk Level | enum | - | high | Contract clause risk level | Contract review |
| SF-0396 | Legal | `clause_comment` | Clause Comment | text | - | Missing liquidated damages cap | Contract review comment | Contract review |
| SF-0397 | Knowledge | `kb_domain` | Knowledge Base Domain | enum | - | repair | repair/policy/hr/product | RAG |
| SF-0398 | Knowledge | `kb_doc_id` | Knowledge Document ID | string | - | KB-REP-0012 | Document identifier | RAG |
| SF-0399 | Knowledge | `kb_chunk_id` | Knowledge Chunk ID | string | - | CHK-88 | Vector chunk identifier | RAG |
| SF-0400 | Knowledge | `kb_score` | Retrieval Relevance Score | number | 0-1 | 0.83 | Retrieval relevance score | RAG |

## 3. Demo Core Model Mapping (recommended)

| shared/models Entity | Primary Standard Fields (excerpt) |
|----------------------|----------------------------------|
| `Customer` | customer_id, phone_masked, oneid, identity_type, rfm_segment, service_expire_date, renew_* |
| `Vehicle` | vin, vehicle_model, color, battery_*, is_smart_vehicle, ota_version, batch_no, plant |
| `Ticket` | ticket_id, ticket_type, fault_category, ticket_channel, desc_text, sentiment, tag_*, vin, customer_id |
| `Order` | order_id, dealer_id, sku_id, order_qty, order_status, audit_result, policy_version |
| `TagVocabulary` | tag_id, tag_name, tag_domain, tag_parent_id, tag_vocab_version, sentiment enum |
| `AIOutput` | ai_output_id, producer_skill, consumer_allow, payload, payload_schema, run_id, generated_at |

## 4. Revision History

| Version | Date | Notes |
|---------|------|-------|
| V1.0 | 2026-08-01 | Initial release: generalized from feature list and report fields; 400 standard fields |
