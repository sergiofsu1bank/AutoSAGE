from dataclasses import dataclass
from typing import Optional
import time
import os

from openai import OpenAI


# ==================================================
# Contracts
# ==================================================

@dataclass(frozen=True)
class LLMRequest:
    system_prompt: str
    user_prompt: str
    context: Optional[str] = None
    model: str = "gpt-4o-mini"
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None


@dataclass(frozen=True)
class LLMUsage:
    tokens_input: int
    tokens_output: int
    latency_ms: int
    model: str


@dataclass(frozen=True)
class LLMResponse:
    text: str
    usage: LLMUsage


# ==================================================
# OpenAI Adapter (REAL)
# ==================================================

class OpenAIAdapter:
    """
    Real OpenAI adapter.
    """

    def __init__(self, timeout_seconds: int = 30) -> None:
        self._client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
            timeout=timeout_seconds,
        )

    def generate(self, request: LLMRequest) -> LLMResponse:
        start = time.time()

        messages = [
            {"role": "system", "content": request.system_prompt},
        ]

        if request.context:
            messages.append(
                {"role": "system", "content": f"Context:\n{request.context}"}
            )

        messages.append(
            {"role": "user", "content": request.user_prompt}
        )

        response = self._client.chat.completions.create(
            model=request.model,
            messages=messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )

        latency_ms = int((time.time() - start) * 1000)

        usage = LLMUsage(
            tokens_input=response.usage.prompt_tokens,
            tokens_output=response.usage.completion_tokens,
            latency_ms=latency_ms,
            model=request.model,
        )

        return LLMResponse(
            text=response.choices[0].message.content,
            usage=usage,
        )
