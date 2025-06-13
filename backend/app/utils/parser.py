from pathlib import Path

def parse_document(path: Path) -> str:
    if path.suffix == ".pdf":
        return parse_pdf(path)
    elif path.suffix == ".docx":
        return parse_docx(path)
    else:
        return ""

def parse_pdf(path: Path) -> str:
    from pdfminer.high_level import extract_text
    return extract_text(str(path))

def parse_docx(path: Path) -> str:
    import docx
    doc = docx.Document(str(path))
    return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
