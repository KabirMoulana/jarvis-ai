"""
jarvis/skills/regex_helper.py
Regex helper — JARVIS tests and explains regular expressions.
Useful for developers who need quick regex help by voice.
"""
import re


_COMMON_PATTERNS = {
    "email":      r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
    "phone":      r"^\+?[\d\s\-\(\)]{7,15}$",
    "url":        r"https?://[^\s/$.?#].[^\s]*",
    "ip":         r"^(\d{1,3}\.){3}\d{1,3}$",
    "postcode uk":r"^[A-Z]{1,2}\d[A-Z\d]? \d[A-Z]{2}$",
    "date":       r"\d{4}-\d{2}-\d{2}",
    "time":       r"\d{1,2}:\d{2}(:\d{2})? ?(am|pm)?",
    "password strong": r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
    "credit card":r"\d{4}[\s-]\d{4}[\s-]\d{4}[\s-]\d{4}",
    "hex color":  r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$",
}


def test_regex(pattern: str, text: str) -> str:
    """Test a regex pattern against text."""
    try:
        matches = re.findall(pattern, text)
        if matches:
            return f"Pattern matches! Found {len(matches)} match(es): {', '.join(str(m) for m in matches[:5])}, sir."
        return f"No matches found for that pattern in the text, sir."
    except re.error as e:
        return f"Invalid regex pattern: {e}, sir."


def get_common_pattern(name: str) -> str:
    """Return a common regex pattern by name."""
    name = name.lower().strip()
    for key, pattern in _COMMON_PATTERNS.items():
        if name in key or key in name:
            return f"Pattern for {key}: {pattern}, sir."
    patterns = ", ".join(_COMMON_PATTERNS.keys())
    return f"Pattern not found. Available: {patterns}, sir."


def validate_with_pattern(pattern_name: str, value: str) -> str:
    """Validate a value against a named common pattern."""
    pattern_name = pattern_name.lower()
    for key, pattern in _COMMON_PATTERNS.items():
        if pattern_name in key or key in pattern_name:
            match = bool(re.match(pattern, value.strip(), re.IGNORECASE))
            result = "valid" if match else "invalid"
            return f"'{value}' is {result} for {key} format, sir."
    return f"Pattern '{pattern_name}' not found, sir."


def extract_emails(text: str) -> str:
    emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    if not emails:
        return "No email addresses found in the text, sir."
    return f"Found {len(emails)} email(s): {', '.join(emails)}, sir."


def extract_urls(text: str) -> str:
    urls = re.findall(r"https?://[^\s/$.?#].[^\s]*", text)
    if not urls:
        return "No URLs found in the text, sir."
    return f"Found {len(urls)} URL(s): {', '.join(urls[:5])}, sir."


def extract_numbers(text: str) -> str:
    numbers = re.findall(r"-?\d+\.?\d*", text)
    if not numbers:
        return "No numbers found in the text, sir."
    return f"Numbers found: {', '.join(numbers)}, sir."
