import re

CITATION_RE = re.compile(
    r"\[[0-9]{1,3}\]|\([A-Z][A-Za-z.'\-]+,\s*\d{4}\)|https?://\S+"
)
SENTENCE_RE = re.compile(r"[^.!?\n]+(?:[.!?]+|$)", re.MULTILINE)

DISCLAIMER = (
    "This is an editorial rewrite from a language model. It is not certified as human-authored, "
    "and it is not a guarantee about any AI detector."
)
DETECT_DISCLAIMER = (
    "This score is a probabilistic estimate based on writing patterns. Human writing can be flagged, "
    "and AI-assisted writing can be missed. Do not treat the score as proof of authorship."
)


def word_count(text: str) -> int:
    return len(re.findall(r"\S+", text.strip()))


def character_count(text: str) -> int:
    return len(text)


def sentences(text: str) -> list[str]:
    parts = [part.strip() for part in SENTENCE_RE.findall(text) if part.strip()]
    return parts or ([text.strip()] if text.strip() else [])


def citations(text: str) -> list[str]:
    return CITATION_RE.findall(text)


def headings(text: str) -> list[str]:
    return [line.strip() for line in text.splitlines() if line.strip().startswith("#")]


def missing_markers(source: str, rewritten: str) -> list[str]:
    warnings: list[str] = []
    for marker in citations(source):
        if marker not in rewritten:
            warnings.append(f"Citation or link not found in the rewrite: {marker}")
    for heading in headings(source):
        if heading not in rewritten:
            warnings.append(f"Heading not found in the rewrite: {heading}")
    return warnings


def title_from_text(text: str, fallback: str = "Untitled draft") -> str:
    words = re.findall(r"\S+", text)
    if not words:
        return fallback
    title = " ".join(words[:8])
    return title[:180]
