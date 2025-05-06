import pdfplumber
import re

def parse_document_sections(pdf_path):
    """
    Parse the OM-D PDF und splitte nach numerischen Überschriften.
    Liefert dict: {'1.1': 'Heading One Content One', ...}
    """
    # PDF mit pdfplumber öffnen
    sections = {}
    full_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            full_text += text + "\n"

    # Kompakte Darstellung: alle Zeilenumbrüche → Leerzeichen, mehrfaches Whitespace reduzieren
    full_text = re.sub(r'[\r\n]+', ' ', full_text)
    full_text = re.sub(r'\s+', ' ', full_text).strip()

    # Regex: Abschnitts-ID (z.B. 1.1, 3.10.4) gefolgt vom Inhalt bis zur nächsten ID oder Dokumentende
    pattern = re.compile(
        r'(?P<id>\d+(?:\.\d+)+)\s+'          # Abschnitts-ID
        r'(?P<content>.*?)'                  # Inhalt (non-greedy)
        r'(?=(?:\d+(?:\.\d+)+\s+)|\Z)',      # bis zur nächsten ID oder Ende
        re.DOTALL
    )

    for match in pattern.finditer(full_text):
        sec_id = match.group("id")
        content = match.group("content").strip()
        content = re.sub(r'\s+', ' ', content)
        sections[sec_id] = content

    return sections