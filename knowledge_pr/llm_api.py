"""Shared OpenAI-compatible API client for knowledge-pr scripts.

Mirrors the ApiLLM backend in fact-compare/compare_claims.py, with one
behavioral difference: an empty/None response is returned as "" and callers
are expected to treat unparseable output as an explicit ERROR verdict rather
than silently defaulting to any real label.
"""

import getpass
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import os
from typing import List, Optional, Tuple

# Point KPR_SERVER_READY at the file your serve script writes (line1=api_base, line2=model),
# or just pass --api-base/--api-model explicitly on the CLI.
DEFAULT_READY_FILE = Path(os.environ.get("KPR_SERVER_READY", "server_ready.txt"))


def read_endpoint(ready_file: Path = DEFAULT_READY_FILE) -> Tuple[Optional[str], Optional[str]]:
    """Read (api_base, api_model) from a server_ready.txt written by serve_llm.sh."""
    if not ready_file.exists():
        return None, None
    lines = [ln.strip() for ln in ready_file.read_text().splitlines() if ln.strip()]
    if not lines:
        return None, None
    api_base = lines[0]
    api_model = lines[1] if len(lines) > 1 else None
    return api_base, api_model


class ApiLLM:
    """Remote API backend — calls an OpenAI-compatible vLLM server."""

    def __init__(
        self,
        api_base: str,
        api_model: str,
        enable_thinking: bool = False,
        temperature: float = 0.0,
        max_tokens: int = 4096,
        concurrency: int = 16,
    ):
        import openai

        self._client = openai.OpenAI(base_url=api_base, api_key="dummy")
        self._api_model = api_model
        self._enable_thinking = enable_thinking
        self._temperature = temperature
        self._max_tokens = max_tokens
        self._concurrency = concurrency
        self._user = os.environ.get("USER") or getpass.getuser()

    def _call_one(self, prompt: str) -> str:
        for attempt in range(5):
            try:
                response = self._client.chat.completions.create(
                    model=self._api_model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=self._temperature,
                    max_tokens=self._max_tokens,
                    user=self._user,
                    extra_body={"chat_template_kwargs": {"enable_thinking": self._enable_thinking}},
                )
                msg = response.choices[0].message
                return msg.content or getattr(msg, "reasoning_content", None) or ""
            except Exception:
                if attempt == 4:
                    raise
                time.sleep(2 ** attempt)
        return ""

    def batch_infer(self, prompts: List[str]) -> List[str]:
        results: List[str] = [""] * len(prompts)
        with ThreadPoolExecutor(max_workers=self._concurrency) as pool:
            futures = {pool.submit(self._call_one, p): i for i, p in enumerate(prompts)}
            for future in as_completed(futures):
                results[futures[future]] = future.result()
        return results
