"""
jarvis/skills/ai_image_gen.py
AI image generation — JARVIS generates images using
Stable Diffusion (local) or opens online AI image tools.
"""
import webbrowser
import urllib.parse
import os


def generate_image_online(prompt: str, tool: str = "ideogram") -> str:
    """Open an online AI image generator with the prompt."""
    encoded = urllib.parse.quote(prompt)
    tools = {
        "ideogram":   f"https://ideogram.ai/t/explore?q={encoded}",
        "leonardo":   f"https://app.leonardo.ai/",
        "bing":       f"https://www.bing.com/images/create?q={encoded}",
        "playground": f"https://playground.com/create?q={encoded}",
        "midjourney": "https://www.midjourney.com",
    }
    tool  = tool.lower().strip()
    url   = tools.get(tool, tools["bing"])
    webbrowser.open(url)
    return f"Opening {tool.capitalize()} for image generation, sir. Prompt: '{prompt}'."


def generate_with_stable_diffusion(prompt: str, output_path: str = "") -> str:
    """Generate an image using local Stable Diffusion (requires diffusers)."""
    try:
        from diffusers import StableDiffusionPipeline
        import torch

        pipe = StableDiffusionPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            torch_dtype=torch.float16
        )
        pipe = pipe.to("mps" if torch.backends.mps.is_available() else "cpu")

        image = pipe(prompt, num_inference_steps=20).images[0]

        if not output_path:
            from datetime import datetime
            output_path = os.path.expanduser(
                f"~/Desktop/jarvis_gen_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            )
        image.save(output_path)

        import subprocess, sys
        if sys.platform == "darwin":
            subprocess.Popen(["open", output_path])

        return f"Image generated and saved to Desktop, sir."
    except ImportError:
        return (
            "Local Stable Diffusion not available, sir. "
            "Install with: pip install diffusers transformers torch. "
            "Or say 'generate image online' to use a web tool."
        )
    except Exception as e:
        return f"Image generation failed: {e}"


def list_image_tools() -> str:
    tools = "Bing Image Creator (free), Ideogram, Leonardo AI, Playground AI, Midjourney"
    return f"Available AI image tools, sir: {tools}."


def open_image_tool(tool: str = "bing") -> str:
    return generate_image_online("", tool)
