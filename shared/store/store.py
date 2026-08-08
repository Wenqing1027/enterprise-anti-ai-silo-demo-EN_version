"""SharedStore: Agent dynamic output shared layer (anti-AI-silo L7 slim). （BLUEPRINT 1.3）： - write_ai_output / read_ai_outputs - JSON （ JSON， memory）"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from shared.models.ai_assets import AIOutput, RunLog, TagVocabulary
from shared.models.enums import StepStatus
from shared.store import paths
from shared.store.json_backend import load_json, load_list, save_list


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _as_dict(model: AIOutput | RunLog) -> dict[str, Any]:
    return model.model_dump(mode="json")


class SharedStore:
    """Unified read/write AIOutput / RunLog / shared tag view."""

    def __init__(
        self,
        *,
        runtime_dir: Path | None = None,
        persist: bool = True,
    ) -> None:
        self.runtime_dir = runtime_dir or paths.RUNTIME_DIR
        self.persist = persist
        self.ai_outputs_file = self.runtime_dir / "ai_outputs.json"
        self.run_logs_file = self.runtime_dir / "run_logs.json"
        self._memory_outputs: list[dict[str, Any]] = []
        self._memory_logs: list[dict[str, Any]] = []
        if self.persist:
            self.runtime_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # AIOutput
    # ------------------------------------------------------------------

    def write_ai_output(
        self,
        *,
        producer_skill: str,
        payload: dict[str, Any] | list[Any],
        consumer_allow: list[str] | None = None,
        run_id: str | None = None,
        payload_schema: str | None = None,
        ai_output_id: str | None = None,
        ts: datetime | None = None,
    ) -> AIOutput:
        """Assetize output: write shared layer for other Skill/Agent consume."""
        if not producer_skill:
            raise ValueError("producer_skill is required")
        if payload is None:
            raise ValueError("payload is required")

        output = AIOutput(
            ai_output_id=ai_output_id or f"AIO-{uuid.uuid4().hex[:12]}",
            producer_skill=producer_skill,
            consumer_allow=list(consumer_allow or []),
            payload=payload,
            payload_schema=payload_schema,
            run_id=run_id or f"run-{uuid.uuid4().hex[:10]}",
            ts=ts or _utcnow(),
        )
        rows = self._load_outputs()
        rows.append(_as_dict(output))
        self._save_outputs(rows)
        return output

    def get_ai_output(self, ai_output_id: str) -> AIOutput | None:
        for row in self._load_outputs():
            if row.get("ai_output_id") == ai_output_id:
                return AIOutput.model_validate(row)
        return None

    def read_ai_outputs(
        self,
        *,
        consumer_skill: str | None = None,
        producer_skill: str | None = None,
        customer_id: str | None = None,
        vin: str | None = None,
        tag_id: str | None = None,
        run_id: str | None = None,
        limit: int | None = None,
    ) -> list[AIOutput]:
        """Skill consumerShared output。 ： - consumer_skill： output consumer_allow， this skill； consumer_allow ， consumer 。 - payload customer_id / vin / tag_id （Story2 ）。"""
        results: list[AIOutput] = []
        for row in self._load_outputs():
            out = AIOutput.model_validate(row)
            if producer_skill and out.producer_skill != producer_skill:
                continue
            if run_id and out.run_id != run_id:
                continue
            if consumer_skill and not self._consumer_allowed(out, consumer_skill):
                continue
            if not self._payload_match(
                out.payload,
                customer_id=customer_id,
                vin=vin,
                tag_id=tag_id,
            ):
                continue
            results.append(out)

        # ， tagstatus
        results.sort(key=lambda x: x.ts or datetime.min.replace(tzinfo=timezone.utc), reverse=True)
        if limit is not None:
            return results[:limit]
        return results

    # ------------------------------------------------------------------
    # Shared tags view（ AIOutput.payload ， Story2 ）
    # ------------------------------------------------------------------

    def read_shared_tags(
        self,
        *,
        consumer_skill: str | None = None,
        customer_id: str | None = None,
        vin: str | None = None,
    ) -> list[dict[str, Any]]:
        """Project tag view from shared output.

        Expected payload shape (fill/tag skills):
        {"customer_id", "vin", "tag_id", "sentiment", ...}
        Also accepts payload["tags"] = ["TAG-open-complaint", ...]
        """
        tags: list[dict[str, Any]] = []
        for out in self.read_ai_outputs(
            consumer_skill=consumer_skill,
            customer_id=customer_id,
            vin=vin,
        ):
            payload = out.payload
            if isinstance(payload, dict):
                if payload.get("tag_id"):
                    tags.append(
                        {
                            "tag_id": payload.get("tag_id"),
                            "sentiment": payload.get("sentiment"),
                            "customer_id": payload.get("customer_id"),
                            "vin": payload.get("vin"),
                            "ticket_id": payload.get("ticket_id"),
                            "source_ai_output_id": out.ai_output_id,
                            "producer_skill": out.producer_skill,
                            "ts": out.ts.isoformat() if out.ts else None,
                        }
                    )
                for t in payload.get("tags") or []:
                    if isinstance(t, str):
                        tags.append(
                            {
                                "tag_id": t,
                                "sentiment": payload.get("sentiment"),
                                "customer_id": payload.get("customer_id"),
                                "vin": payload.get("vin"),
                                "ticket_id": payload.get("ticket_id"),
                                "source_ai_output_id": out.ai_output_id,
                                "producer_skill": out.producer_skill,
                                "ts": out.ts.isoformat() if out.ts else None,
                            }
                        )
                    elif isinstance(t, dict) and t.get("tag_id"):
                        tags.append(
                            {
                                **t,
                                "source_ai_output_id": out.ai_output_id,
                                "producer_skill": out.producer_skill,
                                "ts": out.ts.isoformat() if out.ts else None,
                            }
                        )
        return tags

    def has_blocking_tag(
        self,
        *,
        customer_id: str | None = None,
        vin: str | None = None,
        consumer_skill: str | None = "renewal_plan",
        blocking_tag_ids: list[str] | None = None,
    ) -> tuple[bool, list[str]]:
        """Story2 helper: whether shared tags should block outreach."""
        block_set = set(blocking_tag_ids or ["TAG-open-complaint", "TAG-reputation-risk", "TAG-safety-hazard"])
        found: list[str] = []
        for row in self.read_shared_tags(
            consumer_skill=consumer_skill,
            customer_id=customer_id,
            vin=vin,
        ):
            tid = row.get("tag_id")
            if tid in block_set and tid not in found:
                found.append(str(tid))
        return (len(found) > 0, found)

    def load_tag_vocabulary(self) -> list[TagVocabulary]:
        """read tagdictionary（data/vocab， output）。"""
        raw = load_json(paths.TAG_VOCAB_FILE, default={"tags": []})
        tags = raw.get("tags", []) if isinstance(raw, dict) else raw
        return [TagVocabulary.model_validate(t) for t in tags]

    # ------------------------------------------------------------------
    # Run logs（ ）
    # ------------------------------------------------------------------

    def log_step(
        self,
        *,
        run_id: str,
        step_name: str,
        step_status: StepStatus | str = StepStatus.OK,
        detail: dict[str, Any] | None = None,
        step_ts: datetime | None = None,
    ) -> RunLog:
        status = (
            step_status
            if isinstance(step_status, StepStatus)
            else StepStatus(str(step_status))
        )
        entry = RunLog(
            run_id=run_id,
            step_name=step_name,
            step_status=status,
            step_ts=step_ts or _utcnow(),
            detail=detail,
        )
        rows = self._load_logs()
        rows.append(_as_dict(entry))
        self._save_logs(rows)
        return entry

    def list_run_logs(self, run_id: str | None = None) -> list[RunLog]:
        rows = self._load_logs()
        logs = [RunLog.model_validate(r) for r in rows]
        if run_id:
            logs = [x for x in logs if x.run_id == run_id]
        logs.sort(key=lambda x: x.step_ts or datetime.min.replace(tzinfo=timezone.utc))
        return logs

    # ------------------------------------------------------------------
    # lifecycle
    # ------------------------------------------------------------------

    def clear_runtime(self) -> None:
        """output（ data/entities ）。"""
        self._memory_outputs = []
        self._memory_logs = []
        if self.persist:
            save_list(self.ai_outputs_file, [])
            save_list(self.run_logs_file, [])

    def stats(self) -> dict[str, Any]:
        return {
            "persist": self.persist,
            "runtime_dir": str(self.runtime_dir),
            "ai_outputs": len(self._load_outputs()),
            "run_logs": len(self._load_logs()),
        }

    # ------------------------------------------------------------------
    # internals
    # ------------------------------------------------------------------

    @staticmethod
    def _consumer_allowed(out: AIOutput, consumer_skill: str) -> bool:
        allow = out.consumer_allow
        if not allow:
            return True
        return consumer_skill in allow

    @staticmethod
    def _payload_match(
        payload: dict[str, Any] | list[Any] | None,
        *,
        customer_id: str | None,
        vin: str | None,
        tag_id: str | None,
    ) -> bool:
        if customer_id is None and vin is None and tag_id is None:
            return True
        if not isinstance(payload, dict):
            return False
        if customer_id is not None and payload.get("customer_id") != customer_id:
            return False
        if vin is not None and payload.get("vin") != vin:
            return False
        if tag_id is not None:
            tags = payload.get("tags") or []
            tag_ids = {tag_id}
            if payload.get("tag_id") != tag_id and tag_id not in tags:
                # tags may be list[dict]
                dict_ids = {
                    t.get("tag_id")
                    for t in tags
                    if isinstance(t, dict)
                }
                if tag_id not in dict_ids:
                    return False
        return True

    def _load_outputs(self) -> list[dict[str, Any]]:
        if not self.persist:
            return list(self._memory_outputs)
        return load_list(self.ai_outputs_file)

    def _save_outputs(self, rows: list[dict[str, Any]]) -> None:
        if not self.persist:
            self._memory_outputs = list(rows)
            return
        save_list(self.ai_outputs_file, rows)

    def _load_logs(self) -> list[dict[str, Any]]:
        if not self.persist:
            return list(self._memory_logs)
        return load_list(self.run_logs_file)

    def _save_logs(self, rows: list[dict[str, Any]]) -> None:
        if not self.persist:
            self._memory_logs = list(rows)
            return
        save_list(self.run_logs_file, rows)


# （CLI / Agent ）
default_store = SharedStore(persist=True)