"""
jarvis/skills/document_reader.py
Document reader — JARVIS reads and summarises PDFs, Word docs, and text files.
Requires: pip install PyPDF2 python-docx
"""
import os


def read_pdf(path: str, pages: int = 3) -> str:
    """Read and return text from a PDF file."""
    path = os.path.expanduser(path)
    if not os.path.exists(path):
        return f"File not found: {path}, sir."
    try:
        import PyPDF2
        text  = []
        with open(path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            total  = len(reader.pages)
            for i, page in enumerate(reader.pages[:pages]):
                text.append(page.extract_text() or "")
        content = " ".join(text).strip()[:500]
        return (
            f"PDF has {total} pages, sir. First {min(pages, total)} pages: "
            f"{content}..."
        )
    except ImportError:
        return "PyPDF2 not installed. Run: pip install PyPDF2"
    except Exception as e:
        return f"Could not read PDF: {e}"


def read_docx(path: str) -> str:
    """Read and return text from a Word document."""
    path = os.path.expanduser(path)
    if not os.path.exists(path):
        return f"File not found: {path}, sir."
    try:
        from docx import Document
        doc   = Document(path)
        paras = [p.text for p in doc.paragraphs if p.text.strip()]
        total = len(paras)
        preview = " ".join(paras[:5])[:400]
        return f"Word document with {total} paragraphs, sir. Preview: {preview}..."
    except ImportError:
        return "python-docx not installed. Run: pip install python-docx"
    except Exception as e:
        return f"Could not read document: {e}"


def read_text_file(path: str) -> str:
    """Read a plain text file."""
    path = os.path.expanduser(path)
    if not os.path.exists(path):
        return f"File not found: {path}, sir."
    try:
        with open(path, encoding="utf-8") as f:
            content = f.read()
        lines   = content.splitlines()
        preview = " ".join(lines[:10])[:400]
        return f"Text file with {len(lines)} lines, sir. Content: {preview}..."
    except Exception as e:
        return f"Could not read file: {e}"


def summarise_document(path: str, llm_client=None) -> str:
    """Read a document and summarise it using the LLM."""
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        content = read_pdf(path, pages=5)
    elif ext in (".docx", ".doc"):
        content = read_docx(path)
    else:
        content = read_text_file(path)

    if llm_client and llm_client.is_available():
        prompt = f"Summarise this document in 3 sentences:\n\n{content}"
        return llm_client.chat(prompt)
    return content


def count_words_in_file(path: str) -> str:
    """Count words in a text file."""
    path = os.path.expanduser(path)
    try:
        with open(path, encoding="utf-8") as f:
            content = f.read()
        words = len(content.split())
        chars = len(content)
        return f"The file contains {words:,} words and {chars:,} characters, sir."
    except Exception as e:
        return f"Could not count words: {e}"
