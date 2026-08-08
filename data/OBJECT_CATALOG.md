# Entity Catalog (Structured)

> Qingshu Mobility · Demo synthetic data directory  
> Scope: classified by noun / entity, not by department; all departments share the same IDs.

## A. Master Data

| Object | File | Description |
|------|------|------|
| Org / Region | `entities/orgs.json`, `entities/regions.json` | Org tree and admin regions |
| Dealer | `entities/dealers.json` | Tier-1 dealers |
| Store | `entities/stores.json` | Stores |
| Guide | `entities/guides.json` | Sales guides |
| Customer | `entities/customers.json` | End customers / identity |
| Vehicle | `entities/vehicles.json` | Vehicles (VINs all synthetic `QS0…`) |
| SKU | `entities/skus.json` | Model-color SKUs |
| Competitor | `entities/competitors.json` | Competitor snapshots (fictional brands) |

## B. Transactions & Inventory

| Object | File | Description |
|------|------|------|
| Order | `entities/orders.json` | Pickup / orders |
| Inventory | `entities/inventory.json` | Warehouse / store stock |
| Policy | `entities/policies.json` | Rebate policies and settlement summary |
| ColorPlan | `entities/color_plans.json` | Color production plans |
| SalesMetric | `entities/sales_metrics.json` | Sales / contract achievement slices |
| Health | `entities/dealer_health.json` | Tier-1 business health index |

## C. Service & Voice of Customer

| Object | File | Description |
|------|------|------|
| Ticket | `entities/tickets.json` | Service tickets |
| VoC | `entities/voc_feedback.json` | Feedback / survey slices |
| Telemetry | `entities/telemetry.json` | Connectivity alerts and range/battery |
| Renewal | `entities/renewals.json` | Connectivity renewal pool |
| UserBehavior | `entities/user_behaviors.json` | App behavior / RFM |

## D. Retail Marketing & Outreach

| Object | File | Description |
|------|------|------|
| Retail | `entities/retail_daily.json` | Store daily retail slices |
| Campaign | `entities/campaigns.json` | Campaigns |
| Content | `entities/contents.json` | Social / content account performance |
| Outreach | `entities/outreach.json` | Outreach channel capabilities |

## E. Quality / Inspection / Finance (Extended Master)

| Object | File | Description |
|------|------|------|
| Quality | `entities/quality_checks.json` | OBD / QC records |
| Inspection | `entities/inspections.json` | Store inspections |
| Finance | `entities/finance_expense.json` | Three-way match samples |
| Alert | `entities/alerts.json` | Business alerts |
| StoreDev / Risk | `entities/store_dev.json`, `entities/risks.json` | Store opening and risk control |

## F. Shared Semantics & AI Assets

| Object | File | Description |
|------|------|------|
| TagVocabulary | `vocab/tag_vocabulary.json` | Unified tag dictionary |
| FieldGlossary | `vocab/field_glossary.json` | Cross-department field definitions |
| CapabilityCatalog | `entities/capability_catalog.json` | Skill capability catalog skeleton |
| Knowledge | `knowledge/**` | Unstructured long text (repair / policy / HR) |

## G. Demo Seeds

| Object | File | Description |
|------|------|------|
| Story seeds | `seeds/story_1_fill_ticket.json`, `seeds/story_2_renewal_block.json` | Story1/2 inputs |

## Join Keys (Unified)

`customer_id` · `vin` · `dealer_id` · `store_id` · `sku_id` · `ticket_id` · `order_id` · `tag_id` · `campaign_id` · `oneid`
