
"""Unit tests for notes_command."""
import os
import tempfile
import commands.notes_command as notes_cmd


def test_save_and_read(tmp_path, monkeypatch):
    notes_file = str(tmp_path / "notes.txt")
    monkeypatch.setattr(notes_cmd, "NOTES_FILE", notes_file)
    result = notes_cmd.save_note("buy milk")
    assert result == "Note saved."
    read = notes_cmd.read_notes()
    assert "buy milk" in read


def test_handle_save():
    result = notes_cmd.handle("take a note call dentist")
    assert result == "Note saved."


def test_handle_no_match():
    assert notes_cmd.handle("play music") is None
