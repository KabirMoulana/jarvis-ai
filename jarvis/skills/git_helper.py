"""
jarvis/skills/git_helper.py
Git helper — JARVIS runs git commands by voice.
Status, add, commit, push, pull, branch management.
"""
import subprocess
import os
import re


def _run(cmd: list[str], cwd: str | None = None) -> tuple[int, str, str]:
    result = subprocess.run(cmd, capture_output=True, text=True,
                            cwd=cwd, timeout=30)
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def git_status(repo_path: str = ".") -> str:
    code, out, err = _run(["git", "status", "--short"], cwd=repo_path)
    if code != 0:
        return f"Not a git repository, sir. {err}"
    if not out:
        return "Working directory is clean, sir. Nothing to commit."
    lines   = out.splitlines()
    staged  = [l for l in lines if l[0] in "MADRC"]
    changed = [l for l in lines if l[1] in "MD ?" and l[0] == " "]
    untracked = [l for l in lines if l.startswith("??")]
    parts   = []
    if staged:    parts.append(f"{len(staged)} staged")
    if changed:   parts.append(f"{len(changed)} modified")
    if untracked: parts.append(f"{len(untracked)} untracked")
    return f"Git status: {', '.join(parts)}, sir."


def git_log(count: int = 5, repo_path: str = ".") -> str:
    code, out, err = _run(
        ["git", "log", f"--oneline", f"-{count}"], cwd=repo_path
    )
    if code != 0:
        return f"Git log failed: {err}, sir."
    if not out:
        return "No commits found, sir."
    commits = out.splitlines()
    return f"Last {len(commits)} commits: " + " | ".join(commits) + ", sir."


def git_current_branch(repo_path: str = ".") -> str:
    code, out, err = _run(["git", "branch", "--show-current"], cwd=repo_path)
    if code != 0:
        return f"Not in a git repo, sir."
    return f"Current branch: {out}, sir."


def git_diff_summary(repo_path: str = ".") -> str:
    code, out, err = _run(["git", "diff", "--stat"], cwd=repo_path)
    if code != 0:
        return f"Git diff failed: {err}"
    if not out:
        return "No uncommitted changes, sir."
    lines = out.splitlines()
    return f"Changes: {lines[-1]}, sir." if lines else "No changes, sir."


def git_stash(repo_path: str = ".") -> str:
    code, out, err = _run(["git", "stash"], cwd=repo_path)
    if code != 0:
        return f"Stash failed: {err}, sir."
    return f"Changes stashed, sir. {out}"


def git_stash_pop(repo_path: str = ".") -> str:
    code, out, err = _run(["git", "stash", "pop"], cwd=repo_path)
    if code != 0:
        return f"Stash pop failed: {err}, sir."
    return "Stash restored, sir."


def git_list_branches(repo_path: str = ".") -> str:
    code, out, err = _run(["git", "branch", "-a"], cwd=repo_path)
    if code != 0:
        return f"Could not list branches: {err}, sir."
    branches = [b.strip().replace("* ", "") for b in out.splitlines()][:8]
    return f"Branches: {', '.join(branches)}, sir."
