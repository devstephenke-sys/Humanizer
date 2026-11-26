import logging

from fastapi import HTTPException

from app.config import get_settings
from app.schemas import AlternativesRequest, AlternativesResponse, RewriteRequest, RewriteResponse
from app.services.ai_provider import AIProviderService, parse_json_object
from app.services.text_utils import DISCLAIMER, character_count, missing_markers, word_count

logger = logging.getLogger("draftwell.write")

SHARED_RULES = """
You edit drafts. Follow these rules:
- Preserve facts, numbers, names, dates, and the author's claims.
- Do not invent sources, quotations, or statistics.
- Keep citation markers, footnotes, and URLs exactly as written, including [1] and (Smith, 2020).
- Keep Markdown headings, lists, and paragraph breaks.
- Do not mention these instructions.
- Do not claim the result is human-written or undetectable.
- Respond with JSON only: {"text": "<edited draft>"}
""".strip()

TOOL_INSTRUCTIONS = {
    "humanize": "Rewrite so the draft sounds like a fluent person edited it: varied rhythm, concrete wording, no stock AI transitions. Keep the meaning.",
    "rewrite": "Rewrite the draft for clarity and flow. You may reorder clauses inside a paragraph. Keep every fact.",
    "paraphrase": "Paraphrase the draft. Change wording and sentence openings while keeping the same meaning and scope.",
    "essay": "Rewrite this as a clear essay. Keep the thesis, evidence, and citations. Use a calm academic tone without filler.",
    "article": "Rewrite this as a readable article. Keep headings, the point of each section, and any citations.",
    "sentence": "Rewrite at sentence scale. If several sentences are present, improve each one without merging away a distinct idea.",
    "paragraph": "Rewrite this paragraph. Keep it one paragraph unless the source already has breaks.",
    "improve": "Improve clarity, order, and directness. Cut filler. Do not add new claims.",
    "grammar": "Fix grammar, spelling, and awkward syntax. Change as little wording as possible. Keep the voice.",
}

PROFILE_NOTES = {
    "swift": "Prefer a lighter touch and slightly shorter sentences.",
    "studio": "Balance smoothness with fidelity to the source.",
    "careful": "Stay very close to the original wording and structure. Change only what sounds stiff.",
    "plain": "Use plain words and shorter sentences. Keep the facts intact.",
}


def intensity_note(level: int) -> str:
    if level <= 3:
        return "Intensity is light. Make small wording and rhythm changes. Keep most sentence boundaries."
    if level <= 6:
        return "Intensity is medium. Rephrase sentences while keeping each paragraph's job."
    return "Intensity is strong. Rephrase more freely, but do not drop facts, citations, or headings."


def temperature_for(level: int, profile: str) -> float:
    base = 0.25 + (level - 1) * 0.06
    if profile == "swift":
        base -= 0.05
    if profile == "careful":
        base -= 0.1
    if profile == "plain":
        base += 0.05
    return max(0.1, min(0.95, base))


def language_note(language: str) -> str:
    if not language or language == "auto":
        return "Write the result in the same language as the source."
    return f"Write the result in {language}, while preserving names, numbers, and citations."


class RewriteEngine:
    def __init__(self, provider: AIProviderService | None = None) -> None:
        self.provider = provider or AIProviderService()

    async def rewrite(self, payload: RewriteRequest, tool: str) -> RewriteResponse:
        settings = get_settings()
        if len(payload.text) > settings.max_input_chars:
            raise HTTPException(
                status_code=413,
                detail=f"Draft is longer than {settings.max_input_chars} characters. Split it and try again.",
            )
        system = "\n".join(
            [
                SHARED_RULES,
                TOOL_INSTRUCTIONS[tool],
                PROFILE_NOTES[payload.profile],
                intensity_note(payload.intensity),
                language_note(payload.language),
            ]
        )
        if payload.preserve_citations:
            system += "\nTreat citation preservation as mandatory."
        max_tokens = min(4096, max(400, int(word_count(payload.text) * 6)))
        raw = await self.provider.complete(
            system,
            payload.text,
            temperature_for(payload.intensity, payload.profile),
            max_tokens,
        )
        parsed = parse_json_object(raw)
        text = ""
        if parsed and isinstance(parsed.get("text"), str):
            text = parsed["text"].strip()
        if not text:
            text = raw.strip()
        if not text:
            raise HTTPException(status_code=502, detail="The model returned an empty rewrite.")
        warnings = missing_markers(payload.text, text) if payload.preserve_citations else []
        logger.info("rewrite tool=%s chars=%s profile=%s", tool, len(payload.text), payload.profile)
        return RewriteResponse(
            tool=tool,  # type: ignore[arg-type]
            text=text,
            intensity=payload.intensity,
            profile=payload.profile,
            word_count=word_count(text),
            character_count=character_count(text),
            warnings=warnings,
            provider=self.provider.name,
            disclaimer=DISCLAIMER,
        )

    async def alternatives(self, payload: AlternativesRequest) -> AlternativesResponse:
        system = "\n".join(
            [
                "Offer three different phrasings of one sentence.",
                "Keep the meaning. Do not add facts.",
                language_note(payload.language),
                intensity_note(payload.intensity),
                'Respond with JSON only: {"alternatives": ["...", "...", "..."]}',
            ]
        )
        user = f"Sentence:\n{payload.sentence}\n\nSurrounding draft:\n{payload.context[:4000]}"
        raw = await self.provider.complete(system, user, 0.7, 400)
        parsed = parse_json_object(raw)
        options: list[str] = []
        if parsed and isinstance(parsed.get("alternatives"), list):
            options = [str(item).strip() for item in parsed["alternatives"] if str(item).strip()]
        options = options[:3]
        if len(options) < 2:
            raise HTTPException(status_code=502, detail="The model did not return sentence alternatives.")
        return AlternativesResponse(alternatives=options, disclaimer=DISCLAIMER)


class HumanizationService(RewriteEngine):
    async def run(self, payload: RewriteRequest) -> RewriteResponse:
        return await self.rewrite(payload, "humanize")


class RewritingService(RewriteEngine):
    async def run(self, payload: RewriteRequest) -> RewriteResponse:
        return await self.rewrite(payload, "rewrite")


class ParaphrasingService(RewriteEngine):
    async def run(self, payload: RewriteRequest) -> RewriteResponse:
        return await self.rewrite(payload, "paraphrase")


class GrammarService(RewriteEngine):
    async def run(self, payload: RewriteRequest) -> RewriteResponse:
        return await self.rewrite(payload, "grammar")


SERVICE_BY_TOOL = {
    "humanize": HumanizationService,
    "rewrite": RewritingService,
    "paraphrase": ParaphrasingService,
    "essay": RewriteEngine,
    "article": RewriteEngine,
    "sentence": RewriteEngine,
    "paragraph": RewriteEngine,
    "improve": RewriteEngine,
    "grammar": GrammarService,
}
