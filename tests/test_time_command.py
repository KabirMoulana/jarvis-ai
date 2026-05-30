
"""Unit tests for time_command."""
import re
from commands import time_command


def test_get_time_format():
    result = time_command.get_time()
    assert re.search(r"\d{1,2}:\d{2}", result), f"Unexpected time format: {result}"


def test_get_date_format():
    result = time_command.get_date()
    assert "Today is" in result


def test_handle_time():
    assert time_command.handle("what time is it") is not None


def test_handle_date():
    assert time_command.handle("what is today's date") is not None


def test_handle_no_match():
    assert time_command.handle("play music") is None
