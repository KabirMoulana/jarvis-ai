
"""Opens a web search in the default browser."""
import webbrowser
import urllib.parse


def search_web(query: str) -> str:
    url = "https://www.google.com/search?q=" + urllib.parse.quote(query)
    webbrowser.open(url)
    return f"Searching the web for: {query}"


def handle(command: str) -> str | None:
    triggers = ["search for", "google", "look up", "search"]
    for trigger in triggers:
        if trigger in command:
            query = command.replace(trigger, "").strip()
            return search_web(query)
    return None
