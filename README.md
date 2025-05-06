# EASA Part-FCL → OM-D Mapping CLI

Dieses Python-Tool automatisiert die Zuordnung von EASA Part-FCL-Regularien (Annex I) zu den entsprechenden Abschnitten im Unternehmens-Handbuch (OM D Rev29).

## Projektstruktur

```
project_root/
├── Pipfile               # Pipenv-Konfiguration
├── Pipfile.lock          # automatisch erzeugt
├── .gitignore            # Git-Ausnahmen
├── pytest.ini            # Pytest-Konfiguration
├── .env.example          # Beispiel-Umgebungsvariablen
├── README.md             # Projektdokumentation
├── regulations/          # Enthält die EASA-XML-Datei
│   └── Easy Access Rules for Aircrew.xml
├── documents/            # Unternehmens-Handbuch (nur lokal, nicht im Repo)
│   └── OM D Rev29.pdf
├── results/              # Generierte CSV-Ausgabe (nicht versioniert)
├── src/                  # Python-Package
│   ├── __init__.py
│   ├── main.py           # CLI-Einstiegspunkt
│   ├── parse_regulations.py
│   ├── parse_document.py
│   ├── vector_search.py
│   ├── semantic_match.py
│   └── export_results.py
└── tests/                # Unit-Tests mit pytest
    ├── test_parse_regulations.py
    ├── test_parse_document.py
    ├── test_export_results.py
    └── test_vector_search.py  
```

## pytest.ini

```ini
[pytest]
minversion = 6.0
testpaths = tests
pythonpath = src
addopts = -q
```

*Diese Konfiguration stellt sicher, dass `src/` als Importpfad hinzugefügt wird.*

## Voraussetzungen

* Python 3.8+ installiert
* [Pipenv](https://pipenv.pypa.io/) für Environment-Management
* OpenAI-API-Key

## Installation

```bash
# Pipenv-Environment anlegen und Abhängigkeiten installieren
pipenv install --dev
```

## Umgebungsvariablen (`.env`)

Erstelle im Projektstamm eine Datei `.env` mit folgenden Einträgen:

```
OPENAI_API_KEY=dein_api_key
EMBEDDING_MODEL=text-embedding-3-small
LLM_MODEL=gpt-4.1-mini
SIMILARITY_THRESHOLD=0.7
MAX_CANDIDATES=50
```

## Unternehmens-Handbuch

Lege das PDF `OM D Rev29.pdf` in den Ordner `documents/`. Dieser Ordner ist in `.gitignore` ausgenommen und enthält vertrauliche Unterlagen.

## Nutzung

```bash
pipenv shell
python src/main.py --regs regulations/Easy\ Access\ Rules\ for\ Aircrew.xml \
  --doc documents/OM\ D\ Rev29.pdf --out results/part-fcl_to_omd_map.csv
```

## Tests

Führe die Unit-Tests mit pytest aus. Dank `pytest.ini` werden die Module aus `src/` korrekt gefunden:

```bash
pipenv run python -m pytest -q
```

---

*Viel Erfolg!*
