import pytest
from src.vector_search import init_chroma, search_candidates

@pytest.mark.skip(reason="Benötigt OpenAI-API-Key und Chroma-Setup")
def test_vector_search_basic(monkeypatch):
    # Diese Tests sind Platzhalter und werden beim Vorhandensein eines API-Keys ausgeführt
    pass