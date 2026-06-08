"""Prompt library — JARVIS stores and recalls LLM prompt templates."""
import json, os, random
from datetime import date

_FILE = os.path.join(os.path.dirname(__file__), "..", "memory", "prompts.json")

_BUILTIN_PROMPTS = {
    "summarise": "Summarise the following in 3 bullet points: {content}",
    "email": "Write a professional email from {sender} to {recipient} about {topic}. Tone: {tone}.",
    "explain": "Explain {concept} to a {audience} in simple terms. Use an analogy.",
    "critique": "Critique the following work and suggest 3 specific improvements: {work}",
    "brainstorm": "Generate 10 creative ideas for {topic}. Be unconventional.",
    "cover letter": "Write a cover letter for a {role} position at {company}. My background: {background}.",
    "cold email": "Write a cold outreach email to {target} about {offering}. Keep it under 100 words.",
    "refine": "Improve the following text for clarity, concision, and impact: {text}",
    "debate": "Present the strongest argument for AND against: {topic}",
    "analogy": "Explain {concept} using an analogy from {domain}.",
}

def _load() -> dict:
    try:
        if os.path.exists(_FILE):
            with open(_FILE) as f: return json.load(f)
    except: pass
    return {}

def _save(data: dict):
    os.makedirs(os.path.dirname(_FILE), exist_ok=True)
    with open(_FILE, "w") as f: json.dump(data, f, indent=2)

def get_prompt(name: str, **kwargs) -> str:
    all_prompts = {**_BUILTIN_PROMPTS, **_load()}
    for key, template in all_prompts.items():
        if name.lower() in key or key in name.lower():
            result = template
            for k, v in kwargs.items():
                result = result.replace(f"{{{k}}}", str(v))
            return f"Prompt, sir:\n{result}"
    return f"Prompt '{name}' not found. Available: {', '.join(all_prompts.keys())}, sir."

def save_prompt(name: str, template: str) -> str:
    data = _load()
    data[name.lower()] = template
    _save(data)
    return f"Prompt '{name}' saved, sir."

def list_prompts() -> str:
    custom = _load()
    all_p  = list(_BUILTIN_PROMPTS.keys()) + list(custom.keys())
    return f"Available prompts: {', '.join(all_p)}, sir."

def get_random_prompt() -> str:
    name, template = random.choice(list(_BUILTIN_PROMPTS.items()))
    return f"Prompt idea — '{name}': {template}, sir."
