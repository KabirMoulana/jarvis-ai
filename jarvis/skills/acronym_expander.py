"""
jarvis/skills/acronym_expander.py
Acronym expander — JARVIS explains tech, business, and
common acronyms instantly.
"""

_ACRONYMS = {
    # Tech
    "API":   "Application Programming Interface",
    "CLI":   "Command Line Interface",
    "CSS":   "Cascading Style Sheets",
    "DNS":   "Domain Name System",
    "GPU":   "Graphics Processing Unit",
    "HTML":  "HyperText Markup Language",
    "HTTP":  "HyperText Transfer Protocol",
    "HTTPS": "HyperText Transfer Protocol Secure",
    "IDE":   "Integrated Development Environment",
    "IP":    "Internet Protocol",
    "JSON":  "JavaScript Object Notation",
    "JWT":   "JSON Web Token",
    "LLM":   "Large Language Model",
    "ML":    "Machine Learning",
    "OS":    "Operating System",
    "OOP":   "Object-Oriented Programming",
    "RAM":   "Random Access Memory",
    "REST":  "Representational State Transfer",
    "SDK":   "Software Development Kit",
    "SQL":   "Structured Query Language",
    "SSH":   "Secure Shell",
    "SSL":   "Secure Sockets Layer",
    "TLS":   "Transport Layer Security",
    "UI":    "User Interface",
    "URL":   "Uniform Resource Locator",
    "UX":    "User Experience",
    "VPN":   "Virtual Private Network",
    "XML":   "eXtensible Markup Language",
    "YAML":  "YAML Ain't Markup Language",
    # Business
    "B2B":   "Business to Business",
    "B2C":   "Business to Consumer",
    "CEO":   "Chief Executive Officer",
    "CFO":   "Chief Financial Officer",
    "CTO":   "Chief Technology Officer",
    "KPI":   "Key Performance Indicator",
    "MVP":   "Minimum Viable Product",
    "OKR":   "Objectives and Key Results",
    "P&L":   "Profit and Loss",
    "ROI":   "Return on Investment",
    "SaaS":  "Software as a Service",
    "SME":   "Subject Matter Expert",
    # AI/ML
    "AI":    "Artificial Intelligence",
    "CNN":   "Convolutional Neural Network",
    "GAN":   "Generative Adversarial Network",
    "GPT":   "Generative Pre-trained Transformer",
    "NLP":   "Natural Language Processing",
    "RNN":   "Recurrent Neural Network",
    "RLHF":  "Reinforcement Learning from Human Feedback",
    # Iron Man
    "JARVIS":"Just A Rather Very Intelligent System",
    "FRIDAY":"Female Replacement Intelligent Digital Assistant Youth",
    "SHIELD":"Strategic Homeland Intervention, Enforcement and Logistics Division",
    "HYDRA": "Hysterical Organization dedicated to the ruthless victory of ARNIM ZOLA",
}


def expand(acronym: str) -> str:
    """Expand an acronym."""
    key = acronym.upper().strip()
    if key in _ACRONYMS:
        return f"{key} stands for: {_ACRONYMS[key]}, sir."
    # Fuzzy search
    matches = {k: v for k, v in _ACRONYMS.items() if acronym.upper() in k}
    if matches:
        parts = [f"{k}: {v}" for k, v in list(matches.items())[:3]]
        return "Possible matches: " + " | ".join(parts) + ", sir."
    return f"Acronym '{acronym}' not in database, sir."


def add_acronym(acronym: str, expansion: str) -> str:
    """Add a custom acronym."""
    _ACRONYMS[acronym.upper()] = expansion
    return f"Added '{acronym.upper()}' = {expansion}, sir."


def random_acronym() -> str:
    """Return a random acronym."""
    import random
    key, value = random.choice(list(_ACRONYMS.items()))
    return f"Did you know? {key} = {value}, sir."


def list_category(category: str) -> str:
    """List acronyms by category hint."""
    cat   = category.lower()
    found = []
    if cat in ("ai", "ml", "machine learning"):
        found = [(k, v) for k, v in _ACRONYMS.items()
                 if any(w in v.lower() for w in ["intelligence", "learning", "neural", "language"])]
    elif cat in ("tech", "technology"):
        found = [(k, v) for k, v in _ACRONYMS.items()
                 if any(w in v.lower() for w in ["protocol", "interface", "system", "language"])]
    if found:
        return ", ".join(f"{k}" for k, _ in found[:10]) + ", sir."
    return f"No acronyms found for category '{category}', sir."
