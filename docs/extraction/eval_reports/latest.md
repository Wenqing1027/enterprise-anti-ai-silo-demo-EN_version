# Extraction gold-standard eval report

> Generated at: 2026-08-05T16:00:44+08:00  
> Script: `scripts/eval_extraction.py`

## Overview

- Overall: **PASS**
- ticket_fields: PASS
- voc_entities: PASS

## ticket_fields

| Metric | Actual | Threshold | Result |
|--------|--------|-----------|--------|
| schema compliance rate | 1.0 | 1.0 | ✅ |
| ticket_type accuracy | 0.86 | 0.8 | ✅ |
| fault_category accuracy | 0.8636 | 0.75 | ✅ |
| tag_id accuracy | 0.98 | 0.75 | ✅ |
| Missed block count | 0 | 0 | ✅ |
| sentiment accuracy | 0.68 (strict) / 1.0 (tolerance, for acceptance) | 0.8 | ✅ |
| ID recall | 1.0 | 0.95 | ✅ |

> ticket sentiment acceptance: phase 1 allows one-grade tolerance for non-complaint `neu↔neg`.

## voc_entities

| Metric | Actual | Threshold | Result |
|--------|--------|-----------|--------|
| schema compliance rate | 1.0 | 1.0 | ✅ |
| tag_id hit | 1.0 | 0.8 | ✅ |
| Missed block count | 0 | 0 | ✅ |
| sentiment accuracy | 0.92 | 0.85 | ✅ |
| tag_domain accuracy | 1.0 | 0.9 | ✅ |
| Out-of-vocabulary tag rate | 0.0 | 0.05 | ✅ |

## Failure / warning samples

- `T50` stop=validated tag=TAG-renewal-entry-hard-to-find sent=pos tag_hit=False blocking_ok=None
