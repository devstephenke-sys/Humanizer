import json
import logging
import re

import httpx
from fastapi import HTTPException

from app.config import Settings, get_settings

logger = logging.getLogger("draftwell.ai")


class ProviderError(Exception):
    pass


class AIProviderService:
    """One interface over OpenAI-compatible APIs, Anthropic, and Ollama."""

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()

    @property
    def name(self) -> str:
        return self.settings.ai_provider.lower()

    def ensure_configured(self) -> None:
        if self.settings.provider_configured:
            return
        provider = self.name
        if provider == "anthropic":
            hint = "Set ANTHROPIC_API_KEY."
        elif provider == "ollama":
            hint = "Run Ollama and set OLLAMA_BASE_URL and OLLAMA_MODEL."
        else:
            hint = "Set OPENAI_API_KEY. OPENAI_BASE_URL can point at any OpenAI-compatible API."
        raise HTTPException(
            status_code=503,
            detail=f"No language model is configured ({provider}). {hint}",
        )

    async def complete(self, system: str, user: str, temperature: float, max_tokens: int) -> str:
        self.ensure_configured()
        provider = self.name
        try:
            if provider == "anthropic":
                return await self._anthropic(system, user, temperature, max_tokens)
            if provider == "ollama":
                return await self._ollama(system, user, temperature)
            return await self._openai(system, user, temperature, max_tokens)
        except HTTPException:
            raise
        except httpx.HTTPError as exc:
            logger.exception("Language model request failed")
            raise HTTPException(status_code=502, detail="The language model could not be reached.") from exc
        except ProviderError as exc:
            logger.error("Language model returned an error: %s", exc)
            raise HTTPException(status_code=502, detail="The language model returned an error.") from exc

    async def _openai(self, system: str, user: str, temperature: float, max_tokens: int) -> str:
        url = self.settings.openai_base_url.rstrip("/") + "/chat/completions"
        payload = {
            "model": self.settings.openai_model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        }
        headers = {"Authorization": f"Bearer {self.settings.openai_api_key}"}
        async with httpx.AsyncClient(timeout=90) as client:
            response = await client.post(url, json=payload, headers=headers)
        if response.status_code >= 400:
            raise ProviderError(response.text[:500])
        data = response.json()
        return data["choices"][0]["message"]["content"]

    async def _anthropic(self, system: str, user: str, temperature: float, max_tokens: int) -> str:
        payload = {
            "model": self.settings.anthropic_model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "system": system,
            "messages": [{"role": "user", "content": user}],
        }
        headers = {
            "x-api-key": self.settings.anthropic_api_key,
            "anthropic-version": "2023-06-01",
        }
        async with httpx.AsyncClient(timeout=90) as client:
            response = await client.post("https://api.anthropic.com/v1/messages", json=payload, headers=headers)
        if response.status_code >= 400:
            raise ProviderError(response.text[:500])
        data = response.json()
        blocks = data.get("content", [])
        text = "".join(block.get("text", "") for block in blocks if block.get("type") == "text")
        if not text:
            raise ProviderError("empty anthropic response")
        return text

    async def _ollama(self, system: str, user: str, temperature: float) -> str:
        url = self.settings.ollama_base_url.rstrip("/") + "/api/chat"
        payload = {
            "model": self.settings.ollama_model,
            "stream": False,
            "options": {"temperature": temperature},
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        }
        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(url, json=payload)
        if response.status_code >= 400:
            raise ProviderError(response.text[:500])
        data = response.json()
        return data["message"]["content"]


def parse_json_object(raw: str) -> dict | None:
    cleaned = raw.strip()
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", cleaned, flags=re.IGNORECASE | re.DOTALL).strip()
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
        if not match:
            return None
        try:
            data = json.loads(match.group(0))
        except json.JSONDecodeError:
            return None
    return data if isinstance(data, dict) else None
