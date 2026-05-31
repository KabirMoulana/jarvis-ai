"""
jarvis/skills/face_auth.py
JARVIS face authentication stub — Iron Man style.
Uses OpenCV + face_recognition for owner verification.
Falls back gracefully if libraries are missing.

Install:  pip install opencv-python face_recognition
"""

try:
    import cv2
    import face_recognition
    import numpy as np
    import pickle
    import os
    _AVAILABLE = True
except ImportError:
    _AVAILABLE = False

_ENCODINGS_FILE = os.path.join(os.path.dirname(__file__), "face_encodings.pkl") if _AVAILABLE else ""
_MAX_ATTEMPTS   = 3


def is_available() -> bool:
    return _AVAILABLE


def enroll_owner(name: str = "Sir") -> str:
    """
    Capture a photo from the webcam and save the face encoding.
    Call this once to register the owner.
    """
    if not _AVAILABLE:
        return "Face authentication libraries not installed. Run: pip install opencv-python face_recognition"

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return "Camera not accessible, sir."

    print("[FaceAuth] Look at the camera. Press SPACE to capture.")
    frame_to_encode = None
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("JARVIS — Enrolment (SPACE to capture, Q to quit)", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord(" "):
            frame_to_encode = frame.copy()
            break
        if key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

    if frame_to_encode is None:
        return "Enrolment cancelled."

    rgb   = cv2.cvtColor(frame_to_encode, cv2.COLOR_BGR2RGB)
    encs  = face_recognition.face_encodings(rgb)
    if not encs:
        return "No face detected in the frame. Please try again, sir."

    data  = {"name": name, "encoding": encs[0]}
    with open(_ENCODINGS_FILE, "wb") as f:
        pickle.dump(data, f)

    return f"Owner '{name}' enrolled successfully, sir."


def authenticate(timeout_secs: int = 8) -> tuple[bool, str]:
    """
    Attempt to authenticate the person in front of the camera.
    Returns (success: bool, message: str).
    """
    if not _AVAILABLE:
        return True, "Face auth unavailable — access granted by default."

    if not os.path.exists(_ENCODINGS_FILE):
        return True, "No owner enrolled — access granted. Run enroll_owner() to set up face lock."

    with open(_ENCODINGS_FILE, "rb") as f:
        data = pickle.load(f)

    known_enc  = data["encoding"]
    owner_name = data.get("name", "sir")

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return True, "Camera unavailable — access granted, sir."

    import time
    start   = time.time()
    success = False
    message = "Authentication failed."

    while time.time() - start < timeout_secs:
        ret, frame = cap.read()
        if not ret:
            continue
        rgb       = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        locations = face_recognition.face_locations(rgb)
        encodings = face_recognition.face_encodings(rgb, locations)

        for enc in encodings:
            match = face_recognition.compare_faces([known_enc], enc, tolerance=0.5)
            if match[0]:
                success = True
                message = f"Identity confirmed. Welcome back, {owner_name}."
                break
        if success:
            break

    cap.release()
    cv2.destroyAllWindows()

    if not success:
        message = "Face not recognised. Access denied, sir."

    return success, message
