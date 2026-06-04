"""
jarvis/skills/text_summarizer.py
Text summarizer — JARVIS summarises long text, articles, or clipboard content.
Uses LLM if available, falls back to extractive summarization.
"""
import re
import urllib.request
from html.parser import HTMLParser


class _HTMLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self._text = []
    def handle_data(self, data):
        self._text.append(data)
    def get_text(self):
        return " ".join(self._text)


def summarise_text(text: str, sentences: int = 3, llm_client=None) -> str:
    """Summarise a block of text."""
    text = text.strip()
    if not text:
        return "No text to summarise, sir."

    if llm_client and llm_client.is_available():
        prompt = (
            f"Summarise the following text in exactly {sentences} concise sentences. "
            f"Be direct and factual:\n\n{text[:3000]}"
        )
        return llm_client.chat(prompt)

    return _extractive_summary(text, sentences)


def summarise_url(url: str, llm_client=None) -> str:
    """Fetch a webpage and summarise its content."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "JarvisAI/3.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="replace")

        stripper = _HTMLStripper()
        stripper.feed(html)
        text = stripper.get_text()
        text = re.sub(r"\s+", " ", text).strip()

        if not text:
            return "Could not extract text from that URL, sir."
        return summarise_text(text[:3000], llm_client=llm_client)
    except Exception as e:
        return f"Could not fetch URL: {e}"


def summarise_clipboard(llm_client=None) -> str:
    """Summarise whatever is currently on the clipboard."""
    import subprocess, sys
    try:
        if sys.platform == "darwin":
            text = subprocess.run(["pbpaste"], capture_output=True, text=True).stdout
        else:
            text = ""
        if not text.strip():
            return "Clipboard is empty, sir."
        return summarise_text(text, llm_client=llm_client)
    except Exception as e:
        return f"Could not read clipboard: {e}"


def _extractive_summary(text: str, n: int = 3) -> str:
    """Simple extractive summarisation — pick top-scoring sentences."""
    sentences = re.split(r"(?<=[.!?])\s+", text)
    if len(sentences) <= n:
        return text

    # Score by word frequency
    words  = re.findall(r"\w+", text.lower())
    freq   = {}
    for w in words:
        if len(w) > 3:
            freq[w] = freq.get(w, 0) + 1

    def score(sent):
        return sum(freq.get(w.lower(), 0) for w in re.findall(r"\w+", sent))

    scored = sorted(enumerate(sentences), key=lambda x: score(x[1]), reverse=True)
    top_n  = sorted(scored[:n], key=lambda x: x[0])
    summary = " ".join(s for _, s in top_n)
    return f"Summary, sir: {summary}"
