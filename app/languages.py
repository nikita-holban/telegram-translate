from __future__ import annotations

import re

# Common languages keyed by ISO 639-1 code. Used both to recognize inline
# override prefixes and to canonicalize /setlang input. Anything outside this
# table is still understood by the LLM — see resolve_target().
LANGUAGE_NAMES: dict[str, str] = {
    "ar": "Arabic",
    "cs": "Czech",
    "de": "German",
    "el": "Greek",
    "en": "English",
    "es": "Spanish",
    "fa": "Persian",
    "fr": "French",
    "he": "Hebrew",
    "hi": "Hindi",
    "id": "Indonesian",
    "it": "Italian",
    "ja": "Japanese",
    "ko": "Korean",
    "nl": "Dutch",
    "pl": "Polish",
    "pt": "Portuguese",
    "ro": "Romanian",
    "ru": "Russian",
    "sv": "Swedish",
    "tr": "Turkish",
    "uk": "Ukrainian",
    "vi": "Vietnamese",
    "zh": "Chinese",
}

# A prefix is an alphabetic token (plus spaces/hyphens) up to 20 chars,
# followed by a colon. The body (DOTALL) keeps any further colons intact.
_PREFIX_RE = re.compile(r"^\s*([A-Za-z][A-Za-z \-]{0,19})\s*:\s*(.+)$", re.DOTALL)


def normalize_language(value: str) -> str | None:
    """Map an ISO 639-1 code or English language name to a canonical name.

    Returns None when the value is not a recognized language.
    """
    key = value.strip().lower()
    if key in LANGUAGE_NAMES:
        return LANGUAGE_NAMES[key]
    for name in LANGUAGE_NAMES.values():
        if name.lower() == key:
            return name
    return None


def parse_query(text: str) -> tuple[str | None, str]:
    """Split an optional ``lang: body`` override prefix off an inline query.

    Returns ``(target_language, body)``. ``target_language`` is None when no
    *recognized* language prefix is present; an ordinary colon in the text
    (e.g. ``Note: buy milk``) is left untouched as part of the body.
    """
    match = _PREFIX_RE.match(text)
    if match:
        candidate, body = match.group(1).strip(), match.group(2).strip()
        target = normalize_language(candidate)
        if target is not None and body:
            return target, body
    return None, text.strip()


def resolve_target(value: str) -> str | None:
    """Resolve a user-supplied target language for the /setlang command.

    Recognized codes/names are canonicalized; other plausible language tokens
    are accepted as typed (the LLM interprets them). Returns None for input
    that clearly is not a language.
    """
    value = value.strip()
    canonical = normalize_language(value)
    if canonical is not None:
        return canonical
    if 1 < len(value) <= 30 and all(ch.isalpha() or ch in " -" for ch in value):
        return value.title()
    return None
