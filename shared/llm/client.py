"""DeepSeek LLM client (OpenAI-compatible API)."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

# .env（ cwd key）
_ROOT = Path(__file__).resolve().parents[2]
_ENV_FILE = _ROOT / ".env"
load_dotenv(_ENV_FILE, override=False)

DEFAULT_BASE_URL = "https://api.deepseek.com/v1"

# Cursor / IDE HTTP(S)_PROXY；httpx/openai ，
# api.deepseek.com Connection error。 ， 。
_PROXY_ENV_KEYS = (
    "HTTP_PROXY",
    "HTTPS_PROXY",
    "ALL_PROXY",
    "http_proxy",
    "https_proxy",
    "all_proxy",
    "SOCKS_PROXY",
    "SOCKS5_PROXY",
    "socks_proxy",
    "socks5_proxy",
)


def _trust_proxy_env() -> bool:
    return (os.getenv("DEEPSEEK_TRUST_ENV") or "").strip().lower() in {
        "1",
        "true",
        "yes",
    }


def _strip_proxy_env() -> None:
    if _trust_proxy_env():
        return
    for key in _PROXY_ENV_KEYS:
        os.environ.pop(key, None)
    # DNS/ （Errno 8 / Connection error）
    os.environ["NO_PROXY"] = "*"
    os.environ["no_proxy"] = "*"


_strip_proxy_env()


def _normalize_base_url(raw: str | None) -> str:
    """/v1 OpenAI 。"""
    url = (raw or DEFAULT_BASE_URL).strip().rstrip("/")
    if not url:
        url = DEFAULT_BASE_URL.rstrip("/")
    # https://api.deepseek.com → https://api.deepseek.com/v1
    if url.endswith("/v1"):
        return url
    if url.rstrip("/") == "https://api.deepseek.com":
        return DEFAULT_BASE_URL
    # ： /v1 （DeepSeek ）
    if "deepseek.com" in url and not url.endswith("/v1"):
        return url + "/v1"
    return url


@dataclass(frozen=True)
class LLMConfig:
    api_key: str
    model: str = "deepseek-chat"
    base_url: str = DEFAULT_BASE_URL
    temperature: float = 0.2
    max_tokens: int = 2048


def load_llm_config(*, profile: str = "default") -> LLMConfig:
    # .env （uvicorn/reload ）
    if _ENV_FILE.is_file():
        load_dotenv(_ENV_FILE, override=False)

    profile_key = (profile or "default").strip().lower()
    if profile_key == "extraction":
        key = (
            os.getenv("DEEPSEEK_EXTRACTION_API_KEY")
            or os.getenv("DEEPSEEK_API_KEY")
            or os.getenv("OPENAI_API_KEY")
            or ""
        ).strip()
        if not key:
            raise RuntimeError(
                "Missing DEEPSEEK_EXTRACTION_API_KEY (or DEEPSEEK_API_KEY). "
                f"Set it in {_ENV_FILE} (see .env.example)."
            )
        model = (
            os.getenv("DEEPSEEK_EXTRACTION_MODEL")
            or os.getenv("DEEPSEEK_MODEL")
            or "deepseek-chat"
        ).strip() or "deepseek-chat"
        temperature = float(os.getenv("DEEPSEEK_EXTRACTION_TEMPERATURE", "0.1"))
    elif profile_key == "rag":
        key = (
            os.getenv("DEEPSEEK_RAG_API_KEY")
            or os.getenv("DEEPSEEK_API_KEY")
            or os.getenv("OPENAI_API_KEY")
            or ""
        ).strip()
        if not key:
            raise RuntimeError(
                "Missing DEEPSEEK_RAG_API_KEY (or DEEPSEEK_API_KEY). "
                f"Set it in {_ENV_FILE} (see .env.example)."
            )
        model = (
            os.getenv("DEEPSEEK_RAG_MODEL")
            or os.getenv("DEEPSEEK_MODEL")
            or "deepseek-chat"
        ).strip() or "deepseek-chat"
        temperature = float(os.getenv("DEEPSEEK_RAG_TEMPERATURE", "0.2"))
    else:
        key = (os.getenv("DEEPSEEK_API_KEY") or os.getenv("OPENAI_API_KEY") or "").strip()
        if not key:
            raise RuntimeError(
                "Missing DEEPSEEK_API_KEY. "
                f"Set it in {_ENV_FILE} (see .env.example)."
            )
        model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat").strip() or "deepseek-chat"
        temperature = float(os.getenv("DEEPSEEK_TEMPERATURE", "0.2"))

    return LLMConfig(
        api_key=key,
        model=model,
        base_url=_normalize_base_url(os.getenv("DEEPSEEK_BASE_URL")),
        temperature=temperature,
        max_tokens=int(os.getenv("DEEPSEEK_MAX_TOKENS", "2048")),
    )


class DeepSeekClient:
    """：chat.completions + tool calling。"""

    def __init__(self, config: LLMConfig | None = None) -> None:
        import httpx
        from openai import OpenAI

        _strip_proxy_env()
        self.config = config or load_llm_config()
        # DEEPSEEK_TRUST_ENV=1
        trust_env = _trust_proxy_env()
        http_client = httpx.Client(
            timeout=httpx.Timeout(60.0, connect=20.0),
            trust_env=trust_env,
            proxy=None,
        )
        self._client = OpenAI(
            api_key=self.config.api_key,
            base_url=self.config.base_url,
            timeout=60.0,
            max_retries=2,
            http_client=http_client,
        )

    def chat(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
        *,
        temperature: float | None = None,
        tool_choice: str | dict[str, Any] | None = None,
        response_format: dict[str, Any] | None = None,
    ) -> Any:
        import time

        kwargs: dict[str, Any] = {
            "model": self.config.model,
            "messages": messages,
            "temperature": self.config.temperature if temperature is None else temperature,
            "max_tokens": self.config.max_tokens,
        }
        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = tool_choice if tool_choice is not None else "auto"
        elif tool_choice == "none":
            kwargs["tool_choice"] = "none"
        if response_format and not tools:
            kwargs["response_format"] = response_format

        attempts = max(1, int(os.getenv("DEEPSEEK_RETRIES", "3")))
        last_exc: Exception | None = None
        for i in range(attempts):
            try:
                _strip_proxy_env()
                return self._client.chat.completions.create(**kwargs)
            except Exception as exc:  # noqa: BLE001
                last_exc = exc
                msg = str(exc).lower()
                retryable = any(
                    x in msg
                    for x in (
                        "connection error",
                        "connecterror",
                        "timed out",
                        "timeout",
                        "503",
                        "service_unavailable",
                        "too busy",
                        "502",
                        "429",
                    )
                )
                if not retryable or i >= attempts - 1:
                    break
                time.sleep(1.2 * (i + 1))

        assert last_exc is not None
        root: BaseException = last_exc
        while getattr(root, "__cause__", None) is not None:
            root = root.__cause__  # type: ignore[assignment]
        raise RuntimeError(
            f"DeepSeek （base_url={self.config.base_url},"
            f"model={self.config.model}）: {last_exc}"
            + (f" | cause={root}" if root is not last_exc else "")
        ) from last_exc


def get_llm_client(*, profile: str = "default") -> DeepSeekClient:
    return DeepSeekClient(load_llm_config(profile=profile))