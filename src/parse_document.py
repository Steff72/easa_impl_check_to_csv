import fitz  # PyMuPDF
import re


def parse_document_sections(pdf_path):
    """
    Parse the OM-D PDF and split into sections by numeric headings.
    Returns dict: {'3.10.4': 'section text...', ...}
    """
    doc = fitz.open(pdf_path)
    full_text = ''
    for page in doc:
        full_text += page.get_text()
    pattern = re.compile(r'(^|\n)(?P<id>\d+\.\d+(?:\.\d+)*)(?:\s+)(?P<title>[^\n]+)', re.MULTILINE)
    matches = list(pattern.finditer(full_text))
    sections = {}
    for i, match in enumerate(matches):
        sec_id = match.group('id')
        start = match.end()
        end = matches[i+1].start() if i+1 < len(matches) else len(full_text)
        sec_text = full_text[start:end].strip()
        sections[sec_id] = sec_text
    return sections