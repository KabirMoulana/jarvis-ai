"""
jarvis/skills/whatsapp.py
WhatsApp messaging via pywhatkit (web-based, no API key).
Send messages, schedule messages, and send to groups.
Requires: pip install pywhatkit
"""
import re
from datetime import datetime, timedelta


def send_message(phone: str, message: str, wait_seconds: int = 15) -> str:
    """
    Send a WhatsApp message to a phone number.
    phone format: +1234567890 (with country code)
    """
    phone = _clean_phone(phone)
    if not phone:
        return "Invalid phone number, sir. Include country code e.g. +1234567890."
    try:
        import pywhatkit as kit
        now  = datetime.now()
        hour = now.hour
        minute = (now.minute + 2) % 60   # 2 minutes from now
        if now.minute >= 58:
            hour = (hour + 1) % 24
        kit.sendwhatmsg(phone, message, hour, minute,
                        wait_time=wait_seconds, tab_close=True)
        return f"WhatsApp message scheduled to {phone}, sir. Browser will open shortly."
    except ImportError:
        return "pywhatkit not installed, sir. Run: pip install pywhatkit"
    except Exception as e:
        return f"WhatsApp send failed: {e}"


def send_to_group(group_id: str, message: str) -> str:
    """Send a message to a WhatsApp group."""
    try:
        import pywhatkit as kit
        now    = datetime.now()
        hour   = now.hour
        minute = (now.minute + 2) % 60
        kit.sendwhatmsg_to_group(group_id, message, hour, minute,
                                 wait_time=15, tab_close=True)
        return f"Group message scheduled, sir."
    except ImportError:
        return "pywhatkit not installed. Run: pip install pywhatkit"
    except Exception as e:
        return f"Group send failed: {e}"


def send_image(phone: str, image_path: str, caption: str = "") -> str:
    """Send an image via WhatsApp."""
    phone = _clean_phone(phone)
    try:
        import pywhatkit as kit
        kit.sendwhats_image(phone, image_path, caption)
        return f"Image sent to {phone}, sir."
    except ImportError:
        return "pywhatkit not installed. Run: pip install pywhatkit"
    except Exception as e:
        return f"Image send failed: {e}"


def parse_whatsapp_command(text: str) -> tuple[str, str] | None:
    """
    Parse 'send WhatsApp to John saying hello' or
    'WhatsApp +447911123456 I'm running late'.
    Returns (phone_or_name, message) or None.
    """
    m = re.search(
        r"(?:send\s+)?whatsapp\s+(?:to\s+)?(\+?\d[\d\s\-]+|\w+)\s+(?:saying\s+|message\s+)?(.+)",
        text, re.IGNORECASE
    )
    if m:
        return m.group(1).strip(), m.group(2).strip()
    return None


def _clean_phone(phone: str) -> str:
    cleaned = re.sub(r"[\s\-\(\)]", "", phone)
    if not cleaned.startswith("+"):
        cleaned = "+" + cleaned
    return cleaned if re.match(r"^\+\d{7,15}$", cleaned) else ""
