"""
jarvis/skills/code_runner.py
Code execution — JARVIS runs small Python snippets by voice or command.
Sandboxed execution with timeout protection.
"""
import subprocess
import sys
import tempfile
import os
import signal


def run_python(code: str, timeout: int = 10) -> str:
    """Execute a Python code snippet and return the output."""
    code = code.strip()
    if not code:
        return "No code provided, sir."

    # Basic safety check — block dangerous operations
    blocked = ["import os", "import subprocess", "import sys", "__import__",
               "open(", "exec(", "eval(", "shutil", "rmdir", "remove"]
    for b in blocked:
        if b in code:
            return f"That code contains restricted operations, sir. I can't execute it."

    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write(code)
            tmp_path = f.name

        result = subprocess.run(
            [sys.executable, tmp_path],
            capture_output=True, text=True, timeout=timeout
        )
        os.unlink(tmp_path)

        if result.returncode == 0:
            output = result.stdout.strip()
            return f"Code executed successfully, sir. Output: {output}" if output else "Code ran with no output, sir."
        else:
            return f"Code error, sir: {result.stderr.strip()[:200]}"

    except subprocess.TimeoutExpired:
        return f"Code execution timed out after {timeout} seconds, sir."
    except Exception as e:
        return f"Execution error: {e}"


def run_shell(command: str) -> str:
    """Run a safe shell command and return output."""
    ALLOWED = ["ls", "pwd", "echo", "date", "whoami", "hostname",
               "python3 --version", "pip list", "uname"]
    cmd_base = command.strip().split()[0] if command.strip() else ""
    if cmd_base not in ALLOWED:
        return f"Shell command '{cmd_base}' not in allowed list, sir. Safety first."
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=5
        )
        return result.stdout.strip() or result.stderr.strip() or "No output."
    except Exception as e:
        return f"Shell error: {e}"


def evaluate_expression(expr: str) -> str:
    """Safely evaluate a Python expression."""
    try:
        import math
        safe_globals = {k: v for k, v in math.__dict__.items() if not k.startswith("_")}
        result = eval(expr, {"__builtins__": {}}, safe_globals)
        return f"Result: {result}, sir."
    except Exception as e:
        return f"Could not evaluate expression: {e}"
