"""
jarvis/skills/mindmap_generator.py
Mind map generator — JARVIS creates text-based mind maps
for brainstorming and concept exploration.
"""


def generate_mindmap(topic: str, llm_client=None) -> str:
    """Generate a mind map structure for a topic."""
    if llm_client and llm_client.is_available():
        prompt = (
            f"Create a simple mind map for '{topic}' with exactly 4 main branches "
            f"and 2 sub-points each. Format as plain text with dashes and indentation. "
            f"Be concise."
        )
        return llm_client.chat(prompt)
    return _static_mindmap(topic)


def _static_mindmap(topic: str) -> str:
    """Return a static mind map template."""
    return (
        f"Mind map: {topic.upper()}\n"
        f"├── What is it?\n"
        f"│   ├── Core definition\n"
        f"│   └── Key characteristics\n"
        f"├── Why does it matter?\n"
        f"│   ├── Benefits\n"
        f"│   └── Problems it solves\n"
        f"├── How does it work?\n"
        f"│   ├── Core process\n"
        f"│   └── Key components\n"
        f"└── What's next?\n"
        f"    ├── Applications\n"
        f"    └── Future potential\n"
        f"\nSir, enable Ollama for a topic-specific mind map."
    )


def generate_project_mindmap(project: str) -> str:
    """Generate a project planning mind map."""
    return (
        f"Project mind map: {project.upper()}\n"
        f"├── Goals\n"
        f"│   ├── Primary objective\n"
        f"│   └── Success metrics\n"
        f"├── Resources\n"
        f"│   ├── Team/tools needed\n"
        f"│   └── Budget estimate\n"
        f"├── Timeline\n"
        f"│   ├── Milestones\n"
        f"│   └── Deadlines\n"
        f"├── Risks\n"
        f"│   ├── Potential blockers\n"
        f"│   └── Mitigation strategies\n"
        f"└── Next actions\n"
        f"    ├── This week\n"
        f"    └── This month\n"
    )


def generate_learning_mindmap(subject: str) -> str:
    """Generate a learning plan mind map."""
    return (
        f"Learning map: {subject.upper()}\n"
        f"├── Foundations\n"
        f"│   ├── Core concepts\n"
        f"│   └── Prerequisites\n"
        f"├── Intermediate\n"
        f"│   ├── Key skills\n"
        f"│   └── Practice projects\n"
        f"├── Advanced\n"
        f"│   ├── Specialisations\n"
        f"│   └── Real-world applications\n"
        f"└── Resources\n"
        f"    ├── Books / courses\n"
        f"    └── Communities\n"
    )
