"""
jarvis/skills/sentiment_analyzer.py
Sentiment analysis — JARVIS tells you how positive, negative,
or neutral a piece of text is. Uses TextBlob if available,
with a keyword-based fallback.
"""

_POSITIVE_WORDS = {
    "great", "excellent", "amazing", "wonderful", "fantastic", "good",
    "love", "happy", "joy", "brilliant", "perfect", "outstanding",
    "superb", "awesome", "best", "beautiful", "incredible", "exciting",
    "thrilled", "delighted", "positive", "success", "win", "triumph",
}

_NEGATIVE_WORDS = {
    "bad", "terrible", "awful", "horrible", "hate", "sad", "angry",
    "worst", "failure", "broken", "wrong", "poor", "disappointing",
    "disaster", "problem", "issue", "error", "fail", "negative",
    "terrible", "dreadful", "pathetic", "useless", "ugly", "boring",
}


def analyse_sentiment(text: str) -> str:
    """Analyse the sentiment of a piece of text."""
    text = text.strip()
    if not text:
        return "No text provided, sir."

    try:
        from textblob import TextBlob
        blob       = TextBlob(text)
        polarity   = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        label      = _polarity_label(polarity)
        return (
            f"Sentiment analysis, sir: {label} "
            f"(polarity: {polarity:+.2f}, "
            f"subjectivity: {subjectivity:.0%})."
        )
    except ImportError:
        pass

    return _keyword_sentiment(text)


def _keyword_sentiment(text: str) -> str:
    words    = set(text.lower().split())
    pos      = len(words & _POSITIVE_WORDS)
    neg      = len(words & _NEGATIVE_WORDS)
    if pos > neg:
        return f"That reads as positive sentiment, sir ({pos} positive indicators)."
    elif neg > pos:
        return f"That reads as negative sentiment, sir ({neg} negative indicators)."
    else:
        return "That reads as neutral sentiment, sir."


def _polarity_label(polarity: float) -> str:
    if polarity >= 0.5:   return "very positive"
    if polarity >= 0.1:   return "positive"
    if polarity >= -0.1:  return "neutral"
    if polarity >= -0.5:  return "negative"
    return "very negative"


def analyse_mood_from_journal(entries: list[str]) -> str:
    """Analyse mood trend across multiple journal entries."""
    if not entries:
        return "No journal entries provided, sir."
    try:
        from textblob import TextBlob
        scores = [TextBlob(e).sentiment.polarity for e in entries]
        avg    = sum(scores) / len(scores)
        trend  = "improving" if scores[-1] > scores[0] else "declining"
        return (
            f"Journal mood analysis, sir: average sentiment {avg:+.2f} ({_polarity_label(avg)}). "
            f"Trend: {trend} over {len(entries)} entries."
        )
    except ImportError:
        return "Install textblob for journal mood analysis: pip install textblob"


def batch_analyse(texts: list[str]) -> str:
    """Analyse sentiment for multiple texts at once."""
    if not texts:
        return "No texts provided, sir."
    results = []
    for i, text in enumerate(texts[:5], 1):
        result = analyse_sentiment(text)
        results.append(f"{i}. {result}")
    return " ".join(results)
