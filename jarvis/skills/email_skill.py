"""
jarvis/skills/email_skill.py
Email reading via IMAP — reads unread subject lines aloud.
Works with Gmail, Outlook, iCloud — any IMAP provider.
Credentials stored in .env — never hardcoded.

Gmail setup:
  1. Enable IMAP in Gmail settings
  2. Create an App Password (2FA required)
  3. Set JARVIS_EMAIL and JARVIS_EMAIL_PASSWORD in .env
"""
import imaplib
import email
from email.header import decode_header
import os
import re


_HOST     = os.getenv("JARVIS_EMAIL_HOST", "imap.gmail.com")
_PORT     = int(os.getenv("JARVIS_EMAIL_PORT", "993"))
_USER     = os.getenv("JARVIS_EMAIL", "")
_PASSWORD = os.getenv("JARVIS_EMAIL_PASSWORD", "")


def _decode_str(value: str | bytes, charset="utf-8") -> str:
    if isinstance(value, bytes):
        try:
            return value.decode(charset or "utf-8", errors="replace")
        except Exception:
            return value.decode("latin-1", errors="replace")
    return value or ""


def _connect() -> imaplib.IMAP4_SSL | None:
    if not _USER or not _PASSWORD:
        return None
    try:
        mail = imaplib.IMAP4_SSL(_HOST, _PORT)
        mail.login(_USER, _PASSWORD)
        return mail
    except Exception:
        return None


def get_unread_count() -> str:
    mail = _connect()
    if mail is None:
        return "Email not configured, sir. Set JARVIS_EMAIL and JARVIS_EMAIL_PASSWORD in your .env file."
    try:
        mail.select("INBOX")
        _, data = mail.search(None, "UNSEEN")
        count   = len(data[0].split()) if data[0] else 0
        mail.logout()
        if count == 0:
            return "No unread emails, sir. Your inbox is clear."
        return f"You have {count} unread email{'s' if count > 1 else ''} in your inbox, sir."
    except Exception as e:
        return f"Could not check email: {e}"


def read_unread_subjects(limit: int = 5) -> str:
    mail = _connect()
    if mail is None:
        return "Email not configured, sir. Set JARVIS_EMAIL and JARVIS_EMAIL_PASSWORD in your .env file."
    try:
        mail.select("INBOX")
        _, data = mail.search(None, "UNSEEN")
        ids     = data[0].split()
        if not ids:
            mail.logout()
            return "No unread emails, sir."

        recent  = ids[-limit:]
        subjects = []
        senders  = []

        for uid in reversed(recent):
            _, msg_data = mail.fetch(uid, "(RFC822.HEADER)")
            raw         = msg_data[0][1]
            msg         = email.message_from_bytes(raw)

            # Subject
            subj_raw = decode_header(msg.get("Subject", "No subject"))
            subject  = "".join(_decode_str(part, enc) for part, enc in subj_raw)
            subject  = re.sub(r"\s+", " ", subject).strip()

            # Sender name only
            from_raw = decode_header(msg.get("From", "Unknown"))
            sender   = "".join(_decode_str(p, e) for p, e in from_raw)
            sender   = re.sub(r"<.*?>", "", sender).strip().strip('"')

            subjects.append(f"{sender}: {subject}")

        mail.logout()
        intro = f"Your {len(subjects)} most recent unread email{'s' if len(subjects) > 1 else ''}, sir. "
        return intro + ". ".join(f"{i+1}. {s}" for i, s in enumerate(subjects)) + "."

    except Exception as e:
        return f"Error reading emails: {e}"


def get_latest_from(sender_query: str) -> str:
    """Find the latest email from a specific sender."""
    mail = _connect()
    if mail is None:
        return "Email not configured, sir."
    try:
        mail.select("INBOX")
        _, data = mail.search(None, f'FROM "{sender_query}"')
        ids     = data[0].split()
        if not ids:
            mail.logout()
            return f"No emails found from {sender_query}, sir."
        _, msg_data = mail.fetch(ids[-1], "(RFC822.HEADER)")
        msg     = email.message_from_bytes(msg_data[0][1])
        subj    = decode_header(msg.get("Subject", "No subject"))
        subject = "".join(_decode_str(p, e) for p, e in subj)
        mail.logout()
        return f"Latest email from {sender_query}: {subject}."
    except Exception as e:
        return f"Error: {e}"
