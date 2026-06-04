"""
jarvis/skills/email_composer.py
AI-powered email composer — JARVIS drafts emails by voice
and sends them via SMTP. Uses LLM to write professional emails.
"""
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

_SMTP_HOST = os.getenv("JARVIS_EMAIL_SMTP_HOST", "smtp.gmail.com")
_SMTP_PORT = int(os.getenv("JARVIS_EMAIL_SMTP_PORT", "587"))
_USER      = os.getenv("JARVIS_EMAIL", "")
_PASSWORD  = os.getenv("JARVIS_EMAIL_PASSWORD", "")

_TEMPLATES = {
    "meeting": (
        "Meeting Request",
        "I hope this message finds you well. I would like to schedule a meeting "
        "to discuss {topic}. Please let me know your availability. "
        "Best regards."
    ),
    "follow up": (
        "Following Up",
        "I wanted to follow up on our previous conversation regarding {topic}. "
        "Please let me know if you need any additional information. "
        "Best regards."
    ),
    "thank you": (
        "Thank You",
        "I wanted to take a moment to express my sincere gratitude for {topic}. "
        "It was greatly appreciated. Best regards."
    ),
    "apology": (
        "Apologies",
        "I sincerely apologize for {topic}. I take full responsibility and will "
        "ensure this does not happen again. Best regards."
    ),
    "introduction": (
        "Introduction",
        "My name is {name} and I am reaching out regarding {topic}. "
        "I would love the opportunity to connect. Best regards."
    ),
}


def draft_email(to: str, subject: str, body: str) -> str:
    """Return a formatted email draft for review."""
    return (
        f"Email drafted, sir.\n"
        f"To: {to}\n"
        f"Subject: {subject}\n"
        f"Body: {body}\n"
        f"Say 'send it' to send or 'discard' to cancel."
    )


def send_email(to: str, subject: str, body: str) -> str:
    """Send an email via SMTP."""
    if not _USER or not _PASSWORD:
        return "Email not configured, sir. Set JARVIS_EMAIL and JARVIS_EMAIL_PASSWORD in .env."
    try:
        msg              = MIMEMultipart()
        msg["From"]      = _USER
        msg["To"]        = to
        msg["Subject"]   = subject
        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(_SMTP_HOST, _SMTP_PORT) as server:
            server.starttls()
            server.login(_USER, _PASSWORD)
            server.send_message(msg)
        return f"Email sent to {to}, sir."
    except Exception as e:
        return f"Failed to send email: {e}"


def use_template(template_name: str, to: str, topic: str = "", name: str = "") -> str:
    """Draft an email from a template."""
    tmpl = None
    for key, val in _TEMPLATES.items():
        if key in template_name.lower():
            tmpl = val
            break
    if not tmpl:
        templates = ", ".join(_TEMPLATES.keys())
        return f"Template not found, sir. Available: {templates}."
    subject = tmpl[0]
    body    = tmpl[1].format(topic=topic or "the matter at hand", name=name or "your contact")
    return draft_email(to, subject, body)


def quick_reply(to: str, original_subject: str, reply_body: str) -> str:
    """Send a quick reply to an email."""
    subject = f"Re: {original_subject}" if not original_subject.startswith("Re:") else original_subject
    return send_email(to, subject, reply_body)
