
"""Centralized logging for Jarvis."""
import logging
import os
from datetime import datetime

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
log_file = os.path.join(LOG_DIR, f"jarvis_{datetime.now().strftime('%Y%m%d')}.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger("jarvis")
