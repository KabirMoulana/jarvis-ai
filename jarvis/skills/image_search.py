"""
jarvis/skills/image_search.py
Image search — JARVIS opens image searches and downloads
wallpapers/images by voice.
"""
import webbrowser
import urllib.request
import urllib.parse
import json
import os


def search_images(query: str) -> str:
    """Open a Google image search for the query."""
    encoded = urllib.parse.quote(query)
    webbrowser.open(f"https://www.google.com/search?tbm=isch&q={encoded}")
    return f"Searching images for '{query}', sir."


def search_wallpapers(query: str = "space 4k") -> str:
    """Open Unsplash for wallpaper search."""
    encoded = urllib.parse.quote(query)
    webbrowser.open(f"https://unsplash.com/s/photos/{encoded}")
    return f"Opening Unsplash for '{query}' wallpapers, sir."


def download_image(url: str, filename: str = "") -> str:
    """Download an image from a URL to the Desktop."""
    save_dir = os.path.expanduser("~/Desktop")
    if not filename:
        filename = f"jarvis_image_{url.split('/')[-1][:20]}.jpg"
    path = os.path.join(save_dir, filename)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "JarvisAI/3.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            with open(path, "wb") as f:
                f.write(resp.read())
        return f"Image downloaded to Desktop as {filename}, sir."
    except Exception as e:
        return f"Download failed: {e}"


def get_random_wallpaper(category: str = "nature") -> str:
    """Get a random high-quality wallpaper from Unsplash."""
    try:
        url = f"https://source.unsplash.com/1920x1080/?{urllib.parse.quote(category)}"
        return download_image(url, f"wallpaper_{category.replace(' ', '_')}.jpg")
    except Exception as e:
        return f"Wallpaper download failed: {e}"


def search_gif(query: str) -> str:
    """Open GIPHY for GIF search."""
    encoded = urllib.parse.quote(query)
    webbrowser.open(f"https://giphy.com/search/{encoded}")
    return f"Opening GIPHY for '{query}' GIFs, sir."
