"""
jarvis/skills/email_scheduler.py
Email scheduler — JARVIS schedules emails to be sent later.
Drafts are stored and sent at the specified time.
"""
import json
import os
import threading
import time
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

_FILE     = os.path.join(os.path.dirname(__file__), "..", "memory", "scheduled_emails.json")
_USER     = os.getenv("JARVIS_EMAIL", "")
_PASSWORD = os.getenv("JARVIS_EMAIL_PASSWORD", "")
_HOST     = os.getenv("JARVIS_EMAIL_SMTP_HOST", "smtp.gmail.com")
_PORT     = int(os.getenv("JARVIS_EMAIL_SMTP_PORT", "587"))


def _load() -> list:
    try:
        if os.path.exists(_FILE):
            with open(_FILE) as f:
                return json.load(f)
    except Exception:
        pass
    return []


def _save(data: list):
    os.makedirs(os.path.dirname(_FILE), exist_ok=True)
    with open(_FILE, "w") as f:
        json.dump(data, f, indent=2, default=str)


def schedule_email(to: str, subject: str, body: str,
                   send_at: datetime, callback=None) -> str:
    """Schedule an email to be sent at a specific time."""
    data = _load()
    entry = {
        "id":      len(data) + 1,
        "to":      to,
        "subject": subject,
        "body":    body,
        "send_at": send_at.isoformat(),
        "sent":    False,
    }
    data.append(entry)
    _save(data)

    delay = (send_at - datetime.now()).total_seconds()
    if delay > 0:
        def _fire():
            result = _send_now(to, subject, body)
            entry["sent"] = True
            _save(data)
            msg = f"Scheduled email to {to} sent, sir."
            if callback: callback(msg)

        t = threading.Timer(delay, _fire)
        t.daemon = True
        t.start()

    time_str = send_at.strftime("%I:%M %p")
    return f"Email to {to} scheduled for {time_str}, sir."


def _send_now(to: str, subject: str, body: str) -> bool:
    if not _USER or not _PASSWORD:
        return False
    try:
        msg           = MIMEMultipart()
        msg["From"]   = _USER
        msg["To"]     = to
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))
        with smtplib.SMTP(_HOST, _PORT) as server:
            server.starttls()
            server.login(_USER, _PASSWORD)
            server.send_message(msg)
        return True
    except Exception:
        return False


def list_scheduled() -> str:
    data    = _load()
    pending = [e for e in data if not e["sent"]]
    if not pending:
        return "No scheduled emails, sir."
    parts = [f"{e['id']}. To: {e['to']} at {e['send_at'][11:16]}" for e in pending]
    return f"{len(pending)} scheduled email(s): " + "; ".join(parts) + ", sir."


def cancel_scheduled(email_id: int) -> str:
    data = _load()
    for e in data:
        if e["id"] == email_id and not e["sent"]:
            e["sent"] = True  # Mark as sent to prevent sending
            _save(data)
            return f"Scheduled email {email_id} cancelled, sir."
    return f"Email {email_id} not found or already sent, sir."
