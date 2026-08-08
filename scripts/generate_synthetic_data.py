#!/usr/bin/env python3
"""Generate Qingshu Mobility demo synthetic data (entities / vocab / knowledge / seeds).

Compliance:
- Never write real customers, VINs, phone numbers, or OEM internal data
- VINs use QS0 prefix for synthetic frames
- Phones stored masked only; deterministic pseudo-random, not real ranges
- Run: `python scripts/generate_synthetic_data.py`
"""

from __future__ import annotations

import hashlib
import json
import random
import string
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
SEED = 20260801  # reproducible; change seed for a new batch

rng = random.Random(SEED)

MODELS = [
    "E40", "E60", "E80", "S7", "S9", "C3", "M1 Pro", "CityGo", "TrailX", "LiteAir",
]
COLORS = ["Matte Black", "Stellar Grey", "Arctic White", "Flame Red", "Mint Green", "Midnight Blue", "Sand Gold"]
CONFIGS = ["Standard lead-acid", "Comfort lithium", "Flagship lithium", "Graphene range edition"]
BATTERY = [
    ("lithium", "48V24Ah", 80),
    ("lithium", "48V32Ah", 100),
    ("lead_acid", "48V20Ah", 55),
    ("graphene", "48V24Ah", 90),
]
CITIES = [
    ("Jiangsu", "Nanjing", "320115", "Jiangning District"),
    ("Jiangsu", "Suzhou", "320505", "Huqiu District"),
    ("Zhejiang", "Hangzhou", "330106", "Xihu District"),
    ("Zhejiang", "Ningbo", "330212", "Yinzhou District"),
    ("Anhui", "Hefei", "340104", "Shushan District"),
    ("Shandong", "Jinan", "370102", "Lixia District"),
    ("Sichuan", "Chengdu", "510107", "Wuhou District"),
    ("Guangdong", "Guangzhou", "440106", "Tianhe District"),
]
SURNAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Wilson", "Moore", "Taylor", "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", "Thompson", "Lee", "Chen"]
GIVEN = [
    "Alex", "Jordan", "Taylor", "Morgan", "Casey", "Riley", "Avery", "Quinn", "Skyler", "Jamie",
    "Blake", "Cameron", "Drew", "Emery", "Finley", "Harper", "Jesse", "Kai", "Logan", "Parker",
]


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def fake_name() -> str:
    return rng.choice(SURNAMES) + rng.choice(GIVEN)


def fake_phone_masked() -> str:
    """Return a masked phone; middle four digits are always ****."""
    prefix = "1" + rng.choice(list("35789")) + str(rng.randint(0, 9))
    suffix = f"{rng.randint(0, 9999):04d}"
    return f"{prefix}****{suffix}"


def fake_vin(seq: int) -> str:
    """Synthetic VIN: QS0 + pseudo-random body, length 17, not a real OEM prefix."""
    body = hashlib.sha256(f"qingshu-vin-{SEED}-{seq}".encode()).hexdigest()[:14].upper()
    body = body.replace("O", "A").replace("I", "B")
    vin = ("QS0" + body)[:17]
    assert len(vin) == 17
    return vin


def fake_openid(seq: int) -> str:
    return "qs_oid_" + hashlib.md5(f"openid-{SEED}-{seq}".encode()).hexdigest()[:16]


def fake_oneid(seq: int) -> str:
    return "OID-" + hashlib.md5(f"oneid-{SEED}-{seq}".encode()).hexdigest()[:8]


def daterange_back(days_max: int = 800) -> date:
    return date(2026, 8, 1) - timedelta(days=rng.randint(30, days_max))


def iso(dt: datetime) -> str:
    return dt.astimezone(timezone(timedelta(hours=8))).isoformat()


# ---------------------------------------------------------------------------
# 1)
# ---------------------------------------------------------------------------

def write_object_catalog() -> None:
    text = """# Object catalog (structured)

> Qingshu Mobility · Demo synthetic data directory  
> Grouped by noun objects / entities, not by department; all departments share the same IDs.

## A. Master data

| Object | File | Notes |
|------|------|------|
| Org / Region | `entities/orgs.json`, `entities/regions.json` | Org tree and admin regions |
| Dealer | `entities/dealers.json` | Tier-1 dealers |
| Store | `entities/stores.json` | Retail stores |
| Guide | `entities/guides.json` | Store guides |
| Customer | `entities/customers.json` | End customers / identities |
| Vehicle | `entities/vehicles.json` | Vehicles (VINs always synthetic `QS0…`) |
| SKU | `entities/skus.json` | Model-color SKUs |
| Competitor | `entities/competitors.json` | Competitor snapshots (fictional brands) |

## B. Transactional / inventory

| Object | File | Notes |
|------|------|------|
| Order | `entities/orders.json` | Pickup / orders |
| Inventory | `entities/inventory.json` | Warehouse / store inventory |
| Policy | `entities/policies.json` | Rebate policy and settlement summary |
| ColorPlan | `entities/color_plans.json` | Color production plan |
| SalesMetric | `entities/sales_metrics.json` | Sales / contract attainment slices |
| Health | `entities/dealer_health.json` | Tier-1 dealer health index |

## C. Service / VoC

| Object | File | Notes |
|------|------|------|
| Ticket | `entities/tickets.json` | Service tickets |
| VoC | `entities/voc_feedback.json` | Feedback / survey slices |
| Telemetry | `entities/telemetry.json` | IoT alerts, mileage, SOC |
| Renewal | `entities/renewals.json` | Connectivity renewal pool |
| UserBehavior | `entities/user_behaviors.json` | App behavior / RFM |

## D. Retail marketing / outreach

| Object | File | Notes |
|------|------|------|
| Retail | `entities/retail_daily.json` | Store retail daily slice |
| Campaign | `entities/campaigns.json` | Campaigns |
| Content | `entities/contents.json` | Content / channel account performance |
| Outreach | `entities/outreach.json` | Outreach channel capacity |

## E. Quality / inspection / finance (extended master)

| Object | File | Notes |
|------|------|------|
| Quality | `entities/quality_checks.json` | OBD / QC records |
| Inspection | `entities/inspections.json` | Store inspections |
| Finance | `entities/finance_expense.json` | Three-way match samples |
| Alert | `entities/alerts.json` | Business alerts |
| StoreDev / Risk | `entities/store_dev.json`, `entities/risks.json` | Store opening and risk |

## F. Shared semantics and AI assets

| Object | File | Notes |
|------|------|------|
| TagVocabulary | `vocab/tag_vocabulary.json` | Unified tag dictionary |
| FieldGlossary | `vocab/field_glossary.json` | Cross-department field meanings |
| CapabilityCatalog | `entities/capability_catalog.json` | Skill capability catalog skeleton |
| DepartmentFlows | `entities/department_flows.json` | Department flows (**manual**; not written by this script) |
| Knowledge | `knowledge/**` | Long-form docs (repair / policy / HR) |
| KnowledgeChunks | `knowledge/chunks.json` | RAG chunks (**`scripts/build_kb_chunks.py`**; not written here) |
| KnowledgeIndex | `knowledge/tfidf_index.json` | RAG TF-IDF index (**`scripts/build_kb_index.py`**; not written here) |

## G. Demo seeds

| Object | File | Notes |
|------|------|------|
| Story seeds | `seeds/story_1_fill_ticket.json`, `seeds/story_2_renewal_block.json` | Story1/2 inputs |

## Shared keys (global)

`customer_id` · `vin` · `dealer_id` · `store_id` · `sku_id` · `ticket_id` · `order_id` · `tag_id` · `campaign_id` · `oneid`
"""
    _write_text(DATA / "OBJECT_CATALOG.md", text)


# ---------------------------------------------------------------------------
# 2)
# ---------------------------------------------------------------------------

def write_field_glossary() -> None:
    """Build cross-department field glossary from docs/standard-field-glossary.csv."""
    import csv

    csv_path = ROOT / "docs" / "standard-field-glossary.csv"
    fields = []
    # Sanitize real OEM brand names in examples to fictional brands
    brand_sanitize = {
        "Yadea": "North Star Mobility",
        "Aima": "Cloud Shuttle Power",
        "Tailg": "Star Orbit Mobility",
        "Luyuan": "Qingshu",
    }
    with csv_path.open(encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            example = row["example"] or ""
            meaning = row["description"] or ""
            related = row["related_reports"] or ""
            for bad, good in brand_sanitize.items():
                example = example.replace(bad, good)
                meaning = meaning.replace(bad, good)
                related = related.replace(bad, good)
            fields.append({
                "field_id": row["field_id"],
                "field": row["field_name"],
                "cn": row["cn_name"],
                "entity": row["entity"],
                "domain": row["domain"],
                "data_type": row["data_type"],
                "unit": row["unit"],
                "example": example,
                "meaning": meaning,
                "related_reports": related,
            })

    principles = [
        {"rule": "One meaning, one name", "detail": "One business meaning maps to one field_name; no department-specific synonyms"},
        {"rule": "Masking first", "detail": "Phones use phone_masked only; VINs use QS0 synthetic prefix only"},
        {"rule": "Shared join keys", "detail": "customer_id/vin/dealer_id/store_id/sku_id/tag_id are global"},
        {"rule": "Department variance in Skills", "detail": "Scripts and decision tables live in Skills, not field forks"},
    ]
    _write_json(DATA / "vocab" / "field_glossary.json", {
        "version": "v1.1",
        "brand": "Qingshu Mobility",
        "principle": "Unify field names and meanings across departments; department differences belong in Skills",
        "source": "docs/standard-field-glossary.csv",
        "principles": principles,
        "fields": fields,
    })
    lines = [
        "# Cross-department field glossary",
        "",
        "> Synced with `field_glossary.json`; full set from `docs/standard-field-glossary.csv`.",
        "> Principle: field names and meanings must match no matter which department uses them.",
        "",
        "## Principles",
        "",
    ]
    for p in principles:
        lines.append(f"- **{p['rule']}**: {p['detail']}")
    lines += [
        "",
        f"## Field list ({len(fields)} entries)",
        "",
        "| ID | Field | CN label | Entity | Domain | Type | Meaning |",
        "|--------|--------|------|------|--------|------|------|",
    ]
    for g in fields:
        meaning = g["meaning"].replace("|", "\\|")
        lines.append(
            f"| {g['field_id']} | `{g['field']}` | {g['cn']} | {g['entity']} | {g['domain']} | {g['data_type']} | {meaning} |"
        )
    _write_text(DATA / "vocab" / "FIELD_GLOSSARY.md", "\n".join(lines))


# ---------------------------------------------------------------------------
# 3) Vocab tags
# ---------------------------------------------------------------------------

def build_vocab() -> list[dict]:
    version = "voc-tags-2026.08"
    tags = [
        ("TAG-ROOT-PRODUCT", "Vehicle experience", "product", None),
        ("TAG-short-range", "Short range", "product", "TAG-ROOT-PRODUCT"),
        ("TAG-weak-power", "Weak power", "product", "TAG-ROOT-PRODUCT"),
        ("TAG-noise", "Noise / suspension", "product", "TAG-ROOT-PRODUCT"),
        ("TAG-brake", "Brake issues", "product", "TAG-ROOT-PRODUCT"),
        ("TAG-slow-charging", "Slow charging", "product", "TAG-ROOT-PRODUCT"),
        ("TAG-controller-fault", "Controller fault", "product", "TAG-ROOT-PRODUCT"),
        ("TAG-battery-swelling", "Battery swelling / heat rise", "product", "TAG-ROOT-PRODUCT"),
        ("TAG-dashboard-blackout", "Dashboard blackout", "product", "TAG-ROOT-PRODUCT"),
        ("TAG-ROOT-SERVICE", "Service experience", "service", None),
        ("TAG-warranty-dispute", "Warranty dispute", "service", "TAG-ROOT-SERVICE"),
        ("TAG-slow-onsite-service", "Slow onsite repair", "service", "TAG-ROOT-SERVICE"),
        ("TAG-poor-attitude", "Service attitude", "service", "TAG-ROOT-SERVICE"),
        ("TAG-parts-stockout", "Parts stockout", "service", "TAG-ROOT-SERVICE"),
        ("TAG-ROOT-APP", "App / connectivity", "app", None),
        ("TAG-pairing-failure", "Pairing failure", "app", "TAG-ROOT-APP"),
        ("TAG-gps-drift", "Inaccurate location", "app", "TAG-ROOT-APP"),
        ("TAG-renewal-entry-hard-to-find", "Renewal entry hard to find", "app", "TAG-ROOT-APP"),
        ("TAG-push-spam", "Too many pushes", "app", "TAG-ROOT-APP"),
        ("TAG-ROOT-CHANNEL", "Channel / retail", "channel", None),
        ("TAG-non-exclusive-display", "Non-exclusive display", "channel", "TAG-ROOT-CHANNEL"),
        ("TAG-vi-violation", "VI violation", "channel", "TAG-ROOT-CHANNEL"),
        ("TAG-overstock-no-sales", "Overstock / no sell-through", "channel", "TAG-ROOT-CHANNEL"),
        ("TAG-ROOT-RISK", "Risk / sentiment", "risk", None),
        ("TAG-open-complaint", "Open complaint", "risk", "TAG-ROOT-RISK"),
        ("TAG-reputation-risk", "Reputation risk", "risk", "TAG-ROOT-RISK"),
        ("TAG-safety-hazard", "Safety hazard", "risk", "TAG-ROOT-RISK"),
    ]
    return [
        {
            "tag_id": tid,
            "tag_name": name,
            "tag_domain": domain,
            "tag_parent_id": parent,
            "tag_vocab_version": version,
        }
        for tid, name, domain, parent in tags
    ]


# ---------------------------------------------------------------------------
# Entities
# ---------------------------------------------------------------------------

def build_regions_orgs() -> tuple[list, list]:
    regions = []
    for i, (prov, city, code, county) in enumerate(CITIES):
        regions.append({
            "region_id": f"REG-{code}",
            "province": prov,
            "city": city,
            "county_code": code,
            "county_name": county,
        })
    orgs = [
        {"org_id": "NATION-CN", "org_name": "Qingshu Mobility - National", "org_level": "nation", "parent_org_id": None, "org_path": "National"},
        {"org_id": "WZ-EAST", "org_name": "East war zone", "org_level": "warzone", "parent_org_id": "NATION-CN", "org_path": "National/East"},
        {"org_id": "WZ-SOUTH", "org_name": "South war zone", "org_level": "warzone", "parent_org_id": "NATION-CN", "org_path": "National/South"},
        {"org_id": "WZ-WEST", "org_name": "West war zone", "org_level": "warzone", "parent_org_id": "NATION-CN", "org_path": "National/West"},
        {"org_id": "WZ-NORTH", "org_name": "North war zone", "org_level": "warzone", "parent_org_id": "NATION-CN", "org_path": "National/North"},
        {"org_id": "SZ-EAST-SN", "org_name": "East - South Jiangsu subzone", "org_level": "subzone", "parent_org_id": "WZ-EAST", "org_path": "National/East/South Jiangsu"},
        {"org_id": "SZ-EAST-ZJ", "org_name": "East - North Zhejiang subzone", "org_level": "subzone", "parent_org_id": "WZ-EAST", "org_path": "National/East/North Zhejiang"},
        {"org_id": "SZ-SOUTH-GD", "org_name": "South - Central Guangdong subzone", "org_level": "subzone", "parent_org_id": "WZ-SOUTH", "org_path": "National/South/Central GD"},
    ]
    return regions, orgs


def build_dealers_stores_guides(regions: list, n_dealers: int = 20) -> tuple[list, list, list]:
    dealers, stores, guides = [], [], []
    warzone_cycle = ["WZ-EAST", "WZ-EAST", "WZ-SOUTH", "WZ-WEST", "WZ-NORTH"]
    for i in range(1, n_dealers + 1):
        reg = regions[(i - 1) % len(regions)]
        did = f"DLR-{3000 + i}"
        dealers.append({
            "dealer_id": did,
            "dealer_name": f"Qingshu {reg['city']} Tier-1 dealer #{(i % 3) + 1}",
            "legal_person": fake_name(),
            "open_account_date": str(daterange_back(1500)),
            "developer_name": fake_name(),
            "org_id": warzone_cycle[(i - 1) % len(warzone_cycle)],
            "province": reg["province"],
            "city": reg["city"],
            "county_code": reg["county_code"],
        })
        for j in range(1, 3):
            sid = f"ST-{did[-4:]}{j}"
            st_type = rng.choice(["exclusive", "exclusive", "mixed", "non_exclusive"])
            stores.append({
                "store_id": sid,
                "store_name": f"Qingshu {reg['city']}{reg['county_name']}{' Exclusive' if st_type == 'exclusive' else ' Experience'} Store {j}",
                "store_address": f"{reg['province']}{reg['city']}{reg['county_name']} Demo Rd {rng.randint(1, 200)}",
                "store_type": st_type,
                "store_grade": rng.choice(["A", "B", "B", "C", "D"]),
                "store_area_sqm": float(rng.choice([80, 100, 120, 150, 200])),
                "biz_district": f"{reg['county_name']} business district",
                "dealer_id": did,
                "province": reg["province"],
                "city": reg["city"],
            })
            guides.append({
                "guide_id": f"GD-{sid[-5:]}",
                "store_id": sid,
                "channel_account_id": f"DY-{rng.randint(10000, 99999)}",
                "guide_name": fake_name(),
            })
    return dealers, stores, guides


def build_skus() -> list:
    skus = []
    for model in MODELS:
        for color in COLORS[:5]:
            color_code = {"Matte Black": "BK", "Stellar Grey": "GY", "Arctic White": "WH", "Flame Red": "RD", "Mint Green": "GN"}[color]
            sid = f"SKU-{model.replace(' ', '')}-{color_code}"
            asp = rng.choice([2599, 2999, 3299, 3599, 3999, 4299])
            skus.append({
                "sku_id": sid,
                "sku_name": f"{model} {color}",
                "vehicle_model": model,
                "color": color,
                "asp_cny": float(asp),
                "hot_slow_flag": rng.choice(["hot", "normal", "normal", "slow"]),
                "substitute_sku_id": None,
            })
    # wire substitutes for some reds -> grey
    by_model = {}
    for s in skus:
        by_model.setdefault(s["vehicle_model"], []).append(s)
    for model, items in by_model.items():
        red = next((x for x in items if x["color"] == "Flame Red"), None)
        grey = next((x for x in items if x["color"] == "Flame Red"), None)
        if red and grey:
            red["substitute_sku_id"] = grey["sku_id"]
    return skus


def build_competitors() -> list:
    brands = [
        ("Beichen Mobility", "Pulse X1", 3499, 0.22),
        ("CloudShuttle Power", "Yuno S", 3199, 0.18),
        ("Haichuan Two-Wheel", "HC-Max", 2899, 0.15),
        ("Star Orbit Mobility", "Orbit 7", 3799, 0.12),
    ]
    out = []
    for i, (b, m, price, share) in enumerate(brands, 1):
        out.append({
            "competitor_id": f"CP-{i:02d}",
            "competitor_brand": b,
            "competitor_model": m,
            "competitor_price_cny": float(price),
            "competitor_share": share * 100,
            "competitor_share_pp_change": round(rng.uniform(-2.0, 1.5), 1),
            "promo_type": rng.choice(["Trade-in promo", "Back-to-school discount", "Free helmet"]),
            "promo_region": rng.choice(["East China", "Zhejiang-Fujian", "Chengdu-Chongqing", "Greater Bay Area periphery"]),
            "promo_window": "2026-07-01~2026-07-31",
            "price_cut_amt": float(rng.choice([0, 200, 300, 500])),
            "sentiment_score": round(rng.uniform(0.45, 0.75), 2),
            "launch_date": str(date(2026, rng.randint(3, 6), rng.randint(1, 28))),
            "battery_type": "lithium",
            "claimed_range_km": float(rng.choice([60, 70, 80, 90])),
        })
    return out


def build_customers_vehicles(
    n_customers: int, stores: list
) -> tuple[list, list, list, list]:
    customers, vehicles, behaviors, renewals = [], [], [], []
    for i in range(1, n_customers + 1):
        cid = f"CUS-{10000 + i}"
        customers.append({
            "customer_id": cid,
            "phone_masked": fake_phone_masked(),
            "openid": fake_openid(i),
            "unionid": "qs_uid_" + hashlib.md5(f"uid-{SEED}-{i}".encode()).hexdigest()[:12],
            "identity_type": rng.choices(
                ["end_user", "prospect", "dealer"], weights=[0.85, 0.1, 0.05]
            )[0],
            "oneid": fake_oneid(i),
            "oneid_match_method": "phone",
            "province": (loc := rng.choice(CITIES))[0],
            "city": loc[1],
        })
        # 1 vehicle each, some get second
        n_v = 1 if rng.random() > 0.15 else 2
        for k in range(n_v):
            seq = i * 10 + k
            vin = fake_vin(seq)
            model = rng.choice(MODELS)
            color = rng.choice(COLORS)
            btype, bspec, rng_km = rng.choice(BATTERY)
            smart = rng.random() > 0.18
            purchase = daterange_back(900)
            vehicles.append({
                "vin": vin,
                "frame_no": f"FR-{rng.randint(100000, 999999)}",
                "sn": f"SN-2026{rng.randint(100000, 999999)}",
                "vehicle_model": model,
                "vehicle_config": rng.choice(CONFIGS),
                "color": color,
                "battery_type": btype,
                "battery_spec": bspec,
                "claimed_range_km": float(rng_km),
                "purchase_date": str(purchase),
                "purchase_year": purchase.year,
                "is_smart_vehicle": smart,
                "plant": rng.choice(["Trade-in promo", "Back-to-school discount", "Free helmet"]),
                "line_id": f"LINE-{rng.randint(1, 6):02d}",
                "batch_no": f"BATCH-2026W{rng.randint(10, 30):02d}-{model.replace(' ', '')}",
                "ota_version": rng.choice(["v2.1.0", "v2.2.3", "v2.3.1", "v2.4.0"]),
                "customer_id": cid,
                "store_id": rng.choice(stores)["store_id"],
            })
            behaviors.append({
                "customer_id": cid,
                "vin": vin,
                "app_register_flag": True if smart else rng.random() > 0.4,
                "bind_vehicle_flag": smart and rng.random() > 0.2,
                "last_active_at": iso(datetime(2026, 7, rng.randint(1, 28), rng.randint(8, 22), tzinfo=timezone.utc)),
                "active_days_30d": rng.randint(0, 25),
                "mau_flag": rng.random() > 0.35,
                "dau_flag": rng.random() > 0.7,
                "rfm_segment": rng.choice(["high_value", "potential", "silent", "churn_risk"]),
                "r_days": rng.randint(1, 120),
                "f_month": rng.randint(0, 20),
                "m_value": float(rng.randint(0, 2000)),
                "first_touch_channel": rng.choice(["400", "App", "Store", "E-commerce"]),
                "last_touch_channel": rng.choice(["400", "App", "store", "Push"]),
            })
            if smart:
                expire = date(2026, 8, 1) + timedelta(days=rng.randint(-20, 60))
                layer = "T-7" if (expire - date(2026, 8, 1)).days <= 7 else (
                    "T-30" if (expire - date(2026, 8, 1)).days <= 30 else "sleep"
                )
                if rng.random() < 0.15:
                    layer = "sleep"
                renewals.append({
                    "customer_id": cid,
                    "vin": vin,
                    "service_expire_date": str(expire),
                    "due_renew_flag": expire <= date(2026, 8, 31),
                    "paid_flag": rng.random() < 0.22,
                    "paid_type": rng.choice(["renew", "unknown", "new_purchase"]),
                    "active_t30_flag": layer in ("T-30", "T-7") and rng.random() > 0.3,
                    "active_t7_flag": layer == "T-7" and rng.random() > 0.4,
                    "sleep_90d_app_flag": layer == "sleep",
                    "active_90d_4g_flag": rng.random() > 0.25,
                    "renew_intent_score": round(rng.uniform(0.1, 0.95), 2),
                    "renew_pool_layer": layer,
                    "outreach_channel": rng.choice(["push", "sms", "ai_call", "human", "wecom"]),
                    "intent_level": rng.choice(["high", "mid", "low"]),
                })
            else:
                renewals.append({
                    "customer_id": cid,
                    "vin": vin,
                    "service_expire_date": None,
                    "due_renew_flag": False,
                    "paid_flag": False,
                    "paid_type": "unknown",
                    "active_t30_flag": False,
                    "active_t7_flag": False,
                    "sleep_90d_app_flag": True,
                    "active_90d_4g_flag": False,
                    "renew_intent_score": 0.05,
                    "renew_pool_layer": "non_smart",
                    "outreach_channel": "push",
                    "intent_level": "low",
                })
    return customers, vehicles, behaviors, renewals


def build_orders_inventory(dealers, stores, skus, n_orders: int = 80) -> tuple[list, list, list, list]:
    orders, inventory, policies, color_plans = [], [], [], []
    for i in range(1, n_orders + 1):
        d = rng.choice(dealers)
        st = rng.choice([s for s in stores if s["dealer_id"] == d["dealer_id"]] or stores)
        sku = rng.choice(skus)
        status = rng.choice(["pending_audit", "approved", "approved", "rejected", "shipped", "completed"])
        audit = None
        if status == "pending_audit":
            audit = rng.choice(["pass", "reject_shortage", "suggest_substitute"])
        elif status == "rejected":
            audit = "reject_shortage"
        elif status in ("approved", "shipped", "completed"):
            audit = "pass"
        orders.append({
            "order_id": f"SO-2026{i:04d}",
            "dealer_id": d["dealer_id"],
            "store_id": st["store_id"],
            "sku_id": sku["sku_id"],
            "customer_id": None,
            "order_qty": rng.randint(5, 60),
            "order_status": status,
            "audit_result": audit,
            "policy_version": "2026Q3-rebate-V3",
        })
    for sku in skus:
        inventory.append({
            "sku_id": sku["sku_id"],
            "store_id": None,
            "dealer_id": None,
            "wms_stock_qty": rng.randint(0, 200),
            "wms_in_transit_qty": rng.randint(0, 80),
            "store_stock_qty": rng.randint(0, 20),
            "stock_days_cover": round(rng.uniform(0.5, 25), 1),
            "stock_age_days": rng.randint(0, 60),
            "inventory_turn_days": round(rng.uniform(10, 55), 1),
            "shortage_days": rng.choice([0, 0, 0, 3, 7, 11]),
            "demand_daily_est": round(rng.uniform(2, 25), 1),
            "lost_units_est": rng.randint(0, 200),
            "lost_gmv_est": float(rng.randint(0, 600000)),
            "lost_margin_est": float(rng.randint(0, 120000)),
            "shortage_root_cause": rng.choice(["production", "logistics", "color_plan", "supply", None]),
            "replenish_qty_suggest": rng.randint(0, 200),
            "eta_date": str(date(2026, 8, rng.randint(2, 20))),
        })
    for d in dealers:
        qty = rng.randint(400, 1200)
        policies.append({
            "dealer_id": d["dealer_id"],
            "settlement_id": f"STL-2026Q3-{d['dealer_id'][-4:]}",
            "policy_version": "2026Q3-rebate-V3",
            "current_rebate_tier": "Silver" if qty < 800 else "Gold",
            "current_pickup_qty_mtd": qty,
            "qty_to_next_tier": max(0, 800 - qty) if qty < 800 else max(0, 1200 - qty),
            "next_tier_name": "Gold" if qty < 800 else "Diamond",
            "next_tier_rebate_amt": float(28000 if qty < 800 else 45000),
            "rebate_rate": 3.5 if qty < 800 else 4.2,
            "color_bonus_amt": float(rng.choice([0, 1000, 2000])),
            "clawback_amt": float(rng.choice([0, 0, 500])),
            "payable_amt": float(rng.randint(8000, 50000)),
            "pay_status": rng.choice(["unpaid", "unpaid", "paid"]),
        })
    for week in ("2026-W30", "2026-W31", "2026-W32"):
        for model in MODELS[:5]:
            for color in COLORS[:4]:
                color_plans.append({
                    "color_plan_week": week,
                    "vehicle_model": model,
                    "color": color,
                    "color_plan_qty": rng.randint(0, 150),
                    "plant": rng.choice(["East Plant 1", "South Plant 2"]),
                })
    return orders, inventory, policies, color_plans


def build_tickets_voc(customers, vehicles, stores, tags, n_tickets: int = 100) -> tuple[list, list]:
    tickets, voc = [], []
    fault_tags = [t for t in tags if t["tag_domain"] == "product" and t["tag_parent_id"]]
    risk_tags = [t for t in tags if t["tag_domain"] == "risk" and t["tag_parent_id"]]
    descs = [
        "Real-world range is well below the rated spec; a full charge covers less than half expected city mileage.",
        "Weak hill-climb power; motor shows overheat protection with two riders.",
        "Front fork noise; excessive vibration after speed bumps; suspect shock leak.",
        "Soft brake feel; longer stopping distance in rain; customer requests onsite check.",
        "Charger indicator abnormal; still not full after 8+ hours charging.",
        "App pairing keeps saying device offline; still fails after vehicle restart.",
        "Dashboard occasionally blackouts; requires power cycle to recover.",
        "Complaint: store did not follow warranty policy for battery replacement; ticket open over 7 days.",
        "Controller fault code caused speed limit; nearby shop says parts out of stock.",
        "Severe GPS drift; find-vehicle feature cannot locate the bike accurately.",
    ]
    for i in range(1, n_tickets + 1):
        cust = rng.choice(customers)
        vehs = [v for v in vehicles if v["customer_id"] == cust["customer_id"]] or vehicles
        veh = rng.choice(vehs)
        ttype = rng.choices(
            ["fault", "consult", "complaint", "other"], weights=[0.55, 0.25, 0.15, 0.05]
        )[0]
        tag = rng.choice(fault_tags if ttype != "complaint" else fault_tags + risk_tags)
        # Story ： 「complaint 」
        if i <= 6:
            tag = next(t for t in tags if t["tag_id"] == "TAG-open-complaint")
            ttype = "complaint"
        sent = "neg" if ttype in ("fault", "complaint") else rng.choice(["neu", "pos", "neg"])
        desc = rng.choice(descs)
        tid = f"TK-202607{i:04d}"
        tickets.append({
            "ticket_id": tid,
            "customer_id": cust["customer_id"],
            "vin": veh["vin"],
            "store_id": veh.get("store_id") or rng.choice(stores)["store_id"],
            "dealer_id": next(s["dealer_id"] for s in stores if s["store_id"] == (veh.get("store_id") or stores[0]["store_id"])),
            "tag_id": tag["tag_id"],
            "sentiment": sent,
            "ticket_type": ttype,
            "fault_category": rng.choice(
                ["battery", "motor", "brake", "controller", "charging", "dashboard", "other"]
            ) if ttype == "fault" else None,
            "consult_category": rng.choice(["Vehicle info", "Parts", "System matters", "Registration"]) if ttype == "consult" else None,
            "ticket_channel": rng.choice(["400", "App", "E-commerce", "Store"]),
            "ticket_status": "open" if tag["tag_id"] == "TAG-open-complaint" else rng.choice(["open", "processing", "closed"]),
            "ticket_created_at": iso(datetime(2026, 7, rng.randint(1, 28), rng.randint(9, 20), tzinfo=timezone.utc)),
            "handle_duration_min": float(rng.randint(5, 90)),
            "is_complaint": ttype == "complaint" or tag["tag_id"] == "TAG-open-complaint",
            "three_guarantees_reject_flag": rng.random() < 0.08,
            "desc_text": desc,
            "desc_chars": len(desc),
            "transcript_text": f"Agent: Hello, Qingshu Mobility service. Customer: {desc}",
            "agent_id": f"AG-{rng.randint(2000, 2999)}",
            "sop_item": "whetherVIN",
            "sop_pass_fail": rng.choice(["pass", "pass", "fail"]),
            "risk_words": ["lawsuit"] if rng.random() < 0.1 else [],
        })
        voc.append({
            "feedback_id": f"FB-{90000 + i}",
            "ticket_id": tid,
            "customer_id": cust["customer_id"],
            "vin": veh["vin"],
            "nps": rng.randint(-100, 100),
            "csat": round(rng.uniform(1.5, 5.0), 1),
            "nps_delta": rng.randint(-15, 10),
            "feedback_cnt": 1,
            "tag_id": tag["tag_id"],
            "tag_name": tag["tag_name"],
            "tag_domain": tag["tag_domain"],
            "sentiment": sent,
            "sentiment_score": round(rng.uniform(-0.95, 0.9), 2),
            "problem_theme": tag["tag_name"],
            "theme_cnt": rng.randint(10, 300),
            "neg_ratio": round(rng.uniform(20, 85), 1),
            "wow_change": round(rng.uniform(-10, 30), 1),
            "closed_loop_rate": round(rng.uniform(30, 90), 1),
            "recurrence_rate": round(rng.uniform(5, 25), 1),
            "cover_dim": "vehicle",
            "module_name": None,
            "sample_voice": desc,
            "clue_confidence": rng.choice(["weak", "medium"]),
            "pr_risk_level": "P1" if tag["tag_id"] == "TAG-open-complaint" else rng.choice(["P2", "P2", "P1"]),
            "consumer_sat_score": None,
            "channel_sat_score": None,
            "survey_recover_rate": None,
            "dissatisfaction_reason": tag["tag_name"] if sent == "neg" else None,
        })
    return tickets, voc


def build_telemetry(vehicles: list) -> list:
    out = []
    for v in rng.sample(vehicles, k=min(40, len(vehicles))):
        out.append({
            "vin": v["vin"],
            "fault_code": rng.choice([None, None, "BMS_OT_01", "MCU_OC_02", "GPS_DRIFT", "CHG_TIMEOUT"]),
            "iot_alert_cnt": rng.randint(0, 5),
            "mileage_km": float(rng.randint(200, 12000)),
            "soc_pct": float(rng.randint(15, 100)),
            "telemetry_coverage_rate": 81.0,
            "battery_health_pct": float(rng.randint(78, 99)),
            "ota_version": v["ota_version"],
        })
    return out


def build_misc(dealers, stores, skus, vehicles) -> dict:
    sales = []
    for d in dealers:
        target = rng.randint(800, 2000)
        qty = int(target * rng.uniform(0.7, 1.05))
        sales.append({
            "dealer_id": d["dealer_id"],
            "org_id": d["org_id"],
            "period": "2026-07",
            "sales_qty": qty,
            "sales_target_qty": target,
            "sales_achieve_rate": round(100 * qty / target, 1),
            "contract_qty": int(qty * 0.9),
            "contract_target_qty": int(target * 0.92),
            "contract_achieve_rate": round(100 * (qty * 0.9) / (target * 0.92), 1),
            "yoy_sales_qty": int(qty * rng.uniform(0.85, 1.1)),
            "yoy_rate": round(rng.uniform(-5, 20), 1),
            "mom_sales_qty": int(qty * rng.uniform(0.9, 1.1)),
            "mom_rate": round(rng.uniform(-12, 8), 1),
            "rank_dealer": rng.randint(1, 40),
            "full_achieve_outlet_cnt": rng.randint(2, 20),
            "full_achieve_outlet_ratio": round(rng.uniform(20, 60), 1),
            "abnormal_outlet_cnt": rng.randint(0, 8),
            "abnormal_outlet_ratio": round(rng.uniform(0, 20), 1),
            "abnormal_reason": rng.choice(["Low pickup", "High returns", "Compliance issue", None]),
            "abnormal_reason_cnt": rng.randint(0, 9),
            "core_market_gap_to_top3": rng.randint(100, 2000),
            "online_sales_qty": rng.randint(10, 120),
            "rank_warzone": None,
            "rank_subzone": None,
        })
    health = []
    for d in dealers:
        health.append({
            "dealer_id": d["dealer_id"],
            "period": "2026-07",
            "sales_score": float(rng.randint(50, 95)),
            "retail_score": float(rng.randint(45, 90)),
            "compliance_score": float(rng.randint(55, 100)),
            "complaint_score": float(rng.randint(40, 95)),
            "inventory_turn_score": float(rng.randint(40, 90)),
            "health_index": float(rng.randint(50, 92)),
        })
    retail = []
    for st in stores:
        retail.append({
            "store_id": st["store_id"],
            "report_date": "2026-07-28",
            "retail_qty": rng.randint(0, 20),
            "retail_qty_day": rng.randint(0, 6),
            "retail_qty_mtd": rng.randint(20, 180),
            "retail_yoy": round(rng.uniform(-10, 25), 1),
            "writeoff_qty": rng.randint(0, 30),
            "redeem_rate": round(rng.uniform(40, 90), 1),
            "gross_margin_amt": float(rng.randint(2000, 20000)),
            "gross_margin_rate": round(rng.uniform(12, 22), 1),
            "non_exclusive_rate": 0.0 if st["store_type"] == "exclusive" else round(rng.uniform(10, 40), 1),
            "non_exclusive_flag": st["store_type"] != "exclusive",
        })
    campaigns = [
        {
            "campaign_id": "CAMP-summer-trade-in",
            "campaign_name": "Summer trade-in",
            "campaign_goal": "retailrenewal",
            "campaign_budget": 50000.0,
            "participants": 3200,
            "campaign_roi": 2.4,
            "campaign_complaint_rate": 0.3,
        },
        {
            "campaign_id": "CAMP-back-to-school",
            "campaign_name": "Back-to-school retail",
            "campaign_goal": "Boost August retail conversion",
            "campaign_budget": 30000.0,
            "participants": 1800,
            "campaign_roi": 1.9,
            "campaign_complaint_rate": 0.2,
        },
    ]
    contents = []
    for g in rng.sample(
        [{"guide_id": f"GD-{s['store_id'][-5:]}", "store_id": s["store_id"], "channel_account_id": f"DY-{10000+i}"} for i, s in enumerate(stores)],
        k=min(16, len(stores)),
    ):
        contents.append({
            **g,
            "short_video_cnt": rng.randint(5, 40),
            "followers": rng.randint(800, 30000),
            "play_cnt": rng.randint(2000, 120000),
            "gmv_convert_rate": round(rng.uniform(0.3, 3.5), 2),
            "deals_cnt": rng.randint(0, 50),
            "gmv": float(rng.randint(0, 150000)),
            "aov": float(rng.choice([2599, 2999, 3299, 3599])),
            "valid_seller_flag": rng.random() > 0.4,
            "live_sessions": rng.randint(0, 8),
            "live_watch_uv": rng.randint(0, 8000),
            "influencer_cvr": round(rng.uniform(0.5, 2.5), 2),
            "refund_rate": round(rng.uniform(0.5, 3.0), 2),
            "content_script_id": f"SCRIPT-{rng.choice(["Range", "Trade-in", "Safety"])}-01",
            "benchmark_case_id": "CASE-range-01",
            "short_video_valid_participate_rate": round(rng.uniform(20, 60), 1),
        })
    outreach = [
        {"channel": ch, "channel_quota_daily": q, "delivery_rate": dr, "open_rate": op, "connect_rate": cr, "transfer_human_cnt": th, "template_approve_days": 2.0}
        for ch, q, dr, op, cr, th in [
            ("push", 20000, 96.2, 28.4, None, 0),
            ("sms", 8000, 94.0, 12.0, None, 0),
            ("ai_call", 3000, 99.0, None, 41.0, 86),
            ("human", 500, 99.0, None, 55.0, 0),
            ("wecom", 2000, 90.0, 35.0, None, 12),
        ]
    ]
    quality = []
    for v in rng.sample(vehicles, k=min(25, len(vehicles))):
        quality.append({
            "vin": v["vin"],
            "test_station": f"OBD-test bench-{rng.randint(1, 4):02d}",
            "test_ts": iso(datetime(2026, 6, rng.randint(1, 28), 10, tzinfo=timezone.utc)),
            "obd_protocol": "ISO15765",
            "voltage_v": round(rng.uniform(48, 56), 1),
            "current_a": round(rng.uniform(5, 20), 1),
            "speed_rpm": float(rng.randint(200, 600)),
            "controller_temp_c": float(rng.randint(30, 70)),
            "qc_result": rng.choice(["pass", "pass", "pass", "fail"]),
            "operator_id": f"OP-{rng.randint(100, 399)}",
            "part_name": rng.choice(["Trade-in promo", "Back-to-school discount", "Free helmet"]),
            "part_batch_no": f"PB-{rng.randint(1000, 9999)}",
            "supplier_id": f"SUP-{rng.randint(8000, 8999)}",
            "delta_e": round(rng.uniform(0.2, 1.5), 2),
            "gloss": float(rng.randint(70, 95)),
            "defect_type": rng.choice([None, None, "Paint defect", "Assembly gap"]),
            "anomaly_score": round(rng.uniform(0.1, 0.9), 2),
            "predict_fail_days": rng.randint(7, 60),
            "release_ts": iso(datetime(2026, 6, rng.randint(1, 28), 16, tzinfo=timezone.utc)),
            "trace_package_url": f"synthetic://trace/{v['vin']}.zip",
            "recall_level": "watch",
        })
    inspections = []
    for st in rng.sample(stores, k=min(18, len(stores))):
        inspections.append({
            "inspect_id": f"INS-20260728-{st['store_id'][-4:]}",
            "store_id": st["store_id"],
            "inspect_time": iso(datetime(2026, 7, 28, 8, 30, tzinfo=timezone.utc)),
            "check_item": rng.choice(["VI compliance", "Display layout", "Competitor logo", "Staff uniform"]),
            "ai_confidence": round(rng.uniform(0.7, 0.98), 2),
            "pass_fail": "fail" if st["store_type"] == "non_exclusive" else rng.choice(["pass", "pass", "fail"]),
            "photo_url": f"synthetic://inspect/{st['store_id']}.jpg",
            "morning_photo_url": f"synthetic://inspect/{st['store_id']}-am.jpg",
            "evening_photo_url": f"synthetic://inspect/{st['store_id']}-pm.jpg",
            "competitor_logo_detected": ["Beichen Mobility"] if st["store_type"] != "exclusive" and rng.random() > 0.5 else [],
            "suspect_type": "Non-exclusive display" if st["store_type"] != "exclusive" else None,
            "vi_score": float(rng.randint(55, 98)),
            "rectify_ticket_id": f"RC-{st['store_id'][-4:]}" if st["store_type"] != "exclusive" else None,
            "due_date": "2026-08-05",
        })
    finance = []
    for i in range(1, 13):
        inv = round(rng.uniform(500, 3000), 2)
        po = inv + rng.choice([0, 0, 20, -15])
        finance.append({
            "expense_id": f"EXP-202607-{100 + i}",
            "employee_id": f"EMP-{rng.randint(1000, 1999)}",
            "invoice_no": f"INV-SYN-{rng.randint(100000, 999999)}",
            "po_no": f"PO-SYN-{rng.randint(10000, 99999)}",
            "receipt_amt": inv,
            "invoice_amt": inv,
            "po_amt": float(po),
            "match_status": "match" if abs(po - inv) < 0.01 else "mismatch",
            "diff_amt": round(abs(po - inv), 2),
            "diff_reason": None if abs(po - inv) < 0.01 else rng.choice(["Price mismatch", "SKU mismatch", "Quantity mismatch"]),
            "revenue_forecast": None,
            "pickup_forecast_units": None,
            "rebate_cashout_forecast": None,
            "opex_forecast": None,
            "net_cash_forecast": None,
            "forecast_confidence_low": None,
            "forecast_confidence_high": None,
        })
    alerts = []
    for i, d in enumerate(dealers[:8], 1):
        alerts.append({
            "alert_id": f"ALERT-20260728-{i:03d}",
            "alert_type": rng.choice(["sales_drop", "compliance", "shortage", "complaint", "competitor"]),
            "dealer_id": d["dealer_id"],
            "store_id": None,
            "metric_name": "mom_rate",
            "metric_value": round(rng.uniform(-15, -8), 1),
            "threshold_value": -10.0,
            "severity": rng.choice(["P0", "P1", "P2"]),
            "required_action": rng.choice(["Replenish color within 3 days", "VI", "renewalcomplaint"]),
            "due_date": "2026-08-05",
            "verify_method": rng.choice(["Inspection", "Sales review", "Ticket follow-up"]),
        })
    store_dev = []
    for reg in CITIES:
        store_dev.append({
            "county_code": reg[2],
            "county_name": reg[3],
            "blank_l1_plan_cnt": rng.randint(2, 10),
            "blank_l1_opened_cnt": rng.randint(0, 6),
            "blank_l1_achieve_rate": round(rng.uniform(30, 90), 1),
            "store_dev_plan_cnt": rng.randint(10, 40),
            "store_dev_done_cnt": rng.randint(5, 30),
            "store_dev_rate": round(rng.uniform(40, 85), 1),
            "market_capacity_annual": rng.randint(15000, 50000),
            "self_coverage_flag": rng.choice(["yes", "weak", "blank"]),
            "open_roi_months": float(rng.randint(10, 20)),
            "support_quota_total_wan": float(rng.randint(8, 20)),
            "support_quota_applied_wan": float(rng.randint(2, 10)),
            "support_quota_remain_wan": float(rng.randint(1, 10)),
            "first_order_qty": rng.randint(40, 120),
            "m1_m3_order_qty": rng.randint(100, 400),
            "gantt_owner": fake_name(),
            "gantt_start": "2026-07-01",
            "gantt_end": "2026-09-15",
            "fitout_suggest_grade": rng.choice(["A", "B", "C"]),
        })
    risks = []
    for d in dealers:
        risks.append({
            "dealer_id": d["dealer_id"],
            "company_name": d["dealer_name"],
            "credit_code": "91" + hashlib.md5(f"credit-{SEED}-{d['dealer_id']}".encode()).hexdigest()[:16].upper(),
            "reg_capital_wan": float(rng.choice([100, 200, 500, 1000])),
            "lawsuit_cnt_3y": rng.randint(0, 3),
            "dishonest_flag": False,
            "negative_news_cnt_90d": rng.randint(0, 2),
            "risk_level": rng.choice(["low", "low", "medium", "high"]),
            "risk_score": float(rng.randint(20, 85)),
            "admission_suggest": rng.choice(["pass", "pass", "supplement", "reject"]),
        })
    # Skill → （ ToolRegistry / data/entities/capability_catalog.json ）
    catalog = [
        {
            "skill_id": "fill_ticket",
            "skill_desc": "Fill service tickets and write shared AI output",
            "input_schema": {"text": "string", "customer_id": "string?", "vin": "string?"},
            "output_schema": {"ticket_draft": "object", "ai_output_id": "string"},
            "allowed_tools": [
                "get_customer", "get_vehicle", "get_ticket", "list_tickets",
                "extract_ticket_fields", "suggest_voc_tags", "get_tag",
                "write_ai_output", "log_step",
            ],
        },
        {
            "skill_id": "renewal_plan",
            "skill_desc": "Plan renewal outreach; blocked by open complaint tags",
            "input_schema": {"customer_id": "string", "vin": "string?"},
            "output_schema": {"allow_outreach": "boolean", "reason": "string"},
            "allowed_tools": [
                "get_customer", "get_vehicle", "get_renewal", "get_user_behavior",
                "score_renewal", "route_renewal_pool", "read_ai_outputs",
                "read_shared_tags", "check_outreach_block", "log_step",
            ],
        },
        {
            "skill_id": "repair_kb",
            "skill_desc": "Repair KB RAG Q&A",
            "input_schema": {"query": "string", "vin": "string?"},
            "output_schema": {"answer": "string", "citations": "list"},
            "allowed_tools": [
                "search_kb", "get_kb_document", "list_kb_domains", "log_step",
            ],
        },
        {
            "skill_id": "policy_kb",
            "skill_desc": "Warranty / rebate policy RAG Q&A",
            "input_schema": {"query": "string", "dealer_id": "string?"},
            "output_schema": {"answer": "string", "citations": "list"},
            "allowed_tools": [
                "search_kb", "get_kb_document", "list_kb_domains", "log_step",
            ],
        },
        {
            "skill_id": "hr_rules",
            "skill_desc": "HR rules and agent QA SOP RAG Q&A",
            "input_schema": {"query": "string"},
            "output_schema": {"answer": "string", "citations": "list"},
            "allowed_tools": [
                "search_kb", "get_kb_document", "list_kb_domains", "log_step",
            ],
        },
        {
            "skill_id": "voc_tagging",
            "skill_desc": "VoC sentiment",
            "input_schema": {"text": "string", "customer_id": "string?"},
            "output_schema": {"tag_id": "string", "sentiment": "string"},
            "allowed_tools": [
                "suggest_voc_tags", "list_tags", "get_tag", "list_voc",
                "write_ai_output", "list_capabilities", "log_step",
            ],
        },
        {
            "skill_id": "shared_write",
            "skill_desc": "Shared AI output write example",
            "input_schema": {"payload": "object"},
            "output_schema": {"ai_output_id": "string"},
            "allowed_tools": [
                "write_ai_output", "read_ai_outputs", "get_ai_output", "log_step",
            ],
        },
        {
            "skill_id": "crm_lookup",
            "skill_desc": "CRM / order / inventory lookup",
            "input_schema": {"customer_id": "string?", "vin": "string?", "order_id": "string?"},
            "output_schema": {"entities": "object"},
            "allowed_tools": [
                "get_customer", "get_vehicle", "list_vehicles", "get_order",
                "list_orders", "list_inventory", "get_dealer", "get_store",
                "get_sku", "log_step",
            ],
        },
        {
            "skill_id": "channel_ops",
            "skill_desc": "Channel alerts and inspection lookup",
            "input_schema": {"dealer_id": "string?"},
            "output_schema": {"insights": "object"},
            "allowed_tools": [
                "get_dealer", "get_dealer_health", "list_alerts", "list_sales_metrics",
                "list_retail_daily", "list_inspections", "get_risk", "get_policy",
                "simulate_rebate_tier", "log_step",
            ],
        },
    ]
    return {
        "sales_metrics": sales,
        "dealer_health": health,
        "retail_daily": retail,
        "campaigns": campaigns,
        "contents": contents,
        "outreach": outreach,
        "quality_checks": quality,
        "inspections": inspections,
        "finance_expense": finance,
        "alerts": alerts,
        "store_dev": store_dev,
        "risks": risks,
        "capability_catalog": catalog,
    }


# ---------------------------------------------------------------------------
# Knowledge (unstructured)
# ---------------------------------------------------------------------------

def write_knowledge() -> None:
    """Write repair / policy / HR / product / channel knowledge docs."""
    docs = {
        "repair/range-anomaly-troubleshooting.md": """# Range anomaly troubleshooting (Qingshu Mobility · E40/E60/E80/S7/S9)

## 1. Intake checklist
1. Confirm full charge (App SOC=100%).
2. Ask: load, terrain, tire pressure, ambient temperature (<5°C affects range).
3. Collect VIN (Demo QS0), OTA version, battery health (SOH), recent usage pattern.

## 2. Common causes
| Symptom | Likely cause | Next step |
|---------|--------------|-----------|
| ~50% of rated | BMS calibration / aging | Check SOH; schedule health test |
| Hill climb weak | Tire pressure low | Set 2.5–3.0 bar; check MCU logs |
| Sudden drop | Controller thermal limit | Inspect connectors; OTA check |

## 3. Agent script (with references)
- "Please share VIN, OTA version, and typical route so we can narrow causes."
- "If SOH below 80%, see warranty policy doc before promising replacement."
- "Do not guarantee range numbers; cite measured SOH and conditions."

## 4. Escalation
- Same VIN ≥2 range complaints in 30 days → supervisor review
- Telemetry `BMS_OT_01` → tag `TAG-reputation-risk`

## 5. Shared layer
- Write `tag_id` (`TAG-short-range`) and `sentiment` via AIOutput when persisting
- Open complaints (`TAG-open-complaint`) must be read by renewal Planning skill before outreach
""",
        "repair/motor-noise-and-speed-limit.md": """# Motor noise and speed limit

## Symptoms
- Whine or rattle under load; speed capped ~15 km/h; customer says "bike feels limp"

## Steps
1. Read telemetry: `MCU_OC_02` (overcurrent), `MCU_OT_01` (overtemp)
2. Confirm whether noise is constant or load-dependent
3. Check brake drag and wheel alignment
4. OTA: recommend v2.3.1+ if below

## Actions
- Test ride ≥3 km; compare rated vs actual top speed
- Create ticket with fault_category=motor; attach audio note if available
- If safety concern → `TAG-safety-hazard`; do not dismiss as "normal"

## Agent tone
- Acknowledge inconvenience; avoid blaming rider technique without data
""",
        "repair/app-pairing-failure.md": """# App pairing / bind failure

## Preconditions
1. Vehicle must be smart (4G) model
2. App login and network OK
3. Store may assist with in-person bind

## Steps
1. VIN check: `is_smart_vehicle=true`
2. Renewal context: non-smart units skip connected-service bind flows
3. Guide customer to store bind if remote fails twice
4. Retry after 2 minutes; reboot app

## Tags
- Pairing issues → `TAG-pairing-failure`
- Do not mark `TAG-open-complaint` for pure IoT bind failures unless attitude/policy dispute
""",
        "repair/brake-noise-and-pads.md": """# Brake noise and pad wear

## Symptoms
- Squeal when braking; soft lever; longer stopping distance

## Steps
1. Visual pad inspection (<2 mm → replace)
2. Check rotor contamination and caliper alignment
3. Road test at low speed

## Ticket fields
- `fault_category=brake`
- `desc_text`: noise type, when it occurs, whether worsening
""",
        "repair/charging-port-and-charger-compatibility.md": """# Charging port and charger compatibility

## Policy
- Use approved chargers (e.g. QS-CHG-48-xx series)
- Third-party fast chargers may void warranty on port damage

## Steps
1. Inspect port pins and moisture
2. Confirm charger model and LED behavior
3. Telemetry: `CHG_OT_01` overtemp

## Script
"Please confirm charger model and whether the port feels loose; we may schedule inspection."
""",
        "policy/warranty-and-battery-policy.md": """# Warranty and battery policy summary (Demo)

> Demo RAG corpus; cite clause IDs in answers.

## Warranty term
- Standard: 12 months from purchase (vehicle frame)
- Battery module: 12 months; SOH≥80% threshold for replacement review

## Battery
- Free inspection within 6 months for abnormal drain reports
- Replacement requires BMS log + authorized service ticket

## Service SLA
- Store response within 48h for warranty tickets
- Denied claims must cite policy section in writing

## Tags
- Disputes → `TAG-warranty-dispute`
- Media/threats → `TAG-reputation-risk`
""",
        "policy/2026Q3-pickup-rebate.md": """# 2026 Q3 pickup rebate policy · version `2026Q3-rebate-V3`

| Tier | Min pickup | Rebate | Note |
|------|------------|--------|------|
| Bronze | ≥300 | 2.0% | |
| Silver | ≥800 | 3.5% | +0.5% color bonus |
| Gold | ≥1200 | 4.2% | |
| Diamond | ≥1800 | 5.0% | requires inspection pass |

## Settlement rules
- Primary dealer account only; split orders not merged
- Clawback on P0 compliance violations

## Fields
`settlement_id`, `dealer_id`, `policy_version`, `current_rebate_tier`, `payable_amt`, `clawback_amt`
""",
        "policy/renewal-outreach-red-lines.md": """# Renewal outreach red lines

1. If tag `TAG-open-complaint` present → **forbidden** proactive Push/SMS/AI call
2. Ladder: Push → SMS → AI call → human; max 3 touches/day/channel
3. `non_smart` vehicles excluded from renewal rate denominator
4. High intent (`intent_level=high`) still requires gate pass
5. Must call `read_ai_outputs` / `read_shared_tags` before outreach

## Story2
Planning skill `renewal_plan` reads complaint tags; sets `allow_outreach=false` when blocked
""",
        "policy/store-vi-and-non-exclusive-red-lines.md": """# Store VI and non-exclusive display red lines

## Forbidden
- Mixed-brand display (`TAG-non-exclusive-display`)
- VI violations (`TAG-vi-violation`)
- Unauthorized signage

## Inspection flow
1. Vision/inspection output feeds compliance ticket
2. Set `due_date` and `verify_method` on ticket
3. P0 may block Diamond rebate tier
""",
        "hr/employee-policy-qa-summary.md": """# HR policy Q&A summary

## Conduct
- Agents must not promise warranty outcomes beyond policy
- Store staff must not share customer PII in group chats

## Data handling
- Mask phone numbers in demos (QS0 synthetic VINs only)
- Do not paste raw VoC into public channels

## Escalation keywords
- "lawsuit", "media", "12315" → supervisor + `TAG-reputation-risk`
""",
        "hr/agent-qa-sop-highlights.md": """# Agent QA SOP highlights

1. Confirm VIN read-back
2. Confirm customer identity
3. Confirm next step and timeline
4. Forbidden phrases: "guaranteed fix", "definitely free"

## Examples (fail)
- "We will definitely replace the battery for free" → QA fail, coach agent
""",
        "product/model-selling-points-and-competitor-talking-points.md": """# Model selling points and competitor talking points

## E60
- Strengths: range, App connectivity, comfort
- Line: "Rated range assumes standard load and 25°C"

## S9
- Strengths: torque, smart features, design
- Competitors: compare on total cost of ownership, not headline price

## Fictional competitors
- Pulse X1: lower price, shorter warranty
- Yuno S: strong rebate wars in some regions
- Orbit 7: channel conflict risk; stay policy-compliant
""",
        "product/ota-release-notes-v2.md": """# OTA release notes v2.x

| Version | Highlights | Risk |
|---------|------------|------|
| v2.1.0 | Baseline connectivity | |
| v2.2.3 | BMS tuning | |
| v2.3.1 | Motor controller fix | Recommended for MCU noise reports |
| v2.4.0 | App UI refresh | |

VoC field `ota_version` should match vehicle record when advising upgrades.
""",
        "channel/tier1-pickup-and-color-stockout-scripts.md": """# Tier-1 pickup and color stockout scripts

## Opening
"Reviewing your pickup plan and color availability before we commit to the next tier."

## Gold tier nudge
"You are 188 units from Gold; at 2.8% rebate that materially changes margin. Shall we align color production?"

## Escalation
- Color stockout P0 → alert ops + replenishment ticket
""",
        "channel/store-opening-checklist.md": """# Store opening checklist

1. Domain/trade area approved
2. Fit-out inspection scheduled
3. First orders 1–3 SKUs placed
4. Staff training pass/supplement recorded
5. VI photos uploaded
""",
    }
    for rel, body in docs.items():
        _write_text(DATA / "knowledge" / rel, body)

    index = []
    for rel in docs:
        index.append({
            "kb_domain": rel.split("/")[0],
            "kb_doc_id": rel.replace("/", "__").replace(".md", ""),
            "path": f"knowledge/{rel}",
            "title": Path(rel).stem,
            "chars": len(docs[rel]),
        })
    _write_json(DATA / "knowledge" / "index.json", {
        "brand": "Qingshu Mobility",
        "documents": index,
        "total_docs": len(index),
        "total_chars": sum(len(v) for v in docs.values()),
    })


def write_seeds(customers, vehicles, tickets, renewals) -> None:
    # pick a complaint-open ticket for story 1/2
    open_complaint = next(
        t for t in tickets
        if t.get("tag_id") == "TAG-open-complaint" and t.get("ticket_status") == "open"
    )
    cust = next(c for c in customers if c["customer_id"] == open_complaint["customer_id"])
    veh = next(v for v in vehicles if v["vin"] == open_complaint["vin"])
    renew = next(
        (r for r in renewals if r["customer_id"] == cust["customer_id"] and r["vin"] == veh["vin"]),
        renewals[0],
    )
    _write_json(DATA / "seeds" / "story_1_fill_ticket.json", {
        "story": "Story1-assetize output",
        "agent_type": "react",
        "skill_id": "fill_ticket",
        "input": {
            "text": open_complaint["desc_text"],
            "customer_id": cust["customer_id"],
            "vin": veh["vin"],
            "channel": "400",
        },
        "expect_write_ai_output": {
            "producer_skill": "fill_ticket",
            "consumer_allow": ["renewal_plan", "voc_tagging"],
            "payload_keys": ["ticket_id", "tag_id", "sentiment", "customer_id", "vin"],
        },
        "fixture_ticket_id": open_complaint["ticket_id"],
    })
    _write_json(DATA / "seeds" / "story_2_renewal_block.json", {
        "story": "Story2-typeconsumer",
        "agent_type": "planning",
        "skill_id": "renewal_plan",
        "input": {
            "customer_id": cust["customer_id"],
            "vin": veh["vin"],
        },
        "renewal_snapshot": renew,
        "expect": {
            "allow_outreach": False,
            "block_reason_contains": "complaint",
            "read_from_shared": True,
        },
    })
    _write_json(DATA / "seeds" / "demo_query_pack.json", {
        "sample_vins": [v["vin"] for v in vehicles[:5]],
        "sample_customer_ids": [c["customer_id"] for c in customers[:5]],
        "sample_dealer_ids": sorted({t["dealer_id"] for t in tickets if t.get("dealer_id")})[:5],
        "kb_smoke_queries": [
            "How do I troubleshoot range below rated?",
            "2026Q3 Silver rebate tier",
            "Complaint blocks AI renewal outreach",
        ],
    })


def write_manifest(stats: dict) -> None:
    _write_json(DATA / "MANIFEST.json", {
        "brand": "Qingshu Mobility",
        "generated_at": iso(datetime.now(timezone.utc)),
        "seed": SEED,
        "compliance": {
            "real_customer_data": False,
            "real_vin": False,
            "real_phone": False,
            "vin_prefix": "QS0",
            "phone_storage": "masked_only",
            "source": "fully_synthetic",
            "note": "Fully synthetic; never store real customers, OEM data, VINs, or phone numbers",
        },
        "stats": stats,
    })
    _write_text(
        DATA / "README.md",
        f"""# Synthetic data directory

Brand: **Qingshu Mobility**  
Seed: `{SEED}`  
Regenerate: `python scripts/generate_synthetic_data.py`

## Compliance
- No real customer, vehicle, ticket, or OEM internal data
- VINs always start with `QS0…`
- Phones stored as `phone_masked` only (middle four digits masked)

## Layout
| Path | Purpose |
|------|---------|
| `OBJECT_CATALOG.md` | Entity catalog |
| `vocab/field_glossary.json` | Field meanings |
| `vocab/tag_vocabulary.json` | Tag dictionary |
| `entities/*.json` | Entity JSON |
| `knowledge/**` | KB source docs |
| `seeds/*.json` | Story1/2 seeds |
| `MANIFEST.json` | Generation manifest |

## Stats
{json.dumps(stats, ensure_ascii=False, indent=2)}""",
    )


def main() -> None:
    # clean generated json/md under data (keep dirs)
    for sub in ("entities", "vocab", "knowledge", "seeds"):
        p = DATA / sub
        if p.exists():
            for f in p.rglob("*"):
                if f.is_file() and f.name != ".gitkeep":
                    f.unlink()

    write_object_catalog()
    write_field_glossary()
    tags = build_vocab()
    _write_json(DATA / "vocab" / "tag_vocabulary.json", {
        "version": tags[0]["tag_vocab_version"],
        "tags": tags,
    })

    regions, orgs = build_regions_orgs()
    dealers, stores, guides = build_dealers_stores_guides(regions, n_dealers=20)
    skus = build_skus()
    competitors = build_competitors()
    customers, vehicles, behaviors, renewals = build_customers_vehicles(120, stores)
    orders, inventory, policies, color_plans = build_orders_inventory(dealers, stores, skus, n_orders=80)
    tickets, voc = build_tickets_voc(customers, vehicles, stores, tags, n_tickets=120)
    telemetry = build_telemetry(vehicles)
    misc = build_misc(dealers, stores, skus, vehicles)

    ent = DATA / "entities"
    mapping = {
        "regions.json": regions,
        "orgs.json": orgs,
        "dealers.json": dealers,
        "stores.json": stores,
        "guides.json": guides,
        "skus.json": skus,
        "competitors.json": competitors,
        "customers.json": customers,
        "vehicles.json": vehicles,
        "user_behaviors.json": behaviors,
        "renewals.json": renewals,
        "orders.json": orders,
        "inventory.json": inventory,
        "policies.json": policies,
        "color_plans.json": color_plans,
        "tickets.json": tickets,
        "voc_feedback.json": voc,
        "telemetry.json": telemetry,
        "sales_metrics.json": misc["sales_metrics"],
        "dealer_health.json": misc["dealer_health"],
        "retail_daily.json": misc["retail_daily"],
        "campaigns.json": misc["campaigns"],
        "contents.json": misc["contents"],
        "outreach.json": misc["outreach"],
        "quality_checks.json": misc["quality_checks"],
        "inspections.json": misc["inspections"],
        "finance_expense.json": misc["finance_expense"],
        "alerts.json": misc["alerts"],
        "store_dev.json": misc["store_dev"],
        "risks.json": misc["risks"],
        "capability_catalog.json": misc["capability_catalog"],
        # ：department_flows.json Planning ， mapping， 。
    }
    for name, payload in mapping.items():
        _write_json(ent / name, payload)

    write_knowledge()
    write_seeds(customers, vehicles, tickets, renewals)

    stats = {name: len(payload) if isinstance(payload, list) else 1 for name, payload in mapping.items()}
    stats["tag_vocabulary"] = len(tags)
    stats["knowledge_docs"] = len(list((DATA / "knowledge").rglob("*.md")))
    stats["field_glossary"] = len(json.loads((DATA / "vocab" / "field_glossary.json").read_text(encoding="utf-8"))["fields"])
    write_manifest(stats)

    
    for v in vehicles:
        assert v["vin"].startswith("QS0") and len(v["vin"]) == 17, v["vin"]
    for c in customers:
        assert "****" in c["phone_masked"] and len(c["phone_masked"]) == 11, c["phone_masked"]
    assert any(t["tag_id"] == "TAG-open-complaint" and t["ticket_status"] == "open" for t in tickets)

    print("OK synthetic data written under", DATA)
    print(json.dumps(stats, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()