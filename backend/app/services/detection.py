"""Probabilistic writing-pattern analyzer.

The score is an estimate of how strongly a passage resembles common AI-draft
patterns such as uniform sentence length and stock transitions. It is not a
classifier trained on a private detector, and it is not proof of authorship.
"""

from __future__ import annotations

import math
import re
import statistics

from app.schemas import DetectResponse, SentenceSignal
from app.services.text_utils import DETECT_DISCLAIMER, character_count, sentences, word_count

TRANSITION_PHRASES = (
    "furthermore",
    "moreover",
    "additionally",
    "in addition",
    "it is important to note",
    "it is essential",
    "it is worth noting",
    "plays a crucial role",
    "in conclusion",
    "in today's",
    "delve",
    "tapestry",
    "multifaceted",
    "pivotal",
    "underscore",
    "foster",
    "leverage",
    "robust",
    "comprehensive",
    "noteworthy",
    "a testament",
    "not only",
    "cutting-edge",
    "realm",
    "landscape",
    "ever-evolving",
    "significant",
    "significantly",
    "utilize",
    "in order to",
)

CONTRACTIONS = ("'t", "'s", "'re", "'ve", "'ll", "'d", "n't")


def _syllables(word: str) -> int:
    groups = re.findall(r"[aeiouy]+", word.lower())
    return max(1, len(groups))


def reading_ease(text: str) -> float | None:
    words = re.findall(r"[A-Za-z']+", text)
    sentence_count = max(1, len(sentences(text)))
    if len(words) < 5:
        return None
    syllables = sum(_syllables(word) for word in words)
    score = 206.835 - 1.015 * (len(words) / sentence_count) - 84.6 * (syllables / len(words))
    return round(max(0.0, min(100.0, score)), 1)


def _clamp(value: float) -> int:
    return int(round(max(0.0, min(100.0, value))))


def _label_for(ai_likelihood: int) -> str:
    if ai_likelihood >= 67:
        return "higher"
    if ai_likelihood >= 40:
        return "mixed"
    return "lower"


def _sentence_score(sentence: str) -> tuple[int, str]:
    words = re.findall(r"[A-Za-z']+", sentence)
    if not words:
        return 50, "Too little text in this sentence to judge."
    lowered = sentence.lower()
    hits = sum(1 for phrase in TRANSITION_PHRASES if phrase in lowered)
    length_penalty = 0
    if 12 <= len(words) <= 28:
        length_penalty += 12
    if len(words) > 32:
        length_penalty += 8
    contraction_relief = 14 if any(token in lowered for token in CONTRACTIONS) else 0
    personal = 8 if re.search(r"\b(i|we|my|our)\b", lowered) else 0
    question = 6 if "?" in sentence else 0
    score = 38 + hits * 16 + length_penalty - contraction_relief - personal - question
    note = "Stock phrasing and even cadence show up here." if score >= 67 else (
        "Mixed signals. Read it in context before changing it." if score >= 40 else
        "More varied or conversational cues in this sentence."
    )
    return _clamp(score), note


def _overall(text: str, parts: list[str]) -> tuple[int, list[str]]:
    signals: list[str] = []
    words = re.findall(r"[A-Za-z']+", text.lower())
    if len(words) < 8 or not parts:
        return 50, ["The sample is too short for a stable estimate."]

    lengths = [len(re.findall(r"[A-Za-z']+", part)) for part in parts]
    lengths = [item for item in lengths if item > 0]
    mean = statistics.mean(lengths) if lengths else 0
    stdev = statistics.pstdev(lengths) if len(lengths) > 1 else 0
    coefficient = (stdev / mean) if mean else 0

    score = 42.0
    if coefficient < 0.22:
        score += 18
        signals.append("Sentence lengths are unusually even, which is a common draft pattern.")
    elif coefficient > 0.55:
        score -= 12
        signals.append("Sentence lengths vary, which is more typical of edited prose.")
    else:
        signals.append("Sentence length variation is moderate.")

    lowered = text.lower()
    phrase_hits = sum(lowered.count(phrase) for phrase in TRANSITION_PHRASES)
    density = phrase_hits / max(1, len(words) / 80)
    score += min(28, density * 10)
    if phrase_hits:
        signals.append(f"Found {phrase_hits} stock transition or filler phrase{'s' if phrase_hits != 1 else ''}.")
    else:
        score -= 6
        signals.append("Few stock transition phrases.")

    unique = len(set(words)) / len(words)
    if unique < 0.45:
        score += 8
        signals.append("Vocabulary repeats more than usual.")
    elif unique > 0.72:
        score -= 6
        signals.append("Vocabulary is fairly varied for this length.")

    if any(token in lowered for token in CONTRACTIONS):
        score -= 8
        signals.append("Contractions lower the pattern score.")
    if re.search(r"\b(i|we|my|our)\b", lowered):
        score -= 4

    sentence_scores = [_sentence_score(part)[0] for part in parts]
    if sentence_scores:
        score = score * 0.62 + (sum(sentence_scores) / len(sentence_scores)) * 0.38

    if not math.isfinite(score):
        score = 50
    return _clamp(score), signals


class DetectionService:
    def analyze(self, text: str, mode: str) -> DetectResponse:
        cleaned = text.strip()
        parts = sentences(cleaned)
        ai_likelihood, signals = _overall(cleaned, parts)
        words = word_count(cleaned)
        warning = None
        if words < 100:
            warning = (
                "Results may be less reliable under 100 words. Add a fuller passage before leaning on the score."
            )
            signals.append("Short samples move the score around more.")

        sentence_rows: list[SentenceSignal] = []
        if mode == "deep":
            for part in parts:
                likelihood, note = _sentence_score(part)
                sentence_rows.append(
                    SentenceSignal(
                        text=part,
                        ai_likelihood=likelihood,
                        label=_label_for(likelihood),  # type: ignore[arg-type]
                        note=note,
                    )
                )

        if ai_likelihood >= 67:
            label = "Reads more like common AI-draft patterns"
        elif ai_likelihood >= 40:
            label = "Mixed signals"
        else:
            label = "Reads more like varied edited prose"

        summary = (
            f"Estimated AI-pattern score {ai_likelihood} out of 100. "
            f"The complementary human-like phrasing figure is {100 - ai_likelihood}. "
            "Use it as a revision hint, then check meaning, sources, and your own drafts."
        )
        return DetectResponse(
            mode=mode,  # type: ignore[arg-type]
            word_count=words,
            character_count=character_count(cleaned),
            ai_likelihood=ai_likelihood,
            human_like=100 - ai_likelihood,
            label=label,
            summary=summary,
            reading_ease=reading_ease(cleaned),
            short_text_warning=warning,
            signals=signals,
            sentences=sentence_rows,
            disclaimer=DETECT_DISCLAIMER,
        )
