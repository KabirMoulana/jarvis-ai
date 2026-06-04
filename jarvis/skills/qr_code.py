"""
jarvis/skills/qr_code.py
QR code generator — JARVIS generates QR codes for URLs,
text, WiFi credentials, contact cards, and more.
Requires: pip install qrcode[pil]
"""
import os
from datetime import datetime


def generate_qr(data: str, filename: str = "", save_dir: str = "") -> str:
    """Generate a QR code for any text or URL."""
    try:
        import qrcode
        from PIL import Image
    except ImportError:
        return "QR code generation unavailable. Run: pip install 'qrcode[pil]'"

    save_dir = save_dir or os.path.expanduser("~/Desktop")
    os.makedirs(save_dir, exist_ok=True)

    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename  = f"jarvis_qr_{timestamp}.png"

    path = os.path.join(save_dir, filename)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(path)

    _open_file(path)
    return f"QR code generated and saved to Desktop as {filename}, sir."


def generate_wifi_qr(ssid: str, password: str, security: str = "WPA") -> str:
    """Generate a WiFi QR code."""
    wifi_string = f"WIFI:T:{security};S:{ssid};P:{password};;"
    return generate_qr(wifi_string, f"wifi_{ssid.replace(' ', '_')}.png")


def generate_contact_qr(name: str, phone: str = "", email: str = "") -> str:
    """Generate a vCard QR code."""
    vcard = f"BEGIN:VCARD\nVERSION:3.0\nFN:{name}\n"
    if phone: vcard += f"TEL:{phone}\n"
    if email: vcard += f"EMAIL:{email}\n"
    vcard += "END:VCARD"
    return generate_qr(vcard, f"contact_{name.replace(' ', '_')}.png")


def generate_url_qr(url: str) -> str:
    """Generate a QR code for a URL."""
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    return generate_qr(url, f"url_qr_{datetime.now().strftime('%H%M%S')}.png")


def _open_file(path: str):
    import sys, subprocess
    try:
        if sys.platform == "darwin":
            subprocess.Popen(["open", path])
        elif sys.platform == "win32":
            os.startfile(path)
        else:
            subprocess.Popen(["xdg-open", path])
    except Exception:
        pass
