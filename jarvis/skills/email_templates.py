"""
jarvis/skills/email_templates.py
Email templates library — JARVIS drafts professional emails
for common business scenarios with one command.
"""

_TEMPLATES = {
    "job application": {
        "subject": "Application for {role} Position",
        "body": """Dear Hiring Manager,

I am writing to express my strong interest in the {role} position at {company}.

With my background in {background}, I believe I would be a valuable addition to your team.

I would welcome the opportunity to discuss how my skills align with your needs.

Thank you for your consideration.

Kind regards,
{name}"""
    },
    "cold outreach": {
        "subject": "Quick Question About {topic}",
        "body": """Hi {first_name},

I came across your work on {topic} and was genuinely impressed.

I'm {name}, and I work on {background}. I'd love to connect and explore potential synergies.

Would you be open to a 15-minute call this week?

Best,
{name}"""
    },
    "project update": {
        "subject": "Project Update — {project}",
        "body": """Hi {first_name},

Quick update on {project}:

Status: {status}
Completed: {completed}
Next steps: {next_steps}
Blockers: {blockers}

Happy to discuss further. Let me know if you have any questions.

Best,
{name}"""
    },
    "apology": {
        "subject": "Sincere Apologies — {issue}",
        "body": """Dear {first_name},

I want to sincerely apologise for {issue}.

This fell below the standard I hold myself to, and I take full responsibility.

To make this right, I will {resolution}.

I value our relationship and am committed to ensuring this does not happen again.

Sincerely,
{name}"""
    },
    "resignation": {
        "subject": "Resignation — {name}",
        "body": """Dear {manager},

I am writing to formally resign from my position at {company}, effective {date}.

This was not an easy decision. I have genuinely valued my time here and the opportunities I've been given.

I am committed to ensuring a smooth transition and will assist in training my replacement.

Thank you for everything.

Kind regards,
{name}"""
    },
    "invoice": {
        "subject": "Invoice #{invoice_number} — {company}",
        "body": """Dear {first_name},

Please find attached Invoice #{invoice_number} for {description}.

Amount due: {amount}
Due date: {due_date}

Payment details: {payment_details}

Please don't hesitate to reach out with any questions.

Best regards,
{name}"""
    },
}


def get_template(template_name: str, **kwargs) -> str:
    """Get an email template filled with provided values."""
    name_lower = template_name.lower()
    template   = None
    for key in _TEMPLATES:
        if name_lower in key or key in name_lower:
            template = _TEMPLATES[key]
            break
    if not template:
        available = ", ".join(_TEMPLATES.keys())
        return f"Template '{template_name}' not found, sir. Available: {available}."

    subject = template["subject"]
    body    = template["body"]

    for k, v in kwargs.items():
        subject = subject.replace(f"{{{k}}}", str(v))
        body    = body.replace(f"{{{k}}}", str(v))

    # Replace unfilled placeholders
    import re
    subject = re.sub(r"\{[^}]+\}", "[fill in]", subject)
    body    = re.sub(r"\{[^}]+\}", "[fill in]", body)

    return f"Subject: {subject}\n\n{body}"


def list_templates() -> str:
    return f"Email templates available: {', '.join(_TEMPLATES.keys())}, sir."
