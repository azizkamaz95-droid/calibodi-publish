"""Légendes par réseau. TikTok : courte (accroche + question + hashtags du sujet), pas la description complète avec les
sources (elles sont à l'écran et sur YouTube). Remplace l'ancien suffixe fixe « #CaliBodi #fitness #workout #squat »."""
import re

MAX_TAGS = 5


def _tags(text):
    out, seen = [], set()
    for t in re.findall(r"#[\wÀ-ÿ]+", text):
        if t.lower() not in seen:
            seen.add(t.lower())
            out.append(t)
    return out


def tiktok_caption(title, description):
    lines = [l.strip() for l in description.splitlines()]
    question = next((l for l in lines if l.startswith("👉")), "")
    tags = _tags(description)
    for extra in ("#fitness", "#CaliBodi"):
        if extra.lower() not in {t.lower() for t in tags}:
            tags.append(extra)
    tags = tags[:MAX_TAGS]
    parts = [title.strip()]
    if question:
        parts.append(question)
    parts.append("Vidéo générée par IA.")
    parts.append(" ".join(tags))
    return "\n\n".join(parts)[:2200]
