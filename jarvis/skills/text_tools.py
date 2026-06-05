"""
jarvis/skills/text_tools.py
Text processing tools — JARVIS transforms text by voice.
Uppercase, lowercase, title case, reverse, count, encode, decode.
"""
import base64
import hashlib
import re


def to_uppercase(text: str) -> str:
    result = text.upper()
    _copy(result)
    return f"Uppercase: {result}"


def to_lowercase(text: str) -> str:
    result = text.lower()
    _copy(result)
    return f"Lowercase: {result}"


def to_title_case(text: str) -> str:
    result = text.title()
    _copy(result)
    return f"Title case: {result}"


def to_snake_case(text: str) -> str:
    result = re.sub(r"\s+", "_", text.strip().lower())
    result = re.sub(r"[^\w_]", "", result)
    _copy(result)
    return f"Snake case: {result}"


def to_camel_case(text: str) -> str:
    words  = text.strip().split()
    result = words[0].lower() + "".join(w.title() for w in words[1:])
    _copy(result)
    return f"Camel case: {result}"


def reverse_text(text: str) -> str:
    result = text[::-1]
    _copy(result)
    return f"Reversed: {result}"


def count_text(text: str) -> str:
    words   = len(text.split())
    chars   = len(text)
    chars_ns = len(text.replace(" ", ""))
    sentences = len(re.findall(r"[.!?]+", text))
    return f"Characters: {chars} ({chars_ns} without spaces). Words: {words}. Sentences: {sentences}, sir."


def encode_base64(text: str) -> str:
    encoded = base64.b64encode(text.encode()).decode()
    _copy(encoded)
    return f"Base64 encoded: {encoded[:60]}{'...' if len(encoded) > 60 else ''}, sir."


def decode_base64(text: str) -> str:
    try:
        decoded = base64.b64decode(text.strip()).decode()
        _copy(decoded)
        return f"Decoded: {decoded}, sir."
    except Exception:
        return "Invalid base64 string, sir."


def hash_text(text: str, algorithm: str = "sha256") -> str:
    algos = {"md5": hashlib.md5, "sha1": hashlib.sha1,
             "sha256": hashlib.sha256, "sha512": hashlib.sha512}
    func = algos.get(algorithm.lower(), hashlib.sha256)
    result = func(text.encode()).hexdigest()
    _copy(result)
    return f"{algorithm.upper()} hash: {result[:32]}..., sir."


def remove_duplicates(text: str) -> str:
    words  = text.split()
    seen   = set()
    result = " ".join(w for w in words if not (w.lower() in seen or seen.add(w.lower())))
    return f"Duplicates removed: {result}, sir."


def _copy(text: str):
    import subprocess, sys
    try:
        if sys.platform == "darwin":
            subprocess.run(["pbcopy"], input=text.encode(), check=True)
    except Exception:
        pass
