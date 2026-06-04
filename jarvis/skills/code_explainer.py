"""
jarvis/skills/code_explainer.py
Code explainer — JARVIS explains code snippets, error messages,
and programming concepts using the LLM.
"""


def explain_code(code: str, llm_client=None) -> str:
    """Explain what a code snippet does."""
    if not code.strip():
        return "No code provided, sir."
    if llm_client and llm_client.is_available():
        prompt = (
            f"Explain this code in 2-3 simple sentences. "
            f"Be concise and clear:\n\n{code[:1000]}"
        )
        return llm_client.chat(prompt)
    return _basic_code_analysis(code)


def explain_error(error: str, llm_client=None) -> str:
    """Explain a programming error message."""
    if llm_client and llm_client.is_available():
        prompt = f"Explain this error message and how to fix it in 2 sentences:\n\n{error}"
        return llm_client.chat(prompt)
    return _basic_error_analysis(error)


def explain_concept(concept: str, llm_client=None) -> str:
    """Explain a programming concept."""
    if llm_client and llm_client.is_available():
        prompt = f"Explain '{concept}' in programming in 2-3 simple sentences, like explaining to a smart beginner."
        return llm_client.chat(prompt)
    return _concept_fallback(concept)


def _basic_code_analysis(code: str) -> str:
    lines   = code.strip().splitlines()
    imports = [l for l in lines if l.strip().startswith(("import", "from"))]
    funcs   = [l for l in lines if l.strip().startswith("def ")]
    classes = [l for l in lines if l.strip().startswith("class ")]
    parts   = [f"{len(lines)} lines of code"]
    if imports: parts.append(f"imports: {', '.join(i.split()[-1] for i in imports[:3])}")
    if funcs:   parts.append(f"functions: {', '.join(f.split('def ')[-1].split('(')[0] for f in funcs[:3])}")
    if classes: parts.append(f"classes: {', '.join(c.split('class ')[-1].split(':')[0] for c in classes[:3])}")
    return f"Code analysis, sir: {'. '.join(parts)}. Enable Ollama for full explanation."


def _basic_error_analysis(error: str) -> str:
    error = error.lower()
    if "syntaxerror" in error:
        return "SyntaxError: There's a typo or missing character in your code, sir. Check colons, parentheses, and indentation."
    if "nameerror" in error:
        return "NameError: A variable or function is being used before it's defined, sir."
    if "typeerror" in error:
        return "TypeError: You're mixing incompatible data types, sir. Check your function arguments."
    if "indexerror" in error:
        return "IndexError: You're accessing a list index that doesn't exist, sir. Check your list length."
    if "keyerror" in error:
        return "KeyError: The dictionary key you're accessing doesn't exist, sir."
    if "importerror" in error or "modulenotfounderror" in error:
        return "ImportError: A required package is not installed, sir. Try pip install [package_name]."
    return f"Error detected, sir. Enable Ollama for detailed analysis. Raw: {error[:100]}"


def _concept_fallback(concept: str) -> str:
    concepts = {
        "recursion": "Recursion is when a function calls itself. Like a mirror facing a mirror — it repeats until a base condition stops it.",
        "api": "An API is a set of rules for how programs talk to each other. Like a waiter taking your order to the kitchen.",
        "async": "Async programming lets code run tasks without waiting for each to finish. Like cooking multiple dishes at once.",
        "oop": "Object-Oriented Programming organises code into objects with properties and methods, like blueprints for real-world things.",
        "git": "Git tracks changes to code over time, letting you go back to earlier versions and collaborate with others.",
    }
    for key, explanation in concepts.items():
        if key in concept.lower():
            return f"{explanation}, sir."
    return f"Enable Ollama for an explanation of '{concept}', sir."
