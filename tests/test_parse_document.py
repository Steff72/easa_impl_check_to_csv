import pytest
import fitz
from src.parse_document import parse_document_sections

# Dummy Page and Document für Test
class DummyPage:
    def __init__(self, text):
        self._text = text
    def get_text(self):
        return self._text

class DummyDoc:
    def __init__(self, pages):
        self._pages = pages
    def __iter__(self):
        return iter(self._pages)

@pytest.fixture(autouse=True)
def mock_fitz_open(monkeypatch):
    # Simuliere PDF mit zwei Überschriften
    text = '1.1 Heading One Content One 2.2.1 Subheading Content Two'
    monkeypatch.setattr(fitz, 'open', lambda path: DummyDoc([DummyPage(text)]))

def test_parse_document_sections():
    sections = parse_document_sections('dummy.pdf')
    assert '1.1' in sections
    assert 'Content One' in sections['1.1']
    assert '2.2.1' in sections