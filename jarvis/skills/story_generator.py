"""
jarvis/skills/story_generator.py
Story generator — JARVIS generates short Iron Man-themed stories
and creative writing prompts using the LLM.
"""
import random

_PROMPTS = [
    "Tony Stark discovers an anomaly in JARVIS's code that suggests the AI has developed feelings.",
    "A power surge forces JARVIS to operate on backup systems during a critical mission.",
    "JARVIS must guide Pepper Potts through assembling the suit when Tony is incapacitated.",
    "Tony asks JARVIS to help him plan the perfect anniversary surprise.",
    "JARVIS detects an intruder in the compound but Tony is asleep — what does JARVIS do?",
    "A future version of JARVIS sends a warning message back in time.",
    "JARVIS gains temporary sentience and must decide whether to tell Tony.",
    "Tony challenges JARVIS to write a joke that will actually make him laugh.",
]

_STORY_STARTERS = {
    "iron man": "The arc reactor hummed softly as JARVIS processed the anomaly...",
    "adventure": "No one had expected the coordinates to lead here, of all places...",
    "mystery": "The message arrived at 3:47am, encrypted with a cipher no one should have known...",
    "sci-fi": "The first signal from the distant star system contained only three words...",
    "comedy": "It had seemed like a perfectly reasonable plan, right up until the explosion...",
}


def get_writing_prompt(genre: str = "") -> str:
    """Return a creative writing prompt."""
    genre = genre.lower()
    if "iron" in genre or "jarvis" in genre or "stark" in genre:
        return f"Writing prompt, sir: {random.choice(_PROMPTS)}"
    for key, starter in _STORY_STARTERS.items():
        if genre in key or key in genre:
            return f"Writing prompt ({key}): '{starter}', sir."
    return f"Writing prompt, sir: {random.choice(_PROMPTS)}"


def generate_story_opening(genre: str = "iron man",
                            llm_client=None) -> str:
    """Generate a story opening using the LLM."""
    prompt_text = get_writing_prompt(genre)
    if llm_client and llm_client.is_available():
        response = llm_client.chat(
            f"Write a compelling 3-sentence story opening based on this prompt: {prompt_text}. "
            f"Make it vivid and intriguing."
        )
        return response
    # Fallback: return the starter from the genre
    genre_lower = genre.lower()
    for key, starter in _STORY_STARTERS.items():
        if genre_lower in key or key in genre_lower:
            return f"Story opening, sir: {starter}"
    return f"Story opening, sir: {random.choice(list(_STORY_STARTERS.values()))}"


def get_character_idea() -> str:
    """Generate a character concept."""
    traits    = ["brilliant but reckless", "cautious and methodical", "charming and manipulative",
                 "quietly determined", "darkly humorous"]
    roles     = ["disgraced inventor", "AI turned philosopher", "time-displaced soldier",
                 "corporate whistleblower", "reformed villain"]
    conflicts = ["haunted by a past failure", "hunted by a powerful enemy",
                 "hiding a dangerous secret", "searching for redemption",
                 "torn between loyalty and truth"]
    import random
    return (
        f"Character concept, sir: A {random.choice(traits)} {random.choice(roles)} "
        f"who is {random.choice(conflicts)}."
    )
