"""
jarvis/skills/calendar_skill.py
Calendar integration — reads events from a local ICS file or Google Calendar.
No API key needed for local ICS (iCloud, Outlook export).
Google Calendar requires credentials.json from Google Cloud Console.
"""
import os
import json
from datetime import datetime, date, timedelta

# ── Local ICS parser (no dependencies) ───────────────────────────────────────
_ICS_PATH = os.getenv("JARVIS_CALENDAR_ICS", "")


def _parse_ics(path: str, target_date: date) -> list[dict]:
    events = []
    try:
        with open(path, encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return []

    for block in content.split("BEGIN:VEVENT"):
        if "END:VEVENT" not in block:
            continue
        def _get(key):
            for line in block.splitlines():
                if line.startswith(key + ":") or line.startswith(key + ";"):
                    return line.split(":", 1)[-1].strip()
            return ""

        summary = _get("SUMMARY")
        dtstart = _get("DTSTART")
        dtend   = _get("DTEND")

        try:
            if len(dtstart) == 8:
                event_date = datetime.strptime(dtstart, "%Y%m%d").date()
                time_str   = "All day"
            else:
                dt         = datetime.strptime(dtstart[:15], "%Y%m%dT%H%M%S")
                event_date = dt.date()
                time_str   = dt.strftime("%I:%M %p")

            if event_date == target_date and summary:
                events.append({"summary": summary, "time": time_str})
        except Exception:
            continue

    return sorted(events, key=lambda e: e["time"])


def get_today_events() -> str:
    return get_events_for_date(date.today())


def get_tomorrow_events() -> str:
    return get_events_for_date(date.today() + timedelta(days=1))


def get_events_for_date(target: date) -> str:
    label = "today" if target == date.today() else target.strftime("%A, %B %d")

    # Try local ICS first
    if _ICS_PATH and os.path.exists(_ICS_PATH):
        events = _parse_ics(_ICS_PATH, target)
        if not events:
            return f"No events scheduled for {label}, sir."
        lines = [f"{e['time']}: {e['summary']}" for e in events]
        return f"You have {len(events)} event(s) for {label}: " + "; ".join(lines) + "."

    # Try Google Calendar
    try:
        return _google_calendar_events(target, label)
    except ImportError:
        pass
    except Exception as e:
        return f"Calendar error: {e}"

    return (
        f"No calendar connected, sir. "
        f"Set JARVIS_CALENDAR_ICS in your .env to point to an ICS file, "
        f"or install google-auth-oauthlib for Google Calendar."
    )


def _google_calendar_events(target: date, label: str) -> str:
    from googleapiclient.discovery import build
    from google.oauth2.credentials  import Credentials
    from google_auth_oauthlib.flow  import InstalledAppFlow

    SCOPES   = ["https://www.googleapis.com/auth/calendar.readonly"]
    creds    = None
    token_f  = os.path.join(os.path.dirname(__file__), "..", "memory", "gcal_token.json")
    creds_f  = os.path.join(os.path.dirname(__file__), "..", "memory", "credentials.json")

    if os.path.exists(token_f):
        creds = Credentials.from_authorized_user_file(token_f, SCOPES)
    if not creds or not creds.valid:
        flow  = InstalledAppFlow.from_client_secrets_file(creds_f, SCOPES)
        creds = flow.run_local_server(port=0)
        with open(token_f, "w") as f:
            f.write(creds.to_json())

    service  = build("calendar", "v3", credentials=creds)
    start    = datetime.combine(target, datetime.min.time()).isoformat() + "Z"
    end      = datetime.combine(target + timedelta(days=1), datetime.min.time()).isoformat() + "Z"
    result   = service.events().list(
        calendarId="primary", timeMin=start, timeMax=end,
        singleEvents=True, orderBy="startTime"
    ).execute()
    items = result.get("items", [])

    if not items:
        return f"No events scheduled for {label}, sir."

    lines = []
    for item in items:
        summary = item.get("summary", "Untitled event")
        start_t = item["start"].get("dateTime", item["start"].get("date", ""))
        try:
            t = datetime.fromisoformat(start_t.replace("Z", "")).strftime("%I:%M %p")
        except Exception:
            t = "All day"
        lines.append(f"{t}: {summary}")

    return f"You have {len(lines)} event(s) for {label}: " + "; ".join(lines) + "."
