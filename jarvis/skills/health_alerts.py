"""Health alerts — JARVIS monitors health metrics and warns when thresholds exceeded."""
import threading, time, json, os
from datetime import datetime

_FILE = os.path.join(os.path.dirname(__file__), "..", "memory", "health_alerts.json")
_THRESHOLDS = {"heart_rate_max": 100, "heart_rate_min": 50, "water_min_ml": 2000, "sleep_min_hours": 6}
_monitoring = False

def set_threshold(metric: str, value: float) -> str:
    key = metric.lower().replace(" ", "_")
    _THRESHOLDS[key] = value
    return f"Threshold for {metric} set to {value}, sir."

def check_heart_rate(bpm: int) -> str:
    if bpm > _THRESHOLDS["heart_rate_max"]:
        return f"Warning: Heart rate {bpm} BPM is above {_THRESHOLDS['heart_rate_max']} BPM. Consider resting, sir."
    if bpm < _THRESHOLDS["heart_rate_min"]:
        return f"Warning: Heart rate {bpm} BPM is below {_THRESHOLDS['heart_rate_min']} BPM. Monitor closely, sir."
    return f"Heart rate {bpm} BPM is within normal range, sir."

def check_daily_water(ml: float) -> str:
    goal = _THRESHOLDS["water_min_ml"]
    pct  = min(ml / goal * 100, 100)
    if ml < goal * 0.5:
        return f"Alert: Only {ml:.0f}ml water today. You're under 50% of your {goal}ml goal, sir."
    if ml >= goal:
        return f"Hydration goal met! {ml:.0f}ml consumed — {pct:.0f}% of daily target, sir."
    return f"Hydration: {ml:.0f}ml / {goal}ml ({pct:.0f}%), sir."

def check_sleep(hours: float) -> str:
    min_h = _THRESHOLDS["sleep_min_hours"]
    if hours < min_h:
        deficit = min_h - hours
        return f"Sleep deficit alert: {hours:.1f} hours logged — {deficit:.1f} hours below minimum, sir."
    if hours >= 8:
        return f"Excellent sleep: {hours:.1f} hours. Well rested, sir."
    return f"Sleep: {hours:.1f} hours. Adequate, sir."

def start_posture_reminder(interval_mins: int = 30, callback=None) -> str:
    def _remind():
        while True:
            time.sleep(interval_mins * 60)
            msg = "Posture check, sir. Sit up straight, shoulders back, screen at eye level."
            print(f"\n🪑  {msg}")
            if callback: callback(msg)
    t = threading.Thread(target=_remind, daemon=True)
    t.start()
    return f"Posture reminders active every {interval_mins} minutes, sir."

def get_health_thresholds() -> str:
    parts = [f"{k}: {v}" for k, v in _THRESHOLDS.items()]
    return "Health thresholds, sir: " + " | ".join(parts) + "."
