"""
jarvis/skills/terminal_ui.py
Terminal UI components — rich formatted output for JARVIS.
Tables, progress bars, banners, and color output.
"""
import shutil
import sys


def print_banner(text: str, style: str = "box"):
    """Print a styled banner."""
    width = min(shutil.get_terminal_size((80, 20)).columns - 4, 60)
    if style == "box":
        border = "═" * width
        print(f"\n  ╔{border}╗")
        lines  = _wrap_text(text, width - 2)
        for line in lines:
            print(f"  ║ {line.ljust(width - 2)} ║")
        print(f"  ╚{border}╝\n")
    elif style == "simple":
        print(f"\n  {'─' * width}")
        print(f"  {text}")
        print(f"  {'─' * width}\n")


def print_table(headers: list[str], rows: list[list], title: str = "") -> str:
    """Print a formatted table and return as string."""
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))

    sep   = "  ├" + "┼".join("─" * (w + 2) for w in col_widths) + "┤"
    top   = "  ┌" + "┬".join("─" * (w + 2) for w in col_widths) + "┐"
    bot   = "  └" + "┴".join("─" * (w + 2) for w in col_widths) + "┘"

    lines = []
    if title:
        lines.append(f"\n  {title}")
    lines.append(top)
    header_row = "  │" + "│".join(f" {h.ljust(w)} " for h, w in zip(headers, col_widths)) + "│"
    lines.append(header_row)
    lines.append(sep)
    for row in rows:
        data_row = "  │" + "│".join(f" {str(c).ljust(w)} " for c, w in zip(row, col_widths)) + "│"
        lines.append(data_row)
    lines.append(bot)
    output = "\n".join(lines)
    print(output)
    return output


def print_progress(label: str, value: float, max_val: float = 100,
                   width: int = 30, color: bool = True):
    """Print a progress bar."""
    pct    = min(value / max_val, 1.0)
    filled = int(width * pct)
    bar    = "█" * filled + "░" * (width - filled)
    pct_str = f"{pct * 100:.0f}%"
    print(f"  {label:<20} [{bar}] {pct_str}")


def print_status_table(items: dict[str, str]):
    """Print a key-value status table."""
    max_key = max(len(k) for k in items) if items else 10
    print()
    for key, val in items.items():
        print(f"  {key.ljust(max_key + 2)}  {val}")
    print()


def _wrap_text(text: str, width: int) -> list[str]:
    words, lines, line = text.split(), [], ""
    for word in words:
        if len(line) + len(word) + 1 <= width:
            line = f"{line} {word}".strip()
        else:
            if line: lines.append(line)
            line = word
    if line: lines.append(line)
    return lines or [""]


def clear_line():
    sys.stdout.write(f"\r{' ' * shutil.get_terminal_size((80,20)).columns}\r")
    sys.stdout.flush()


def print_separator():
    width = shutil.get_terminal_size((80, 20)).columns
    print("  " + "─" * (width - 4))
