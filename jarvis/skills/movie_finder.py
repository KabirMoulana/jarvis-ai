"""
jarvis/skills/movie_finder.py
Movie finder — JARVIS recommends movies and shows.
Uses the OMDB API (free tier) or falls back to curated lists.
"""
import urllib.request
import urllib.parse
import json
import os
import webbrowser

_OMDB_KEY = os.getenv("OMDB_API_KEY", "")
_OMDB_URL = "http://www.omdbapi.com/"

_CURATED = {
    "action":   ["Mad Max: Fury Road", "John Wick", "Top Gun: Maverick", "The Dark Knight"],
    "sci-fi":   ["Interstellar", "Inception", "Ex Machina", "Blade Runner 2049", "Dune"],
    "comedy":   ["The Grand Budapest Hotel", "Superbad", "Game Night", "The Nice Guys"],
    "drama":    ["The Shawshank Redemption", "Parasite", "The Godfather", "1917"],
    "thriller": ["Gone Girl", "Prisoners", "Knives Out", "Get Out", "Parasite"],
    "iron man": ["Iron Man", "Iron Man 2", "Iron Man 3", "Avengers", "Avengers: Endgame"],
    "horror":   ["Get Out", "A Quiet Place", "Hereditary", "The Conjuring"],
    "animation":["Spider-Man: Into the Spider-Verse", "Up", "Soul", "Coco", "Spirited Away"],
}


def search_movie(title: str) -> str:
    """Look up a movie by title."""
    if _OMDB_KEY:
        try:
            params  = urllib.parse.urlencode({"t": title, "apikey": _OMDB_KEY})
            url     = f"{_OMDB_URL}?{params}"
            req     = urllib.request.Request(url, headers={"User-Agent": "JarvisAI/3.0"})
            with urllib.request.urlopen(req, timeout=6) as resp:
                data = json.loads(resp.read())
            if data.get("Response") == "True":
                return (
                    f"{data['Title']} ({data['Year']}). "
                    f"Rating: {data.get('imdbRating', 'N/A')}/10. "
                    f"Genre: {data.get('Genre', 'N/A')}. "
                    f"{data.get('Plot', '')[:150]}, sir."
                )
        except Exception:
            pass

    return f"Set OMDB_API_KEY in .env for movie details, sir. Try searching: https://www.imdb.com/find?q={urllib.parse.quote(title)}"


def recommend_movie(genre: str = "") -> str:
    """Recommend a movie for a genre."""
    import random
    genre = genre.lower().strip()
    for key in _CURATED:
        if genre in key or key in genre:
            movie = random.choice(_CURATED[key])
            return f"I recommend '{movie}' for {key}, sir."
    movie = random.choice([m for movies in _CURATED.values() for m in movies])
    return f"How about '{movie}', sir? A fine choice by any measure."


def get_genre_list(genre: str) -> str:
    """List movies for a genre."""
    genre = genre.lower()
    for key, movies in _CURATED.items():
        if genre in key or key in genre:
            return f"{key.title()} recommendations: " + ", ".join(movies) + ", sir."
    genres = ", ".join(_CURATED.keys())
    return f"Genres available: {genres}, sir."


def open_imdb(title: str) -> str:
    """Open IMDB search for a movie."""
    encoded = urllib.parse.quote(title)
    webbrowser.open(f"https://www.imdb.com/find?q={encoded}")
    return f"Opening IMDB for '{title}', sir."


def open_streaming(title: str, platform: str = "netflix") -> str:
    """Search for a movie on a streaming platform."""
    encoded = urllib.parse.quote(title)
    urls = {
        "netflix":    f"https://www.netflix.com/search?q={encoded}",
        "prime":      f"https://www.amazon.com/s?k={encoded}&i=instant-video",
        "disney":     f"https://www.disneyplus.com/search/{encoded}",
        "apple tv":   f"https://tv.apple.com/search?term={encoded}",
    }
    url = urls.get(platform.lower(), urls["netflix"])
    webbrowser.open(url)
    return f"Searching {platform.title()} for '{title}', sir."
