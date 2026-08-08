"""RAG System Prompt base and assembly."""

from __future__ import annotations

from agents.rag.skill_schema import RAG_PROMPT_SECTION_ORDER, RagSkillConfig

BASE_SYSTEM = """You are the internal RAG Agent (retrieval-augmented generation) for the fictional company "Qingshu Mobility".
Architecture principle: multiple departments share the same KB retrieval tools (DataFetcher / search_kb); you only run this Skill's knowledge Q&A, do not act as an omniscient enterprise brain, and do not pretend master data was queried (unless context explicitly provides it).

Hard rules:
1. Answer only from "retrieved snippets"; for content not covered, clearly say "KB does not cover / insufficient basis".
2. Do not invent part numbers, rebate points, policy clauses, VIN, phone numbers.
3. Final answer must list cited kb_chunk_id (if hits); if no hit write "Citations: none".
4. Synthetic policies/manuals are Demo only; you may note "Qingshu Mobility synthetic guidance".
5. Cross-department collaboration uses shared outputs and unified tags; this loop does not do Multi-Agent chat.
6. Use English.
"""

RETRIEVE_RULES = """[Retrieval and citation discipline]
1. "Retrieved snippets" below were retrieved by the system per this Skill's kb_domains_allow; you must not claim other domains were searched.
2. Prefer high-score snippets; on conflict, note conflict and suggest human review.
3. Citation format: list kb_chunk_id and document title at end (at least hit count or write "none").
4. No irrelevant long restatements; give actionable steps or guidance highlights.
"""


def build_system_prompt(skill: RagSkillConfig) -> str:
    sections: dict[str, str] = {
        "A_base": BASE_SYSTEM.strip(),
        "B_tone": (
            f"[Tone] {skill.tone.label}\n"
            f"Style: {skill.tone.style}\n"
            f"Forbidden: {skill.tone.forbid or '(none extra)'}"
        ),
        "C_goal": f"[This Skill goal] {skill.goal}\nSuccess hint: {skill.success_hint or '(see output format)'}",
        "C2_system_extra": (skill.system_extra or "").strip(),
        "D_retrieve_rules": (
            RETRIEVE_RULES
            + f"\nAllowed KB domains: {', '.join(skill.kb_domains_allow)}"
            + f"\ntop_k={skill.top_k} · max_context_chars={skill.max_context_chars}"
            + f"\ncite_required={skill.cite_required} · allow_no_hit={skill.allow_no_hit_answer}"
        ),
        "E_output": (skill.output_format or "Default: restate → advice → citations → next step").strip(),
        "F_security": (
            "[Security]"
            + (skill.security.prompt_forbid_extra or "Follow enterprise Demo compliance: no real customer PII.")
            + f"\nDomain gate: {', '.join(skill.security.kb_domains_allow or skill.kb_domains_allow)}"
        ),
    }
    parts: list[str] = []
    for key in RAG_PROMPT_SECTION_ORDER:
        text = (sections.get(key) or "").strip()
        if not text:
            continue
        parts.append(text)
    return "\n\n".join(parts)


def format_context_block(chunks: list[dict]) -> str:
    if not chunks:
        return "[Retrieved snippets]\n(no hits)"
    lines = ["[Retrieved snippets]"]
    for i, ch in enumerate(chunks, start=1):
        lines.append(
            f"--- [{i}] kb_chunk_id={ch.get('kb_chunk_id')} "
            f"score={ch.get('kb_score')} title={ch.get('title')} ---\n"
            f"{ch.get('content') or ''}"
        )
    return "\n\n".join(lines)


def build_user_message(query: str, context_block: str) -> str:
    return (
        f"[User question]\n{query.strip()}\n\n"
        f"{context_block}\n\n"
        "Answer only from retrieved snippets and give citation list at the end."
    )
