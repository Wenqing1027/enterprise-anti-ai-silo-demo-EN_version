# Cross-Department Standard Field Definitions (Structured)

> Synced with `field_glossary.json`.

## Field details (400 total)

| Field ID | Field | Label | Entity | Domain | Type | Meaning |
|--------|--------|------|------|--------|------|------|
| SF-0001 | `report_id` | Report ID | ReportMeta | Metadata | string | Unique ID for one report instance |
| SF-0002 | `report_type` | Report type | ReportMeta | Metadata | enum | Report type code |
| SF-0003 | `period` | Reporting period | ReportMeta | Metadata | string | Month / week / day / custom range |
| SF-0004 | `period_type` | Period type | ReportMeta | Metadata | enum | day|week|month|quarter|custom |
| SF-0005 | `period_start` | Period start | ReportMeta | Metadata | date | Period start date |
| SF-0006 | `period_end` | Period end | ReportMeta | Metadata | date | Period end date |
| SF-0007 | `generated_at` | Generated at | ReportMeta | Metadata | datetime | Report generation timestamp |
| SF-0008 | `data_as_of` | Data as of | ReportMeta | Metadata | datetime | Data as-of timestamp |
| SF-0009 | `run_id` | Run ID | ReportMeta | Metadata | string | Agent / pipeline run ID |
| SF-0010 | `producer_skill` | Producer skill | ReportMeta | Metadata | string | Producer skill that writes to shared layer |
| SF-0011 | `traffic_light` | Traffic light | ReportMeta | Metadata | enum | red|yellow|green |
| SF-0012 | `narrative_summary` | NLG summary | ReportMeta | Metadata | text | Natural language summary |
| SF-0013 | `action_suggestions` | Action suggestions | ReportMeta | Metadata | json | Structured suggestions array |
| SF-0014 | `org_id` | Organization ID | Org | Organization | string | Unique organization node ID |
| SF-0015 | `org_name` | Organization name | Org | Organization | string | Organization display name |
| SF-0016 | `org_level` | Organization level | Org | Organization | enum | nation|warzone|subzone|block|dealer|outlet|store |
| SF-0017 | `parent_org_id` | Parent Org Id | Org | Organization | string | Organization tree parent node |
| SF-0018 | `org_path` | Organization path | Org | Organization | string | Full hierarchy path |
| SF-0019 | `province` | Province | Region | Organization | string | Admin region - province |
| SF-0020 | `city` | City | Region | Organization | string | Admin region - city |
| SF-0021 | `county_code` | County code | Region | Organization | string | National county/district code |
| SF-0022 | `county_name` | County Name | Region | Organization | string | County/district name |
| SF-0023 | `dealer_id` | Tier-1 / dealer ID | Dealer | Channel master data | string | Unique dealer ID |
| SF-0024 | `dealer_name` | Dealer Name | Dealer | Channel master data | string | Dealer name |
| SF-0025 | `legal_person` | Legal person | Dealer | Channel master data | string | Legal representative |
| SF-0026 | `open_account_date` | Account opening date | Dealer | Channel master data | date | Dealer account opening date |
| SF-0027 | `developer_name` | Developer | Dealer | Channel master data | string | Channel development owner |
| SF-0028 | `store_id` | Store ID | Store | Channel master data | string | Unique store ID |
| SF-0029 | `store_name` | Store Name | Store | Channel master data | string | Store name |
| SF-0030 | `store_address` | Store address | Store | Channel master data | string | Full address |
| SF-0031 | `store_type` | Store type | Store | Channel master data | enum | exclusive|mixed|non_exclusive |
| SF-0032 | `store_grade` | Store grade | Store | Channel master data | enum | A|B|C|D |
| SF-0033 | `store_area_sqm` | Store area | Store | Channel master data | number | Floor area |
| SF-0034 | `biz_district` | Business district | Store | Channel master data | string | Opening Gantt business district |
| SF-0035 | `guide_id` | Guide ID | Guide | Channel master data | string | Sales guide ID |
| SF-0036 | `channel_account_id` | Social account ID | Guide | Channel master data | string | Douyin / WeChat Channels etc. account |
| SF-0037 | `customer_id` | Customer ID | Customer | Customer / user | string | Unified customer master ID |
| SF-0038 | `phone_masked` | Phone (masked) | Customer | Customer / user | string | Masked phone number |
| SF-0039 | `openid` | OpenID | Customer | Customer / user | string | OpenID field value |
| SF-0040 | `unionid` | UnionID | Customer | Customer / user | string | UnionID field value |
| SF-0041 | `identity_type` | Identity type | Customer | Customer / user | enum | end_user|dealer|prospect|employee |
| SF-0042 | `oneid` | OneID | Customer | Customer / user | string | Cross-system unified identity |
| SF-0043 | `oneid_match_method` | Identity match method | Customer | Customer / user | enum | phone|device|vin|probabilistic |
| SF-0044 | `app_register_flag` | App registered flag | UserBehavior | Customer / user | boolean | Whether registered on App |
| SF-0045 | `bind_vehicle_flag` | Vehicle paired flag | UserBehavior | Customer / user | boolean | Whether vehicle pairing completed |
| SF-0046 | `last_active_at` | Last active at | UserBehavior | Customer / user | datetime | Last App / connectivity activity |
| SF-0047 | `active_days_30d` | Active days in last 30 days | UserBehavior | Customer / user | int | Active days in last 30 days |
| SF-0048 | `mau_flag` | Mau Flag | UserBehavior | Customer / user | boolean | Monthly active user flag |
| SF-0049 | `dau_flag` | Dau Flag | UserBehavior | Customer / user | boolean | Daily active user flag |
| SF-0050 | `rfm_segment` | RFM segment | UserBehavior | Customer / user | enum | high_value|potential|silent|churn_risk |
| SF-0051 | `r_days` | R (days since last active) | UserBehavior | Customer / user | int | Recency |
| SF-0052 | `f_month` | F (monthly interactions) | UserBehavior | Customer / user | int | Frequency |
| SF-0053 | `m_value` | M (monetary value) | UserBehavior | Customer / user | number | Parts / service spend etc. |
| SF-0054 | `first_touch_channel` | First touch channel | UserBehavior | Customer / user | string | First touch channel |
| SF-0055 | `last_touch_channel` | Last touch channel | UserBehavior | Customer / user | string | Last touch channel |
| SF-0056 | `service_expire_date` | Connectivity service expiry | Renewal | Customer / user | date | Smart vehicle service expiry |
| SF-0057 | `due_renew_flag` | Due renew flag | Renewal | Customer / user | boolean | Enters due-renewal pool |
| SF-0058 | `paid_flag` | Paid flag | Renewal | Customer / user | boolean | Whether paid (distinguish new vs renew) |
| SF-0059 | `paid_type` | Paid type | Renewal | Customer / user | enum | new_purchase|renew|unknown |
| SF-0060 | `active_t30_flag` | Active within 30 days before expiry | Renewal | Customer / user | boolean | Active within 30 days before expiry field value |
| SF-0061 | `active_t7_flag` | Active within 7 days before expiry | Renewal | Customer / user | boolean | Active within 7 days before expiry field value |
| SF-0062 | `sleep_90d_app_flag` | Sleep 90d App Flag | Renewal | Customer / user | boolean | No App use in 90 days |
| SF-0063 | `active_90d_4g_flag` | Active 90d 4g Flag | Renewal | Customer / user | boolean | 4G vehicle connected in last 90 days |
| SF-0064 | `renew_intent_score` | Renewal intent score | Renewal | Customer / user | number | Model / rule intent score |
| SF-0065 | `renew_pool_layer` | Renewal pool layer | Renewal | Customer / user | enum | T-30|T-7|sleep|non_smart |
| SF-0066 | `outreach_channel` | Outreach channel | Renewal | Customer / user | enum | push|sms|ai_call|human|wecom |
| SF-0067 | `intent_level` | Call intent level | Renewal | Customer / user | enum | high|mid|low |
| SF-0068 | `vin` | VIN | Vehicle | Vehicle | string | VIN field value |
| SF-0069 | `frame_no` | Frame part number | Vehicle | Vehicle | string | Frame part number field value |
| SF-0070 | `sn` | Vehicle serial number | Vehicle | Vehicle | string | Vehicle serial number field value |
| SF-0071 | `vehicle_model` | Model | Vehicle | Vehicle | string | Model field value |
| SF-0072 | `vehicle_config` | Trim / config type | Vehicle | Vehicle | string | Trim / config type field value |
| SF-0073 | `color` | Color | Vehicle | Vehicle | string | Color field value |
| SF-0074 | `battery_type` | Battery type | Vehicle | Vehicle | enum | lead_acid|lithium|graphene |
| SF-0075 | `battery_spec` | Battery spec | Vehicle | Vehicle | string | Battery spec field value |
| SF-0076 | `claimed_range_km` | Rated range | Vehicle | Vehicle | number | Rated range field value |
| SF-0077 | `purchase_date` | Purchase date | Vehicle | Vehicle | date | Purchase date field value |
| SF-0078 | `purchase_year` | Purchase year | Vehicle | Vehicle | int | Purchase year field value |
| SF-0079 | `is_smart_vehicle` | Smart vehicle flag | Vehicle | Vehicle | boolean | Smart vehicle flag field value |
| SF-0080 | `plant` | Production base | Vehicle | Vehicle | string | Production base field value |
| SF-0081 | `line_id` | Production line ID | Vehicle | Vehicle | string | Production line ID field value |
| SF-0082 | `batch_no` | Vehicle production batch | Vehicle | Vehicle | string | Vehicle production batch field value |
| SF-0083 | `ota_version` | OTA version | Vehicle | Vehicle | string | OTA version field value |
| SF-0084 | `sku_id` | SKU ID | SKU | Product SKU | string | SKU ID field value |
| SF-0085 | `sku_name` | SKU name | SKU | Product SKU | string | SKU name field value |
| SF-0086 | `asp_cny` | Average selling price ASP | SKU | Product SKU | number | Average selling price ASP field value |
| SF-0087 | `hot_slow_flag` | Hot / slow mover flag | SKU | Product SKU | enum | hot|normal|slow |
| SF-0088 | `substitute_sku_id` | Substitute SKU | SKU | Product SKU | string | Substitute SKU field value |
| SF-0089 | `competitor_brand` | Competitor brand | Competitor | Product SKU | string | Competitor brand field value |
| SF-0090 | `competitor_model` | Competitor Model | Competitor | Product SKU | string | Competitor Model field value |
| SF-0091 | `competitor_price_cny` | Competitor price | Competitor | Product SKU | number | Competitor price field value |
| SF-0092 | `competitor_share` | Competitor regional share | Competitor | Product SKU | number | Competitor regional share field value |
| SF-0093 | `competitor_share_pp_change` | Share change (pp) | Competitor | Product SKU | number | Share change (pp) field value |
| SF-0094 | `promo_type` | Promotion type | Competitor | Product SKU | string | Promotion type field value |
| SF-0095 | `promo_region` | Promotion region | Competitor | Product SKU | string | Promotion region field value |
| SF-0096 | `promo_window` | Promotion window | Competitor | Product SKU | string | Promotion window field value |
| SF-0097 | `price_cut_amt` | Price cut amount | Competitor | Product SKU | number | Price cut amount field value |
| SF-0098 | `sentiment_score` | Reputation score | Competitor | Product SKU | number | Reputation score field value |
| SF-0099 | `launch_date` | Launch date | Competitor | Product SKU | date | Launch date field value |
| SF-0100 | `sales_qty` | Sales Qty | SalesMetric | Sales targets | int | Sales Qty field value |
| SF-0101 | `sales_target_qty` | Sales Target Qty | SalesMetric | Sales targets | int | Sales Target Qty field value |
| SF-0102 | `sales_achieve_rate` | Sales Achieve Rate | SalesMetric | Sales targets | number | Sales Achieve Rate field value |
| SF-0103 | `contract_qty` | Contract Qty | SalesMetric | Sales targets | int | Contract Qty field value |
| SF-0104 | `contract_target_qty` | Contract Target Qty | SalesMetric | Sales targets | int | Contract Target Qty field value |
| SF-0105 | `contract_achieve_rate` | Contract Achieve Rate | SalesMetric | Sales targets | number | Contract Achieve Rate field value |
| SF-0106 | `yoy_sales_qty` | Yoy Sales Qty | SalesMetric | Sales targets | int | Yoy Sales Qty field value |
| SF-0107 | `yoy_rate` | Yoy Rate | SalesMetric | Sales targets | number | Yoy Rate field value |
| SF-0108 | `mom_sales_qty` | Mom Sales Qty | SalesMetric | Sales targets | int | Mom Sales Qty field value |
| SF-0109 | `mom_rate` | Mom Rate | SalesMetric | Sales targets | number | Mom Rate field value |
| SF-0110 | `rank_warzone` | Rank Warzone | SalesMetric | Sales targets | int | Rank Warzone field value |
| SF-0111 | `rank_subzone` | Rank Subzone | SalesMetric | Sales targets | int | Rank Subzone field value |
| SF-0112 | `rank_dealer` | Rank Dealer | SalesMetric | Sales targets | int | Rank Dealer field value |
| SF-0113 | `full_achieve_outlet_cnt` | Full Achieve Outlet Cnt | SalesMetric | Sales targets | int | Full Achieve Outlet Cnt field value |
| SF-0114 | `full_achieve_outlet_ratio` | Full Achieve Outlet Ratio | SalesMetric | Sales targets | number | Full Achieve Outlet Ratio field value |
| SF-0115 | `abnormal_outlet_cnt` | Abnormal Outlet Cnt | SalesMetric | Sales targets | int | Abnormal Outlet Cnt field value |
| SF-0116 | `abnormal_outlet_ratio` | Abnormal Outlet Ratio | SalesMetric | Sales targets | number | Abnormal Outlet Ratio field value |
| SF-0117 | `abnormal_reason` | Abnormal Reason | SalesMetric | Sales targets | string | Abnormal Reason field value |
| SF-0118 | `abnormal_reason_cnt` | Abnormal Reason Cnt | SalesMetric | Sales targets | int | Abnormal Reason Cnt field value |
| SF-0119 | `core_market_gap_to_top3` | Core Market Gap To Top3 | SalesMetric | Sales targets | int | Core Market Gap To Top3 field value |
| SF-0120 | `online_sales_qty` | Online Sales Qty | SalesMetric | Sales targets | int | Online Sales Qty field value |
| SF-0121 | `health_index` | Health Index | Health | Sales targets | number | Health Index field value |
| SF-0122 | `sales_score` | Sales Score | Health | Sales targets | number | Sales Score field value |
| SF-0123 | `retail_score` | Retail Score | Health | Sales targets | number | Retail Score field value |
| SF-0124 | `compliance_score` | Compliance Score | Health | Sales targets | number | Compliance Score field value |
| SF-0125 | `complaint_score` | Complaint Score | Health | Sales targets | number | Complaint Score field value |
| SF-0126 | `inventory_turn_score` | Inventory Turn Score | Health | Sales targets | number | Inventory Turn Score field value |
| SF-0127 | `blank_l1_plan_cnt` | Blank L1 Plan Cnt | StoreDev | Channel development | int | Blank L1 Plan Cnt field value |
| SF-0128 | `blank_l1_opened_cnt` | Blank L1 Opened Cnt | StoreDev | Channel development | int | Blank L1 Opened Cnt field value |
| SF-0129 | `blank_l1_achieve_rate` | Blank L1 Achieve Rate | StoreDev | Channel development | number | Blank L1 Achieve Rate field value |
| SF-0130 | `store_dev_plan_cnt` | Store Dev Plan Cnt | StoreDev | Channel development | int | Store Dev Plan Cnt field value |
| SF-0131 | `store_dev_done_cnt` | Store Dev Done Cnt | StoreDev | Channel development | int | Store Dev Done Cnt field value |
| SF-0132 | `store_dev_rate` | Store Dev Rate | StoreDev | Channel development | number | Store Dev Rate field value |
| SF-0133 | `market_capacity_annual` | Market Capacity Annual | StoreDev | Channel development | int | Market Capacity Annual field value |
| SF-0134 | `self_coverage_flag` | Self Coverage Flag | StoreDev | Channel development | enum | yes|weak|blank |
| SF-0135 | `open_roi_months` | Open Roi Months | StoreDev | Channel development | number | Open Roi Months field value |
| SF-0136 | `support_quota_total_wan` | Support Quota Total Wan | StoreDev | Channel development | number | Support Quota Total Wan field value |
| SF-0137 | `support_quota_applied_wan` | Support Quota Applied Wan | StoreDev | Channel development | number | Support Quota Applied Wan field value |
| SF-0138 | `support_quota_remain_wan` | Support Quota Remain Wan | StoreDev | Channel development | number | Support Quota Remain Wan field value |
| SF-0139 | `first_order_qty` | First Order Qty | StoreDev | Channel development | int | First Order Qty field value |
| SF-0140 | `m1_m3_order_qty` | M1 M3 Order Qty | StoreDev | Channel development | int | M1 M3 Order Qty field value |
| SF-0141 | `gantt_owner` | Gantt Owner | StoreDev | Channel development | string | Gantt Owner field value |
| SF-0142 | `gantt_start` | Gantt Start | StoreDev | Channel development | date | Gantt Start field value |
| SF-0143 | `gantt_end` | Gantt End | StoreDev | Channel development | date | Gantt End field value |
| SF-0144 | `fitout_suggest_grade` | Fitout Suggest Grade | StoreDev | Channel development | enum | Fitout Suggest Grade field value |
| SF-0145 | `credit_code` | Credit Code | Risk | Channel development | string | Credit Code field value |
| SF-0146 | `reg_capital_wan` | Reg Capital Wan | Risk | Channel development | number | Reg Capital Wan field value |
| SF-0147 | `lawsuit_cnt_3y` | Lawsuit Cnt 3y | Risk | Channel development | int | Lawsuit Cnt 3y field value |
| SF-0148 | `dishonest_flag` | Dishonest Flag | Risk | Channel development | boolean | Dishonest Flag field value |
| SF-0149 | `negative_news_cnt_90d` | Negative News Cnt 90d | Risk | Channel development | int | Negative News Cnt 90d field value |
| SF-0150 | `risk_level` | Risk Level | Risk | Channel development | enum | low|medium|high |
| SF-0151 | `risk_score` | Risk Score | Risk | Channel development | number | Risk Score field value |
| SF-0152 | `admission_suggest` | Admission Suggest | Risk | Channel development | enum | pass|supplement|reject |
| SF-0153 | `order_id` | Order Id | Order | Orders / inventory / policy | string | Order Id field value |
| SF-0154 | `order_qty` | Order Qty | Order | Orders / inventory / policy | int | Order Qty field value |
| SF-0155 | `order_status` | Order Status | Order | Orders / inventory / policy | enum | Order Status field value |
| SF-0156 | `audit_result` | Audit Result | Order | Orders / inventory / policy | enum | Audit Result field value |
| SF-0157 | `wms_stock_qty` | Wms Stock Qty | Inventory | Orders / inventory / policy | int | Wms Stock Qty field value |
| SF-0158 | `wms_in_transit_qty` | Wms In Transit Qty | Inventory | Orders / inventory / policy | int | Wms In Transit Qty field value |
| SF-0159 | `store_stock_qty` | Store Stock Qty | Inventory | Orders / inventory / policy | int | Store Stock Qty field value |
| SF-0160 | `stock_days_cover` | Stock Days Cover | Inventory | Orders / inventory / policy | number | Stock Days Cover field value |
| SF-0161 | `stock_age_days` | Stock Age Days | Inventory | Orders / inventory / policy | int | Stock Age Days field value |
| SF-0162 | `inventory_turn_days` | Inventory Turn Days | Inventory | Orders / inventory / policy | number | Inventory Turn Days field value |
| SF-0163 | `shortage_days` | Shortage Days | Inventory | Orders / inventory / policy | int | Shortage Days field value |
| SF-0164 | `demand_daily_est` | Demand Daily Est | Inventory | Orders / inventory / policy | number | Demand Daily Est field value |
| SF-0165 | `lost_units_est` | Lost Units Est | Inventory | Orders / inventory / policy | int | Lost Units Est field value |
| SF-0166 | `lost_gmv_est` | Lost Gmv Est | Inventory | Orders / inventory / policy | number | Lost Gmv Est field value |
| SF-0167 | `lost_margin_est` | Lost Margin Est | Inventory | Orders / inventory / policy | number | Lost Margin Est field value |
| SF-0168 | `shortage_root_cause` | Shortage Root Cause | Inventory | Orders / inventory / policy | enum | Shortage Root Cause field value |
| SF-0169 | `replenish_qty_suggest` | Replenish Qty Suggest | Inventory | Orders / inventory / policy | int | Replenish Qty Suggest field value |
| SF-0170 | `eta_date` | Eta Date | Inventory | Orders / inventory / policy | date | Eta Date field value |
| SF-0171 | `policy_version` | Policy Version | Policy | Orders / inventory / policy | string | Policy Version field value |
| SF-0172 | `current_rebate_tier` | Current Rebate Tier | Policy | Orders / inventory / policy | string | Current Rebate Tier field value |
| SF-0173 | `current_pickup_qty_mtd` | Current Pickup Qty Mtd | Policy | Orders / inventory / policy | int | Current Pickup Qty Mtd field value |
| SF-0174 | `qty_to_next_tier` | Qty To Next Tier | Policy | Orders / inventory / policy | int | Qty To Next Tier field value |
| SF-0175 | `next_tier_name` | Next Tier Name | Policy | Orders / inventory / policy | string | Next Tier Name field value |
| SF-0176 | `next_tier_rebate_amt` | Next Tier Rebate Amt | Policy | Orders / inventory / policy | number | Next Tier Rebate Amt field value |
| SF-0177 | `rebate_rate` | Rebate Rate | Policy | Orders / inventory / policy | number | Rebate Rate field value |
| SF-0178 | `color_bonus_amt` | Color Bonus Amt | Policy | Orders / inventory / policy | number | Color Bonus Amt field value |
| SF-0179 | `clawback_amt` | Clawback Amt | Policy | Orders / inventory / policy | number | Clawback Amt field value |
| SF-0180 | `payable_amt` | Payable Amt | Policy | Orders / inventory / policy | number | Payable Amt field value |
| SF-0181 | `settlement_id` | Settlement Id | Policy | Orders / inventory / policy | string | Settlement Id field value |
| SF-0182 | `pay_status` | Pay Status | Policy | Orders / inventory / policy | enum | unpaid|paid|exception |
| SF-0183 | `color_plan_week` | Color Plan Week | ColorPlan | Orders / inventory / policy | string | Color Plan Week field value |
| SF-0184 | `color_plan_qty` | Color Plan Qty | ColorPlan | Orders / inventory / policy | int | Color Plan Qty field value |
| SF-0185 | `retail_qty` | Retail Qty | Retail | Retail / marketing | int | Retail Qty field value |
| SF-0186 | `retail_qty_day` | Retail Qty Day | Retail | Retail / marketing | int | Retail Qty Day field value |
| SF-0187 | `retail_qty_mtd` | Retail Qty Mtd | Retail | Retail / marketing | int | Retail Qty Mtd field value |
| SF-0188 | `retail_yoy` | Retail Yoy | Retail | Retail / marketing | number | Retail Yoy field value |
| SF-0189 | `writeoff_qty` | Writeoff Qty | Retail | Retail / marketing | int | Writeoff Qty field value |
| SF-0190 | `redeem_rate` | Redeem Rate | Retail | Retail / marketing | number | Redeem Rate field value |
| SF-0191 | `gross_margin_amt` | Gross Margin Amt | Retail | Retail / marketing | number | Gross Margin Amt field value |
| SF-0192 | `gross_margin_rate` | Gross Margin Rate | Retail | Retail / marketing | number | Gross Margin Rate field value |
| SF-0193 | `non_exclusive_rate` | Non Exclusive Rate | Retail | Retail / marketing | number | Non Exclusive Rate field value |
| SF-0194 | `non_exclusive_flag` | Non Exclusive Flag | Retail | Retail / marketing | boolean | Non Exclusive Flag field value |
| SF-0195 | `campaign_id` | Campaign Id | Campaign | Retail / marketing | string | Campaign Id field value |
| SF-0196 | `campaign_name` | Campaign Name | Campaign | Retail / marketing | string | Campaign Name field value |
| SF-0197 | `campaign_goal` | Campaign Goal | Campaign | Retail / marketing | string | Campaign Goal field value |
| SF-0198 | `campaign_budget` | Campaign Budget | Campaign | Retail / marketing | number | Campaign Budget field value |
| SF-0199 | `participants` | Participants | Campaign | Retail / marketing | int | Participants field value |
| SF-0200 | `campaign_roi` | Campaign Roi | Campaign | Retail / marketing | number | Campaign Roi field value |
| SF-0201 | `campaign_complaint_rate` | Campaign Complaint Rate | Campaign | Retail / marketing | number | Campaign Complaint Rate field value |
| SF-0202 | `short_video_cnt` | Short Video Cnt | Content | Retail / marketing | int | Short Video Cnt field value |
| SF-0203 | `short_video_valid_participate_rate` | Short Video Valid Participate Rate | Content | Retail / marketing | number | Short Video Valid Participate Rate field value |
| SF-0204 | `followers` | Followers | Content | Retail / marketing | int | Followers field value |
| SF-0205 | `play_cnt` | Play Cnt | Content | Retail / marketing | int | Play Cnt field value |
| SF-0206 | `gmv_convert_rate` | Gmv Convert Rate | Content | Retail / marketing | number | Gmv Convert Rate field value |
| SF-0207 | `deals_cnt` | Deals Cnt | Content | Retail / marketing | int | Deals Cnt field value |
| SF-0208 | `gmv` | Gmv | Content | Retail / marketing | number | Gmv field value |
| SF-0209 | `aov` | Aov | Content | Retail / marketing | number | Aov field value |
| SF-0210 | `valid_seller_flag` | Valid Seller Flag | Content | Retail / marketing | boolean | Valid Seller Flag field value |
| SF-0211 | `live_sessions` | Live Sessions | Content | Retail / marketing | int | Live Sessions field value |
| SF-0212 | `live_watch_uv` | Live Watch Uv | Content | Retail / marketing | int | Live Watch Uv field value |
| SF-0213 | `influencer_cvr` | Influencer Cvr | Content | Retail / marketing | number | Influencer Cvr field value |
| SF-0214 | `refund_rate` | Refund Rate | Content | Retail / marketing | number | Refund Rate field value |
| SF-0215 | `content_script_id` | Content Script Id | Content | Retail / marketing | string | Content Script Id field value |
| SF-0216 | `benchmark_case_id` | Benchmark Case Id | Content | Retail / marketing | string | Benchmark Case Id field value |
| SF-0217 | `channel_quota_daily` | Channel Quota Daily | Outreach | Retail / marketing | int | Channel Quota Daily field value |
| SF-0218 | `delivery_rate` | Delivery Rate | Outreach | Retail / marketing | number | Delivery Rate field value |
| SF-0219 | `open_rate` | Open Rate | Outreach | Retail / marketing | number | Open Rate field value |
| SF-0220 | `connect_rate` | Connect Rate | Outreach | Retail / marketing | number | Connect Rate field value |
| SF-0221 | `transfer_human_cnt` | Transfer Human Cnt | Outreach | Retail / marketing | int | Transfer Human Cnt field value |
| SF-0222 | `template_approve_days` | Template Approve Days | Outreach | Retail / marketing | number | Template Approve Days field value |
| SF-0223 | `ticket_id` | Ticket Id | Ticket | Tickets / service | string | Ticket Id field value |
| SF-0224 | `ticket_type` | Ticket Type | Ticket | Tickets / service | enum | fault|consult|complaint|other |
| SF-0225 | `fault_category` | Fault Category | Ticket | Tickets / service | enum | Fault Category field value |
| SF-0226 | `consult_category` | Consult Category | Ticket | Tickets / service | string | Consult Category field value |
| SF-0227 | `ticket_channel` | Ticket Channel | Ticket | Tickets / service | string | Ticket Channel field value |
| SF-0228 | `ticket_status` | Ticket Status | Ticket | Tickets / service | enum | open|processing|closed |
| SF-0229 | `ticket_created_at` | Ticket Created At | Ticket | Tickets / service | datetime | Ticket Created At field value |
| SF-0230 | `handle_duration_min` | Handle Duration Min | Ticket | Tickets / service | number | Handle Duration Min field value |
| SF-0231 | `is_complaint` | Is Complaint | Ticket | Tickets / service | boolean | Is Complaint field value |
| SF-0232 | `three_guarantees_reject_flag` | Three Guarantees Reject Flag | Ticket | Tickets / service | boolean | Three Guarantees Reject Flag field value |
| SF-0233 | `desc_text` | Desc Text | Ticket | Tickets / service | text | Desc Text field value |
| SF-0234 | `desc_chars` | Desc Chars | Ticket | Tickets / service | int | Desc Chars field value |
| SF-0235 | `transcript_text` | Transcript Text | Ticket | Tickets / service | text | Transcript Text field value |
| SF-0236 | `agent_id` | Agent Id | Ticket | Tickets / service | string | Agent Id field value |
| SF-0237 | `sop_item` | Sop Item | Ticket | Tickets / service | string | Sop Item field value |
| SF-0238 | `sop_pass_fail` | Sop Pass Fail | Ticket | Tickets / service | enum | pass|fail |
| SF-0239 | `risk_words` | Risk Words | Ticket | Tickets / service | json | Risk Words field value |
| SF-0240 | `feedback_id` | Feedback Id | VoC | Tickets / service | string | Feedback Id field value |
| SF-0241 | `nps` | NPS | VoC | Tickets / service | number | NPS field value |
| SF-0242 | `csat` | CSAT | VoC | Tickets / service | number | CSAT field value |
| SF-0243 | `nps_delta` | Nps Delta | VoC | Tickets / service | number | Nps Delta field value |
| SF-0244 | `feedback_cnt` | Feedback Cnt | VoC | Tickets / service | int | Feedback Cnt field value |
| SF-0245 | `tag_id` | Tag Id | VoC | Tickets / service | string | Tag Id field value |
| SF-0246 | `tag_name` | Tag Name | VoC | Tickets / service | string | Tag Name field value |
| SF-0247 | `tag_domain` | Tag Domain | VoC | Tickets / service | enum | product|service|app|channel|risk |
| SF-0248 | `sentiment` | Sentiment | VoC | Tickets / service | enum | pos|neu|neg |
| SF-0249 | `sentiment_score` | Sentiment Score | VoC | Tickets / service | number | Sentiment Score field value |
| SF-0250 | `problem_theme` | Problem Theme | VoC | Tickets / service | string | Problem Theme field value |
| SF-0251 | `theme_cnt` | Theme Cnt | VoC | Tickets / service | int | Theme Cnt field value |
| SF-0252 | `neg_ratio` | Neg Ratio | VoC | Tickets / service | number | Neg Ratio field value |
| SF-0253 | `wow_change` | Wow Change | VoC | Tickets / service | number | Wow Change field value |
| SF-0254 | `closed_loop_rate` | Closed Loop Rate | VoC | Tickets / service | number | Closed Loop Rate field value |
| SF-0255 | `recurrence_rate` | Recurrence Rate | VoC | Tickets / service | number | Recurrence Rate field value |
| SF-0256 | `cover_dim` | Cover Dim | VoC | Tickets / service | enum | vehicle|non_vehicle|all |
| SF-0257 | `module_name` | Module Name | VoC | Tickets / service | enum | app|miniapp|website|hotline|aftersales |
| SF-0258 | `sample_voice` | Sample Voice | VoC | Tickets / service | text | Sample Voice field value |
| SF-0259 | `clue_confidence` | Clue Confidence | VoC | Tickets / service | enum | weak|medium |
| SF-0260 | `severity_risk_level` | Severity Risk Level | VoC | Tickets / service | enum | P0|P1|P2 |
| SF-0261 | `consumer_sat_score` | Consumer Sat Score | VoC | Tickets / service | number | Consumer Sat Score field value |
| SF-0262 | `channel_sat_score` | Channel Sat Score | VoC | Tickets / service | number | Channel Sat Score field value |
| SF-0263 | `survey_recover_rate` | Survey Recover Rate | VoC | Tickets / service | number | Survey Recover Rate field value |
| SF-0264 | `dissatisfaction_reason` | Dissatisfaction Reason | VoC | Tickets / service | string | Dissatisfaction Reason field value |
| SF-0265 | `fault_code` | Fault Code | Telemetry | Connectivity / IoT | string | Fault Code field value |
| SF-0266 | `iot_alert_cnt` | Iot Alert Cnt | Telemetry | Connectivity / IoT | int | Iot Alert Cnt field value |
| SF-0267 | `mileage_km` | Mileage Km | Telemetry | Connectivity / IoT | number | Mileage Km field value |
| SF-0268 | `soc_pct` | Soc Pct | Telemetry | Connectivity / IoT | number | Soc Pct field value |
| SF-0269 | `telemetry_coverage_rate` | Telemetry Coverage Rate | Telemetry | Connectivity / IoT | number | Telemetry Coverage Rate field value |
| SF-0270 | `battery_health_pct` | Battery Health Pct | Telemetry | Connectivity / IoT | number | Battery Health Pct field value |
| SF-0271 | `test_station` | Test Station | Quality | Manufacturing quality | string | Test Station field value |
| SF-0272 | `test_ts` | Test Ts | Quality | Manufacturing quality | datetime | Test Ts field value |
| SF-0273 | `obd_protocol` | Obd Protocol | Quality | Manufacturing quality | string | Obd Protocol field value |
| SF-0274 | `voltage_v` | Voltage V | Quality | Manufacturing quality | number | Voltage V field value |
| SF-0275 | `current_a` | Current A | Quality | Manufacturing quality | number | Current A field value |
| SF-0276 | `speed_rpm` | Speed Rpm | Quality | Manufacturing quality | number | Speed Rpm field value |
| SF-0277 | `controller_temp_c` | Controller Temp C | Quality | Manufacturing quality | number | Controller Temp C field value |
| SF-0278 | `qc_result` | Qc Result | Quality | Manufacturing quality | enum | pass|fail |
| SF-0279 | `operator_id` | Operator Id | Quality | Manufacturing quality | string | Operator Id field value |
| SF-0280 | `part_name` | Part Name | Quality | Manufacturing quality | string | Part Name field value |
| SF-0281 | `part_batch_no` | Part Batch No | Quality | Manufacturing quality | string | Part Batch No field value |
| SF-0282 | `supplier_id` | Supplier Id | Quality | Manufacturing quality | string | Supplier Id field value |
| SF-0283 | `delta_e` | Delta E | Quality | Manufacturing quality | number | Delta E field value |
| SF-0284 | `gloss` | Gloss | Quality | Manufacturing quality | number | Gloss field value |
| SF-0285 | `defect_type` | Defect Type | Quality | Manufacturing quality | string | Defect Type field value |
| SF-0286 | `anomaly_score` | Anomaly Score | Quality | Manufacturing quality | number | Anomaly Score field value |
| SF-0287 | `predict_fail_days` | Predict Fail Days | Quality | Manufacturing quality | int | Predict Fail Days field value |
| SF-0288 | `release_ts` | Release Ts | Quality | Manufacturing quality | datetime | Release Ts field value |
| SF-0289 | `trace_package_url` | Trace Package Url | Quality | Manufacturing quality | string | Trace Package Url field value |
| SF-0290 | `recall_level` | Recall Level | Quality | Manufacturing quality | enum | watch|targeted|recall_eval |
| SF-0291 | `inspect_id` | Inspect Id | Inspection | Inspection / compliance | string | Inspect Id field value |
| SF-0292 | `inspect_time` | Inspect Time | Inspection | Inspection / compliance | datetime | Inspect Time field value |
| SF-0293 | `check_item` | Check Item | Inspection | Inspection / compliance | string | Check Item field value |
| SF-0294 | `ai_confidence` | Ai Confidence | Inspection | Inspection / compliance | number | Ai Confidence field value |
| SF-0295 | `pass_fail` | Pass Fail | Inspection | Inspection / compliance | enum | pass|fail |
| SF-0296 | `photo_url` | Photo Url | Inspection | Inspection / compliance | string | Photo Url field value |
| SF-0297 | `morning_photo_url` | Morning Photo Url | Inspection | Inspection / compliance | string | Morning Photo Url field value |
| SF-0298 | `evening_photo_url` | Evening Photo Url | Inspection | Inspection / compliance | string | Evening Photo Url field value |
| SF-0299 | `competitor_logo_detected` | Competitor Logo Detected | Inspection | Inspection / compliance | json | Competitor Logo Detected field value |
| SF-0300 | `suspect_type` | Suspect Type | Inspection | Inspection / compliance | string | Suspect Type field value |
| SF-0301 | `vi_score` | Vi Score | Inspection | Inspection / compliance | number | Vi Score field value |
| SF-0302 | `rectify_ticket_id` | Rectify Ticket Id | Inspection | Inspection / compliance | string | Rectify Ticket Id field value |
| SF-0303 | `due_date` | Due Date | Inspection | Inspection / compliance | date | Due Date field value |
| SF-0304 | `mention_cnt_24h` | Mention Cnt 24h | Brand | Inspection / compliance | int | Mention Cnt 24h field value |
| SF-0305 | `reputation_score` | Reputation Score | Brand | Inspection / compliance | number | Reputation Score field value |
| SF-0306 | `hotspot_term` | Hotspot Term | Brand | Inspection / compliance | string | Hotspot Term field value |
| SF-0307 | `growth_velocity` | Growth Velocity | Brand | Inspection / compliance | number | Growth Velocity field value |
| SF-0308 | `mi_consistency_score` | Mi Consistency Score | Brand | Inspection / compliance | number | Mi Consistency Score field value |
| SF-0309 | `bvp_memorability` | Bvp Memorability | Brand | Inspection / compliance | number | Bvp Memorability field value |
| SF-0310 | `bvp_understanding` | Bvp Understanding | Brand | Inspection / compliance | number | Bvp Understanding field value |
| SF-0311 | `purchase_intent` | Purchase Intent | Brand | Inspection / compliance | number | Purchase Intent field value |
| SF-0312 | `energy_kwh_per_vehicle` | Energy Kwh Per Vehicle | Brand | Inspection / compliance | number | Energy Kwh Per Vehicle field value |
| SF-0313 | `co2e_t` | Co2e T | Brand | Inspection / compliance | number | Co2e T field value |
| SF-0314 | `scrap_battery_recycle_rate` | Scrap Battery Recycle Rate | Brand | Inspection / compliance | number | Scrap Battery Recycle Rate field value |
| SF-0315 | `expense_id` | Expense Id | Finance | Finance | string | Expense Id field value |
| SF-0316 | `invoice_no` | Invoice No | Finance | Finance | string | Invoice No field value |
| SF-0317 | `po_no` | Po No | Finance | Finance | string | Po No field value |
| SF-0318 | `receipt_amt` | Receipt Amt | Finance | Finance | number | Receipt Amt field value |
| SF-0319 | `invoice_amt` | Invoice Amt | Finance | Finance | number | Invoice Amt field value |
| SF-0320 | `po_amt` | Po Amt | Finance | Finance | number | Po Amt field value |
| SF-0321 | `match_status` | Match Status | Finance | Finance | enum | match|mismatch |
| SF-0322 | `diff_amt` | Diff Amt | Finance | Finance | number | Diff Amt field value |
| SF-0323 | `diff_reason` | Diff Reason | Finance | Finance | string | Diff Reason field value |
| SF-0324 | `revenue_forecast` | Revenue Forecast | Finance | Finance | number | Revenue Forecast field value |
| SF-0325 | `pickup_forecast_units` | Pickup Forecast Units | Finance | Finance | int | Pickup Forecast Units field value |
| SF-0326 | `rebate_cashout_forecast` | Rebate Cashout Forecast | Finance | Finance | number | Rebate Cashout Forecast field value |
| SF-0327 | `opex_forecast` | Opex Forecast | Finance | Finance | number | Opex Forecast field value |
| SF-0328 | `net_cash_forecast` | Net Cash Forecast | Finance | Finance | number | Net Cash Forecast field value |
| SF-0329 | `forecast_confidence_low` | Forecast Confidence Low | Finance | Finance | number | Forecast Confidence Low field value |
| SF-0330 | `forecast_confidence_high` | Forecast Confidence High | Finance | Finance | number | Forecast Confidence High field value |
| SF-0331 | `cum_sales_units` | Cum Sales Units | Activation | App activation | int | Cum Sales Units field value |
| SF-0332 | `active_owners_est` | Active Owners Est | Activation | App activation | int | Active Owners Est field value |
| SF-0333 | `app_register_cnt` | App Register Cnt | Activation | App activation | int | App Register Cnt field value |
| SF-0334 | `bind_vehicle_cnt` | Bind Vehicle Cnt | Activation | App activation | int | Bind Vehicle Cnt field value |
| SF-0335 | `mau` | Mau | Activation | App activation | int | Mau field value |
| SF-0336 | `dau` | Dau | Activation | App activation | int | Dau field value |
| SF-0337 | `activation_rate` | Activation Rate | Activation | App activation | number | Activation Rate field value |
| SF-0338 | `funnel_step` | Funnel Step | Activation | App activation | string | Funnel Step field value |
| SF-0339 | `funnel_uv` | Funnel Uv | Activation | App activation | int | Funnel Uv field value |
| SF-0340 | `funnel_cvr` | Funnel Cvr | Activation | App activation | number | Funnel Cvr field value |
| SF-0341 | `tab_name` | Tab Name | Activation | App activation | string | Tab Name field value |
| SF-0342 | `pv` | PV | Activation | App activation | int | PV field value |
| SF-0343 | `uv` | UV | Activation | App activation | int | UV field value |
| SF-0344 | `stay_seconds` | Stay Seconds | Activation | App activation | number | Stay Seconds field value |
| SF-0345 | `push_click_rate` | Push Click Rate | Activation | App activation | number | Push CTR |
| SF-0346 | `faq_cnt` | Faq Cnt | Activation | App activation | int | Faq Cnt field value |
| SF-0347 | `top20_ticket_coverage_rate` | Top20 Ticket Coverage Rate | Activation | App activation | number | Top20 Ticket Coverage Rate field value |
| SF-0348 | `oneid_coverage_rate` | Oneid Coverage Rate | Activation | App activation | number | Oneid Coverage Rate field value |
| SF-0349 | `orphan_user_cnt` | Orphan User Cnt | Activation | App activation | int | Orphan User Cnt field value |
| SF-0350 | `koc_score` | Koc Score | Activation | App activation | number | Koc Score field value |
| SF-0351 | `post_cnt` | Post Cnt | Activation | App activation | int | Post Cnt field value |
| SF-0352 | `interact_rate` | Interact Rate | Activation | App activation | number | Interact Rate field value |
| SF-0353 | `platform_order_cnt` | Platform Order Cnt | O2O | App activation | int | Platform Order Cnt field value |
| SF-0354 | `lead_phone_cnt` | Lead Phone Cnt | O2O | App activation | int | Lead Phone Cnt field value |
| SF-0355 | `store_redeem_cnt` | Store Redeem Cnt | O2O | App activation | int | Store Redeem Cnt field value |
| SF-0356 | `alert_id` | Alert Id | Alert | Alerts / coordination | string | Alert Id field value |
| SF-0357 | `alert_type` | Alert Type | Alert | Alerts / coordination | enum | Alert Type field value |
| SF-0358 | `metric_name` | Metric Name | Alert | Alerts / coordination | string | Metric Name field value |
| SF-0359 | `metric_value` | Metric Value | Alert | Alerts / coordination | number | Metric Value field value |
| SF-0360 | `threshold_value` | Threshold Value | Alert | Alerts / coordination | number | Threshold Value field value |
| SF-0361 | `severity` | Severity | Alert | Alerts / coordination | enum | P0|P1|P2 |
| SF-0362 | `required_action` | Required Action | Alert | Alerts / coordination | string | Required Action field value |
| SF-0363 | `verify_method` | Verify Method | Alert | Alerts / coordination | string | Verify Method field value |
| SF-0364 | `cross_issue_cnt` | Cross Issue Cnt | Collab | Alerts / coordination | int | Cross Issue Cnt field value |
| SF-0365 | `closed_cnt` | Closed Cnt | Collab | Alerts / coordination | int | Closed Cnt field value |
| SF-0366 | `overdue_cnt` | Overdue Cnt | Collab | Alerts / coordination | int | Overdue Cnt field value |
| SF-0367 | `response_hours` | Response Hours | Collab | Alerts / coordination | number | Response Hours field value |
| SF-0368 | `pilot_vs_control_delta` | Pilot Vs Control Delta | Collab | Alerts / coordination | number | Pilot Vs Control Delta field value |
| SF-0369 | `resolution_id` | Resolution Id | Collab | Alerts / coordination | string | Resolution Id field value |
| SF-0370 | `owner_dept` | Owner Dept | Collab | Alerts / coordination | string | Owner Dept field value |
| SF-0371 | `verify_metric` | Verify Metric | Collab | Alerts / coordination | string | Verify Metric field value |
| SF-0372 | `ai_output_id` | AI outputID | AIOutput | Shared AI assets | string | AI outputID field value |
| SF-0373 | `producer_skill` | Producer Skill | AIOutput | Shared AI assets | string | Producer Skill field value |
| SF-0374 | `consumer_allow` | Consumer Allow | AIOutput | Shared AI assets | json | Consumer Allow field value |
| SF-0375 | `payload` | Payload | AIOutput | Shared AI assets | json | Payload field value |
| SF-0376 | `payload_schema` | Payload Schema | AIOutput | Shared AI assets | string | Payload Schema field value |
| SF-0377 | `tag_vocab_version` | Tag Vocab Version | TagVocabulary | Shared AI assets | string | Tag Vocab Version field value |
| SF-0378 | `tag_parent_id` | Tag Parent Id | TagVocabulary | Shared AI assets | string | Tag Parent Id field value |
| SF-0379 | `skill_id` | Skill ID | CapabilityCatalog | Shared AI assets | string | Skill ID field value |
| SF-0380 | `skill_desc` | Skill Desc | CapabilityCatalog | Shared AI assets | text | Skill Desc field value |
| SF-0381 | `input_schema` | Input Schema | CapabilityCatalog | Shared AI assets | json | Input Schema field value |
| SF-0382 | `output_schema` | Output Schema | CapabilityCatalog | Shared AI assets | json | Output Schema field value |
| SF-0383 | `allowed_tools` | Allowed Tools | CapabilityCatalog | Shared AI assets | json | Allowed Tools field value |
| SF-0384 | `step_name` | Step Name | RunLog | Shared AI assets | string | Step Name field value |
| SF-0385 | `step_status` | Step Status | RunLog | Shared AI assets | enum | ok|error|skipped |
| SF-0386 | `step_ts` | Step Ts | RunLog | Shared AI assets | datetime | Step Ts field value |
| SF-0387 | `process_id` | Process Id | Process | Process / HR / legal | string | Process Id field value |
| SF-0388 | `redundant_step` | Redundant Step | Process | Process / HR / legal | string | Redundant Step field value |
| SF-0389 | `bottleneck_step` | Bottleneck Step | Process | Process / HR / legal | string | Bottleneck Step field value |
| SF-0390 | `cycle_time_hours` | Cycle Time Hours | Process | Process / HR / legal | number | Cycle Time Hours field value |
| SF-0391 | `proposal_level` | Proposal Level | Process | Process / HR / legal | enum | L1|L2|L3 |
| SF-0392 | `job_id` | Job Id | HR | Process / HR / legal | string | Job Id field value |
| SF-0393 | `match_score` | Match Score | HR | Process / HR / legal | number | Match Score field value |
| SF-0394 | `contract_id` | Contract Id | Legal | Process / HR / legal | string | Contract Id field value |
| SF-0395 | `clause_risk_level` | Clause Risk Level | Legal | Process / HR / legal | enum | low|medium|high |
| SF-0396 | `clause_comment` | Clause Comment | Legal | Process / HR / legal | text | Clause Comment field value |
| SF-0397 | `kb_domain` | Kb Domain | Knowledge | Process / HR / legal | enum | repair|policy|hr|product |
| SF-0398 | `kb_doc_id` | Kb Doc Id | Knowledge | Process / HR / legal | string | Kb Doc Id field value |
| SF-0399 | `kb_chunk_id` | Kb Chunk Id | Knowledge | Process / HR / legal | string | Kb Chunk Id field value |
| SF-0400 | `kb_score` | Kb Score | Knowledge | Process / HR / legal | number | Kb Score field value |
