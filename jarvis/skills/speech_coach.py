"""
jarvis/skills/speech_coach.py
Speech coach — JARVIS helps you practice public speaking.
Tracks speaking pace, filler words, and gives feedback.
"""
import re
import time


_FILLER_WORDS = {
    "um", "uh", "like", "you know", "basically", "literally",
    "actually", "honestly", "right", "so", "anyway", "kind of",
    "sort of", "i mean", "well", "just", "really", "very",
}

_IDEAL_WPM_RANGE = (130, 170)


def analyse_speech(text: str, duration_secs: float = 0) -> str:
    """Analyse a speech transcript for pace, fillers, and clarity."""
    text   = text.strip()
    words  = text.split()
    count  = len(words)

    # Filler word detection
    text_lower = text.lower()
    fillers    = []
    for filler in _FILLER_WORDS:
        occurrences = text_lower.count(filler)
        if occurrences > 0:
            fillers.append(f"'{filler}' x{occurrences}")

    # Sentence length analysis
    sentences = re.split(r"[.!?]+", text)
    sentences = [s.strip() for s in sentences if s.strip()]
    avg_len   = sum(len(s.split()) for s in sentences) / max(len(sentences), 1)

    # WPM if duration given
    wpm_str = ""
    if duration_secs > 0:
        wpm     = count / (duration_secs / 60)
        rating  = "too slow" if wpm < 110 else "ideal" if wpm <= 180 else "too fast"
        wpm_str = f" Speaking pace: {wpm:.0f} WPM ({rating})."

    filler_str = f" Filler words: {', '.join(fillers[:5])}." if fillers else " No filler words detected — excellent!"
    length_str = f" Average sentence length: {avg_len:.0f} words."

    return (
        f"Speech analysis, sir: {count} words, {len(sentences)} sentences."
        f"{wpm_str}{filler_str}{length_str}"
    )


def get_speaking_tip() -> str:
    """Return a random public speaking tip."""
    tips = [
        "Pause deliberately — silence is more powerful than filler words, sir.",
        "Make eye contact with different parts of the audience, not just one person, sir.",
        "Vary your pace — slow down for important points, speed up for lists, sir.",
        "Use the rule of three — audiences remember things in groups of three best, sir.",
        "Start strong — the first 30 seconds determine your audience's attention, sir.",
        "End with a call to action or a memorable closing line, sir.",
        "Record yourself speaking — most people are surprised by their own habits, sir.",
        "Breathe from your diaphragm for a deeper, more authoritative voice, sir.",
    ]
    import random
    return random.choice(tips)


def practice_prompt() -> str:
    """Return a speech practice prompt."""
    prompts = [
        "Describe your dream project in exactly 60 seconds.",
        "Explain what you do for work to someone who knows nothing about it.",
        "Tell a 2-minute story about an obstacle you overcame.",
        "Pitch your favourite app to a room of investors.",
        "Explain the plot of your favourite movie in under 90 seconds.",
    ]
    import random
    return f"Practice prompt, sir: {random.choice(prompts)}"


def count_filler_words(text: str) -> str:
    """Count filler words in a piece of text."""
    text_lower = text.lower()
    found      = {}
    for filler in _FILLER_WORDS:
        count = text_lower.count(filler)
        if count:
            found[filler] = count
    if not found:
        return "No filler words found — clean speech, sir."
    total = sum(found.values())
    top   = sorted(found.items(), key=lambda x: x[1], reverse=True)[:5]
    parts = [f"'{w}' x{c}" for w, c in top]
    return f"{total} filler word(s) found: {', '.join(parts)}, sir."
