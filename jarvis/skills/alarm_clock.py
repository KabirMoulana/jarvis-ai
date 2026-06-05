"""
jarvis/skills/alarm_clock.py
Smart alarm clock — JARVIS wakes you with a custom message,
motivational quote, weather, and your agenda for the day.
"""
import threading
import time
from datetime import datetime


_alarm_thread = None
_alarm_active = False


def set_smart_alarm(hour: int, minute: int, callback=None) -> str:
    """Set a smart alarm that wakes with a full morning briefing."""
    global _alarm_thread, _alarm_active

    now     = datetime.now()
    target  = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    from datetime import timedelta
    if target <= now:
        target += timedelta(days=1)

    delay = (target - datetime.now()).total_seconds()
    _alarm_active = True

    def _fire():
        global _alarm_active
        if not _alarm_active:
            return
        time_str = target.strftime("%I:%M %p")
        msg = (
            f"Good morning, sir. It is {time_str}. "
            f"Rise and shine. The world awaits your genius."
        )
        # Play system beep
        try:
            import sys
            for _ in range(3):
                sys.stdout.write("\a")
                sys.stdout.flush()
                time.sleep(0.5)
        except Exception:
            pass

        print(f"\n⏰  {msg}")
        if callback:
            callback(msg)
            # Follow up with morning briefing
            try:
                from jarvis.skills.briefing import get_briefing
                briefing = get_briefing()
                time.sleep(2)
                callback(briefing)
            except Exception:
                pass

    _alarm_thread = threading.Timer(delay, _fire)
    _alarm_thread.daemon = True
    _alarm_thread.start()

    time_str = target.strftime("%I:%M %p")
    return (
        f"Smart alarm set for {time_str}, sir. "
        f"I'll wake you with the morning briefing."
    )


def cancel_smart_alarm() -> str:
    global _alarm_active, _alarm_thread
    _alarm_active = False
    if _alarm_thread:
        _alarm_thread.cancel()
    return "Smart alarm cancelled, sir."


def sleep_calculator(wake_hour: int, wake_minute: int) -> str:
    """Calculate optimal bedtimes based on 90-minute sleep cycles."""
    from datetime import datetime, timedelta
    wake  = datetime.now().replace(hour=wake_hour, minute=wake_minute, second=0)
    times = []
    for cycles in range(6, 1, -1):
        sleep_time = wake - timedelta(minutes=cycles * 90 + 15)
        times.append(f"{sleep_time.strftime('%I:%M %p')} ({cycles} cycles, {cycles * 1.5:.0f}h)")
    return (
        f"To wake at {wake.strftime('%I:%M %p')} feeling refreshed, "
        f"go to sleep at one of: " + " | ".join(times[:4]) + ", sir."
    )


def get_optimal_wake_time(sleep_hour: int, sleep_minute: int) -> str:
    """Given a bedtime, calculate the best times to wake up."""
    from datetime import datetime, timedelta
    bed  = datetime.now().replace(hour=sleep_hour, minute=sleep_minute, second=0)
    times = []
    for cycles in range(3, 7):
        wake = bed + timedelta(minutes=cycles * 90 + 15)
        times.append(f"{wake.strftime('%I:%M %p')} ({cycles} cycles)")
    return (
        f"If you sleep at {bed.strftime('%I:%M %p')}, "
        f"optimal wake times are: " + " | ".join(times) + ", sir."
    )
