
"""Unit tests for ConversationMemory."""
from utils.memory import ConversationMemory


def test_add_and_context():
    mem = ConversationMemory()
    mem.add("user", "Hello")
    mem.add("assistant", "Hi there")
    ctx = mem.get_context()
    assert "User: Hello" in ctx
    assert "Jarvis: Hi there" in ctx


def test_clear():
    mem = ConversationMemory()
    mem.add("user", "test")
    mem.clear()
    assert mem.get_context() == ""


def test_max_turns():
    mem = ConversationMemory(max_turns=2)
    for i in range(10):
        mem.add("user", f"msg {i}")
    lines = mem.get_context().strip().split("\n")
    assert len(lines) <= 4  # 2 turns * 2 roles
