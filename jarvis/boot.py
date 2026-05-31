"""
jarvis/boot.py
JARVIS cinematic boot sequence — Iron Man style.
Prints an animated startup banner with system checks,
then speaks the greeting.
"""
import time
import sys


BOOT_LINES = [
    ("", 0.0),
    ("  ╔══════════════════════════════════════════════════╗", 0.05),
    ("  ║         J.A.R.V.I.S  SYSTEM INITIALISING        ║", 0.05),
    ("  ║   Just A Rather Very Intelligent System v3.0    ║", 0.03),
    ("  ╚══════════════════════════════════════════════════╝", 0.05),
    ("", 0.1),
    ("  [■■■■■■■■■■■■■■■■■■■■■■■■]  Core systems ... OK", 0.08),
    ("  [■■■■■■■■■■■■■■■■■■■■■■■■]  Voice engine  ... OK", 0.08),
    ("  [■■■■■■■■■■■■■■■■■■■■■■■■]  Memory banks  ... OK", 0.08),
    ("  [■■■■■■■■■■■■■■■■■■■■■■■■]  LLM brain     ... ONLINE", 0.08),
    ("  [■■■■■■■■■■■■■■■■■■■■■■■■]  Skills layer  ... LOADED", 0.08),
    ("", 0.1),
    ("  All systems nominal. Welcome back, sir.", 0.05),
    ("", 0.0),
]

GREETING = (
    "Good day, sir. All systems are online and operating at full capacity. "
    "J.A.R.V.I.S. is at your service."
)


def run_boot_sequence(speaker=None):
    """Print the animated boot banner. Optionally speak the greeting."""
    for line, delay in BOOT_LINES:
        print(line)
        if delay:
            time.sleep(delay)
    if speaker:
        speaker.speak(GREETING)
    else:
        print(f"\nJarvis: {GREETING}\n")
