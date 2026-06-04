"""
jarvis/skills/object_detection.py
Real-time object detection via webcam — JARVIS identifies
what's in front of the camera using OpenCV and a pre-trained model.
Requires: pip install opencv-python
Optional: pip install ultralytics (for YOLOv8)
"""
import os
import sys


def scan_environment(duration_secs: int = 5) -> str:
    """
    Capture from webcam and identify objects.
    Uses YOLOv8 if available, else falls back to OpenCV DNN.
    """
    try:
        from ultralytics import YOLO
        return _yolo_scan(duration_secs)
    except ImportError:
        pass
    try:
        import cv2
        return _opencv_scan(duration_secs)
    except ImportError:
        return (
            "Object detection unavailable, sir. "
            "Install with: pip install ultralytics opencv-python"
        )


def _yolo_scan(duration_secs: int) -> str:
    from ultralytics import YOLO
    import cv2, time

    model = YOLO("yolov8n.pt")   # nano model — downloads automatically
    cap   = cv2.VideoCapture(0)
    if not cap.isOpened():
        return "Camera not accessible, sir."

    detected = {}
    start    = time.time()

    while time.time() - start < duration_secs:
        ret, frame = cap.read()
        if not ret:
            break
        results = model(frame, verbose=False)
        for r in results:
            for box in r.boxes:
                label = model.names[int(box.cls)]
                conf  = float(box.conf)
                if conf > 0.5:
                    detected[label] = max(detected.get(label, 0), conf)

    cap.release()

    if not detected:
        return "No objects detected in the environment, sir."

    top = sorted(detected.items(), key=lambda x: x[1], reverse=True)[:5]
    items = ", ".join(f"{label} ({conf:.0%})" for label, conf in top)
    return f"Environment scan complete, sir. Detected: {items}."


def _opencv_scan(duration_secs: int) -> str:
    import cv2, time

    # Load pre-trained face + body detector
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    body_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_fullbody.xml"
    )

    cap      = cv2.VideoCapture(0)
    detected = set()
    start    = time.time()

    while time.time() - start < duration_secs:
        ret, frame = cap.read()
        if not ret:
            break
        gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        bodies= body_cascade.detectMultiScale(gray, 1.1, 4)
        if len(faces)  > 0: detected.add(f"{len(faces)} face(s)")
        if len(bodies) > 0: detected.add(f"{len(bodies)} person(s)")

    cap.release()

    if not detected:
        return "No objects detected in the environment, sir."
    return f"Detected: {', '.join(detected)}, sir."


def take_photo(save_path: str = "") -> str:
    """Capture a single photo from the webcam."""
    try:
        import cv2
        from datetime import datetime
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return "Camera not accessible, sir."
        ret, frame = cap.read()
        cap.release()
        if not ret:
            return "Failed to capture photo, sir."
        if not save_path:
            save_path = os.path.expanduser(
                f"~/Desktop/jarvis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            )
        cv2.imwrite(save_path, frame)
        return f"Photo saved to {save_path}, sir."
    except ImportError:
        return "OpenCV not installed. Run: pip install opencv-python"
    except Exception as e:
        return f"Camera error: {e}"
