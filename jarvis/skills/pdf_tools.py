"""
jarvis/skills/pdf_tools.py
PDF tools — JARVIS merges, splits, and extracts text from PDFs.
Requires: pip install PyPDF2
"""
import os


def merge_pdfs(input_paths: list[str], output_path: str = "") -> str:
    """Merge multiple PDF files into one."""
    try:
        import PyPDF2
    except ImportError:
        return "PyPDF2 not installed. Run: pip install PyPDF2"

    if not output_path:
        output_path = os.path.expanduser("~/Desktop/merged_output.pdf")

    try:
        merger = PyPDF2.PdfMerger()
        for path in input_paths:
            path = os.path.expanduser(path)
            if not os.path.exists(path):
                return f"File not found: {path}, sir."
            merger.append(path)
        merger.write(output_path)
        merger.close()
        return f"Merged {len(input_paths)} PDFs into {os.path.basename(output_path)}, sir."
    except Exception as e:
        return f"PDF merge failed: {e}"


def split_pdf(input_path: str, pages_per_file: int = 1) -> str:
    """Split a PDF into smaller files."""
    try:
        import PyPDF2
    except ImportError:
        return "PyPDF2 not installed. Run: pip install PyPDF2"

    input_path = os.path.expanduser(input_path)
    if not os.path.exists(input_path):
        return f"File not found: {input_path}, sir."

    try:
        reader  = PyPDF2.PdfReader(input_path)
        total   = len(reader.pages)
        outdir  = os.path.dirname(input_path)
        base    = os.path.splitext(os.path.basename(input_path))[0]
        created = []

        for start in range(0, total, pages_per_file):
            writer  = PyPDF2.PdfWriter()
            end     = min(start + pages_per_file, total)
            for i in range(start, end):
                writer.add_page(reader.pages[i])
            out_path = os.path.join(outdir, f"{base}_part{start//pages_per_file+1}.pdf")
            with open(out_path, "wb") as f:
                writer.write(f)
            created.append(os.path.basename(out_path))

        return f"Split into {len(created)} files, sir: {', '.join(created[:5])}."
    except Exception as e:
        return f"PDF split failed: {e}"


def extract_text_from_pdf(path: str, page_range: str = "") -> str:
    """Extract text from a PDF file."""
    try:
        import PyPDF2
    except ImportError:
        return "PyPDF2 not installed. Run: pip install PyPDF2"

    path = os.path.expanduser(path)
    if not os.path.exists(path):
        return f"File not found: {path}, sir."

    try:
        reader = PyPDF2.PdfReader(path)
        total  = len(reader.pages)

        if page_range:
            parts = page_range.split("-")
            start = int(parts[0]) - 1
            end   = int(parts[1]) if len(parts) > 1 else start + 1
        else:
            start, end = 0, min(3, total)

        text = ""
        for i in range(start, end):
            text += reader.pages[i].extract_text() or ""

        preview = text.strip()[:400]
        return (
            f"PDF has {total} pages, sir. "
            f"Pages {start+1}-{end}: {preview}..."
        )
    except Exception as e:
        return f"PDF extraction failed: {e}"


def get_pdf_info(path: str) -> str:
    """Get metadata from a PDF."""
    try:
        import PyPDF2
        path   = os.path.expanduser(path)
        reader = PyPDF2.PdfReader(path)
        meta   = reader.metadata or {}
        pages  = len(reader.pages)
        title  = meta.get("/Title", "Unknown")
        author = meta.get("/Author", "Unknown")
        return (
            f"PDF info, sir: {pages} pages. "
            f"Title: {title}. Author: {author}."
        )
    except ImportError:
        return "PyPDF2 not installed."
    except Exception as e:
        return f"PDF info failed: {e}"
